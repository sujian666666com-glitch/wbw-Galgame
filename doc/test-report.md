# v2.1.0 验收报告

更新：2026-10-25。当前处于发行候选验收阶段，以下按实际证据区分状态。

| 范围 | 当前结果 | 证据 |
| --- | --- | --- |
| 两篇剧情／23新增片段 | 全部接入，静态交叉审查通过 | collaboration/v2.1/story/final-cross-review.md |
| 原有数值规则与菜单 | 22菜单／61选项caption与条件不变 | integration-static-check.json |
| 全量自动回归 | cold/warm各24/24用例、81/81断言通过 | qa/final-automated-report.md |
| 原两个失败 | 单跑及顺序组合通过；native旧篇存读档已复现恢复成功 | QA报告、native/progress.md |
| 选项／新增片段覆盖 | 61选项覆盖；23片段动态经过审计通过 | qa/coverage-matrix.json |
| 代表性v2.0存档 | 4/4恢复原菜单、旧值与persistent；新状态unknown | qa/compat-report.json |
| lint | 无错误或警告，998对白／22菜单／68图片声明／15屏幕 | 隔离正常模式副本，02:14运行 |
| 美术 | 9张新增逐张审查，110原图片哈希不变 | art/manifest.json、art/review.md |
| 原生完整游玩 | 旧篇高／低流程完成；三类结局普通／理想六种完成；续篇待完成 | native/progress.md |
| 实机发现UI缺陷 | slider溢出、标题折行、Esc返回已修；最终实机复测待完成 | tech/native-ui-fixes.md |
| macOS独立包 | 待构建、解压启动、复测 | 构建回执生成后登记 |
| GitHub同步 | 本轮提交尚未推送 | 最终提交与远程核对后更新 |

本报告下的短路径均相对于 `doc/collaboration/v2.1/`。自动化使用测试输入焦点适配；正常run和发行包不包含该适配。自动通过不替代原生完整游玩。

实际测试机器：macOS 26.2、Apple M4、arm64；Ren’Py 8.5.3.26051504。原生窗口虚拟1920×1080，drawable2736×1540。所有游戏测试使用隔离副本和隔离存档；兼容fixture是本任务自然生成的合成存档，未读取或重置个人存档。

范围：macOS静音版，未公证；Windows、Linux、音频、城市地图、日程探索不在本轮交付内。任意历史开发快照若没有同一编译语句映射，不在已验证旧档范围内。字体OFL及第三方声明已纳入打包配置。
