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
Time: 6.163s
```

## 自动化用例

- `full_flow_stable_ideal`：完整理想稳定路线。
- `stable_normal`、`rising_normal`、`startup_normal`：三个普通结局表现。
- `rising_ideal`、`startup_ideal`：上升与创业理想表现。
- `save_load_smoke`：标准保存、读取及状态恢复。

## 静态与素材检查

- 所有公开状态变量均使用 `default` 在使用前初始化。
- 所有 `scene`、`show` 使用的运行时图片均已定义并成功通过 lint。
- 16 张背景与 1 张 CG 均为真正 PNG、`1920×1080`。
- 12 张角色立绘均为真正 RGBA PNG，具备透明通道。
- 原始 `image/` 未删除或覆盖。

## 已知问题与剩余风险

- v1 为静音版本，尚无音乐、音效和配音。
- 未逐项人工通读所有非理想选择，也未专项验证每次回滚后的变量体验。
- 尚未生成 Windows、macOS、Linux 发布包。
- 正式发布前需复核 SDK 随附字体的再分发条款。
