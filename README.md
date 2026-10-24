# 旺不稳的奇妙冒险

基于 Ren'Py 8.5.3 制作的中文视觉小说，当前版本为 `2.0.0`。默认入口是完整续篇《樱镜町·四季镜》，同时保留旧篇《三个月，留下来》作为独立可游路线。

## 内容概览

- 续篇共八段：异象穿越、身份与相遇、春 / Dana、夏 / Luna、秋 / Irene、冬 / Ruby、四季镜终局、后日谈。
- 续篇含 12 组会改变信任、洞察或共同意志的选择，以及 Dana、Luna、Irene、Ruby、返回现实、四季同在 6 个结局。
- 旧篇完整保留开场、六章、10 组选择与稳定、上升、创业 3 个结局。
- 主菜单提供“新篇：樱镜町”和“旧篇：三个月，留下来”两个明确入口。
- 两篇状态相互隔离；旧篇结局写入 persistent，续篇会把该结果作为穿越前记忆接续，同时不破坏旧存档目录。
- 运行时共 51 张图片：27 张背景、16 张透明角色立绘、8 张剧情 CG；续篇生成源图另存于 `image/续篇/生成源图/`。
- 最终回归为 14/14 自动化用例、29/29 断言通过；Ren'Py lint 无错误或警告。

完整剧情见 [续篇大纲](doc/new-chapter-outline.md)，变量、菜单与结局条件见 [路线图](doc/sequel-route-map.md)。

## 启动与检查

使用 Ren'Py Launcher 添加本仓库根目录后启动。仓库本地验证使用官方 Ren'Py 8.5.3 SDK：

```bash
PROJECT="/Users/ik/Desktop/02_学习与资料/game/my-renpy-game"
RENPY="$PROJECT/.work/renpy-sdk/renpy-8.5.3-sdk/renpy.sh"

"$RENPY" "$PROJECT" run
"$RENPY" "$PROJECT" lint --error-code --check-unclosed-tags --all-problems
"$RENPY" "$PROJECT" test global --report-detailed
```

`.work/` 是本机忽略目录；其他环境可把 `RENPY` 换成本机 SDK 入口。直接点击“开始”会进入续篇，也可从主菜单选择任一篇章。

## 项目结构

```text
my-renpy-game/
├── README.md
├── doc/
│   ├── new-chapter-outline.md # 续篇完整剧情
│   ├── sequel-route-map.md    # 选择、变量、结局与素材映射
│   ├── game-story.md          # 旧篇剧情基线
│   ├── game-script.md         # 旧篇脚本基线
│   ├── asset-inventory.md
│   ├── development-tasks.md
│   └── test-report.md
├── image/                     # 原始素材与生成源图，只读保留
└── game/
    ├── core/                  # 双篇角色、图片定义与状态
    ├── fonts/
    ├── images/                # 规范化运行时素材
    ├── story/                 # 旧篇与续篇可执行剧情
    ├── ui/
    ├── options.rpy
    ├── gui.rpy
    ├── screens.rpy
    ├── script.rpy
    └── testcases.rpy
```

## 开发约定

- `image/` 保存原始素材和处理前版本；只在复制到 `game/images/` 后做缩放、转码与抠图。
- 运行时素材使用英文文件名与英文 image 标识，背景和 CG 统一为 `1920×1080`，角色立绘统一为 RGBA 且显示高度不超过 1024 像素。
- 剧情按章节拆分，公共角色、图片和状态分别放在 `game/core/`；两篇不得复用会污染存档的普通变量。
- 新增路线必须同步补自动化点击与结局断言，并更新 `doc/` 中的路线和素材记录。

## 当前边界

- 当前为静音版本，未引入音乐、音效和配音。
- 尚未生成 Windows、macOS 或 Linux 发布包。
- 正式发布前仍需复核 SDK 随附字体的再分发条款，并做一次发布包人工回滚与全屏体验检查。

验收明细见 [测试报告](doc/test-report.md)，素材来源、生成方式与提示词规范见 [素材清单](doc/asset-inventory.md)。
