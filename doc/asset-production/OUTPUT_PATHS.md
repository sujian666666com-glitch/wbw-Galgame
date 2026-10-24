# 生成图片交付路径

项目根目录：

`/Users/ik/Desktop/02_学习与资料/game/my-renpy-game`

本文件规定生成完成后图片应放置的位置。所有路径均以项目根目录为基准，同时给出源图与运行时文件两层。

## 唯一合法根目录

| 用途 | 唯一合法绝对路径 |
| --- | --- |
| 制作基准 | `/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/image/续篇/制作基准/` |
| 所有生成源图 | `/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/image/续篇/生成源图/` |
| 所有游戏运行时图 | `/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/game/images/sequel/` |

文档中的“角色立绘”“证据与物品”等标题只是规格分类，不是文件目录。禁止自行简写为以下不存在的路径：

- 禁止：`image/续篇/角色立绘/`
- 禁止：`image/续篇/证据物品/`
- 禁止：`image/续篇/剧情CG/`

必须使用下文明确列出的 `image/续篇/生成源图/<category>/` 路径。

两个完整示例：

- Dana 担忧色键源图：`/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/image/续篇/生成源图/characters/dana_worried_chroma.png`
- Dana 担忧运行时图：`/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/game/images/sequel/characters/dana_worried.png`
- 春之碎片源图：`/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/image/续篇/生成源图/items/item_fragment_spring_source.png`
- 春之碎片运行时图：`/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/game/images/sequel/items/item_fragment_spring.png`

## 总规则

1. 生成器直接输出、同源编辑母版、色键图和高分辨率图放入 `image/续篇/`。
2. 去背、裁切、缩放、透明度与尺寸验收完成后，复制规范化版本到 `game/images/sequel/`。
3. 不允许直接覆盖源图；运行时图可以由源图重新导出。
4. 城市拓扑和角色设定表仅供制作参考，不进入游戏包。
5. 文件名必须与素材 ID 或组内子文件名一致；源图统一追加 `_source`，色键人物源图统一追加 `_chroma`。
6. 下文中尚不存在的目录，在第一张对应素材验收时创建，不需要提前放空目录。

## 制作基准：只进入 `image/`

| 素材 | 最终保存位置 | 是否进入 `game/` |
| --- | --- | --- |
| `ref_city_topology_v1` | `image/续篇/制作基准/city/ref_city_topology_v1.png` | 否 |
| `ref_dana_model_sheet` | `image/续篇/制作基准/characters/ref_dana_model_sheet.png` | 否 |
| `ref_luna_model_sheet` | `image/续篇/制作基准/characters/ref_luna_model_sheet.png` | 否 |
| `ref_irene_model_sheet` | `image/续篇/制作基准/characters/ref_irene_model_sheet.png` | 否 |
| `ref_ruby_model_sheet` | `image/续篇/制作基准/characters/ref_ruby_model_sheet.png` | 否 |

## 城市地图

源图目录：

`image/续篇/生成源图/map/`

运行时目录：

`game/images/sequel/ui/map/`

| 素材 | 源图文件 | 运行时文件 |
| --- | --- | --- |
| `map_sakurakagami_base` | `map_sakurakagami_base_source.png` | `map_sakurakagami_base.png` |
| `map_mirror_chamber_reveal` | `map_mirror_chamber_reveal_source.png` | `map_mirror_chamber_reveal.png` |

地图底图和镜室覆盖层均为 `1920×1080`。覆盖层必须保持 RGBA 透明，不得与底图合并保存。

## 地图与界面图标

### `ui_location_icon_set`：地点节点

源图目录：`image/续篇/生成源图/ui/location-icons/`

运行时目录：`game/images/sequel/ui/location-icons/`

| 文件名 | 内容 |
| --- | --- |
| `ui_location_old_house.png` | 旧宅区 |
| `ui_location_academy.png` | 樱镜学园 |
| `ui_location_spring_garden.png` | 春庭 |
| `ui_location_archive.png` | 档案馆 |
| `ui_location_coast_lighthouse.png` | 海岸与灯塔 |
| `ui_location_station.png` | 樱镜町车站 |
| `ui_location_mirror_chamber.png` | 四季镜室 |

源图使用相同文件名并在扩展名前追加 `_source`，例如 `ui_location_old_house_source.png`。

### `ui_time_icon_set`：五时段图标

源图目录：`image/续篇/生成源图/ui/time/`

运行时目录：`game/images/sequel/ui/time/`

- `ui_time_dawn.png`
- `ui_time_day.png`
- `ui_time_dusk.png`
- `ui_time_night.png`
- `ui_time_late_night.png`

### `ui_event_marker_set`：四季事件标记

源图目录：`image/续篇/生成源图/ui/events/`

运行时目录：`game/images/sequel/ui/events/`

- `ui_event_spring.png`
- `ui_event_summer.png`
- `ui_event_autumn.png`
- `ui_event_winter.png`

### `ui_state_icon_set`：通用状态图标

源图目录：`image/续篇/生成源图/ui/state/`

运行时目录：`game/images/sequel/ui/state/`

- `ui_state_locked.png`
- `ui_action_rest.png`
- `ui_state_current_location.png`

### `ui_map_portrait_set`：四位女孩地图头像

裁切工作图目录：`image/续篇/生成源图/ui/portraits/`

运行时目录：`game/images/sequel/ui/portraits/`

- `ui_portrait_dana.png`
- `ui_portrait_luna.png`
- `ui_portrait_irene.png`
- `ui_portrait_ruby.png`

裁切工作图使用相同文件名并追加 `_source`，例如 `ui_portrait_dana_source.png`。

所有图标与头像的运行时版本均为 `256×256` RGBA PNG。源图可保留更高分辨率。

## 日常场景背景

源图目录：

`image/续篇/生成源图/backgrounds/`

运行时目录：

`game/images/sequel/backgrounds/`

| 素材 ID | 源图文件 | 运行时文件 |
| --- | --- | --- |
| `bg_old_house_district_day` | `bg_old_house_district_day_source.png` | `bg_old_house_district_day.png` |
| `bg_old_house_district_night` | `bg_old_house_district_night_source.png` | `bg_old_house_district_night.png` |
| `bg_old_house_room_night` | `bg_old_house_room_night_source.png` | `bg_old_house_room_night.png` |
| `bg_academy_courtyard_night` | `bg_academy_courtyard_night_source.png` | `bg_academy_courtyard_night.png` |
| `bg_student_council_day` | `bg_student_council_day_source.png` | `bg_student_council_day.png` |
| `bg_student_council_night` | `bg_student_council_night_source.png` | `bg_student_council_night.png` |
| `bg_spring_garden_night` | `bg_spring_garden_night_source.png` | `bg_spring_garden_night.png` |
| `bg_archive_workday` | `bg_archive_workday_source.png` | `bg_archive_workday.png` |
| `bg_coast_lighthouse_calm_day` | `bg_coast_lighthouse_calm_day_source.png` | `bg_coast_lighthouse_calm_day.png` |
| `bg_coast_lighthouse_calm_night` | `bg_coast_lighthouse_calm_night_source.png` | `bg_coast_lighthouse_calm_night.png` |
| `bg_station_clear_day` | `bg_station_clear_day_source.png` | `bg_station_clear_day.png` |
| `bg_station_clear_night` | `bg_station_clear_night_source.png` | `bg_station_clear_night.png` |

运行时背景统一导出为 `1920×1080` PNG，不得把角色、事件标记或对话框烘焙进去。

## 角色立绘

色键源图目录：

`image/续篇/生成源图/characters/`

运行时目录：

`game/images/sequel/characters/`

| 素材 ID | 色键源图 | RGBA 运行时文件 |
| --- | --- | --- |
| `dana_worried` | `dana_worried_chroma.png` | `dana_worried.png` |
| `dana_determined` | `dana_determined_chroma.png` | `dana_determined.png` |
| `dana_gardening` | `dana_gardening_chroma.png` | `dana_gardening.png` |
| `luna_soft` | `luna_soft_chroma.png` | `luna_soft.png` |
| `luna_alarmed` | `luna_alarmed_chroma.png` | `luna_alarmed.png` |
| `luna_field_coat` | `luna_field_coat_chroma.png` | `luna_field_coat.png` |
| `irene_shaken` | `irene_shaken_chroma.png` | `irene_shaken.png` |
| `irene_relieved` | `irene_relieved_chroma.png` | `irene_relieved.png` |
| `irene_archive_work` | `irene_archive_work_chroma.png` | `irene_archive_work.png` |
| `ruby_distressed` | `ruby_distressed_chroma.png` | `ruby_distressed.png` |
| `ruby_resolute` | `ruby_resolute_chroma.png` | `ruby_resolute.png` |
| `ruby_winter_coat` | `ruby_winter_coat_chroma.png` | `ruby_winter_coat.png` |
| `wangbuwen_surprised` | `wangbuwen_surprised_chroma.png` | `wangbuwen_surprised.png` |
| `wangbuwen_investigating` | `wangbuwen_investigating_chroma.png` | `wangbuwen_investigating.png` |

运行时立绘必须完成去背，四角透明，显示高度不超过 `1024 px`。色键源图不得直接放入 `game/`。

## 剧情 CG

源图目录：

`image/续篇/生成源图/cg/`

运行时目录：

`game/images/sequel/cg/`

| 素材 ID | 源图文件 | 运行时文件 |
| --- | --- | --- |
| `cg_sequel_four_meeting` | `cg_sequel_four_meeting_source.png` | `cg_sequel_four_meeting.png` |
| `cg_ending_dana` | `cg_ending_dana_source.png` | `cg_ending_dana.png` |
| `cg_ending_luna` | `cg_ending_luna_source.png` | `cg_ending_luna.png` |
| `cg_ending_irene` | `cg_ending_irene_source.png` | `cg_ending_irene.png` |
| `cg_ending_ruby` | `cg_ending_ruby_source.png` | `cg_ending_ruby.png` |
| `cg_ending_return` | `cg_ending_return_source.png` | `cg_ending_return.png` |
| `cg_event_dana_optional` | `cg_event_dana_optional_source.png` | `cg_event_dana_optional.png` |
| `cg_event_luna_optional` | `cg_event_luna_optional_source.png` | `cg_event_luna_optional.png` |
| `cg_event_irene_optional` | `cg_event_irene_optional_source.png` | `cg_event_irene_optional.png` |
| `cg_event_ruby_optional` | `cg_event_ruby_optional_source.png` | `cg_event_ruby_optional.png` |

所有运行时 CG 统一为 `1920×1080` PNG。`EVENT_GRAPH_DEPENDENT` 的四张自由事件 CG 在事件图确认前不得创建正式文件。

## 证据与物品

源图目录：

`image/续篇/生成源图/items/`

运行时目录：

`game/images/sequel/items/`

| 素材或子文件 | 源图文件 | 运行时文件 |
| --- | --- | --- |
| `item_generated_identity_dossier` | `item_generated_identity_dossier_source.png` | `item_generated_identity_dossier.png` |
| `item_four_fragments_set`：春之碎片 | `item_fragment_spring_source.png` | `item_fragment_spring.png` |
| `item_four_fragments_set`：夏之碎片 | `item_fragment_summer_source.png` | `item_fragment_summer.png` |
| `item_four_fragments_set`：秋之碎片 | `item_fragment_autumn_source.png` | `item_fragment_autumn.png` |
| `item_four_fragments_set`：冬之碎片 | `item_fragment_winter_source.png` | `item_fragment_winter.png` |
| `item_shared_protocol_network` | `item_shared_protocol_network_source.png` | `item_shared_protocol_network.png` |
| `item_spring_glove_name_card` | `item_spring_glove_name_card_source.png` | `item_spring_glove_name_card.png` |
| `item_tide_paper_tape_recorder` | `item_tide_paper_tape_recorder_source.png` | `item_tide_paper_tape_recorder.png` |
| `item_torn_founder_record` | `item_torn_founder_record_source.png` | `item_torn_founder_record.png` |
| `item_ruby_earring_name` | `item_ruby_earring_name_source.png` | `item_ruby_earring_name.png` |

物品运行时图使用 RGBA PNG；若状态页以卡片形式展示，可保留透明画布并由界面负责底板和文字。

## `npc_resident_sprite_set`：NPC 立绘

色键源图目录：

`image/续篇/生成源图/npc/`

运行时目录：

`game/images/sequel/npc/`

| 子文件 | 色键源图 | RGBA 运行时文件 |
| --- | --- | --- |
| 旧街店主 | `npc_old_street_shopkeeper_chroma.png` | `npc_old_street_shopkeeper.png` |
| 春庭志愿者 | `npc_spring_garden_volunteer_chroma.png` | `npc_spring_garden_volunteer.png` |
| 成年大学部学生 | `npc_academy_student_chroma.png` | `npc_academy_student.png` |
| 车站工作人员 | `npc_station_staff_chroma.png` | `npc_station_staff.png` |
| 档案馆访客 | `npc_archive_visitor_chroma.png` | `npc_archive_visitor.png` |

这些文件属于 `EVENT_GRAPH_DEPENDENT`，事件图确认前只保留路径规划，不创建正式角色。

## `crowd_location_overlay_set`：人群覆盖层

源图目录：

`image/续篇/生成源图/crowds/`

运行时目录：

`game/images/sequel/crowds/`

| 子文件 | 源图文件 | 运行时文件 |
| --- | --- | --- |
| 学园日常人群 | `crowd_academy_day_source.png` | `crowd_academy_day.png` |
| 春庭居民活动 | `crowd_spring_garden_event_source.png` | `crowd_spring_garden_event.png` |
| 车站普通乘客 | `crowd_station_day_source.png` | `crowd_station_day.png` |

运行时覆盖层必须是与目标背景机位对齐的 `1920×1080` RGBA PNG，不允许带不透明背景。

## 透明特效

`vfx_seasonal_particle_set` 对应下表中的春季花瓣、夏季水光、秋季红叶、冬季雪花和冬季霜纹五个子文件。

源图目录：

`image/续篇/生成源图/vfx/`

运行时目录：

`game/images/sequel/vfx/`

| 素材或子文件 | 源图文件 | 运行时文件 |
| --- | --- | --- |
| 春季花瓣 | `vfx_spring_petals_source.png` | `vfx_spring_petals.png` |
| 夏季水光 | `vfx_summer_water_light_source.png` | `vfx_summer_water_light.png` |
| 秋季红叶 | `vfx_autumn_leaves_source.png` | `vfx_autumn_leaves.png` |
| 冬季雪花 | `vfx_winter_snow_source.png` | `vfx_winter_snow.png` |
| 冬季霜纹 | `vfx_winter_frost_source.png` | `vfx_winter_frost.png` |
| `vfx_silver_anomaly_overlay` | `vfx_silver_anomaly_overlay_source.png` | `vfx_silver_anomaly_overlay.png` |
| `vfx_mirror_shard_overlay` | `vfx_mirror_shard_overlay_source.png` | `vfx_mirror_shard_overlay.png` |
| `vfx_ruby_dissolve_mask`：Ruby 全身消散遮罩 | `vfx_ruby_dissolve_mask_source.png` | `vfx_ruby_dissolve_mask.png` |
| Ruby 地图头像消散遮罩 | `vfx_ruby_portrait_dissolve_mask_source.png` | `vfx_ruby_portrait_dissolve_mask.png` |

特效运行时文件必须保留透明通道。消散遮罩为灰度 PNG，不进行色键去背。

## 从生成到入库的顺序

1. 将生成器原始输出保存到对应的 `image/续篇/生成源图/` 子目录。
2. 同源编辑继续基于该源图产生新母版，禁止覆盖上一版本。
3. 按素材类型完成裁切、去背、透明通道、尺寸与构图安全区检查。
4. 将通过验收的规范化版本复制到对应的 `game/images/sequel/` 子目录。
5. 最后再在 Ren'Py 图片定义和界面代码中登记运行时路径；没有进入 `game/` 的制作基准不得被代码引用。

## 快速判断

- 还可能继续编辑、需要保留最高质量版本：放 `image/续篇/`。
- 已完成验收、游戏实际要加载：放 `game/images/sequel/`。
- 只是角色或城市一致性参考：只放 `image/续篇/制作基准/`。
- 色键背景还没去除：绝不能放 `game/`。
