# v2.1 冻结构建短回归（QA）

- 实际执行 Agent：Pi / **deepseek/deepseek-flash**（`PI_MODEL=deepseek-flash`，provider `deepseek`，reasoning high）
- 工作树：`.work/v21/worktrees/qa`，分支 `ik/v21-qa`，HEAD `5d35dfd`（含 `dec3500` 合并；未提交、未 push）
- 时间：2026-10-25 02:24–02:34 UTC+8
- 结论：**设置页新增 smoke、`global` 25/25、2.0 冻结存档 compat 4/4 均通过**。
- 边界：这是 **macOS 主机上的 Ren'Py SDK 自动 GUI 回归**，不是 native 界面验收，也不是 macOS 发布包验收；本报告不声明 native 或 mac 包通过。

## 1. 本次改动（仅 QA 所有权路径）

| 文件 | 改动 |
| --- | --- |
| `game/testcases.rpy` | 新增 `settings_smoke_main_menu_and_in_game`（22 断言）及两个只读 helper：`v21_pref_slider_rect` / `v21_pref_slider_point`。从实时 focus list 读取滑条几何，用 SDK `move`/`drag` 驱动真实 bar。 |
| `tools/v21_coverage_report.py` | 覆盖矩阵新增 `testcases` 计数（global / nested / total），供冻结计数更新。 |
| `tools/v21_supervisor_probe.py` | 最小可移植修复：创建 `.work/v21/supervisor-probe` 与 case 目录时使用 `parents=True`（原实现假定父目录已存在）。 |
| `doc/collaboration/v2.1/qa/resume-report.md` | 给旧的错误 `old-game` / 语句 ID 结论加历史更正标注，原文保留。 |
| `doc/collaboration/v2.1/qa/final-automated-report.md` | 给历史 `global 24` 加后续计数说明（新用例后为 25）。 |
| `doc/collaboration/v2.1/qa/coverage-matrix.json` | 用最终 `global` labels 与本次 compat 结果重新生成；新增 `testcases` 计数。 |

未修改产品剧情/UI/图片（`game/screens.rpy` 保持 Cursor 已修复版本）、`game/script.rpy`、`old-game/`、`.work/v21/compat-v20/**`、用户存档、全局配置或 `ik.md`。未 commit / push。

## 2. 新设置 smoke 的语义

用例名：`settings_smoke_main_menu_and_in_game`

主菜单阶段：
1. 从主菜单点击「系统设置」，确认 `main_menu` 屏隐藏、`preferences` 屏显示。
2. 从实时 focus list 读取两个真实滑条的矩形：
   - `text_cps` 与 `afm_time` 的高度都必须为 **28 px**（旧 bug 是 `slider` 无高度，占满剩余空间）；
   - 两个滑条的纵向间距必须 **0 < gap < 200 px**（旧 bug 约 565 px 空白，并把自动播放项挤出裁剪框）；
   - 自动播放滑条底部必须在 1080 屏幕内。
3. 先 `move` 让滑条获得焦点，再 `drag`：`text_cps` 和 `afm_time` 的偏好值都必须发生改变（验证真实 bar 可拖动，不是只检查变量）。
4. `keysym "K_ESCAPE"` 后必须回到 `main_menu`，`preferences` 消失，且 **没有** `say` / `choice` 屏（证明没有落入 `start`）。
5. 再进入设置，点击可见的「返回」，同样回到 `main_menu`。

游戏内阶段：
6. 从主菜单进入旧篇，完成序章第一个选项（`ability == 3`），记录当前语句节点、`chapter_progress` 与 `ability`。
7. 从 quick menu 打开「设置」，确认非主菜单上下文且滑条仍为 28 px。
8. `K_ESCAPE` 后必须回到同一语句节点，不是 `start`、不是新游戏；`chapter_progress` / `ability` 不变，`choice` 未出现。
9. 恢复被拖动过的 `preferences.text_cps` / `preferences.afm_time`，避免污染后续用例。

证据：`.work/qa/logs/frozen-settings-final.log`（`22/22` 断言通过，`1.207 s`）。

## 3. 隔离副本与执行结果

每个阶段使用全新构建的隔离副本；副本均含当前 `game/` 源码和冻结 `old-game/`：

- `old-game` 复制结果：**27 个文件 / 26 个 `old-game/**/*.rpyc`**（含 `v21_inserts.rpyc`）；`game/` 88 个文件。
- 所有 Ren'Py 进程均经 `tools/v21_gui_lock_exec.py` 获取共享 `.work/v21/gui.lock`，无并发 GUI。

| 运行 | 项目 / saves | 结果 | 用时 | 上限 |
| --- | --- | --- | --- | --- |
| 设置 smoke | `frozen-final-settings` / `frozen-final-settings-saves`（全新） | **PASSED**，22 断言 | 1.207 s（总 2.199 s） | 120 s |
| `global` | `frozen-final-global` / `frozen-final-global-saves`（全新） | **PASSED**，**25/25** 用例、103 断言，8 个 fixture/compat 跳过 | 20.451 s | 120 s |
| compat 4 份 | `frozen-compat-project` / 每夹具独立 saves（全新，空 `game/saves`） | **4/4 PASSED** | 1.120 / 0.936 / 0.897 / 0.930 s，合计约 6.4 s | 每份 45 s |

实际总用时约 **29 秒**（设置 2.2 s + `global` 20.5 s + compat 6.4 s），低于 120 秒总预算；compat 每份均低于 45 秒。

`global` 中的动态 label 审计仍通过：**23/23** 个 `v21_*` label 被真实控制流到达。覆盖矩阵：**22 菜单 / 61 选项全部覆盖**，`23/23` label，`testcases` 为 **25 global / 8 nested / 33 total**。

compat 读回位置与捕获时一致：

| fixture | 恢复位置 | 菜单 |
| --- | --- | --- |
| `v20_old_chapter01_menu` | `game/story/chapter_01.rpy:391` | 3 项 |
| `v20_old_chapter06_menu` | `game/story/chapter_06.rpy:748` | 3 项 |
| `v20_sequel_first_menu` | `game/story/sequel_prologue.rpy:1523` | 2 项 |
| `v20_sequel_finale_menu` | `game/story/sequel_finale.rpy:1467` | 6 项 |

旧值、persistent 与 `sequel_luna_observation_outcome == "unknown"` 均按 `v21_compat_check.py` 的严格条件校验；报告为 `.work/qa/logs/frozen-compat-report.json`（`ok: true`）。

## 4. 复用项目时发现的一次假失败（非产品回归）

第一次把 compat 直接跑在刚跑完 `global` 的同一个隔离项目上，4 份都在 45 s deadline 被回收（`exit 41`），看起来像读档回到不了原菜单。实际根因是 Ren'Py 的保存位置策略：

- `RENPY_PATH_TO_SAVES` 只决定 **user savedir**；
- Ren'Py 还会把 `<project>/game/saves` 作为 **game-local savedir** 加入 `MultiLocation`（`renpy/savelocation.py:698-703`）。

复用项目时，`global` 的 `save_load_smoke` 在 `<project>/game/saves` 写了 slot 1；compat 的 `FileLoad(1)` 因此可能优先读到这份全局测试存档，而不是夹具目录中的 2.0 存档，导致等待菜单超时。改用全新 `frozen-compat-project`（`game/saves` 为空）后 4/4 立即通过，恢复位置和旧值全部正确。因此：

- **不是** 语句 ID / `old-game` 映射回归；
- 复用隔离项目跑 compat 前，必须清空 `<project>/game/saves` 或使用新副本；
- 本报告的最终 compat 证据来自全新副本。

## 5. GUI 锁 / 超级visor 复核

复核 `tools/v21_gui_lock_exec.py`：

- 子进程以 `start_new_session=True` 启动，`pgid == child.pid`；
- 先 SIGTERM，宽限 2 s；仍在则 SIGKILL；
- SIGKILL 后 **不立即解锁**，继续最多 5 s 等待整个进程组从内核消失，超时则抛 `RuntimeError` 而不是静默放锁；
- `group_alive` 在 `os.killpg(pgid, 0)` 返回 `EPERM` 时，仅查询 `ps -axo pgid=,stat=`，忽略 `Z`（zombie）状态；不读取命令行、不输出密钥或用户数据；
- `child.wait(timeout=5)` 后仍按 pgid 检查组，覆盖“wrapper 先退出、孙进程仍活着”的泄漏场景。

实测 `python3 tools/v21_supervisor_probe.py`：**5/5 通过**（`normal` / `deadline` / `signal` / `pause` / `owner`），每例均为 3 代进程、child 与 grandchild 都忽略 SIGTERM，结果 `descendants_dead: true`、`lock_released: true`，退出码分别为 0 / 41 / 143 / 42 / 43。记录在 `.work/v21/supervisor-probe/result.json`；主仓库同一路径已有集成的 5/5 record（pids 不同），本次工作树复跑结果一致。

EPERM 分支另做了同 uid 模拟（强制 `os.killpg(pgid, 0)` 抛 `PermissionError`）：`group_alive(当前组)` 经 `ps` 返回 `True`；一个已回收组的 pgid 返回 `False`。说明 `pgid=,stat=` 查询与 zombie 过滤可用。该分支未被真实 EPERM 触发，仅模拟验证。

## 6. 历史结论更正

`resume-report.md` 第 4 节原判断“`old-game` 不是 Ren'Py 兼容机制、compat 4/4 失败由语句 ID 变化导致”**错误**。`final-automated-report.md` 已给出实际根因（签名验证 UNKNOWN/TRUST 弹窗 + testsuite 嵌套）并记录修复后 4/4 通过；Ren'Py 8.5.3 确实读取 `old-game`（`renpy/script.py:843`）。本次在 `resume-report.md` 顶部、第 4 节和“下一步”处加了更正标注，原文与历史日志均保留，未删除证据。

## 7. 未完成 / 不在结论内

- 未做 native 界面验收、Windows/Linux 验收、macOS 发布包验收，不声明这些通过。
- compat 夹具仍是冻结 2.0 基线上的自产合成存档，不代表真实用户存档升级。
- 未提交、未推送；后续 native / 打包 GUI 由主 Agent 接管。
- 新设置 smoke 首次诊断中的失败均已定位为测试输入/坐标与复用项目存档污染问题，最终用例在全新副本上稳定通过；未无限重试。
