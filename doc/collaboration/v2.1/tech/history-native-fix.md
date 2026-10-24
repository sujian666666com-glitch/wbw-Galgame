# 历史面板与确认文案

- 实际模型：Grok 4.7（契约角色为 Cursor / grok-4.7-high）
- 工作树：`.work/v21/worktrees/tech`
- 改动：`game/screens.rpy`
- 未改：剧情、`style bar` / `style slider`、`gui.UNKNOWN_TOKEN`、`gui.TRUST_TOKEN`、签名校验、图片、存档。未启动 Ren'Py，未编译，未跑测试，未提交。
- 状态：源码已改，视口是否重新出现对白没有实机截图。不能当作通过。主 Agent 需要用真实 app 再截历史面板，并点开读档、覆盖存档、返回主菜单、退出四句确认。

## 历史记录为什么是空的

`history.png` 里标题「历史记录」在，面板底色是 `game_menu` 的 `#242238dd`，里面没有对白，也没有「尚无对白记录。」。这和「`_history_list` 有数据、但视口没画出来」一致。

`style bar` 的 `xsize 1000` / `ysize 28` **没有**被竖向滚动条继承。SDK `renpy/common/00style.rpy` 里 `style bar is default`，`style vscrollbar is default`，两者是兄弟。`vscrollbar` 自己只多了 `bar_vertical True` 和 `bar_invert True`。本游戏没有把 `vscrollbar` 改成 `is bar`。若真继承了那组尺寸和粉色轨道，截图上应有一条大约 1000×28 的横条，而不是一整块空底。

空白来自宽度计算：

1. `config.position_viewport_side` 为真。历史屏 `viewport` 的 `xsize 1060` / `ysize 720` 落到外层 `side("c r")`，不直接成为中间视口的尺寸。
2. `side` 测量右侧条时，把**整宽**交给 `vscrollbar`（`layout.py` 的 `sizeit("r", width, ...)`）。
3. 官方 GUI 用 `style vscrollbar: xsize gui.scrollbar_size` 把这条测量结果收成窄条。本游戏换过界面，没有这条 `xsize`。`Bar.render` 在没有 `xmaximum` 时按给到的宽度返回。
4. 右侧宽度等于 side 全宽后，中间栏被减到 0（`cwidth = min(cwidth, width - right)`）。对白和空状态都在这栏里，框又 `clipping True`，所以什么都看不见。
5. 默认 `thumb` 是 `None`，`fore_bar` / `aft_bar` 是 `Null()`。竖条本身不画轨道和滑块，空底上连滚动条都没有。

`ysize 28` 没有参与这次计算。竖条高度是 side 给的整高，不是 28。

`config.scrollbar_child_size` 会在未指定时给子级高度 32767（`ui.py` 的 `VIEWPORT_SIZE`）。历史用的 `vbox` 不 `yfill`，实际高度仍是内容高；`yinitial 1.0` 会滚到这段内容的底部。这不是这次全空的原因。内容宽度一旦恢复，原有 `text` 的 `xsize 1020` 换行不用改。

## 这次怎么改的

只加在历史 `viewport` 上，不改全局 `style bar`，设置滑条保持原样：

- `vscrollbar_xsize 18`：测量宽度收成窄条，中间栏约剩 1042。
- `vscrollbar_bar_vertical True`、`vscrollbar_bar_invert True`：竖向，滑块方向与 `style vscrollbar` 一致。
- `vscrollbar_yfill True`，不写 `ysize`：拉满视口高度，避免再变成 28。
- `vscrollbar_base_bar Solid("#6d6588")`、`vscrollbar_thumb Solid("#fff8fc")`、`vscrollbar_bar_resizing True`：轨道和滑块用设置条同一套颜色，不再是空的 `Null()` / `None`。
- `child_size (1020, 32767)`，内容 `vbox` 增加 `xsize 1020`。1020 与现有对白换行相同，并小于 1042。32767 只是排版时提供的高度上限；`vbox` 仍按条目收高，短列表停在顶部，长列表由 `yinitial 1.0` 停在最后几句。

空状态文案、说话人名、对白 `xsize 1020` 都没改。

## 确认文案

读档、覆盖、回主菜单、退出的句子来自 `layout.LOADING`、`layout.OVERWRITE_SAVE`、`layout.MAIN_MENU`、`layout.QUIT`。它们在 `00layout.rpy` 里是英文常量，`FileLoad` / `FileSave` / `MainMenu` / `Quit` 直接把常量交给 `confirm`。`gui.*` 上的 `_()` 这四句不会被这几条动作读到。游戏也没有 `config.language`，所以单独写 `translate chinese strings` 不会换掉画面上的句子。

因此在 `screens.rpy` 里于 init 0 覆盖这四个 `layout` 字符串。确认屏仍是原来的「确定 / 取消」和原来的 yes/no 动作。中文保留原意：读档会丢掉未保存进度，覆盖前要确认，回主菜单会丢掉未保存进度，退出前要确认。

没有改 `gui.UNKNOWN_TOKEN`、`gui.TRUST_TOKEN`，没有关签名。删除存档、快进、回放结束这些英文确认也不在这次范围内，仍是原文。
