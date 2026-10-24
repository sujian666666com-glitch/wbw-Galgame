# v2.1 QA 自动验收报告（实际执行）

- 执行 Agent：Pi / **deepseek/deepseek-flash**（reasoning high）
- 工作树：`.work/v21/worktrees/qa`，分支 `ik/v21-qa`（基线 `edb4a7a`，未提交、未 push）
- 时间：2026-10-25 01:32–01:40 UTC+8
- 结论：**自动 GUI 验收全部通过**（compat 4/4、global cold/warm 全通过、两项基线用例单跑与顺序组合通过）。未做 native/发布包验收，不声明 release 通过。
- 未改动：产品剧情/UI/图片、`.work/v21/compat-v20/**`、用户存档、全局 `security_keys.txt`、个人学习清单。仅改 QA 所有权路径。

## 1. 根因 A：签名验证弹窗（已修复）

- 四份 fixture 的 save `signatures` 与 persistent 尾部签名均带公共验证 key；隔离 saves 的 SDK 新私钥不匹配，`renpy/savetoken.py:141 check_load` 进入 `UNKNOWN_TOKEN/TRUST_TOKEN`，`FileLoad(confirm=False)` 不绕过，故 4 例都卡在 `advance until screen "choice"`。
- 修复仅在 QA 工具侧：先按 manifest 校验四份 fixture 的文件 SHA-256；通过后，从**该 fixture 自己的 save 签名**提取公共验证 key（persistent 签名 key 必须相同），写入它自己的隔离目录 `<fixture>/saves/tokens/security_keys.txt`（`verifying-key` 行）。SDK 仍为该隔离目录新建自己的私钥，save 安全验证保持开启。
- 安全边界：
  - 只信任 `v20_old_chapter01_menu` / `v20_old_chapter06_menu` / `v20_sequel_first_menu` / `v20_sequel_finale_menu` 四个已批准、hash 固定的自产合成 fixture；其他 id 直接拒绝。
  - 只写公共验证 key；不读取/复制/输出任何私钥，不访问全局或用户 tokens。报告中只记录 key 的 SHA-256 指纹。
  - 不复制/不修改 `.work/v21/compat-v20` 原夹具；`v21_capture_fixtures.py --check` → `checked 4 fixtures: ok`。
- 兼容性关键：`old-game/` 确实被 Ren'Py 运行时使用（`renpy/script.py:843` 以 `base + "/old-" + game` 读取），此前“old-game 无运行时作用”的判断不成立。四份存档读回后均停在捕获时的原语句与真实菜单。

## 2. 根因 B：testsuite 语法（已修复）

- SDK 语法：`testcase` 只有缩进在 `testsuite` 块内才有父 suite；顶层 testcase 会在 `setup_global_test_suite()` 中全部并入 `global`（旧日志的 `global::compat_*`）。
- 现已将 4 个 capture 用例缩进到 `testsuite fixtures:`，4 个 compat 用例缩进到 `testsuite compat:`，并给两个 suite 加 `enabled False`：`--case global` 时两 suite 被跳过（本次输出 `8 skipped`），显式运行 `compat::compat_*` / `fixtures::capture_*` 时仅选中的 suite 启用。
- 工具已同步改为 suite 全路径：`--case compat::compat_<id>`、`--case fixtures::capture_<id>`。

## 3. 执行证据（实际命令输出，全程共享 `gui.lock`，无并发）

| 运行 | 结果 | 用时 |
| --- | --- | --- |
| 首个 compat `compat::compat_v20_old_chapter01_menu`（带 trace） | PASSED，停在 `game/story/chapter_01.rpy, 391`，3 个选项 | 3.2 s |
| 其余 3 份 compat（逐份 ≤45 s） | PASSED | 合计 5.7 s |
| 最终 4 份 compat 一次跑（带 trace） | **4/4 PASSED**，`ok: true` | 6.4 s |
| `save_load_smoke` 单跑 | PASSED | 4.6 s |
| `sequel_full_flow_true_ending` 单跑 | PASSED | 5.0 s |
| 上述两例顺序组合（同 saves 根连续两次） | 两次均 PASSED | 8.6 s |
| `global` cold（新项目拷贝 + 新 saves） | **PASSED**，24 个回归用例；8 个 fixture/compat 跳过 | 22.6 s |
| `global` warm（同拷贝/saves 重跑） | **PASSED** | 22.0 s |

> 计数说明（后续更新）：本报告执行时 `global` 为 24 个用例。新增 `settings_smoke_main_menu_and_in_game` 后，最终冻结构建的 `global` 为 **25 个用例**（25/25 通过，103 断言）；机器可读计数见 `coverage-matrix.json` 的 `testcases` 字段，执行证据见 `frozen-build-regression.md`。

- 所有进程在报告完成后正常退出（`Status: PASSED`，无“报告完成但不退出”）；未延长任何超时，未反复重试同一失败。
- 四个 compat 的恢复位置：`chapter_01.rpy:391`、`chapter_06.rpy:748`、`sequel_prologue.rpy:1523`、`sequel_finale.rpy:1467`；旧值、persistent 与 2.1 新变量 `default`（`sequel_luna_observation_outcome == "unknown"`）全部一致。
- Trace 现在包含正在显示的 screens 与 `confirm_text`。首个 compat trace 在读档后为 `screens: ["choice", "say"]`、`confirm_text: null`，证明未出现 UNKNOWN/TRUST 提示。

## 4. 新增覆盖与机器可读矩阵

产物：`doc/collaboration/v2.1/qa/coverage-matrix.json`、`doc/collaboration/v2.1/qa/compat-report.json`。

- **61 选项 / 22 菜单**：静态扫描 `game/story/*.rpy` 并与 `game/testcases.rpy` 的 `click` 逐一匹配，**61/61 覆盖，0 缺失**。新增 `old_chapter_02_public_evidence` 补上此前唯一未点击的“发到工作群里公开指出问题”。
- **23 个新增 label 动态经过**：QA-only `config.label_callbacks` 记录真实控制流进入的 `v21_*` label；global cold/warm 末尾审计用例断言 **23/23 全部到达**（非直接 call label 造假），缺失即失败。
- **夏章四值**：`unknown`（compat 读档默认）、`paper_tape`（真结局全程）、`aborted`（低信任流程）、`evacuated`（部分信任流程），均有 testcase 断言。
- **四女主低信任**：`sequel_low_trust_flow` 断言 Dana/Luna/Irene/Ruby 信任均为 0；部分信任流程另断言 0/0/3/4。
- **真结局条件**：满足（真结局流程 + compat 终章 6 选项）与不足（`sequel_true_gate_insight_short`、`sequel_true_gate_missing_fragment`）均断言选项被正确过滤；未改动产品逻辑。

## 5. 产物与未完成项

新增/修改（均未提交）：
- `game/testcases.rpy`：suite 嵌套、`enabled False`、四值/低信任断言、61 项补测、23 label 动态审计。
- `tools/v21_compat_check.py`：hash 校验 + 仅公共 key 信任、suite 全路径、trace。
- `tools/v21_capture_fixtures.py`：suite 全路径。
- `tools/v21_run_tests.py`：`--label-file`。
- `tools/v21_coverage_report.py`：机器可读覆盖矩阵。
- `tools/v21_qa_trace.rpy.txt`：记录显示中 screens 与 confirm 文本。
- `doc/collaboration/v2.1/qa/{final-automated-report.md,coverage-matrix.json,compat-report.json}`。

未完成/不在本报告结论内：
- 未验证 native/Windows/Linux、发布包、真实用户存档升级；compat 夹具为冻结 2.0 基线上自产合成存档。
- 未发现需上报的产品 bug；`old-game` 语句 lineage 在 8.5.3 上工作正常。
- 未 commit / push，未操作 GUI 以外的全局配置，未修改个人学习清单。
