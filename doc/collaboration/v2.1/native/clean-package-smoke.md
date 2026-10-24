# 无测试脚本的 macOS 包复查

2026-10-25 04:22:55–04:33:50（UTC+8），主 Agent 通过原生 CUA 操作。macOS 26.2 / Apple M4 / arm64 / Ren’Py 8.5.3.26051504。

- 固定产品提交：`067899b7a8b525ab3b96f58d242226a0c8143370`。
- 测试 ZIP SHA-256：`58fe95b60d0236b83eef09cb3e59e780419ff5b4e3926c5162d007dbb41a5b00`。
- `archive.rpa` SHA-256：`a337c2b76f5f071dcc9518e511b592b4436e441e277feb7848629eb5f4b36f29`。
- 解压目录 `.work/v21/clean-package/three_months_to_stay.app`；直接运行包内 `Contents/MacOS/three_months_to_stay`，未调用 SDK。
- 应用没有添加 observer、testcases 或测试输入适配；仅用环境变量将存档隔离到本任务目录。共享 GUI 锁和 900 秒上限监管。

## 实际结果

1. 主菜单正常显示，设置中的两根速度条正常；初始自动播放速度非零，窗口标题和中文排版正常，见 `clean-default-preferences.png`。
2. 从旧篇入口正常开始，序章选行动清单后进入第一章，状态为能力 3、好感 0、资金 1100。通过保存页写第 1 页第 1 槽；随后选第一项，状态变为能力 4、好感 3。通过读取页确认读档，状态恢复能力 3、好感 0、资金 1100，且回到原菜单，见 `clean-save-load-restored.png`。
3. 正常返回主菜单并启动续篇，快进在第一个两项菜单停止；选择“逐项核对文件、日期和签名”，继续点击进入旧宅。新增镜面背景、叠字“请不要独自记住”和完整对白均显示，见 `clean-mirror-scene.png`。
4. Esc → 退出游戏 → 中文确认。真实进程返回 0，监管器报告 `child group reaped; lock released`；未依靠超时杀掉游戏。

此记录验证可交付产品的干净包。最终报告归档后可重新构建；最终检查确认源码、图片、字体与全部剧情编译语句逐字节一致；74 份初始化/UI/引擎编译文件仅有经过逐项 opcode 核验的时间编号变化，另有应用构建时间号变化。最终包再次解压启动、读档、进入新增镜面片段并正常退出后，沿用本次及四条完整路线的验收。详见 `../release/acceptance/compilation-comparison.json`。最终产物提交与校验值以随包 `build-receipt.json`、`release-acceptance.json` 为准，避免把后续文档提交冒称为本次测试时的提交。
