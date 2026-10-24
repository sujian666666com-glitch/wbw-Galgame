# v2.1.0 端到端验收报告

更新：2026-10-25。最终发行构建固定于 `35896bc`，随后仅补交付回执文档。**macOS 静音版的代码、剧情、自动回归、原生完整游玩与独立包复查均通过。** 没有已知阻断流程的问题。

| 范围 | 实际结果 | 证据 |
| --- | --- | --- |
| 两篇剧情／23 新增片段 | 全部接入；Claude 对实际执行脚本交叉审查通过；原生经过 23/23 | [剧情审查](collaboration/v2.1/story/final-cross-review.md)、[原生汇总](collaboration/v2.1/native/acceptance-evidence.json) |
| 原菜单、选项与素材 | 22 菜单、61 选项 caption/条件未变；110 份原图片文件哈希未变 | [静态记录](collaboration/v2.1/integration-static-check.json) |
| 全量自动回归 | 最终 27/27 用例、122/122 断言、28/28 hooks；另 4/4 旧档、22/22 兼容断言 | [Pi 最终报告](collaboration/v2.1/qa/final-ui-regression.md)、[原始测试输出](collaboration/v2.1/qa/evidence/final-global-27.log) |
| 基线两失败 | 原因定位为测试输入焦点/顺序状态，未延长超时或削弱断言；单跑、顺序组合、cold/warm 均通过；正常 UI 存读档通过 | [修复报告](collaboration/v2.1/qa/final-automated-report.md)、[证据目录](collaboration/v2.1/qa/evidence/) |
| 61 选项／23 片段覆盖 | 全部选项有用例；23 片段由真实路径动态进入 | [覆盖矩阵](collaboration/v2.1/qa/coverage-matrix.json) |
| 代表性 v2.0 存档 | 4/4 恢复原语句与原菜单、旧数值/persistent；新夏章状态为 unknown | [兼容回执](collaboration/v2.1/qa/compat-report.json) |
| lint | 无错误或警告；998 对白、22 菜单、68 图片声明、15 屏幕 | [集成记录](collaboration/v2.1/integration-review.md) |
| 美术 | 9 张新增资源逐张检查；全部进入真实画面，独立复审无阻断项 | [素材清单](collaboration/v2.1/art/manifest.json)、[GPT-6.1 Sol 原生复审](collaboration/v2.1/art/native-review.md) |
| 原生完整游玩 | 旧篇高/低、续篇理想/低信任四条全程；9 类结局全部到达，旧篇三类普通/理想六种表现均正确 | [完整验收](collaboration/v2.1/native/final-acceptance.md)、[实际游玩记录](collaboration/v2.1/native/playthrough.jsonl) |
| 存读档与交互 | 状态 3→4→读回 3；历史可见并可滚动；回滚、快进、自动、速度条、Esc、全屏、中文确认通过 | [原生验收](collaboration/v2.1/native/final-acceptance.md) |
| 独立 macOS 包 | 无 SDK 启动；无 observer/testcases；双篇入口、自然存读档、新增镜面场景与正常退出通过 | [干净包复查](collaboration/v2.1/native/clean-package-smoke.md)、[包内容检查](collaboration/v2.1/package-content-check.json) |
| 完整可读剧本 | 从产品脚本导出，998 对白、61 选项、9 类结局、23 插入，原句全量一致 | [全分支阅读版](collaboration/v2.1/readable-script/旺不稳的奇妙冒险-v2.1.0-完整剧本.txt) |

## 实际游玩与自动化的边界

四条原生路线从主菜单开始，其他结局从自然终章存档进入，不跳 label 或改状态。普通对白部分使用快进，关键新增片段、关系转折、低信任表达和结局停下来检查，并留有被动全程记录；不声称四遍逐字慢速阅读或全部 61 选项均为手动点击。自动化覆盖全部选项、四种夏章状态、真结局门槛满足与不足；原生验证实际体验、图像与交互。二者互相补充。

原生发现的 slider 溢出、标题折行、Esc 返回、历史 viewport 被滚动条挤成零宽、自动播放默认字段拼错均已修复。新增回归直接检查渲染尺寸与零输入自动推进，避免只查变量而漏掉空白界面。

## 构建与交付对应关系

产品代码和 26 份编译语句映射冻结于 `067899b7a8b525ab3b96f58d242226a0c8143370`。该产品已完成干净包复查；后续提交仅增加测试、文档与验收证据。最终交付仍从一个干净固定 Git 提交构建游戏 ZIP 和源码 ZIP，逐文件比较运行时内容与已验收产品，再解压检查。**最终构建提交、两个 ZIP 的 SHA-256 与重新启动结果记录在交付目录的 `build-receipt.json`、`release-acceptance.json` 和 `SHA256SUMS`**，不把压缩包元数据变化当成代码变化。

源码 ZIP 包含全部产品、美术原件/新增候选、测试、兼容夹具、编译映射、阅读版剧本及各 Agent 的实际报告。游戏 ZIP 排除开发文档、原图、测试、个人记录、SDK、缓存和存档。字体 OFL 与 Ren’Py 许可证保留。实际模型与调用日志指纹见 [agent-runs.json](collaboration/v2.1/agent-runs.json)，原始 CLI 日志、凭据和推理内容不随包。

最终回执已归档：[构建记录](collaboration/v2.1/release/build-receipt.json)、[最终实机验收](collaboration/v2.1/release/release-acceptance.json)。74 份初始化/UI/引擎编译文件的差异经逐项 pickle opcode 比较，仅为 `name_version`/`serial` 时间编号，另有 `CFBundleVersion` 构建时间变化；所有剧情编译文件与源码、素材一致。记录见 [编译对照](collaboration/v2.1/release/acceptance/compilation-comparison.json)。

现有 [私有 GitHub 仓库](https://github.com/sujian666666com-glitch/wbw-Galgame) 保存源码与协作提交。发行版本由 `v2.1.0` 标签固定，是否已同步以远端提交核对和交付回执为准。

## 测试环境与已知限制

实际机器为 macOS 26.2、Apple M4、arm64，Ren’Py 8.5.3.26051504；虚拟分辨率 1920×1080，窗口 drawable 2736×1540，另检查全屏。包包含 Intel/Apple Silicon 引擎，但未宣称 Intel 实机通过。此包未签名、公证；Windows、Linux、音频、城市地图、日程探索不在本轮范围。

代表性旧档为本任务在冻结 v2.0 基线上自然生成的合成存档；任意历史开发快照若没有相同编译语句映射，不在已验证范围内。测试只信任自身已核验夹具的公共验证 key，不读取用户私钥、不关闭签名验证。用户存档和全局 persistent 未改动。所有图形任务串行受锁和时限监管，退出后整组回收。

美术复审保留两项非阻断观感意见：列车人物景别略有差异、镜面提示比叙述中的浅字更亮。没有新增人物身份漂移、缺图、遮脸或流程阻断问题。
