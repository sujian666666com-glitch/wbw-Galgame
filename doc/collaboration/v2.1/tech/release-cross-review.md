# v2.1 发行交叉审查

- 实际模型：Grok 4.7（契约角色为 Cursor / grok-4.7-high）
- 工作树：`.work/v21/worktrees/tech`
- 改动：`game/options.rpy`
- 未改：QA 工作树、`tools/package_macos.py`、界面、对白、`ik.md`。未推送，未跑游戏，未跑测试，未打包装。

## 1. app 包排除

`game/options.rpy` 在归档规则之前增加四条 `None`：

- `old-game/**`
- `README.md`
- `AGENTS.md`
- `*.md`（只命中项目根的单层 markdown，用来盖住同类说明）

`THIRD_PARTY_NOTICES.txt` 与 `licenses/**` 仍是后面的 `"all"`。二者是 `.txt`，不会被 `*.md` 先命中。当前树里有 `README.md`，没有 `AGENTS.md`；规则先写上，避免以后放进根目录就进 app。

SDK 的 `early_base_patterns` 里已有 `old-game/` → `None`。项目规则再写一次，避免只靠引擎默认。`tools/package_macos.py` 的 `source.zip` 是 `git archive`，不走 `build.classify`。`old-game/` 与 `README.md` 都在 git 里，会留在完整源码包。这次没有实际打包。

打包脚本事后扫描的禁入名单仍是 `.git`、`.work`、`ik.md`、`testcases`、`saves`、`cache`、`image/`、`doc/`、`tools/`。它不检查 `old-game`、`README.md`、`AGENTS.md`。分类若失效，这次构建不会因此失败。该脚本不在本角色所有权内，没有改。

## 2. 进程监管（只读）

看了 QA 工作树 `tools/v21_gui_lock_exec.py`、`tools/v21_run_tests.py`，以及主集成 `doc/collaboration/v2.1/process-guard-probe.json`。没有改这些文件。

包装进程用 `start_new_session=True`，直接子进程的 pid 就是进程组。锁在 `finally` 里先 `reap_group` 再写 released、再 `LOCK_UN`。`reap_group` 对仍存活的组先 `SIGTERM`，最多等 2 秒，组还在就 `SIGKILL`。暂停文件、`SIGINT`/`SIGTERM`、父进程 pid 或 `V21_TEST_OWNER_PID` 死亡都会停。`renpy.sh` 用 `exec` 换成引擎二进制，不会自己另开会话，组内子孙仍在这个组里。忽略 TERM 但留在组里的孙进程，会在宽限之后被 `SIGKILL`。这针对先前「组长已退出、孙进程忽略 TERM、两个 Ren'Py 打满 CPU」。

probe 五项与预期一致：

| 用例 | 退出码 | 后代已死 | 锁已放 | PID 数 |
| --- | --- | --- | --- | --- |
| normal | 0 | 是 | 是 | 2 |
| deadline | 41 | 是 | 是 | 2 |
| signal | 143 | 是 | 是 | 2 |
| pause | 42 | 是 | 是 | 2 |
| owner | 43 | 是 | 是 | 2 |

143 是 128+15，说明 signal 用例走到了包装进程自己的 TERM 退出。五项都是两个 PID，没有第三代，也没有记录子进程是否忽略 TERM，或是否走进 `SIGKILL` 分支。因此这份 JSON 证明了这五种脚本化退出，没有复现当时的 Ren'Py 双进程泄漏。

仍在的问题：

1. `SIGKILL` 之后没有再等 `group_alive` 变假，只对直接子进程 `child.wait(timeout=5)` 就放锁。调用 `setsid` / `setpgid` 离开该组的子孙，`killpg` 打不到，锁会在它还活着时放开。
2. `child.wait` 超时，或 `killpg` 抛出 `ProcessLookupError` 以外的错误时，异常从 `finally` 抛出，后面的 released 和 `LOCK_UN` 不会执行。`with` 关闭文件时 flock 会掉，退出码变成回溯，组却可能还在。
3. `v21_run_tests.py` 只把 `SIGINT`/`SIGTERM` 转给包装进程，收尾也只 `terminate()` 再等 10 秒，自己不杀进程组。读 stdout 的循环没有截止时间。包装进程若先退出、漏掉的子孙还占着这条管道，runner 会停在读循环里，进不了自己的 `finally`。对包装进程发 `SIGKILL` 时它的 `finally` 不跑，内核会放锁，组不会被收。
4. runner 没有设置 `V21_TEST_OWNER_PID`，owner 默认是 runner。这和「runner 死亡则停」一致。`alive()` 把 `PermissionError` 当成仍存活；默认 owner 就是父进程，父进程一死，`getppid()` 变化仍会得到 43。这条只在 owner 被设成另一个无权发信号的 pid 时才会漏判。

## 3. 资源与布局（静态）

从产品 `.rpy` 抽出 `images/` 与 `fonts/` 路径 60 条，对应文件都在 `game/` 下，没有缺失。其中包括九张 `game/images/v21/` 图和 `fonts/SourceHanSansLite.ttf`。九个时段变体引用已有背景名，再用 `TintMatrix` / `BrightnessMatrix`，没有额外文件。没有跑 lint，也没有打开游戏。

`config.history_length` 仍是 250。

六项菜单和缩略图设置仍是：

1. 选项栏 `ypos 800`、`yanchor 1.0`、`spacing 12`
2. 存档网格 `3 2`，间距 20
3. 槽按钮 `340×278`，内边距 12
4. 缩略图 `316×178`
5. 时间与存档名 `xsize 316`
6. 页名按钮 `xsize 460`

菜单框 `1160×820`、内边距 `(45, 40)`，内容区 `1070×740`。三列 `3×340+40 = 1060`。两行 `278×2+20 = 576`，加上页码行和间距约 662，低于 740。缩略图宽 316 等于 `340-24`。对白窗 `yalign 1.0`、高 270，顶边在 y=810；选项栏底边在 y=800，六项堆在对白窗上方。历史视口仍是 `1060×720`，对白宽 1020，也在同一内容区内。没有打开界面核对像素。
