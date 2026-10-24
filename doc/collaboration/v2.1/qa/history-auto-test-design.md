# 历史面板与自动播放：未运行测试设计 + 静态审查

- 实际模型：Pi 会话（`PI_PROVIDER=deepseek`，`PI_MODEL=deepseek-flash`，契约角色 Pi / deepseek-flash）
- 工作树：`.work/v21/worktrees/qa`，已合入 `067899b`（`5a3801d`）
- 改动：`game/testcases.rpy`（仅此产品文件）
- 新增文档：本文件
- 未改动：剧情、UI、`screens.rpy`、图片、`options.rpy`、存档、签名、全局配置、`ik.md`。未写其它工作树。
- **未运行**：没有启动 Ren'Py、没有任何 GUI、没有 `lint`、没有跑 testcase、没有截图、没有 commit/push。GUI 锁由主 Agent 持有。
- 结论：源码已交付、未执行。不能当作通过；下列断言第一次真实运行时才产生结果。

## 1. 新增的两个 testcase

都在 `global` testsuite 内，插在 `v21_label_traversal_audit` 之前，因此仍由该审计最后收尾。

### 1.1 `history_panel_visible_text`（`game/testcases.rpy`）

回归对象：原生 2.1 历史面板“面板空白但 `_history_list` 有数据”（见 `../tech/history-native-fix.md`）。

流程全部走真实输入，不用 `Start()`、不跳 label、不设置剧情变量：

1. 主菜单点“旧篇：三个月，留下来”，`advance until screen "choice"`，点第一个选项。
2. 被动等待（`pause 0.2 until eval (...)`，不发点击）直到历史里出现该句 `先把能做的事列清楚`，`assert screen "say" timeout 2.0`。
   - 特意不用 `advance until "先把能做的事列清楚。"`：`advance` 会先发一次点击，理论上可能把这句跳过去，导致 60 s 超时。被动等待没有这个风险。
3. 点快捷菜单“历史”，`assert screen "history"`。
4. `pause` 等到 `v21_history_metrics("先把能做的事列清楚")` 返回非 None（面板至少完成一次渲染）。
5. 断言：
   - `0 < bar_width <= 64`：`side("c r")` 量到的竖滚动条宽度必须是 `vscrollbar_xsize 18` 的窄条。回归时它是整帧宽度（约 1060），直接把中间栏压到 0。
   - `center_width >= 900`：中间对白栏的测量宽度（视口 xsize 1060 / 内容 1020）没有被挤掉。
   - `text_width >= 200`：这条对白**实际排版出来**的文字宽度（`gui.text_size 34`，12 字约 400 px）。0 宽栏时每个字一行，宽度只有约 34。
   - `0 < text_height <= 400`：有实际文字高度，同时排除 0 宽导致的竖排拉伸。
6. 点“返回游戏”，`assert renpy.get_screen("history") is None`，回主菜单。

`yinitial 1.0` 让面板停在底部，最后一条正是这句对白，所以“排版出宽度”的位置就是实际可见区域。

### 1.2 `auto_forward_advances_by_default`（`game/testcases.rpy`）

回归对象：默认 `afm_time` 拼错成别的字段，SDK 读的是 `afm_time`（见 `../tech/history-native-fix.md` 与主 Agent 的 `default preferences.afm_time = 10`）。

1. `assert eval (preferences.afm_time > 0)`：在改任何偏好之前断言默认值。旧状态是 0，`SayBehavior` 的延迟恒为 0，`afm_enable` 能开但永不推进。
2. 备份并临时设置测试偏好（都恢复）：
   - `preferences.text_cps = 0`：实测文字瞬时完成，把等待压到只由 `afm_time` 决定；
   - `preferences.afm_enable = False`：保证下面的开关是唯一开启者。
3. 真实点击进旧篇、第一个选项，被动等到 `先把能做的事列清楚` 这句在历史中，`assert screen "say" timeout 2.0`。
4. 记下 `id(renpy.game.context().current)` 与 `len(_history_list)`。
5. 真实快捷菜单按钮：`move "Auto forward"` → `pause 0.1` → `click "Auto forward"`（按钮 caption 是“自动”，可读文本来自 `Preference("auto-forward", "toggle")` 的 alt “Auto forward”，与 `ui_features_smoke` 一致）。先悬停再点，让按钮持有焦点，避免点击落到 say 上把本句 dismiss，并触发 `using_afm_enable` 自动关掉自动播放。
6. `assert eval (preferences.afm_enable)`：开关确实被真实按钮打开。
7. **此后不再有任何输入**：`pause 0.2 until eval (len(_history_list) > _v21_afm_history) timeout 25.0`。
8. 断言：
   - `assert screen "say" timeout 2.0`；
   - `id(current) != 旧节点`：语句真的换了；
   - `len(_history_list) == 旧值 + 1`：只自然前进一句，没有多跳；
   - `_history_list[-1].what` 含“楼道里的感应灯坏了三盏”：推进到的正是 `call v21_prologue` 的第一句旁白；
   - `preferences.afm_enable` 仍为真（不是被点击关掉后靠别的方式前进）；
   - `renpy.config.skipping is None`（不是快进造成的）。
9. 恢复 `afm_enable`、`text_cps`，回主菜单。

按默认值，本句 `afm_delay = ((config.afm_bonus 25 + 本句过滤后字数) / config.afm_characters 250) * preferences.afm_time 10`，约 1.5 s；下一句约 3 s。25 s 的 until 上限足够，且不会把失败伪装成通过。

## 2. 静态审查：读过的 SDK 源码与依据

SDK 只读：`.work/renpy-sdk/renpy-8.5.3-sdk`。所有 API 都对着源码确认，没有猜。

| 用途 | 源码位置 | 结论 |
| --- | --- | --- |
| `afm_time` 是真实偏好名 | `renpy/preferences.py:112-115` | `Preference("afm_time", ...)`、`afm_enable`、`using_afm_enable` |
| 自动播放延迟与开关 | `renpy/display/behavior.py:732-745` | `afm_delay = ((config.afm_bonus + afm_length)/config.afm_characters) * preferences.afm_time`，另加 `Text.get_time()`；`afm_time` 为 0 时整段条件不成立，永不推进 |
| 点击会关掉自动播放 | `renpy/display/behavior.py:794-803` | `using_afm_enable and afm_enable and not afm_after_click` 时 dismiss 会置 `afm_enable = False`；所以先悬停再点按钮 |
| `config.default_afm_enable = False` | `renpy/common/00defaults.rpy:36,108-132` | 开局 `afm_enable` 为假、`using_afm_enable` 为真（本测试因此自己显式置假再开） |
| `default preferences.*` 合法 | `renpy/parser.py:974-1006`、`renpy/ast.py:765-774`、`renpy/common/000namespaces.rpy:79-105` | `store.preferences` 是 special namespace，`set_default` 写 `_preferences` 并记 `persistent._preference_default`；`repeat_at_default_time = True` |
| 延迟常数 | `renpy/config.py:223,226` | `afm_characters = 250`、`afm_bonus = 25` |
| 竖向滚动条如何进入 `side` | `renpy/ui.py:1111-1163` | `scrollbars "vertical"` 建 `side("c r")` + `Viewport` + `vscrollbar`；`config.position_viewport_side` 时 xsize/ysize 归 side；竖条测量拿整宽 |
| 全宽竖条如何吃掉中间栏 | `renpy/display/layout.py:1867-2070`（`Side.render`） | `sizeit("r", width, ...)` 用整宽；`cwidth = min(cwidth, width - left - right)`；`self.right` / `self.cwidth` 就是这次布局的实测值 |
| `Bar` 宽度来自 style xsize | `renpy/display/behavior.py:2240-2520` | `Bar.render(width, height)` 直接用传入宽高；`xsize`（=xmaximum）由上层 `render()` 裁剪，所以 `vscrollbar_xsize 18` 会把测量宽度收成 18 |
| `Text` 实际排版数据 | `renpy/text/text.py:2529-2560`（`get_layout`）、`669-990`（`Layout.size`）、`1206`（`unscale_pair`）、`2740-2795`（`render` 按 width/height 缓存 layout） | `Text.get_layout()` 返回**已渲染**用过的 Layout；`layout.size` 是字形实际外框，需 `unscale_pair` 还原虚拟分辨率。宽度为 0 时中文会逐字换行，宽度只剩单字宽 |
| 遍历在屏 displayable | `renpy/display/screen.py:499-510,1128-1180` | `renpy.get_screen("history")` 先按 tag 再按名字找 ScreenDisplay；`ScreenDisplay.visit_all(callback)` 递归；`ScreenDisplay.child` 是构建出的树根 |
| `Viewport` 类位置 | `renpy/display/viewport.py:43`、`renpy/__init__.py:493-499` | `renpy.display.viewport.Viewport`；`renpy.text.text.Text`（`renpy.display.text` 只是 `sys.modules` 别名，改用 `renpy.text.text` 更稳） |
| 测试语句语法 | `renpy/test/testparser.py:114-135,235-280,524-541,791-875`、`renpy/test/testast.py:1008-1030,1264-1345,1413-1455` | `pause T until <cond> timeout T`、`assert <cond> timeout T`、`move "<text>"`、`click "<text>"` 均存在；`assert` 无 `timeout` 时**不等待**，所以只有两处 `assert screen "say"` 加了 `timeout 2.0`；`until` 的 `timeout` 会临时替换 `_test.timeout` 并在结束时恢复 |
| 点击的真实语义 | `renpy/test/testmouse.py:95-103`、`renpy/test/testast.py:848-854` | `click` 在同一帧 post motion+press+release；因此先 `move` + `pause 0.1` 让焦点先落到按钮 |
| 文本选择器匹配 | `renpy/test/testfocus.py:31-59` | 被 `find_focus` 找到的可读文本包含 `Preference` 的 alt “Auto forward”（与 `ui_features_smoke` 同一依据） |

## 3. 已经做过的静态检查（不含运行）

1. `game/testcases.rpy` 三处 `init python` 块抽出、去缩进后 `python3 compile()`：全部通过。
2. 两个新 testcase 逐行检查：非空非注释行缩进恰好 4 空格，首词都是合法测试语句（`click`/`advance`/`assert`/`pause`/`$`/`run`/`move`）。
3. 交叉核对：`_history_list` / `h.what` 用法与同文件既有断言一致；`any(... for h in _history_list)` 这种表达式在 `assert eval (...)` 已有先例，`until eval (...)` 走同一 `parse_condition`/`simple_expression` 路径。
4. 交叉核对剧情路径：`game/story/prologue.rpy` 里点第一个选项后就是 `wbw "先把能做的事列清楚。"`，紧接着 `call v21_prologue`，其第一句是 `narrator "楼道里的感应灯坏了三盏。…"`（`game/story/v21_inserts.rpy:30-43`）。两句之间没有 menu、没有其它 say。
5. 未修改任何产品逻辑，`options.rpy` 的 `default preferences.afm_time = 10` 原样保留。

## 4. 残余风险（第一次真跑时请重点看）

1. **`assert screen "say"`**：`say` 屏没有 tag，靠 `get_screen` 按名字查找；若第一次跑报“screen not found”，改成 `assert eval (renpy.get_screen("say") is not None) timeout 2.0`（同样严格，不削弱断言内容）。
2. **`Side.right` 属性名**：按 `layout.py:1966-1972,2000` 应为 `right` / `cwidth`，且只在渲染后才有；helper 用 `hasattr(side, "right")` 保护，未渲染前返回 None 让 `pause until` 重试。若历史屏里出现第二个 `Side`，helper 只取“子级含 `Viewport`”的那个。
3. **`layout.size` 与字号**：`gui.text_size = 34`，12 字约 400 px，`text_width >= 200` 与 `text_height <= 400` 留了余量。若历史上这句被自动换行成两行，高度断言仍有余量。
4. **快捷菜单按钮命中**：沿用 `ui_features_smoke` 的 “Auto forward” 文本。先 `move` 再 `pause 0.1` 再 `click` 是为了让按钮先拿到焦点；若仍出现点击把本句 dismiss（表现为 `assert preferences.afm_enable` 立刻失败），说明焦点没更新，可把 `pause 0.1` 调大到 `0.2`，不要改成直接赋值开关。
5. **`_history_list` 恰好多 1**：靠“检测到新条目当帧”保证；若极端掉帧导致一次多前进两句，断言会失败并报出真实数字，属于应当复查的信号，不要放宽成 `>=`。
6. **首帧竞争**：两处等待都是被动 `pause ... until`，不会象 `advance until` 那样先发点击；`until` 都带 `timeout`，失败会明确超时而不是挂住 60 s。
7. 两个 testcase 都会真实经过 `v21_prologue`，对 `v21_label_traversal_audit` 只是多一条已到达记录，不影响 23 个 label 的完整性判定。

## 5. 需要主 Agent 执行的事（我未做）

- 在 GUI 锁空闲时运行：
  - `tools/v21_run_tests.py`（组合跑）或单跑 `history_panel_visible_text`、`auto_forward_advances_by_default`；
  - 建议同时保留一次“单跑 + 与 `ui_features_smoke` 组合”的结果，便于区分环境波动与新断言问题。
- 若失败，请把 Ren'Py 报错原文与失败断言回传；我按上面第 4 节的边界修，不削弱断言（特别是 `bar_width`、`text_width`、`afm_time > 0`、`+1` 这四条是回归本身）。
- 最终包验收仍需主 Agent 用真实 app 观察一次历史面板对白与默认自动播放。
