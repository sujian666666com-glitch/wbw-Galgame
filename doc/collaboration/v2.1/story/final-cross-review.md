# v2.1 最终交叉审查（剧情）

- 实际模型：deepseek-flash[1m]（本会话）
- 日期：2026-10-25
- 范围：只读主集成树 `game/story/` 产品脚本；为核对接口另只读 `game/core/state.rpy`、`game/core/v21_images.rpy`、`game/screens.rpy`
- 方法：逐文件阅读并 grep 计数，对照 `source-v2.1.txt`、`story/inserts.rpy.txt`、`story/review.md`、`story/manifest.json`
- 限制：未运行 Ren'Py、未跑 lint、未打开窗口、未做人工游玩；以下均为静态审查结论，不改产品

## 结论摘要

未发现阻断性剧情或缺段问题。23 个原稿新增片段均有产品 label，23 个 label 均有且仅有一次 `call`，条件阈值、普通/理想、低信任克制版、夏章四事件、平行世界、耳坠/银铃、真结局门规则与契约一致。剩余问题是静态审查限制和少量非阻断文档/演出接缝，列在末节。

## 1. 23 段与接入点

`game/story/v21_inserts.rpy` 有 23 个 `label v21_`、23 个 `return`（`:30/:51/:89/:126/:167/:205/:244/:278/:309/:341/:371/:395/:435/:475/:526/:567/:615/:662/:681/:702/:723/:745/:764`）。全产品 `call v21_` 共 23 次，分布于 16 个文件，无重复调用。

| # | 原稿片段 | 产品 label（定义行） | 唯一 call |
| --- | --- | --- | --- |
| 01 | 雨夜，第一笔账 | `v21_prologue`（`v21_inserts.rpy:30`） | `prologue.rpy:40`，menu 后、`jump chapter_01` 前 |
| 02 | 第一周的午餐 | `v21_chapter_01`（`:51`） | `chapter_01.rpy:69`，menu 后、jump 前 |
| 03 | 天台上的第二个秘密 | `v21_chapter_02`（`:89`） | `chapter_02.rpy:101`，menu 后、jump 前 |
| 04 | 伞下的距离 | `v21_chapter_03`（`:126`） | `chapter_03.rpy:153`，menu 后、jump 前 |
| 05 | 失去的署名 | `v21_chapter_04`（`:167`） | `chapter_04.rpy:53`，menu 后、`scene bg bedroom_night`（`:55`）前 |
| 06 | 胜利不是终点 | `v21_chapter_05`（`:205`） | `chapter_05.rpy:99`，天台对话后、jump 前 |
| 07 | 三封未发出的消息 | `v21_chapter_06`（`:244`） | `chapter_06.rpy:28`，“那就看远一点。”后、最终 menu（`:30`）前 |
| 08 | 后日谈·稳定线 | `v21_ending_stable`（`:278`） | `endings.rpy:35`，条件分支后、persistent（`:37`）前 |
| 09 | 后日谈·上升线 | `v21_ending_rising`（`:309`） | `endings.rpy:89`，条件分支后、persistent（`:91`）前 |
| 10 | 后日谈·创业线 | `v21_ending_startup`（`:341`） | `endings.rpy:148`，条件分支后、persistent（`:150`）前 |
| 11 | 失效的钟 | `v21_sequel_prologue`（`:371`） | `sequel_prologue.rpy:99`，末句独白后、jump 前 |
| 12 | 四个人的不同距离 | `v21_sequel_chapter_01`（`:395`） | `sequel_chapter_01.rpy:133`，Dana“跟好……”后、jump 前 |
| 13 | 春庭的约定 | `v21_sequel_chapter_02_spring`（`:435`） | `sequel_chapter_02_spring.rpy:121`，Luna 安全方案后、出发句（`:122`）前 |
| 14 | 灯塔里的温差 | `v21_sequel_chapter_03_summer`（`:475`） | `sequel_chapter_03_summer.rpy:144`，“两枚碎片……”后、jump 前 |
| 15 | 秋日未寄出的信 | `v21_sequel_chapter_04_autumn`（`:526`） | `sequel_chapter_04_autumn.rpy:76`，取得秋碎片并复位场景后、“最后一页……”（`:79`）前 |
| 16 | Ruby 的真心 | `v21_sequel_chapter_05_winter`（`:567`） | `sequel_chapter_05_winter.rpy:82`，“那就去把规则改掉。”后、jump 前 |
| 17 | 最后的独处 | `v21_sequel_finale`（`:615`） | `sequel_finale.rpy:36`，“裂纹间……”后、最终 menu（`:38`）前 |
| 18 | 后日谈·Dana 线 | `v21_sequel_ending_dana`（`:662`） | `sequel_endings.rpy:15`，结局 marker（`:16`）前 |
| 19 | 后日谈·Luna 线 | `v21_sequel_ending_luna`（`:681`） | `sequel_endings.rpy:34`，marker（`:35`）前 |
| 20 | 后日谈·Irene 线 | `v21_sequel_ending_irene`（`:702`） | `sequel_endings.rpy:54`，marker（`:55`）前 |
| 21 | 后日谈·Ruby 线 | `v21_sequel_ending_ruby`（`:723`） | `sequel_endings.rpy:73`，marker（`:74`）前 |
| 22 | 后日谈·返回现实线 | `v21_sequel_ending_return`（`:745`） | `sequel_endings.rpy:97`，marker（`:98`）前 |
| 23 | 后日谈·真结局 | `v21_sequel_ending_true`（`:764`） | `sequel_endings.rpy:120`，marker（`:121`）前 |

结局 marker 均晚于新增后日谈；旧篇 persistent 写入均晚于新增后日谈，符合契约。

## 2. 原稿覆盖

`source-v2.1.txt` 中 23 个新增标题全部有对应产品内容；grep 的 24 处匹配中有 1 处是第 5 行阅读说明，实际标题 23 个。逐段核对未见缺失或合并。以下是与原稿的有意差异，均可在 `review.md`/`runtime-review.md` 中找到批准依据：

- 午餐便签由“你昨晚加班，别把自己熬坏”改为“别把自己熬坏，记得好好吃饭”（`v21_inserts.rpy:69`；原稿 `source-v2.1.txt:188`），避免第一天就预设加班。
- 第四章插入段改为“当天晚上”并在回家备份前播放（`v21_inserts.rpy:172`；call 在 `chapter_04.rpy:53`，备份场景在 `:55`），对应 `manifest.json` 第 05 条与 `runtime-review.md:25`。
- 第六章低值版改为“没有重新输入那句已经删掉的问题”（`v21_inserts.rpy:266`），消除草稿箱矛盾，对应 `runtime-review.md:27`。
- 春庭段按产品时序前移到出发句前（call `sequel_chapter_02_spring.rpy:121`，出发句 `:122`；原稿在 `source-v2.1.txt:1549` 之后），对应 `review.md:92`。
- 秋日段前移到“冬之承载者”警告前（call `sequel_chapter_04_autumn.rpy:76`，警告 `:79`；原稿警告在 `source-v2.1.txt:1890`、新增段在 `:1896`）。
- 冬之章开头补“Ruby 把先前取下的水晶耳坠重新戴回耳边”（`v21_inserts.rpy:572`），衔接 `sequel_chapter_05_winter.rpy:18` 的“取下”和 `:44` 的“没有交出来”。
- 真结局 Irene 台词由原稿“门已经不会关闭了”（`source-v2.1.txt:2402`）改为“门不会强迫谁留下。下个四季交界，两边都可以再发出邀请。”（`v21_inserts.rpy:778-779`）。
- 返回邮件补足未证实定性（`v21_inserts.rpy:750-752`；原稿 `source-v2.1.txt:2352-2353`）。

## 3. 普通/理想与低信任

### 3.1 旧篇阈值与三结局

产品分支阈值与契约一致，且旧篇三后日谈条件与结局原条件逐字一致：

| 片段 | 产品条件 | 低值处理 |
| --- | --- | --- |
| 午餐 | `affection >= 3`（`v21_inserts.rpy:61`） | `:70-79`，同事式退热贴便签 |
| 天台碰拳 | `affection >= 3`（`:109`） | `:112-115`，收手 |
| 雨伞 | `affection >= 8`（`:136`） | `:147-156`，同伞不拉近、不整领口 |
| 署名 | `affection >= 8`（`:176`） | `:185-194`，共同取证、无手部相碰 |
| 胜利牵手 | `affection >= 15`（`:217`） | `:224-233`，递水但不牵手 |
| 关系问句 | `affection >= 15`（`:257`） | `:262-267`，不提问 |

- 稳定：产品 `ability >= 7 and affection >= 15`（`v21_inserts.rpy:283`）与 `endings.rpy:20` 一致；理想版牵手 `:289`，普通版不确认牵手 `:295`。
- 上升：产品 `ability >= 9 and affection >= 12`（`:313`）与 `endings.rpy:64` 一致；理想版同车 `:315` 并提出约会 `:321`，普通版独自乘车 `:325`、只约下次吃饭 `:328-330`。
- 创业：产品 `side_project_ready and ability >= 8 and affection >= 15 and money >= 1800`（`:346`）与 `endings.rpy:125` 一致；理想版靠肩 `:347`、约会 `:351`，普通版明确“比原计划晚了几个月才上线” `:354` 与 `:361`。

### 3.2 续篇低信任不确认恋情

- Dana 春庭：高值握手与单独看花 `v21_inserts.rpy:449-453`；低值 `:454-462` 仅共同核对记录、来帮忙种花。
- Luna 灯塔：动作回忆只按事件（`:487-502`）；高值软化表达 `:504-507`；低值 `:508-513` 仅工作评价与次日校准。
- Irene 秋日：高值靠肩与借阅证玩笑 `:540-546`；低值 `:547-554` 共同归档、留手套，不靠肩。
- Ruby 冬夜：高值摘耳坠、脸颊吻、递还戴好 `:583-592`；低值 `:593-603` 不摘耳坠、不接吻。
- 终章独处：四位分别按信任分支，高值 `:622/629/637/645` 使用原稿表达；低值 `:624/632/640/647` 均为职业/个人生活表述，不确认恋情。

## 4. 夏章四种事件

- `default sequel_luna_observation_outcome = "unknown"`：`game/core/state.rpy:23`。
- 三个 M05 选项分别写入：`paper_tape`（`sequel_chapter_03_summer.rpy:43`）、`aborted`（`:56`）、`evacuated`（`:64`）；只写事件标记，原奖励 `luna_affection/sequel_insight` 未改。
- 回忆分支：`v21_inserts.rpy:487-498` 按 paper_tape / aborted / evacuated 分支，`else` 为 unknown 中性版；`luna_affection` 只用于 `:504` 的收束亲密表达，不用于推断动作。
- 基础脚本也按标记改写后续取证描述：`sequel_chapter_03_summer.rpy:73-80`、`:102-109`；unknown 为“按当时实际留下的记录”中性表述。

## 5. 平行世界

- 续篇序章只承接事业回顾：`sequel_prologue.rpy:11-22` 按 `sequel_origin_ending` 展示稳定/上升/创业的事业线。
- 明确平行世界：`sequel_prologue.rpy:24-25`“这是一条平行世界线……和许晚晴之间的感情不在这条线里……不另写他们此后如何相处。”
- 全 `sequel_*.rpy` grep“许晚晴”仅命中该说明句；无许晚晴出场、无“分手”正史，未把旧篇恋爱结果写成续篇既定关系。
- 返回结局只表示回到原世界并保留证据（`sequel_endings.rpy:78-99`），未否定续篇关系，也未新增分手。

## 6. 镜面、银铃与耳坠

- 镜面提示：序章旧宅镜面文字 `v21_inserts.rpy:378-380`，screen 定义 `game/screens.rpy:253-262`，下一句前 `hide`。
- 银铃首次出现：`v21_inserts.rpy:382-383`，序章不解释来历。
- 冬之章回收：`v21_inserts.rpy:577-581` 明确旧宅镜子与镜室门同源、银铃也是四季镜信号，并直接区分“耳坠保存名字，银铃只负责提醒……不是同一件东西”。
- 耳坠状态闭合：冬之章开头戴回 `:572`；高值摘下/递还/戴好 `:584-592`；低值未摘、最后扶正 `:597-603`；终章广播仍使用耳坠 `sequel_finale.rpy:19`。银铃未被写成 Ruby 的所有物。
- CG 边界：`cg v21_xuwanqing_rain_close` 仅在 `affection >= 8` 分支（`v21_inserts.rpy:136-137`）；`cg v21_ruby_ending_kiss` 仅在 Ruby 结局唇吻（`:732`）；冬之章脸颊吻只用 `ruby resolute` 立绘与文字（`:585-590`）。

## 7. 真结局门与返回邮件

- 基础真结局已写明门只在四季交界回应双向邀请：`sequel_endings.rpy:111`。
- 新增后日谈再次落地“四季交界”和“两边同时发出的邀请”：`v21_inserts.rpy:768-769`；Irene 补充门不强迫留下、下个四季交界双方可再邀请：`:778-779`。
- 真结局可达条件：`sequel_truth_ready()` 要求四碎片、四信任 ≥3、洞察 ≥6、共同意志 ≥4（`game/core/state.rpy:49-61`），menu 条件见 `sequel_finale.rpy:41`。
- 返回邮件明确为未证实线索：`v21_inserts.rpy:750-752`；不写新变量、不改 `sequel_route`、不触发真结局。返回线本身是终止结局（`sequel_endings.rpy:78-99`）。

## 8. 剩余问题与限制

1. **未做运行时验证**：本次按指示未运行游戏，未验证实际播放、图片加载、存档兼容和界面。本报告只能证明静态文本/行号一致，不能作为人工游玩或运行通过证据。
2. **非阻断演出接缝**：春庭段 `call` 返回后，`sequel_chapter_02_spring.rpy:122` 的“夜色落下前，一行人向海边灯塔出发。”仍使用插入段设置的 `bg v21_time_spring_garden_evening` 和 Dana 立绘（`v21_inserts.rpy:436-437`），下一章才换景。文本不矛盾；若要求离场画面，需技术决定是否在返回后补 `scene`/`hide`。
3. **文档口径差异**：`manifest.json` 的 `asset_ids` 使用基础背景 ID（如第 08 条 `bg company_street_night`、第 13 条 `bg spring_garden`），产品实际使用时段变体（`v21_inserts.rpy:279`、`:436`）。这与 `tech/story-integration.md:43-58` 的实现说明一致；若用 manifest 做最终资源核销，应按该映射核对，不构成剧情缺陷。
4. **旧稿说明句已过时**：`review.md:46` 称除春庭外“其余叙事顺序与原稿一致”，但实际第四章（call `chapter_04.rpy:53` 在卧室备份 `:55` 前）和秋日段（call `sequel_chapter_04_autumn.rpy:76` 在警告 `:79` 前）也按批准修正调整了顺序；产品与 `manifest.json`/`runtime-review.md` 一致，仅该概括句需按后文修正。
5. **契约阈值接缝（非实现偏差）**：第六章关系问句要求 `affection >= 15`（`v21_inserts.rpy:257`），上升理想结局沿用 `>= 12`（`:313`），因此 affection 12–14 的玩家在第六章看到低值版、却在上升理想后日谈看到“到站以后，我想认真和你约会”（`:321`）。这是契约既定阈值叠加，不是文本矛盾；是否对齐阈值由主 Agent 决定。

未发现其他阻断性剧情连续性问题。
