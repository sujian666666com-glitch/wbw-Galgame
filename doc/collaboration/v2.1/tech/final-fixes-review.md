# v2.1 收尾修复与交叉审查

- 实际模型：Grok 4.7（契约角色为 Cursor / grok-4.7-high）
- 工作树：`.work/v21/worktrees/tech`
- 改动：`game/options.rpy`、`game/screens.rpy`
- 未改：`game/testcases.rpy`、QA 工作树、打包脚本、对白、`ik.md`。未推送，未跑图形测试。

## 1. 历史记录

`define config.history_length = 250` 已写入 `game/options.rpy`。

SDK 在该值为 `None` 时不写入 `_history_list`，历史界面因此一直是空的。250 只保留最近 250 条对白，不新增 persistent，也不改存档目录。QA 里那条历史断言的 `xfail` 条件是 `renpy.config.history_length is None`。产品把长度设上之后，这个条件为假，断言会按真实历史执行，而不是被跳过。测试文件没有改。

没有在界面里点开历史。修复依据是 Pi 对空列表的复现，以及该配置的默认语义。

## 2. 存档缩略图

`FileScreenshot` 从 316×154 改为 316×178。316÷178 ≈ 1.775，与 16:9 一致，不再把截图压扁。存档按钮高度改为 278，内边距仍是 12。截图 178、两行文字和两处间距 8 落在按钮内。

六格仍是 3×2，格宽 340、间距 20，横向上 3×340+40 = 1060。纵向上两行 278×2+20 = 576，加上页码行和间距约 86，合计约 662，低于现有内容区 740。其他界面没有改。

没有打开存档界面核对像素。

## 3. QA 焦点适配（只读）

审查对象是 QA 工作树 `game/testcases.rpy`，没有编辑。

`init -100` 只在 `renpy.game.args.command == "test"` 时把 `Interface.mouse_focused` 换成始终返回 True 的 property，赋值被空 setter 吃掉。Pi 的 trace 与 SDK 一致：`interact_core` 在 `mouse_focused` 为假时把合成鼠标改成 `(-1, -1)`，按钮因此收不到点击。窗口失焦是环境问题，不是剧情分支错误。

可以接受为测试隔离：

- 只在 `test` 命令安装，正常游玩不替换这个属性。
- 发行包按现有 `build.classify` 排除 `game/testcases.rpy`，最终包里没有这段代码。
- 原生界面验收走真实输入，不走这条 property。
- 它不改 store、存档、菜单或对白，只让测试进程里的合成点击不受 OS 失焦影响。

它改变的是测试进程里的输入路由，不是发行产品的行为。测试期间无法再观察到真实失焦，这和「界面验收另用真实输入」是分开的。

冗余：

- property 装上之后，setter 丢弃赋值。`config.periodic_callbacks` 里的 `_v21_qa_keep_mouse_focus`，以及 global / fixtures / compat 三处 `renpy.game.interface.mouse_focused = True`，都不再改变结果。
- 在 property 装上之前，periodic 也不能堵住竞态：失焦事件可以在两次回调之间把标志写回 False，下一次点击仍会落到 `(-1, -1)`。property 才是堵住这个窗口的办法。
- 安装函数把所有异常吞掉。若 `args` 当时还不存在，property 不会装上，而失败没有痕迹，只剩下那个会丢点击的 periodic。

建议留给 QA，本次未改他们的文件：确认 property 已安装后，去掉 periodic 和三处重复赋值；安装失败要能看见，而不是用每帧回调补救。开发树直接运行时仍会加载 `testcases.rpy`，periodic 会注册，但函数在非测试时立刻返回，不改变游玩。发行包不加载该文件。

## 4. 镜面文字与 unknown

镜面屏幕只在 `v21_sequel_prologue` 出现一次。`show screen v21_mirror_caption` 紧挨着「请不要独自记住」那句旁白，下一句「字很快消失」之前执行 `hide screen`。hide 不在条件分支里，跳过对白仍会执行语句，所以到不了银铃和 `return` 时屏幕还开着。`scene` 不会自动关掉 screen，因此这句 hide 是必要的。调用返回后初遇章会换到 `bg old_house_day`。没有重写对白。

`sequel_luna_observation_outcome` 的 default 仍是 `"unknown"`。夏章三支仍只写 `paper_tape` / `aborted` / `evacuated`。共同叙述和公开证据那一支都有 else，不假定取回了纸带。`v21_sequel_chapter_03_summer` 的 else 只说「会听我把话说完」，不编造六十秒、撤离或切断设备。旧档缺这个变量时由 default 补成 unknown。没有改这些句子。

## 未解决

- 历史有内容、缩略图比例，都没有在窗口里看过。
- QA 的 periodic 冗余没有代为删除。
- 九张新图仍缺，lint 若再跑仍会报 not loadable。本次没有为这两处改动重跑 lint。
