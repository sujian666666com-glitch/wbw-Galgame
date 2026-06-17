# 测试报告

## 测试环境与结论

| 项目 | 记录 |
| --- | --- |
| 测试日期 | 2026-06-10 |
| 游戏版本 | `1.0.0` |
| Ren'Py SDK | 官方 Ren'Py 8.5.3 |
| 操作系统 | macOS 26.2，Apple Silicon |
| 设计分辨率 | `1920×1080` |
| 中文字体 | `game/fonts/SourceHanSansLite.ttf` |
| 总体结论 | 第一版通过运行、lint 与自动化主流程验收；发布包尚未生成 |

## 已执行命令

```bash
RENPY="/Volumes/renpy-8.5.3-sdk/renpy-8.5.3-sdk/renpy.app/Contents/MacOS/renpy"
PROJECT="/Users/ik/Desktop/02_学习与资料/game/my-renpy-game"

"$RENPY" "$PROJECT" lint --error-code --check-unclosed-tags --all-problems
"$RENPY" "$PROJECT" test global --report-detailed
"$RENPY" "$PROJECT" run
```

## 测试结果

| 编号 | 测试项 | 实际结果 | 状态 |
| --- | --- | --- | --- |
| T-001 | Ren'Py lint | 234 个对话块、10 个菜单、29 张图片、14 个 screens；无错误与警告 | 通过 |
| T-002 | 项目启动 | 正常进入主菜单，标题、中文字体和背景显示正常 | 通过 |
| T-003 | 完整主线 | 从主菜单推进开场、六章并进入稳定理想结局 | 通过 |
| T-004 | 稳定结局 | 普通与理想表现均可到达 | 通过 |
| T-005 | 上升结局 | 普通与理想表现均可到达 | 通过 |
| T-006 | 创业结局 | 普通与理想表现均可到达 | 通过 |
| T-007 | 状态变量 | 章节、好感度、能力、金钱和路线断言通过 | 通过 |
| T-008 | label 与分支回收 | 六章顺序跳转与三个结局跳转无死路 | 通过 |
| T-009 | 存档与读档 | 保存后改变能力值，再读档正确恢复 | 通过 |
| T-010 | 素材显示 | 运行时素材均可载入；角色透明通道与主菜单背景视觉检查正常 | 通过 |
| T-011 | 回滚与全部普通选项人工通读 | 未逐项人工执行 | 未执行 |
| T-012 | 目标平台打包 | 未生成发布包 | 未执行 |

自动化汇总：

```text
Test suites: 1/1 passed
Test cases: 7/7 passed
Hooks: 7/7 passed
Assertions: 10/10 passed
Time: 7.632s
```

## 自动化用例

- `full_flow_stable_ideal`：完整理想稳定路线。
- `stable_normal`、`rising_normal`、`startup_normal`：三个普通结局表现。
- `rising_ideal`、`startup_ideal`：上升与创业理想表现。
- `save_load_smoke`：标准保存、读取及状态恢复。

## 静态与素材检查

- 所有公开状态变量均使用 `default` 在使用前初始化。
- 既有基线中所有 `scene`、`show` 使用的运行时图片均已定义并成功通过 lint；本次新增 CG 已完成静态引用检查，待 SDK 回归。
- 16 张背景与 2 张 CG 均为真正 PNG、`1920×1080`。
- 12 张角色立绘均为真正 RGBA PNG，具备透明通道。
- 除按用户要求删除旧主角江临的两张原始立绘外，其余 `image/` 原始素材未删除或覆盖。

## 增量验收记录：2026-06-17

本次变更加入用户提供的四人客厅合影，并接入第三章“小爆款”活动主视觉段落。

已执行静态引用检查：

```text
defined_image_files= 30
image_definitions= 30
referenced_images= 84
missing_files= []
missing_defs= []
new_cg= ((1920, 1080), 'RGB')
```

未执行 Ren'Py lint 与自动化测试：README 记录的 `/Volumes/renpy-8.5.3-sdk/renpy-8.5.3-sdk/renpy.app/Contents/MacOS/renpy` 当前未挂载，本机也未发现可替代的 Ren'Py SDK 命令入口。已确认旁边的 `Agent17.app` 为打包运行时，会直接启动原 app，不适合对本项目执行 lint/test。

## 主角更换回归

- 删除旧主角江临的原始与运行时立绘，代码、界面及剧情统一改为王不稳。
- 王不稳普通、自信立绘均为真正 RGBA PNG，四角透明，统一显示高度为 1024 像素。
- 两张真人参考图与两张 Image Gen 生成源图保存在 `image/人物/王不稳/`，正式透明立绘保存在 `game/images/characters/`。
- 使用办公室背景按游戏实际定位合成预览，立绘尺寸、透明边缘和站位检查通过。

## 已知问题与剩余风险

- v1 为静音版本，尚无音乐、音效和配音。
- 未逐项人工通读所有非理想选择，也未专项验证每次回滚后的变量体验。
- 尚未生成 Windows、macOS、Linux 发布包。
- 正式发布前需复核 SDK 随附字体的再分发条款。
