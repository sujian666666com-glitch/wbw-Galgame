# 测试报告

## 测试环境与结论

| 项目 | 记录 |
| --- | --- |
| 测试日期 | 2026-07-13 |
| 游戏版本 | `2.0.0` |
| Ren'Py SDK | 官方 Ren'Py 8.5.3，构建号 `8.5.3.26051504` |
| SDK SHA-256 | `eb0a9be7f0fb13632fe25ceade9a8bed5a1b4d6b6e83bd19eeeb29e1a1bb4a45` |
| 操作系统 | macOS 26.2，Apple Silicon |
| 设计分辨率 | `1920×1080` |
| 总体结论 | 双篇 v2 通过 lint、真实素材加载和全部自动化路线验收；发布包尚未生成 |

## 隔离验证方式

最终测试没有直接使用用户现有存档和缓存。仓库被复制到 `.work/renpy-final-audit.*`，排除 `.git`、`.work`、`game/saves`、`game/cache` 与编译产物，并通过独立 `RENPY_PATH_TO_SAVES` 运行。

```bash
PROJECT="/Users/ik/Desktop/02_学习与资料/game/my-renpy-game"
RENPY="$PROJECT/.work/renpy-sdk/renpy-8.5.3-sdk/renpy.sh"

RENPY_PATH_TO_SAVES="<isolated-saves>" \
  "$RENPY" "<isolated-project>" lint \
  --error-code --check-unclosed-tags --all-problems

RENPY_PATH_TO_SAVES="<isolated-saves>" \
  "$RENPY" "<isolated-project>" test global --report-detailed
```

自动化还会在 suite 开始时备份 `persistent.old_ending_route` 与 `persistent.old_endings_seen`，teardown 时恢复并保存，避免测试结局写入用户记录。

## 最终结果

### Ren'Py lint

```text
Dialogue blocks: 686
Menus: 22（旧篇 10，续篇 12）
Image definitions: 50
Screens: 14
Errors: 0
Warnings: 0
```

### 自动化

```text
Test suites:  1/1 passed
Test cases:  14/14 passed
Test hooks:  15/15 passed
Assertions:  29/29 passed
Time:        11.783 s
Status:      PASSED
```

| 用例 | 覆盖内容 | 状态 |
| --- | --- | --- |
| `full_flow_stable_ideal` | 旧篇从主菜单到稳定理想结局；验证双篇状态隔离 | 通过 |
| `rising_ideal` / `startup_ideal` | 旧篇上升、创业理想表现 | 通过 |
| `stable_normal` / `rising_normal` / `startup_normal` | 旧篇三个普通表现 | 通过 |
| `save_load_smoke` | 标准保存、继续选择、读取及能力值恢复 | 通过 |
| `sequel_full_flow_true_ending` | 续篇 12 个自然选择、四碎片、全信任与真结局 | 通过 |
| `sequel_dana_ending` | Dana《春日归邻》 | 通过 |
| `sequel_luna_ending` | Luna《盛夏坐标》 | 通过 |
| `sequel_irene_ending` | Irene《秋实之书》 | 通过 |
| `sequel_ruby_ending` | Ruby《冬夜来信》 | 通过 |
| `sequel_return_ending` | 返回现实《回到灯火》 | 通过 |
| `sequel_origin_rising_smoke` | 旧篇 rising persistent 在续篇开场可读取，随后恢复 | 通过 |

## 素材与显示校验

- `game/images/` 共 51 张图片；所有文件可被 Ren'Py lint 和测试加载。
- 9 张续篇背景与 6 张续篇 CG 均为真正的 `1920×1080` PNG。
- 4 张续篇立绘运行时尺寸为 `682×1024`、RGBA，alpha 范围 `0..255`，四角 alpha 均为 `0`。
- 主菜单实际使用 `1920×1080` 的 `bg_main_menu_cover_wide.jpg`，左侧有菜单留白、右侧保留原漫画人物。
- 四位女主立绘与四人客厅合影逐一视觉比对：脸型、发色、服装和从左到右身份顺序一致。
- 六张新增 CG 完成视觉抽检：人物无重复、关键道具与季节场景正确、无烘焙文字或水印。

## 过程问题与处理

第一次真实素材回归中，续篇全流程加载六张高分辨率 CG，超过测试原设的 25 秒单例上限；此前已执行的 24 个断言全部通过，日志明确为 `RenpyTestTimeoutError`，不是剧情或分支错误。测试预算随后调整为 60 秒，保留全部点击与断言，重新从空缓存执行后 14 个用例在 11.783 秒内全部通过。

## 已知边界

- 当前为静音版本，未验证音乐、音效或配音混合。
- 自动化覆盖主线和所有结局，但不替代对每个非理想选项文案、连续回滚和快进节奏的发行前人工体验。
- 尚未生成 Windows、macOS、Linux 发布包。
- 正式发布前需复核 SDK 随附字体的再分发条款。
