# 主集成审查与问题关闭记录

本文件区分代码检查、自动测试、原生界面、发行包验收；后者未完成前不宣称交付通过。

## 已关闭的静态问题

- 主Agent核对原61个选项caption与条件与1737ed6完全一致，23个新增label各调用一次；110份原始图片哈希不变。机器记录见integration-static-check.json。
- Claude Code/DeepSeek独立审查实际运行脚本，未发现阻断性剧情矛盾，见story/final-cross-review.md。春庭离场画面在下一章切换，语意连贯，无需额外换景；上升线好感12–14的关系由谨慎问句发展到结局邀约，沿用旧门槛。时段变体以tech/story-integration.md映射为准。历史review.md中的旧概括不覆盖最新逐项报告。
- 五项模拟进程均确认子孙进程被回收、锁释放，见process-guard-probe.json。真实兼容失败运行也在90秒截止后自动清理，无孤儿进程。
- 隔离正常模式副本（无testcases.rpy，仅只读observer）已通过Ren’Py 8.5.3 lint，998对白、22菜单、68 image声明、15屏幕，无错误或警告。

## QA旧报告纠正

qa/resume-report.md是首次恢复阶段的失败快照，不代表最终验收。其“old-game不是兼容机制”的结论错误：SDK renpy/script.py load_file先从oldrpycfn合并语句名称，olddir以动态字符串构造，所以只grep字面old-game会漏查。launcher/game/distribute.rpy还提供update_old_game命令。实际实现遵循该官方机制，不采用猜状态的读档迁移。

主Agent另已证实四份合成fixture签名公钥都不在新隔离saves/tokens的信任集合中；因此FileLoad(confirm=False)仍受check_load中的UNKNOWN_TOKEN提示约束。兼容工具应先校验固定fixture哈希，再仅为其隔离目录登记对应公共验证key，不能关闭验证、复制私钥或修改用户全局tokens。

另发现fixture与compat testcase原为顶层，实际都归global；修正嵌套后应检查suite注册结果。兼容循环应首错即停，避免重复同类超时。上述问题交回Pi修复，结果以其后续报告为准。

## 后续复核

Pi最终报告已明确纠正old-game误判，4份兼容夹具、cold/warm 24用例81断言均通过。Cursor对监管的审查后，主Agent补充了SIGKILL后等待进程组消失，以及Darwin空组瞬时EPERM状态处理；三代进程、子与孙均忽略TERM的五项probe全部通过，确切mock已纳入tools/v21_supervisor_probe.py。外部主动SIGKILL监管器、进程自行setsid脱组不是现有RenPy调用链行为，仍不承诺监管器无法被强制杀死。

原生验收发现三项自动化未覆盖的UI缺陷，已由Cursor修复并合入，见tech/native-ui-fixes.md。正常模式旧篇高低及全部六种结局表现已完成，续篇和发行包继续验收。
