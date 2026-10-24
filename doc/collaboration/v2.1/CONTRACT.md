# v2.1 协作契约

基线：`1737ed686bbc4c4a634d9a564d4ba24b4a1860dc`。原稿为本目录 `source-v2.1.txt`，SHA-256：`bceb94b259b1c94bd01b4b07bd62d82bf6ad0b1a938ae568c1d063f61770a6c9`。

## 已批准范围

Ren'Py 8.5.3，1920×1080，v2.1.0，macOS 静音交付。保留原有22菜单、61选项、9类结局和既有数值。接入23个新增片段。两篇为平行世界线：事业回顾沿用，恋爱关系独立；不增加分手正史。不做地图、日程、音频或其他平台。禁止覆盖既有图片。

## 单一所有权

- 主Agent：本目录根级文档、版本冻结、集成分支、运行报告、打包交付、README/现有总体文档、可读剧本导出。
- Claude Code / deepseek-flash[1m]：仅 `doc/collaboration/v2.1/story/`。定稿23片段及接入表；不直接写产品代码。
- Cursor / grok-4.7-high：`game/` 下产品 `.rpy`，但不写 `game/testcases.rpy` 或图片。技术报告写 `doc/collaboration/v2.1/tech/`。
- Pi / deepseek/deepseek-flash：仅 `game/testcases.rpy`、`tools/v21_*` 验收工具、`doc/collaboration/v2.1/qa/`。不改产品剧情/UI。
- Codex / gpt-6.1-sol：仅 `image/v21/`、`game/images/v21/`、`doc/collaboration/v2.1/art/`。

各自独立工作树/分支，由主Agent审查并集成。各Agent不得提交、切换、合并其他人的分支，不得推送。产物报告写明实际调用模型、变更、检查与未解决问题；未完成不得写通过。

## 剧情接口

新增事件状态：`default sequel_luna_observation_outcome = "unknown"`；夏章M05三项分别写 `paper_tape`、`aborted`、`evacuated`，只记录事实，不改变原奖励。旧档unknown使用中性对白。

Claude交付 `story/inserts.rpy.txt`（可供技术转录的23个Ren'Py label蓝本）及 `story/manifest.json`。每个新增label按 `v21_` 加对应既有label命名（共23个），最终 `return`；不含menu、不修改数值或persistent。manifest逐项列出 `id`、`source_heading`、`target_label`、`placement`、`condition_summary`、`asset_ids`。产品中的新增label由Cursor接入。

插入位置：一般在原章节最后jump之前；旧篇第六章及续篇终章在最终menu之前；旧篇结局在persistent写入之前；续篇结局在“——…结局”marker之前。不得让结局marker提前于新增后日谈。

旧篇亲密程度复用现有好感阶段：午餐>=3，雨伞/署名段>=8，胜利牵手/最终关系问句>=15；低值保留职业互助与克制版本。天台职业动机保留。旧篇三后日谈沿用各结局原有理想条件；上升线理想版同车、普通版异地；创业普通版明确时间过去才上线。

四位续篇角色的章内亲密版以对应信任>=3为条件，低值保留角色表达、不确认恋情。Ruby共通脸颊吻仅高信任、用立绘和文字；专属CG只用于已选Ruby结局的唇吻。保持成年人自愿亲密。夏章所有动作回忆依事件标记，不用好感推断。回收镜面提示与银铃（银铃不是水晶耳坠），返回邮件为未证实线索；真结局门只在四季交界、双方邀请时开启。

## 固定美术接口

| Ren'Py image ID | 运行时路径 | 用途 |
| --- | --- | --- |
| `dana worried` | `game/images/v21/characters/dana_worried.png` | Dana担忧 |
| `luna soft` | `game/images/v21/characters/luna_soft.png` | Luna柔和 |
| `irene shaken` | `game/images/v21/characters/irene_shaken.png` | Irene动摇 |
| `irene relieved` | `game/images/v21/characters/irene_relieved.png` | Irene释然 |
| `ruby resolute` | `game/images/v21/characters/ruby_resolute.png` | Ruby坚定 |
| `bg v21_train_interior_dusk` | `game/images/v21/backgrounds/bg_train_interior_dusk.png` | 上升后日谈 |
| `bg v21_old_house_mirror` | `game/images/v21/backgrounds/bg_old_house_mirror.png` | 旧宅镜面 |
| `cg v21_xuwanqing_rain_close` | `game/images/v21/cg/cg_xuwanqing_rain_close.png` | 高好感雨伞 |
| `cg v21_ruby_ending_kiss` | `game/images/v21/cg/cg_ruby_ending_kiss.png` | Ruby结局 |

图片只以现有插画立绘/CG作参考，不发送真人参考照。人物脸、服装、发型、年龄不可重设。CG和背景1920×1080；立绘RGBA，沿用基础立绘画布/站位，显示高度<=1024。时段变体由技术复用调色；镜中文字用代码叠加，不烘焙进图片。

生图仅由美术负责人串行调用 `/Users/ik/.claude/skills/codex-imagegen/scripts/gen.sh`，明确 `-m gpt-6.1-sol`、`--keep`，表情用 `-e` 现有立绘和 `-t`。所有图片先验收再交付；脚本“全局最新图片”兜底结果必须拒收，不能把OK当成归属证明。

## 验收协作

SDK只读入口：主仓库 `.work/renpy-sdk/renpy-8.5.3-sdk/renpy.sh`。所有测试用隔离项目与独立 `RENPY_PATH_TO_SAVES`。图形测试和原生界面验收不得并发操作；测试进程必须获取主仓库 `.work/v21/gui.lock` 的独占文件锁。

基线两失败：save_load_smoke第119行ability断言；紧随其后的sequel_full_flow_true_ending第133行主菜单等待超时。先单跑/组合/真实界面定位，不只延长超时，不削弱断言。

发布包排除：开发文档、原始image、个人ik.md、测试源码/编译文件、tools、SDK、缓存、存档、日志。完整源码单独归档。保留 `config.save_directory`，新增变量用default；禁止用重置用户存档解决兼容性。
