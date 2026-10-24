# v2.1 技术初始报告

- 实际模型：Grok 4.7（契约角色为 Cursor / grok-4.7-high）
- 工作树：`/Users/ik/Desktop/02_学习与资料/game/my-renpy-game/.work/v21/worktrees/tech`
- 分支：`ik/v21-tech`
- 范围：产品状态、续篇入口、夏章观测事实、九张资源声明、时段调色、打包分类、文本/六选项/历史/存档的最小排版
- 未做：提交、推送、切分支、改 `game/testcases.rpy`、改 `ik.md`、跑图形测试、接入 23 段剧情

未完成，不能记为通过。

## 实际改动

| 文件 | 改动 |
| --- | --- |
| `game/options.rpy` | 版本 `2.1.0`；`has_sound` / `has_music` / `has_voice` 均为 False；`save_directory` 仍是 `three-months-to-stay-1`；重写 `build.classify` |
| `game/core/state.rpy` | 新增 `default sequel_luna_observation_outcome = "unknown"`。既有 default 与 persistent 未改 |
| `game/script.rpy` | 未改。`start`、`original_story_start`、`sequel_start` 仍在 |
| `game/story/sequel_prologue.rpy` | 事业回顾之后写明平行世界线只继承事业、不继承恋爱、不写此后关系 |
| `game/screens.rpy` | 主菜单新篇按钮上方加一句说明；六选项菜单改到对话框上方；历史折行并限制视口；六格存档收进格子；镜面文字用屏幕叠加 |
| `game/ui/status_screen.rpy` | 「旧篇回溯」改为「事业回顾」，避免状态面板暗示整段旧结局（含恋爱）被继承 |
| `game/story/sequel_chapter_03_summer.rpy` | 夏章第一个菜单三支分别写入 `paper_tape` / `aborted` / `evacuated`；共同叙述按结果区分纸带与残缺记录。奖励数字未改 |
| `game/core/v21_images.rpy` | 新建。九张契约资源加 13 个时段变体 |

主菜单按钮文字仍是「新篇：樱镜町」和「旧篇：三个月，留下来」。测试里的 `click "新篇：樱镜町"`、`click "执行 Luna 的分组方案"`、`click "公开可复核证据"` 所用子串都还在。

## 夏章观测

第一个菜单（潮水逼近观测台）：

- 「执行 Luna 的分组方案…」→ `paper_tape`，仍是 Luna 信任 +2、洞察 +1
- 「离开安全绳…」→ `aborted`，无数值奖励
- 「立即撤离…」→ `evacuated`，无数值奖励

共同叙述不再在三条路都说「只有纸带保留了原貌」。`unknown`（旧档缺这个变量时）用中性句，不假定取回了纸带。公开证据那一支的对白同样按结果说纸带、残缺备份或副本；该支奖励仍是 Luna 信任 +1、共同意志 +1。选项按钮原文未改。

## 入口说明

主菜单新篇按钮上方：「平行世界线：只继承事业回顾，不继承恋爱。」

序章在三条事业回顾之后、雨夜街景之前：

- 这是一条平行世界线，接过来的只有事业上走过的路。
- 和许晚晴的感情不在这条线里；不延续那段恋爱，也不另写他们此后如何相处。

没有写分手。

## 资源

九张声明指向契约路径（相对 `game/`），没有占位图。立绘 `xalign` / `yalign` 抄自对应 `normal`：

| image ID | 站位 |
| --- | --- |
| `dana worried` | 0.34, 1.0 |
| `luna soft` | 0.50, 1.0 |
| `irene shaken` / `irene relieved` | 0.66, 1.0 |
| `ruby resolute` | 0.84, 1.0 |

`bg v21_train_interior_dusk`、`bg v21_old_house_mirror`、`cg v21_xuwanqing_rain_close`、`cg v21_ruby_ending_kiss` 使用契约文件，不用调色冒充。

时段变体使用当前支持的 `matrixcolor`（`TintMatrix` 乘 `BrightnessMatrix`）。`im.MatrixColor` 自 7.4.0 起已弃用，所以没有用它。旧 png 没有改。这些 ID 还没有被任何 label `scene`，等 23 段蓝本接入时引用：

| image ID | 调色来源 | 对应原稿画面 |
| --- | --- | --- |
| `bg v21_time_old_house_night` | `bg old_house_day` | 旧宅（夜间） |
| `bg v21_time_spring_garden_dusk` | `bg spring_garden` | 春庭（黄昏） |
| `bg v21_time_spring_garden_evening` | `bg spring_garden` | 春庭（傍晚） |
| `bg v21_time_lighthouse_deep_night` | `bg lighthouse_night` | 海岸灯塔（深夜） |
| `bg v21_time_lighthouse_dawn` | `bg lighthouse_night` | 海岸灯塔（黎明） |
| `bg v21_time_archive_evening` | `bg archive_autumn` | 秋季档案馆（傍晚） |
| `bg v21_time_archive_night` | `bg archive_autumn` | 秋季档案馆（夜间） |
| `bg v21_time_company_street_dusk` | `bg company_street_night` | 公司楼下街道（黄昏） |
| `bg v21_time_company_street_rain` | `bg company_street_night` | 公司楼下街道（雨夜） |
| `bg v21_time_startup_morning` | `bg startup_studio` | 创业工作室（清晨） |
| `bg v21_time_station_first_snow` | `bg sakurakagami_station_winter` | 樱镜町车站（初雪） |
| `bg v21_time_city_street_morning` | `bg company_street_night` | 原世界城市街道（清晨） |
| `bg v21_time_station_boundary` | `bg sakurakagami_station_rain` | 旧车站（四季交界） |

镜中文字不烘焙。需要时：

```
show screen v21_mirror_caption("请不要独自记住")
hide screen v21_mirror_caption
```

剧情还没调用这个屏幕。

## 打包分类

`build.classify` 第一次命中生效，排除写在归档之前。规则只作用于项目目录。没有调用 `build.classify_renpy`。引擎仍由 SDK 另一次 `renpy_patterns` 扫描打包。项目里若出现 `renpy/` 或 `lib/`，SDK 原有的 `early_base_patterns` 会先把它们排除，不会靠本次规则把引擎文件判掉。

按 SDK `launcher/game/distribute.rpy` 的 `match` 用同一套 glob 对样例路径做了本地核对（不是一次真正的发行构建）：

- 排除：`doc/**`、顶层 `image/**`（不含 `game/images/**`）、`ik.md`、`tools/**`、`game/testcases.rpy` / `.rpyc` / `.rpymc`、`game/cache/**`、`game/saves/**`、`*.log`、`log.txt`、`errors.txt`、`traceback.txt`、`.work/**`、`renpy-*-sdk/**`
- 归档：`game/fonts/**`（含 `SourceHanSansLite.ttf`）、`game/**.png`、`game/**.jpg`、`game/**.rpy`、`game/**.rpyc`
- `README.md` 仍落到末尾 `**` → `all`。契约点名的是开发文档，没有要求排除 README

## 排版

对照 1920×1080 和现有字号，只动了会溢出的地方。主菜单底图、左侧栏配色和标题没有重做。

- 对白：现有最长一句 67 字。对话框正文宽 1520、字号 34，约两行，落在高度 270 的窗口内。对话框几何没有改。
- 六选项：终章条件全开时是六个选项。原先 `yalign 0.55` 会让最后一项压进底部对话框。现在选项块底边在 y=800，对话框从 y=810 开始。
- 历史：长句原先没有宽度，会横着伸出记录框。现在视口 1060×720，正文宽 1020，可滚动，空列表有一句提示。
- 存档：六格从 330×280 改为 340×250，截图和文件名限制在内边距里，页名输入宽 460。三列总宽 1060，框内可用约 1070。

## 检查

隔离存档目录 `/tmp/v21-tech-lint-saves`，未使用图形锁，未跑 `test`：

```text
renpy.sh <tech 工作树> lint --error-code --check-unclosed-tags --all-problems
```

Ren'Py 8.5.3.26051504。退出码 1。唯一问题是九张尚未生成的文件 not loadable（立绘各报两次，背景和 CG 各一次）。除此之外脚本能加载。统计：对白块 694（基线报告为 686，增加来自序章两句和夏章分支叙述）、菜单仍为 22、图像 72（原 50 + 九张声明 + 13 个时段变体）、屏幕 15（新增镜面字幕）。时段变体没有报错，说明 `matrixcolor` 表达式已被接受。

没有打开游戏窗口，所以菜单、历史和存档的实际像素没有在界面里点过。

## 基线两则失败（只分析，未改产品，未重跑）

`doc/test-report.md`（2026-07-13）写这两则当时通过。契约把它们记为当前基线失败。本次没有重跑，不能判断哪份记录代表现在的界面结果。

`save_load_smoke` 第 119 行 `assert eval (ability == 4)`：

- 第 110 行要求序章「把三个月的目标拆成行动清单」之后 `ability == 3`。默认能力 2，该支 `ability += 1`，与断言一致。
- 第 119 行点击的是第一章「没事，我正好趁这个机会看看公司的数据。」这一支同时有 `affection += 3` 和 `ability += 1`。若这一支真的执行，能力从 3 变为 4，产品代码和断言一致。
- 所以这次失败不能解释成「选项里少写了能力」。更值得查的是 `FileSave` 之后那次点击有没有真正选中这一支。本次没有改 `chapter_01.rpy`，也没有改奖励。

`sequel_full_flow_true_ending` 第 133 行是 `click "新篇：樱镜町"` 之后的 `advance until screen "choice"`。这发生在任何续篇选项之前。超时且仍停在主菜单，表示点击没有离开主菜单，或游戏在出现选项前回到了主菜单。契约写它紧跟前一则失败。按钮文字这次没改；新增的说明文字不是按钮，也不包含「新篇：樱镜町」这个子串（`find_focus` 按最短包含匹配）。不应靠加长超时或放宽断言处理。

## 疑点

- 终章六个选项里，靠后的几条以前可能被对话框挡住。测试若只点第一条「让整个樱镜町共同记住」，不一定暴露这个问题。本次把整组抬到对话框上方，但是没有重跑。
- 「立刻上传全部原始资料」仍是原来的选项按钮。中止或撤离之后，按钮文字仍说「原始资料」。按保留既有选项，没有改按钮，只改了选中之后的叙述。
- 黎明是把夜间灯塔提亮，初雪和四季交界也只是单层调色。四季交界不会变成四色同框。若蓝本要求可辨认的新构图，应走九张以外的美术，而不是再改旧文件。
- `bg v21_time_city_street_morning` 调的是夜间公司街道，不一定是原稿「原世界城市街道」。接入时要对一下地点。
- lint 对五张立绘各报两次 not loadable，四张单行图像各一次。像是复合 image 被检查了两次，不代表声明写了两遍。
- 分类核对是本地复刻 `match`，不是 `distribute` 打出来的包。空目录是否被 `exclude_empty_directories` 去掉，要以真正构建为准。

## 未解决

- 23 段 `v21_` label 尚未接入。蓝本到达后再插，不在本次改结局 marker 的相对位置。
- 九张 png 不存在。按约定不放占位图。在美术放入 `game/images/v21/` 之前，lint 会一直报 not loadable，引用到这些图像的剧情也不能显示。
- 上述时段变体和镜面屏幕还没有被剧情调用。
- 两则基线测试未重跑，图形界面未验收。
- 没有生成发布包。
