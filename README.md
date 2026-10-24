# 旺不稳的奇妙冒险

Ren’Py 8.5.3 中文 Galgame，当前源码版本 **2.1.0**，1920×1080，macOS 静音版。两篇共 22 组选择、61 个选项、9 类结局；本版接入 23 段日常、恋爱互动与后日谈。

- 《三个月，留下来》：六章职场与恋爱故事，稳定、上升、创业三类结局各有普通／理想表现。
- 《樱镜町·四季镜》：春夏秋冬四位角色、四个角色结局、返回现实与“四季同在”真结局。
- 两篇采用平行感情世界线；续篇只回顾已完成的旧篇事业经历，感情关系独立成立。
- 沿用原有角色和 51 张图片，新增 5 张表情、2 张背景、2 张 CG；原始素材保持不变。

## 运行

已构建的 macOS 包解压后运行其中的 `.app`，不需要安装 SDK。本轮包未公证；使用常规 macOS“打开”流程，勿修改全局安全设置。实际构建、运行状态以 [验收报告](doc/test-report.md) 和随包 `build-receipt.json` 为准。

开发时使用官方 **Ren’Py 8.5.3** Launcher 添加仓库根目录，选择“启动项目”。也可运行：

```bash
/path/to/renpy-8.5.3-sdk/renpy.sh /path/to/my-renpy-game run
```

主菜单可独立选择两篇。单击或空格推进，快捷栏提供保存、读档、回退、历史、快进和自动播放；Esc 打开菜单。设置中可切换窗口／全屏、文字速度和自动播放速度。此版没有音频，设置不显示无效音量控制。

存档目录仍为 `three-months-to-stay-1`。不要为了升级删除个人存档。四份自然生成的 v2.0 代表性存档及编译语句映射纳入兼容验收；不同历史开发快照的任意编译缓存不在已验证范围内。

## 源码与验收

- `game/`：可执行剧情、状态、UI、字体与 60 张运行图片。
- `image/`：保留的原始素材；新增资源及未采用候选分开位于 `image/v21/`。
- `old-game/`：Ren’Py 保存语句身份的编译映射，清洁构建需要它，不是可随意清除的缓存。
- [协作契约](doc/collaboration/v2.1/CONTRACT.md)、[剧情接入表](doc/collaboration/v2.1/story/manifest.json)、[美术清单](doc/collaboration/v2.1/art/manifest.json)：实际分工与交付记录。
- [路线图](doc/sequel-route-map.md)：原有选择和结局规则；本版 [完整可读剧本](doc/collaboration/v2.1/readable-script/旺不稳的奇妙冒险-v2.1.0-完整剧本.txt) 由实际脚本导出，包含条件、选项和所有后日谈。
- `tools/export_story.py`：导出完整剧本到 `releases/v2.1.0/`。
- `tools/package_macos.py`：从干净的固定 Git 提交构建 macOS 包、完整源码 ZIP、校验值和构建回执。

自动化测试必须使用隔离工程、独立存档目录和 `tools/v21_run_tests.py` 的共享 GUI 锁／超时监管。不要同时启动多个 Ren’Py 测试实例。测试输入适配只用于 `test` 命令，发布包不包含测试脚本；正常模式和最终包仍需原生界面验收。

发布包排除开发文档、原图、测试、工具、SDK、缓存与存档，保留运行引擎及许可证。Source Han 字体许可证见 [OFL](licenses/SourceHanSansLite-OFL.txt)，其他声明见 [THIRD_PARTY_NOTICES.txt](THIRD_PARTY_NOTICES.txt)。
