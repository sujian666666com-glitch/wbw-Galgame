# v2.1 剧情接入报告

- 实际模型：Grok 4.7（契约角色为 Cursor / grok-4.7-high）
- 工作树：`.work/v21/worktrees/tech`，已在集成提交 `9bf0c72` 上改产品脚本
- 来源：`doc/collaboration/v2.1/story/inserts.rpy.txt`、`manifest.json`、`review.md`（二审定稿）
- 未做：提交、推送、改 `game/testcases.rpy`、改 `ik.md`、改 `tools/package_macos.py` 与 `tools/export_story.py`、创建占位图、跑图形测试

脚本结构已接入。九张新图仍缺，界面流程未跑，不能记为通过。

## 变更

新增 `game/story/v21_inserts.rpy`。23 个 label 的台词、条件和 `return` 按蓝本转录。蓝本 306 处引号原文全部按顺序保留；产品文件只多出镜面叠加用的「请不要独自记住」。没有 `menu`，没有 `$` 赋值，没有 `persistent` 写入。

在原 label 里各 `call` 一次，没有用 `jump`：

| call | 位置 |
| --- | --- |
| `v21_prologue` | 序章 menu 之后、`jump chapter_01` 之前 |
| `v21_chapter_01` | 第一章 menu 之后、`jump chapter_02` 之前 |
| `v21_chapter_02` | 第二章 menu 之后、`jump chapter_03` 之前 |
| `v21_chapter_03` | 第三章 menu 之后、`jump chapter_04` 之前 |
| `v21_chapter_04` | 证据整理与 `evidence_ready` 之后、`jump chapter_05` 之前 |
| `v21_chapter_05` | 天台对话之后、`jump chapter_06` 之前 |
| `v21_chapter_06` | 「那就看远一点。」之后、最终 menu 之前 |
| `v21_ending_stable` / `rising` / `startup` | 理想/普通分支之后、`persistent.old_ending_route` 之前 |
| `v21_sequel_prologue` | 序章最后一句内心独白之后、`jump sequel_chapter_01` 之前 |
| `v21_sequel_chapter_01` | Dana「跟好。春庭的路可不在你的离线地图里。」之后、jump 之前 |
| `v21_sequel_chapter_02_spring` | Luna「必须遵守我的安全方案。」之后、「夜色落下前…」之前 |
| `v21_sequel_chapter_03_summer` | 「两枚碎片仍在黑暗中发光…」之后、jump 之前 |
| `v21_sequel_chapter_04_autumn` | `autumn_fragment = True` 且已重新显示档案馆与 `irene normal` 之后、「最后一页只记了一个称谓」之前 |
| `v21_sequel_chapter_05_winter` | 「那就去把规则改掉。」之后、jump 之前 |
| `v21_sequel_finale` | 「裂纹间开始推演几条仍可执行的道路。」之后、最终 menu 之前 |
| 六个 `v21_sequel_ending_*` | 各结局最后一段叙述之后、对应「——…结局」marker 之前 |

秋章 `call` 返回后，重新 `scene bg archive_autumn` 并 `show irene normal`，再接「最后一页」警告。插入段会把画面留在傍晚调和 `irene relieved` 上，警告本身仍用章内原来的档案馆和普通立绘。

`sequel_chapter_01` 只改了两句与过夜矛盾的旁白。「第二天清晨」保留。钥匙、住处和备份段仍在。原文「昨晚那把钥匙确实打开了…」改成重新核对门锁；入住清单改为与录取材料、租约同一份笔迹。这是蓝本审查 §6.12 指出的重复，不是另写一场。

银铃与耳坠的区分、真结局门「下个四季交界，两边都可以再发出邀请」按定稿保留，没有退回初稿。

## 画面

时段场景改成同底图的已有调色，没有换另一张画：

| 片段 | 使用 |
| --- | --- |
| 雨伞开场 | `bg v21_time_company_street_rain`（`bg company_street_night`） |
| 稳定后日谈 | `bg v21_time_company_street_dusk` |
| 创业后日谈 | `bg v21_time_startup_morning` |
| 春庭约定、Dana 后日谈 | `bg v21_time_spring_garden_evening` |
| 秋日信 | `bg v21_time_archive_evening` |
| Irene 后日谈 | `bg v21_time_archive_night` |
| Luna 后日谈 | `bg v21_time_lighthouse_dawn` |
| Ruby 后日谈 | `bg v21_time_station_first_snow` |
| 真结局后日谈 | `bg v21_time_station_boundary`（`bg sakurakagami_station_rain`） |
| 上升后日谈、旧宅镜面 | 契约新文件 `bg v21_train_interior_dusk`、`bg v21_old_house_mirror` |

已从 `game/core/v21_images.rpy` 删除未使用的 `v21_time_old_house_night`、`v21_time_spring_garden_dusk`、`v21_time_lighthouse_deep_night`、`v21_time_city_street_morning`。返回后日谈定稿是雨夜，场景仍是 `bg city_anomaly`，没有改成清晨街道。夏章温差仍用章内已有的 `bg lighthouse_night`。

镜面文字：说出「请不要独自记住」时 `show screen v21_mirror_caption`，下一句「字很快消失」之前 `hide screen`。各一次，不跨到下一场景。

CG 只有两处 `scene`：`cg v21_xuwanqing_rain_close` 在 `affection >= 8` 的雨伞分支内；`cg v21_ruby_ending_kiss` 在 `v21_sequel_ending_ruby`。冬章脸颊吻仍是 `ruby resolute` 加文字，没有 CG。靠肩、牵手和额头吻只留在旁白里，没有用普通立绘冒充这些 CG。

## 发行说明

`THIRD_PARTY_NOTICES.txt` 与 `licenses/**` 已在 `game/options.rpy` 里显式标为 `all`，写在排除规则之后、归档规则之前。它们不匹配 `doc/**`、`image/**`、`ik.md`、`tools/**` 或其他排除项。打包脚本没有改。`config.save_directory` 仍是 `three-months-to-stay-1`。

## 实际验证

对照蓝本与产品文件：引号原文 306/306 对齐；23 个 label、23 个 `return`、23 个 `call`，每个 label 恰好被调用一次，调用都在 label 主体而不是菜单分支里。因此沿原有章节和结局路径都能走到对应 `call`。这是静态对账，没有在游戏里点过。

原脚本菜单仍是 22，选项行仍是 61。Ren'Py 8.5.3.26051504 lint 统计同样是 22 个菜单。图像 68：原有 50、契约九张、正在使用的 9 个时段变体。屏幕仍是 15。

lint 命令（隔离存档 `/tmp/v21-tech-lint-saves2`，未取图形锁）：

```text
renpy.sh <tech 工作树> lint --error-code --check-unclosed-tags --all-problems
```

退出码 1。唯一问题仍是九张尚未生成的文件 not loadable。没有语法错误，没有未闭合标签。没有跑 `test`，也没有打开窗口。

## 未解决

- 九张 png 不在本工作树。引用到它们的分支在资源放入 `game/images/v21/` 之前不能显示。
- 23 个 `call` 的实际播放、好感分支和结局 marker 顺序没有在界面里走通。
- 基线两则测试失败仍未重跑。
- 没有生成发布包，因此许可证文件只确认了分类规则，没有在成品包里打开过。
