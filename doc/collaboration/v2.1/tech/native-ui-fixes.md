# 原生界面短修

- 实际模型：Grok 4.7（契约角色为 Cursor / grok-4.7-high）
- 工作树：`.work/v21/worktrees/tech`
- 改动：`game/screens.rpy`
- 未改：`gui.rpy`、静音开关、音量条、图片、剧情。未启动 Ren'Py，未编译，未跑测试，未提交。

修完后的界面没有在引擎里再截一张图。下面的「之前」来自实机截图像素和字体测量；「之后」仍要主 Agent 实机点过才算看到。

## 1. 设置滑条

`settings-before.png` 是 2736×1596。游戏内容区约从标题栏下开始，横向 2736/1920 = 1.425。在设置面板里，粉色标题行是：

- 「文字速度」大约 y 598–640
- 「自动播放速度」大约 y 1445–1490

两行之间空了 805 个截图像素，约 565 个游戏像素。自动播放标题已经贴在框底，框高 820 且 `clipping True`，后面的内容被裁掉。这不是公式推出来的空隙，是这张图上的空带。

原因：`Preference("text speed")` 和 `Preference("auto-forward time")` 的值样式是 `slider`，不是 `bar`。`Bar` 在没拿到样式名时用这个值样式。原来的 `xsize 900` / `ysize 24` 只写在 `style bar` 上，`slider` 没有 `ysize` / `ymaximum`。水平条会按父级给出的剩余高度生成自己的高度，轨道又是空的 `Null()`，滑块是 `None`，所以看起来是一整块空白。

现在两条偏好都写成 `style "slider" xsize 1000 ysize 28`。`style slider` 同时写了 `ysize 28`、`ymaximum 28`、粉色左轨 `#e6b7da`、灰右轨 `#6d6588`、18×28 的浅色滑块，并打开 `bar_resizing`。`style bar` 用同一套，避免以后再套错。没有加音量条，`has_sound` / `has_music` / `has_voice` 没动。

快进三项放在同一行：未读文本、选项后继续、跳过转场。选中时按钮用已有的 `#705a8ddd`。按字号 30 和内边距 28 估算，三钮加间距约 590，内容区宽 1070。整列高度大约 464，框内高 740。这只说明排得下，不能代替实机里滑块是否看得见、拖动是否改文字速度。

## 2. 主菜单标题

`SourceHanSansLite` 在 62 号时，这个标题每个字 advance 是 62。八个字共 496。左侧框 620、左右内边距各 90，内容宽 440。七个字 434 能放下，第八个「险」换行。这和实机「只剩险在第二行」一致。

显示改成「旺不稳的」和「奇妙冒险」各四个字，各 248，`xsize 420`，`line_spacing 8`。副标题「旺不稳的奇妙冒险，开始了。」在 30 号时宽 390，仍在 440 内，没有改。`config.name` 仍是一行，窗口标题不变。没有改图。

## 3. 返回

主菜单上下文里，`ui.interact()` 包着 `main_menu` 屏。从这里 `ShowMenu("preferences")` 只是换成同 tag 的设置屏，不新开一层。全局 `game_menu` 键在 `main_menu` 为真时直接返回，所以 Esc 没有任何效果。若设置屏用 `Return(True)` 结束这次交互，`main_menu_screen` 会返回，接着 `_invoke_main_menu` 跳到 `start`，等于从设置退出并进入游戏。

无参数 `Return()` 的实现是：主菜单里调用 `ShowMenu("main_menu")`，不结束交互；游戏内才返回真值，由 `_game_menu` 走到 `_noisy_return` 回到对白。`game_menu` 屏因此绑定 `key "game_menu" action Return()`。主菜单打开的设置、读档、历史都走这条键。游戏内原有「返回游戏」仍是 `Return()`，「返回主菜单」仍是 `MainMenu()`。

主菜单下的菜单屏左上角另有「返回」，位置 `xpos 110 ypos 88`，动作同样是无参数 `Return()`。它不在 `main_menu` 屏上，主菜单本身的按钮文案没加这一项。导航列从大约 y=321 开始，这个按钮在其上方。

实机还要确认：Esc 和「返回」回到带大标题的主菜单，且不会进入新篇；游戏内 Esc 回到对白，而不是主菜单，也不是重新 `start`。
