# 三个月，留下来

基于 Ren'Py 8.5.3 制作的中文视觉小说第一版。游戏已实现开场、六章主线、9 组有实际影响的选择，以及稳定、上升、创业三个可选结局。

## 启动与检查

使用 Ren'Py Launcher 添加本仓库根目录后启动，或使用官方 SDK 命令：

```bash
RENPY="/Volumes/renpy-8.5.3-sdk/renpy-8.5.3-sdk/renpy.app/Contents/MacOS/renpy"
PROJECT="/Users/ik/Desktop/02_学习与资料/game/my-renpy-game"

"$RENPY" "$PROJECT" run
"$RENPY" "$PROJECT" lint --error-code --check-unclosed-tags --all-problems
"$RENPY" "$PROJECT" test global --report-detailed
```

当前 SDK 路径来自已挂载的 Ren'Py 8.5.3 官方 SDK 镜像；其他环境请替换为本机 SDK 路径。

## 已实现内容

- 默认分辨率 `1920×1080`，自定义主菜单、对话、选择、历史、设置、存档与读档界面。
- 好感度、能力值、金钱、章节进度、关键证据与创业伏笔状态。
- 快捷菜单“状态”面板，以及关键数值变化通知。
- 六章顺序主线与三个始终可选、按数值呈现普通或理想表现的结局。
- 30 张正式运行时图片：16 张背景、12 张透明角色立绘、2 张剧情 CG。
- 项目内简体中文字体，避免依赖本机字体绝对路径。
- 7 个 Ren'Py 自动化用例，覆盖完整理想稳定流程、三个普通/理想结局与存读档恢复。

## 项目结构

```text
my-renpy-game/
├── README.md
├── doc/
│   ├── game-story.md
│   ├── game-script.md
│   ├── asset-inventory.md
│   ├── story-additions.md
│   ├── development-tasks.md
│   └── test-report.md
├── image/                     # 原始素材，只读保留
└── game/
    ├── core/                  # 角色、图片定义与状态
    ├── fonts/                 # 运行时中文字体
    ├── images/                # 规范化运行时素材
    ├── story/                 # 开场、六章与结局
    ├── ui/                    # 状态界面
    ├── options.rpy
    ├── gui.rpy
    ├── screens.rpy
    ├── script.rpy
    └── testcases.rpy
```

## 开发约定

- `image/` 仅保存原始素材和处理前备份，不在其中覆盖或删除文件。
- 素材复制到 `game/images/` 后再转码、缩放或抠图，运行时使用英文文件名与英文 image 标识。
- 剧情按章节拆分；公共角色、图片和状态分别放在 `game/core/`。
- 新增剧情和素材处理需同步更新 `doc/` 中的对应记录。

## 当前限制

- v1 为静音版本，未引入音乐、音效和配音。
- 尚未生成 Windows、macOS 或 Linux 发布包；正式发布前需复核 SDK 随附字体的再分发条款。
- 自动化完整流程覆盖理想稳定路线；其余普通选项已做静态检查，但未逐项进行人工通读。

完整验收结果见 [测试报告](doc/test-report.md)，素材来源与处理记录见 [素材清单](doc/asset-inventory.md)。
