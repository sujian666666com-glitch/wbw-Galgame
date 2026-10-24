# 最终 UI 回归 + 27 项 global + 2.0 兼容：实际执行报告

- 实际模型：`PI_PROVIDER=deepseek`，`PI_MODEL=deepseek-flash`（契约角色 Pi / deepseek-flash）
- 工作树：`.work/v21/worktrees/qa`，HEAD `5a3801d`
- 执行时间：2026-10-25 04:17–04:18（本机）
- Ren'Py：8.5.3.26051504 / macOS-26.2-arm64 / Python 3.12.8
- GUI 锁：主仓库 `.work/v21/gui.lock`，四次运行全部经 `tools/v21_run_tests.py` → `v21_gui_lock_exec.py` 独占获取并带 `--max-runtime 120`；日志内可见 `lock acquired ... limit 120s` 与 `child group reaped; lock released`
- 结论：两个新回归、最终 `global`（27 项）、4 个 2.0 兼容 fixture 全部**首次运行即通过**。没有修改任何 testcase 断言，没有修改产品剧情/UI/图片/options/存档。本节结果全部为真实 Ren'Py 进程 + 真实点击/等待，不是静态推断。

## 1. 执行结果（每次都是全新隔离工程 + 全新存档根）

| # | 用例 | 隔离工程 / 存档 | 用例数 | 断言 | 用时 | 结果 | 日志 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `history_panel_visible_text` | `.work/qa/project-ui-history` / `.work/qa/saves-ui-history` | 1 | 9/9 | 3.671 s | PASSED | `.work/qa/logs/ui-history.log` |
| 2 | `auto_forward_advances_by_default` | `.work/qa/project-ui-afm` / `.work/qa/saves-ui-afm` | 1 | 10/10 | 3.894 s | PASSED | `.work/qa/logs/ui-afm.log` |
| 3 | `global`（最终全量，27 项） | `.work/qa/project-final-27` / `.work/qa/saves-final-27` | 27 | 122/122 | 22.409 s | PASSED | `.work/qa/logs/final-global-27.log` |
| 4 | 2.0 兼容 4 fixture | `.work/qa/project-final-compat`；每 fixture 独立 `.work/qa/compat/<id>/saves` | 4 | 5+4+7+6=22/22 | 0.87–0.99 s/项 | 4/4 PASSED | `.work/qa/logs/compat-*.log`、`.work/qa/logs/compat-report-final.json` |

每次工程都由 `tools/v21_qa_project.py --clean` 新建，`game/` 不复制 `.rpyc`、`old-game/` 完整复制 27 个文件（含 26 个 `.rpyc`），存档根均为新建目录。四次的 `--max-runtime` 都是 120 s，实际最长 22.4 s。

### 1.1 global 的 27 项（与矩阵一致）

`full_flow_stable_ideal`、`rising_ideal`、`startup_ideal`、`stable_normal`、`rising_normal`、`startup_normal`、`save_load_smoke`、`sequel_full_flow_true_ending`、`sequel_dana_ending`、`sequel_luna_ending`、`sequel_irene_ending`、`sequel_ruby_ending`、`sequel_return_ending`、`sequel_origin_rising_smoke`、`full_flow_startup_ideal`、`full_flow_low_old`、`full_flow_mid_old`、`sequel_low_trust_flow`、`sequel_partial_trust_flow`、`sequel_true_gate_insight_short`、`sequel_true_gate_missing_fragment`、`ui_features_smoke`、`settings_smoke_main_menu_and_in_game`、`old_chapter_02_public_evidence`、`history_panel_visible_text`、`auto_forward_advances_by_default`、`v21_label_traversal_audit`。

- 汇总：Test cases 27 passed / 0 failed；Test hooks 28/28；Assertions 122/122；Status PASSED。
- 真实到达的插入 label：`.work/qa/logs/global-labels-final-27.txt` 共 82 行、去重 23 个，`v21_label_traversal_audit` 通过，说明 23 个片段全部由真实游玩路径进入，不是直接 `call` label。
- 基线两失败（`save_load_smoke` 的 ability 断言、`sequel_full_flow_true_ending` 的主菜单等待）本次均通过，未延长任何超时。

## 2. 两个回归的断言（原设计原样，未削弱）

### 2.1 `history_panel_visible_text`（9 条断言）

真实路径：主菜单“旧篇：三个月，留下来” → 首个选项 → 被动等 `先把能做的事列清楚` 进入历史 → 点“历史” → 等 `v21_history_metrics` 返回 → 读取正在渲染的 `side()`/`Viewport`/`Text` 布局 → 点“返回游戏”。

- 进入时 `ability == 3`；
- `0 < bar_width <= 64`（竖滚动条是 18 px 窄条，不是整帧宽）；
- `center_width >= 900`（中间对白栏未被挤到 0）；
- `text_width >= 200`（这句对白真的排版出宽度，不是 0 宽竖排）；
- `0 < text_height <= 400`；
- 关闭面板后 `renpy.get_screen("history") is None`。

关键回归点仍是“历史里有字符串”不够——断言读的是实际渲染 layout，因此面板空白会直接失败。

### 2.2 `auto_forward_advances_by_default`（10 条断言）

- `preferences.afm_time > 0`（默认值本身必须非零，先于一切改动）；
- 用真实快捷菜单按钮打开自动播放，`preferences.afm_enable` 为真；
- 之后**零输入**，25 s 上限内等到 `_history_list` 增长；
- `say` 屏仍在；语句节点 `id()` 改变；历史条目恰好 `+1`；新增条目是 `call v21_prologue` 的第一句“楼道里的感应灯坏了三盏”；`afm_enable` 仍为真；`renpy.config.skipping is None`（排除快进冒充自动推进）。

用时 3.068 s，远小于 25 s 上限，说明推进来自真实 `afm_time` 延迟而不是超时后放过。

## 3. `tools/v21_compat_check.py` 最小加固

只加输入守卫，没有改检查逻辑、没有改 fixture 信任策略、没有扩大重构：

1. `require_clean_input()`：扫 `project/game`、`project/saves`，发现任何 `.save` 或 `persistent` 立即 `SystemExit`，报错要求用 `tools/v21_qa_project.py` 新建隔离副本，并明确“本工具不会删除不是自己创建的存档/持久化文件”。
2. `validate_project()`：拒绝把源仓库本身当 `--project`；拒绝没有 `old-game/*.rpyc` 的工程（没有 2.0 编译树就不可能有真实的语句身份恢复）。
3. 每个 fixture 的 saves 根在复制 fixture 之前也做同一守卫；`--keep` 复用旧目录时会明确拒绝而不是悄悄清空。
4. 默认 fixture 根改为已纳入源码的 `doc/collaboration/v2.1/compatibility/v20`（manifest 存在时优先）；`--fixtures` / `V21_COMPAT_ROOT` 仍可显式指定，`.work/v21/compat-v20` 作为后备仍可用。

守卫自检（不启动 Ren'Py，均为预期失败）：

| 输入 | 结果 |
| --- | --- |
| `--project .`（源码树） | 退出码 1：“refusing to verify compatibility against the source checkout itself” |
| 工程 `game/leftover.save` + `saves/persistent` | 退出码 1：“refusing fake compatibility check: project game/ already contains Ren'Py save state”，并列出文件 |
| 工程缺 `old-game/*.rpyc` | 退出码 1：“project has no compiled 2.0 old-game tree” |

实测兼容运行使用的 fixture 根：`doc/collaboration/v2.1/compatibility/v20`；该目录 manifest 与 `.work/v21/compat-v20/manifest.json` 逐字节相同，8 个 fixture 文件 SHA-256 全部与 manifest 一致。

## 4. 2.0 兼容结果（单独新工程，不与 global 共用）

- report：`.work/qa/logs/compat-report-final.json`（`ok: true`，`checked: 4`，`max_runtime: 120`）
- 信任策略未变：只信任 4 个已批准 fixture 自身 save/persistent 里的**公钥**，不读取私钥、不碰全局 token store。
- 每个 fixture 的恢复位置都与捕获时一致，且都是真实菜单，不是 `start` 回退：

| fixture | 恢复语句 | 菜单 | 断言 | 结果 |
| --- | --- | --- | --- | --- |
| `v20_old_chapter01_menu` | `game/story/chapter_01.rpy:391` | 3 项 | 5/5 | PASSED |
| `v20_old_chapter06_menu` | `game/story/chapter_06.rpy:748` | 3 项 | 4/4 | PASSED |
| `v20_sequel_finale_menu` | `game/story/sequel_finale.rpy:1467` | 6 项 | 7/7 | PASSED |
| `v20_sequel_first_menu` | `game/story/sequel_prologue.rpy:1523` | 2 项 | 6/6 | PASSED |

2.0 数值逐项保留；`sequel_luna_observation_outcome` 在 2.0 档里仍为 `default` 的 `unknown`。

## 5. 机器产物更新

- `doc/collaboration/v2.1/qa/coverage-matrix.json`：由 `tools/v21_coverage_report.py` 用本次实测证据重新生成
  - 菜单 22 / 选项 61 / 覆盖 61 / 缺失 0，`ok: true`
  - v2.1 label 23 / 动态到达 23 / 缺失 0，`ok: true`
  - testcases 35 总计（global 27，fixture+compat 8）
  - compat 4 项均 `passed`
  - `generated_from` 指向 `.work/qa/logs/global-labels-final-27.txt` 与 `.work/qa/logs/compat-report-final.json`
- `doc/collaboration/v2.1/qa/compat-report.json`：替换为本次 `compat-report-final.json` 的实际内容（fixture 根为源码内 `doc/.../compatibility/v20`，4/4 passed）

## 6. 遗留与未解决

1. **仍待人工**：真实 app 打包成品上亲手看一次历史面板滚动与默认自动播放。本报告证明的是自动化测试驱动真实界面，不等同于主 Agent 的最终成品观感验收。
2. **有意行为**：compat `--keep` 复用含 `.save`/`persistent` 的 saves 根会被拒绝，需要换新目录——这是为了防止假兼容验证，不是缺陷。
3. **量纲依赖**：历史回归的阈值绑定现有 `vscrollbar_xsize 18`、`gui.text_size 34`（`bar_width <= 64`、`text_width >= 200`、`text_height <= 400` 留有余量）。若日后改字号或滚动条宽度，需要按新设计同步阈值，不能当作放宽断言。
4. **未做**：未 commit、未 push、未改个人学习清单、未写其它工作树、未改 `game/testcases.rpy` 之外的产品文件、未改存档/全局配置。
5. 结束检查：无 Ren'Py 进程残留；`gui.lock` 为 `released`；工作树内除源码自带的 `doc/.../compatibility/v20/**` fixture 存档外没有新增 `.save`/`persistent`，`game/saves` 不存在。
