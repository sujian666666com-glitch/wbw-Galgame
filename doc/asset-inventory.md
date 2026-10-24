# 素材清单与生成记录

> 更新日期：2026-10-25；下方 v2 原素材记录保留，v2.1 增量见本节。`image/` 保存原始素材与生成源图，`game/images/` 保存游戏实际加载的规范化版本。

## 正式运行时素材

`game/images/` 当前共 60 张图片。v2.1 新增 9 张：5 个透明表情、2 张背景、2 张事件 CG；原 51 张全部复用且未覆盖。新增资源、参考来源、模型、尺寸、原图校验值与驳回候选见 [v2.1 美术 manifest](collaboration/v2.1/art/manifest.json) 和 [一致性审查](collaboration/v2.1/art/review.md)。下表为保留的 v2.0 基线。

| 分类 | 旧篇 / 公共 | 续篇新增 | 合计 | 验收规格 |
| --- | ---: | ---: | ---: | --- |
| 背景与界面背景 | 18 | 9 | 27 | `1920×1080`，PNG 或 JPEG |
| 角色立绘 | 12 | 4 | 16 | RGBA PNG，四角透明，显示高度不超过 1024 px |
| 剧情 CG | 2 | 6 | 8 | `1920×1080` PNG |
| 合计 | 32 | 19 | 51 | 已接入 Ren'Py image 定义或 GUI |

公共素材中保留用户提供的原始漫画主菜单 `bg_main_menu_cover.jpg`，实际界面使用同图扩展的 `bg_main_menu_cover_wide.jpg`；四人客厅合影同时作为旧篇活动视觉与续篇四位女主身份锚点。

## 续篇背景

| 运行时文件 | 场景 | 生成与处理 |
| --- | --- | --- |
| `bg_city_anomaly.png` | 王不稳穿越前的城市异象 | 新生成；银色四季涡流与雨夜城市 |
| `bg_sakurakagami_station_rain.png` | 初到樱镜町车站 | 新生成；旧木车站、海、雨与透明伞 |
| `bg_old_house_day.png` | 旧宅与四人会面 | 新生成；海边旧宅室内 |
| `bg_academy_courtyard.png` | 成人大学部校园 | 新生成；海景、木构校园与庭院 |
| `bg_spring_garden.png` | Dana 的春季花园 | 新生成；花圃、水渠与园艺工具 |
| `bg_lighthouse_night.png` | Luna 的逆潮灯塔 | 新生成；灯塔、月夜逆潮与海上灯火 |
| `bg_archive_autumn.png` | Irene 的秋季档案馆 | 新生成；旧档案室、修补记录与红叶 |
| `bg_sakurakagami_station_winter.png` | Ruby 的冬季车站 | 以雨季车站定向编辑；保留透明伞与暖灯 |
| `bg_mirror_chamber.png` | 四季镜终局 | 新生成；破镜、轨道、四季并存与记忆丝线 |

运行时文件统一缩放为 `1920×1080`；未覆盖生成源图。场景生成源图位于 `image/续篇/生成源图/backgrounds/`。

## 续篇角色与 CG

四位女主的统一身份锚点是 `game/images/cg/cg_four_friends_living_room.png`：画面从左到右为 Dana、Ruby、Irene、Luna。生成立绘和 CG 时固定发色、服装色系、年龄感与人物位置关系，不按单张提示重新设计人物。

| 角色 | 运行时立绘 | 身份不变量 |
| --- | --- | --- |
| Ruby | `ruby_normal.png` | 四人图第二位；红色系、安静克制、冬季记忆线 |
| Dana | `dana_normal.png` | 四人图最左；绿色系、温暖主动、春季花园线 |
| Irene | `irene_normal.png` | 四人图第三位；蓝 / 深色系、成熟理性、秋季档案线 |
| Luna | `luna_normal.png` | 四人图最右；浅色系、敏锐自由、夏季灯塔线 |

立绘先生成纯色 chroma 背景版本，源图保存在 `image/续篇/生成源图/characters/`，再使用 Image Gen skill 随附的 `remove_chroma_key.py` 去背并规范化为 RGBA PNG。

新增 CG：

- `cg_sequel_dana_spring.png`：Dana 与王不稳修复春季花园。
- `cg_sequel_luna_tide.png`：Luna 在逆潮灯塔确认夏季碎片。
- `cg_sequel_irene_archive.png`：Irene 在秋季档案馆修补被撕毁的记录。
- `cg_sequel_ruby_name.png`：Ruby 在冬季车站重新写下自己的名字。
- `cg_sequel_mirror_finale.png`：五人在四季镜前拒绝旧有牺牲规则。
- `cg_sequel_true_ending.png`：四季同在后的海边团体后日谈。

CG 生成源图位于 `image/续篇/生成源图/cg/`，运行时版本位于 `game/images/sequel/cg/`。

## Image Gen 模式与提示词集合

本轮仓库可用能力中没有名为 `imagine` 的 skill，因此使用官方内置 `imagegen` skill 和 `image_gen` 模式完成位图生成与参考图编辑。提示词采用以下可复现骨架，并为每张图补充场景事实：

1. **背景骨架**：`finished 16:9 anime visual-novel background, cinematic lighting, coherent architecture, no characters, no legible text, no watermark, leave foreground room for sprites and dialogue UI`。
2. **角色骨架**：`full-body anime visual-novel character, preserve identity from the four-women reference, fixed hair/clothes/age cues, neutral readable pose, flat chroma-key background, no text, no props touching frame`。
3. **CG 骨架**：`cinematic 16:9 visual-novel CG, preserve all supplied character identities, one clear emotional beat, season-specific light and props, no text, no watermark, safe lower area for dialogue UI`。
4. **同源编辑骨架**：`preserve exact identity, architecture, camera and line work; change only the requested season, weather or canvas extension`。冬季车站以雨季车站为参考，主菜单以用户提供的黑白漫画为参考。

这些约束用于避免同一人物跨图漂移、同一地点换季后变成另一栋建筑，以及主菜单扩图时重新设计人物。

## 旧篇与公共素材来源

- 王不稳：用户提供真人参考图锁定脸型、眼镜、发型与壮实但不胖的身形；运行时使用普通、自信两张透明立绘。
- 许晚晴：普通、开心、严肃、忧虑、生气、惊讶 6 个透明表情。
- 王磊：普通、严肃 2 个透明表情；张浩：普通、得意 2 个透明表情。
- 地铁初遇 CG：原始素材转码并缩放为 `cg_subway_meeting.png`。
- 四人客厅合影：完整人物居中，两侧同图虚化扩展为 `1920×1080`。
- 旧篇缺失背景通过 Image Gen 补齐；原始图片和处理前备份继续保存在 `image/`，不覆盖、不删除。

## 字体与发布边界

- `game/fonts/SourceHanSansLite.ttf` 来自 Ren'Py 8.5.3 SDK 随附字体，用于跨平台简体中文渲染。
- 当前未引入音乐、音效、配音或外部音频素材。
- 字体内嵌版权及 SDK 来源校验已复核，SIL OFL 1.1 与声明随包分发。运行时验收见 [测试报告](test-report.md)。
