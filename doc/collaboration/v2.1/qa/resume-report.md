# v2.1 QA 续跑报告（短阶段）

- 执行 Agent：Pi / `deepseek-flash`（`PI_MODEL=deepseek-flash`，provider `deepseek`，reasoning high）
- 工作树：`.work/v21/worktrees/qa`，分支 `ik/v21-qa`（已含集成提交 `edb4a7a`，未提交修改见下）
- 本阶段状态：**未完成交付，卡在 2.0 存档兼容验证**；按“发现一次异常立刻停并报告”执行，未重试、未跑完整 suite、未 commit / 未 push
- 唯一异常记录：`compat` 四项全部超时（详见第 4 节）

## 1. 本阶段已完成（工具与测试源码，均未提交）

### `game/testcases.rpy`（仅测试文件）

| 改动 | 说明 |
| --- | --- |
| focus override 收敛 | 只保留 `init -100 python` 内 `renpy.game.args.command == "test"` 时把 `Interface.mouse_focused` 覆盖为常真 property；删除 `config.periodic_callbacks` 周期兜底、`_v21_qa_keep_mouse_focus`、`try/except: return` 吞异常，以及 3 处 testsuite 里手写 `$ renpy.game.interface.mouse_focused = True` |
| history 断言恢复 | `options.rpy:18` 已是 `config.history_length = 250`；删除 `xfail`，改为正向断言 `renpy.config.history_length == 250` + `_history_list` 含“先把能做的事列清楚” |
| 存档状态取证 | `v21_capture_state()` 记录新增 `choice_captions`，让 `v21_compat_check.py` 能证明读档后确实停在真实菜单（而不是 start 兜底） |
| 用例集合 | 30 个 testcase = 原 14 + 已写新增分支 8（`full_flow_startup_ideal` / `full_flow_low_old` / `full_flow_mid_old` / `sequel_low_trust_flow` / `sequel_partial_trust_flow` / `sequel_true_gate_insight_short` / `sequel_true_gate_missing_fragment` / `ui_features_smoke`）+ 4 capture + 4 compat。原 14 用例与原断言阈值未改动 |

### `tools/v21_qa_project.py`（重写）

- 复制 `game/`（仍排除 `.rpyc`/缓存，保证 build 反映源码）+ **复制 `old-game/` 且保留 `.rpyc`**（实测 25 个文件：24 个 rpyc + README）。
- trace 模板改为仓库内可追踪文件 `tools/v21_qa_trace.rpy.txt`（`--trace` 时写入 `game/qa_trace.rpy`）；原 `.work/qa/trace/qa_trace.rpy` 不再被引用。
- 路径不再依赖 `WORKTREE.parents[3]`：`REPO_ROOT = Path(__file__).resolve().parents[1]`，默认 `--dest <repo>/.work/qa/project`、`--saves <repo>/.work/qa/saves`，集成到主仓库根目录后同样成立。
- `--clean` 安全：正白名单 `is_isolated()`（必须位于名为 `.work` 的目录之下且其下有具体目标），并拒绝目标等于 source 或 source 的祖先、拒绝 home / `/` / `renpy_saves` / `Library/RenPy`。实测探针：
  - `--dest .` → `error: ... is the source tree or its ancestor`（拒绝）
  - `--dest /tmp/qa-project` → `error: ... not an isolated .work/... destination`（拒绝）
  - `--saves $HOME` → 拒绝
  - 正常 `--dest .work/qa/project-compat --clean` → 成功

### `tools/v21_compat_check.py`（重写）

- `--fixtures` 默认解析到根 `.work/v21/compat-v20`：从 `REPO_ROOT` 向上查找 `.work/v21/compat-v20`（无 `parents[N]`），支持 `V21_COMPAT_ROOT`；集成后自动命中根目录。实测未传 `--fixtures` 即命中主仓库夹具。
- `--output` 机器可读 JSON 报告（`ok` / `checked` / 每夹具 `status` / `problems` / `exit` / `loaded_current` / `choice_captions` / `persistent` / `log`）。
- 通过条件收紧：① 用例成功；② 读档语句与捕获时同文件，且**不得落回 `game/script.rpy`（start 兜底）**；③ `choice_captions` 非空（真实菜单），若夹具记录过菜单则逐条比对；④ 全部 `EXACT_KEYS` 不变；⑤ `persistent`（`old_ending_route` / `old_endings_seen`）整体不变；⑥ 2.0 中不存在的新变量必须仍是 `default`：`sequel_luna_observation_outcome == "unknown"`。
- 每夹具透传 `--max-runtime`（默认 90s）给 `v21_run_tests.py`，所有 Ren'Py 仍走共享 `gui.lock`。
- 附带修正：`tools/v21_capture_fixtures.py` 的 `MAIN_REPO = WORKTREE.parents[3]` 改为向上查找（`--check` 实测 `checked 4 fixtures: ok`）。**未运行 capture，未改动 `.work/v21/compat-v20` 任何文件。**

## 2. 夹具完整性

`python3 tools/v21_capture_fixtures.py --check` → `checked 4 fixtures: ok`（manifest 记录的 save/persistent 的 SHA-256 未变，原 project-fixtures 未触碰、未重新编译）。

## 3. 已验证（有输出证据）

| 检查 | 结果 |
| --- | --- |
| `python3 -m py_compile` 四个工具 | 通过 |
| 隔离项目构建（含 old-game rpyc） | 通过：`game 88 files` / `old-game 25 files (compiled .rpyc kept)` |
| `--clean` 安全探针（3 个恶意目标 + 1 个正常目标） | 通过：恶意目标全部拒绝 |
| 夹具哈希 `--check` | 通过：4/4 ok |
| 4 个 compat 用例 | **失败 4/4**（见第 4 节） |
| 新增 8 个分支用例 / 原 14 用例 | **未运行**（本阶段按指令只跑 compat） |

## 4. 实际异常与证据（未解决）

4 个 compat 用例全部 `exit 41`（`v21_gui_lock_exec.py` 的 runtime deadline），每个约 92 秒，合计 6m09s。Ren'Py 侧不是崩溃，而是**每次都在同一个语句超时**：

```text
[v21-lock 01:25:45] lock acquired; child group 44835; limit 90s
[rpytest] [exc]   - compat_v20_old_chapter01_menu (60.027 s)
renpy.test.types.RenpyTestTimeoutError: Until Statement timed out after 60.0 seconds.
  game/testcases.rpy ... testcase compat_v20_old_chapter01_menu
    advance until screen "choice"
[rpytest] Status: FAILED
[v21-lock 01:27:15] runtime deadline reached
```

- `FileLoad(1, confirm=False, page="1")` 本身没有抛出读档异常，但读档后既没有出现 choice 屏，也没有产生 `after-load.jsonl`（`v21_capture_state()` 从未执行）→ **存档没有恢复到保存时的菜单**，60s testcase 超时先于 90s 进程上限触发，随后进程组被锁持有者按 deadline 回收（`limit 90s` → exit 41）。
- 证据路径：
  - 每个夹具日志：`.work/qa/logs/compat-v20_old_chapter01_menu.log`、`...chapter06_menu.log`、`...sequel_first_menu.log`、`...sequel_finale_menu.log`
  - 机器可读报告：`.work/qa/logs/compat-report.json`（`ok: false`，4 条 `status: failed`，`problems` 里所有字段为 `None` = 读档后没有任何状态被采集）
  - Ren'Py traceback：`.work/qa/project-compat/traceback.txt`（只有 testcase 超时，无读档/脚本异常）
  - Ren'Py log：`.work/qa/project-compat/log.txt`
  - 隔离存档根：`.work/qa/compat/<fixture>/saves/three-months-to-stay-1/`（Ren'Py 已在该目录建 `sync/`、`tokens/`、`backups/`，说明被加载的保存目录路径正确）
- 已验证的前提：`.work/v21/compat-v20` 的 save/persistent 哈希与 manifest 一致，`0` 字节差异；隔离项目复制了 `old-game/*.rpyc`。

### 根因相关的关键发现（需主 Agent 裁决）

`old-game/` **不是 Ren'Py 的兼容机制**：在 SDK `renpy/**/*.py` 中搜索 `old-game` / `old_game` 命中数为 **0**。因此

1. 把 `old-game/*.rpyc` 复制进测试项目，对 Ren'Py 读档**没有任何作用**，它们只是审计/语句 ID lineage 归档（`doc/collaboration/v2.1/v20-compiled-lineage.json` 记录的是哈希清单）。
2. 与“fresh compile 时间戳生成新语句 ID 导致 fallback”一致：2.1 源码重新编译后，2.0 存档里的语句 ID 不再存在，读档无法回到保存时语句。这解释了本次 4/4 失败（`FileLoad` 无异常，但没有回到菜单）。
3. 真正的修复只能落在产品侧语句 ID 稳定性（例如编译时复用 2.0 已编译语句身份）或明确的读档映射，**属于 `game/` 产品脚本与主 Agent 的范围，不在 QA 所有权内**；我没有添加任何猜状态的迁移脚本，也没有改动产品脚本、原素材、用户存档。

## 5. 未完成 / 建议下一步

1. 由主 Agent 决定语句 ID 稳定性的修复方案（QA 侧不能改产品脚本）。修复后在隔离项目上重跑本条命令即可复核：
   `python3 tools/v21_compat_check.py --project .work/qa/project-compat --max-runtime 90 --output .work/qa/logs/compat-report.json`
2. 本阶段未运行完整 suite 与新增 8 个分支用例；compat 通过后再跑 `--case global`。
3. 时间预算已超（约 12 分钟上限，实际因 4×92s 的 compat 超时拉长），未继续重试。工作树内新增/修改均未提交：
   `M game/testcases.rpy`、`?? tools/v21_capture_fixtures.py`、`?? tools/v21_compat_check.py`、`?? tools/v21_gui_lock_exec.py`（主 Agent 修复版，未动）、`?? tools/v21_qa_project.py`、`?? tools/v21_qa_trace.rpy.txt`、`?? tools/v21_run_tests.py`（主 Agent 修复版，未动）。
4. 未修改：`doc/collaboration/v2.1/story/**`、`game/` 产品脚本、`image/**`、`.work/v21/compat-v20/**`、`.work/qa/project-fixtures/**`、全局配置、用户存档。
