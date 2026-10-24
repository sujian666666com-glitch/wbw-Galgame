# 2.0 兼容存档夹具（v2.1 验收用）

由 `tools/v21_capture_fixtures.py` 在冻结的 2.0 基线上真实游玩生成：
每个夹具都从主菜单进入对应篇章，按真实选项走到目标 menu 后用存档 UI 的
page 1 / slot 1 保存，并同步记录当时的 store 状态。生成过程持有
`.work/v21/gui.lock` 独占锁，使用独立 `RENPY_PATH_TO_SAVES` 与隔离 persistent，
不读写用户存档。

## 目录

```text
compat-v20/
├── manifest.json                  # 夹具清单、状态记录、文件 SHA-256
├── README.md
├── v20_old_chapter01_menu/
│   ├── state.json                 # 存档时刻的 store/persistent 状态
│   └── saves/three-months-to-stay-1/1-1-LT1.save
├── v20_old_chapter06_menu/
│   ├── state.json                 # 存档时刻的 store/persistent 状态
│   └── saves/three-months-to-stay-1/1-1-LT1.save
├── v20_sequel_finale_menu/
│   ├── state.json                 # 存档时刻的 store/persistent 状态
│   └── saves/three-months-to-stay-1/1-1-LT1.save
├── v20_sequel_first_menu/
│   ├── state.json                 # 存档时刻的 store/persistent 状态
│   └── saves/three-months-to-stay-1/1-1-LT1.save
```

## 用法（2.1 验证时）

```bash
# 1. 准备隔离存档根目录，把夹具拷进去（不要指向用户存档）
mkdir -p .work/qa/saves-2.1
cp -R .work/v21/compat-v20/<fixture>/saves/three-months-to-stay-1 .work/qa/saves-2.1/

# 2. 用 2.1 项目副本跑 GUI（必须持 gui.lock）
python3 tools/v21_run_tests.py --project .work/qa/project --saves .work/qa/saves-2.1 \
    --case <compat testcase>
```

`state.json` 给出读档后应立即成立的数值；2.1 读入后应保持旧篇数值与进度，
新增变量使用 `default` 的初值（例如 `sequel_luna_observation_outcome = "unknown"`）。

## 夹具一览

### v20_old_chapter01_menu

- 篇：old
- 说明：旧篇：主菜单→旧篇→序章选择后自然到达第一章菜单（ability=3，未做第一章选择）
- 用途：2.1 在旧篇第一章前后插入片段时的早期菜单兼容性；验证 from 2.0 存档读入后数值与进度不变
- 游戏版本：2.0.0 / Ren'Py [8, 5, 3, 26051504]
- 存档时刻语句：`('game/story/chapter_01.rpy', 1041769481, 391)`
- 关键数值：ability=3, affection=0, money=1100, chapter_progress=1, story_arc=old, sequel_chapter_progress=0, sequel_insight=0, sequel_resolve=0, dana_affection=0, luna_affection=0, irene_affection=0, ruby_affection=0

### v20_old_chapter06_menu

- 篇：old
- 说明：旧篇：自然走完序章至第五章（理想数值路线），停在第六章三选项菜单
- 用途：旧篇结局前插入（persistent 写入之前）与第六章菜单的兼容性；同时覆盖三结局选择入口
- 游戏版本：2.0.0 / Ren'Py [8, 5, 3, 26051504]
- 存档时刻语句：`('game/story/chapter_06.rpy', 1041769482, 748)`
- 关键数值：ability=13, affection=27, money=1832, chapter_progress=6, story_arc=old, sequel_chapter_progress=0, sequel_insight=0, sequel_resolve=0, dana_affection=0, luna_affection=0, irene_affection=0, ruby_affection=0

### v20_sequel_finale_menu

- 篇：sequel
- 说明：续篇：自然走完四季章节（全信任/高洞察路线），停在终章六选项菜单之前
- 用途：终章最终 menu 之前插入与真结局前置的兼容性；核对四碎片、insight/resolve、四人信任
- 游戏版本：2.0.0 / Ren'Py [8, 5, 3, 26051504]
- 存档时刻语句：`('game/story/sequel_finale.rpy', 1041769486, 1467)`
- 关键数值：ability=2, affection=0, money=2300, chapter_progress=0, story_arc=sequel, sequel_chapter_progress=6, sequel_insight=6, sequel_resolve=5, dana_affection=3, luna_affection=3, irene_affection=3, ruby_affection=4

### v20_sequel_first_menu

- 篇：sequel
- 说明：续篇：主菜单→新篇→序章自然到达第一个菜单，未做任何续篇选择
- 用途：续篇序章/第一章新增片段的早期兼容性；验证 story_arc/续篇变量初始值
- 游戏版本：2.0.0 / Ren'Py [8, 5, 3, 26051504]
- 存档时刻语句：`('game/story/sequel_prologue.rpy', 1041769486, 1523)`
- 关键数值：ability=2, affection=0, money=2300, chapter_progress=0, story_arc=sequel, sequel_chapter_progress=0, sequel_insight=0, sequel_resolve=0, dana_affection=0, luna_affection=0, irene_affection=0, ruby_affection=0

