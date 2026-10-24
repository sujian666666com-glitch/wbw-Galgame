# --- QA-only test hook: keep synthetic mouse input alive ------------------
#
# Root cause of the v2.1 baseline flakes (reproduced with v21_run_tests.py
# --trace/--focus-chaos): Interface.interact_core() rewrites every mouse
# event to x = y = -1 while Interface.mouse_focused is false:
#
#     if not self.mouse_focused or self.ignore_touch:
#         x = -1
#         y = -1
#
# mouse_focused is maintained from window-focus events. When another
# application takes the OS window focus while a test is running, the next
# synthetic click is delivered at (-1, -1), Button.event() sees a button that
# is not focused and drops it, the game stays on the choice screen, and the
# next `advance until ...` burns the whole 60 s testcase timeout. The click is
# lost for an environment reason, not because of game logic.
#
# Synthetic test input has explicit coordinates and must not depend on which
# window the user is looking at. During the Ren'Py `test` command we therefore
# make mouse_focused a constant True on the interface class. This changes no
# game state, is only installed for `renpy.sh <project> test ...`, and
# testcases.rpy is excluded from release builds by build.classify.
init -100 python:
    if renpy.game.args.command == "test":
        from renpy.display.core import Interface

        Interface.mouse_focused = property(lambda self: True, lambda self, value: None)


init python:
    def v21_choice_captions():
        """Captions currently offered by the choice screen.

        Conditional menu options are filtered by the menu statement before the
        screen is shown, so this is the exact set a player can pick. Used to
        assert ending gates without clicking an unavailable option.
        """

        screen = renpy.get_screen("choice")
        if screen is None:
            return []

        rv = []
        for item in screen.scope.get("items", []):
            caption = getattr(item, "caption", None)
            if caption is not None:
                rv.append(caption)
        return rv

    def v21_capture_state(fixture):
        """Write the live store state for a compatibility fixture.

        Used only by the `fixtures` testsuite; the output path comes from
        V21_QA_STATE_FILE. Records exactly what a 2.1 build must be able to
        read back from the 2.0 save (variables, statement, persistent).
        """

        import json
        import os

        path = os.environ.get("V21_QA_STATE_FILE", "")
        if not path:
            return

        store = renpy.store
        keys = [
            "ability",
            "affection",
            "money",
            "chapter_progress",
            "ending_route",
            "evidence_ready",
            "side_project_ready",
            "story_arc",
            "sequel_chapter_progress",
            "sequel_route",
            "sequel_origin_ending",
            "sequel_luna_observation_outcome",
            "ruby_affection",
            "dana_affection",
            "luna_affection",
            "irene_affection",
            "sequel_insight",
            "sequel_resolve",
            "spring_fragment",
            "summer_fragment",
            "autumn_fragment",
            "winter_fragment",
        ]

        state = {}
        for key in keys:
            if hasattr(store, key):
                state[key] = getattr(store, key)

        try:
            current = repr(renpy.game.context().current)
        except Exception:
            current = "?"

        record = {
            "fixture": fixture,
            "game_version": renpy.config.version,
            "save_directory": renpy.config.save_directory,
            "current": current,
            "state": state,
            "choice_captions": v21_choice_captions(),
            "fragment_count": renpy.store.fragment_count(),
            "persistent": {
                "old_ending_route": renpy.store.persistent.old_ending_route,
                "old_endings_seen": list(renpy.store.persistent.old_endings_seen or []),
            },
        }

        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


init python:
    def v21_pref_slider_rect(field_name):
        """Live screen rectangle (x, y, w, h) of a preferences slider.

        The settings smoke test drives the real bar, not the preference
        variable, so the geometry has to come from the rendered focus list.
        A zero-height / oversized rect is the native regression where the
        `slider` style fell back to the full remaining height and pushed the
        next setting out of the clipped frame.
        """

        from renpy.display.behavior import Bar

        for focus in renpy.display.focus.focus_list:
            widget = getattr(focus, "widget", None)
            if not isinstance(widget, Bar):
                continue
            value = getattr(widget, "value", None)
            if getattr(value, "field", None) != field_name:
                continue
            if focus.x is None:
                continue
            rect = (int(focus.x), int(focus.y), int(focus.w), int(focus.h))
            if rect[2] > 0 and rect[3] > 0:
                return rect
        raise Exception("preferences slider not rendered: " + field_name)

    def v21_pref_slider_point(field_name, fraction):
        """Absolute screen point at `fraction` across a preferences slider."""

        x, y, w, h = v21_pref_slider_rect(field_name)
        return (int(x + w * fraction), int(y + h / 2.0))

    def v21_history_metrics(pattern):
        """Live geometry and laid-out text of the displayed 历史 panel.

        Returns `(bar_width, center_width, text_width, text_height)`, or None
        while the panel is still being built (nothing in the panel is drawn
        before the first render). Used by `history_panel_visible_text`.

        `bar_width` is what the `side("c r")` that `viewport ... scrollbars
        "vertical"` builds (renpy/ui.py:viewport_common) measured for the
        vertical scrollbar. Without `vscrollbar_xsize` the bar is sized at the
        whole frame width, `Side.render` then clamps the middle column
        (`renpy/display/layout.py:Side`) to zero, and the dialogue column is
        laid out but never visible. `center_width` is the measured centre
        column, `text_*` come from the Layout the history `Text` was actually
        rendered with (renpy/text/text.py:Text.get_layout), so keeping the
        string in `_history_list` alone cannot satisfy this helper.
        """

        screen = renpy.get_screen("history")
        if screen is None or screen.child is None:
            return None

        items = []
        screen.visit_all(items.append)

        side = None
        for d in items:
            if not isinstance(d, renpy.display.layout.Side):
                continue
            for child in d.visit():
                if isinstance(child, renpy.display.viewport.Viewport):
                    side = d
                    break
            if side is not None:
                break

        if side is None or not hasattr(side, "right"):
            return None

        for d in items:
            if not isinstance(d, renpy.text.text.Text):
                continue
            try:
                text = d._tts(False)
            except Exception:
                continue
            if pattern not in text:
                continue
            layout = d.get_layout()
            if layout is None:
                return None
            width, height = layout.unscale_pair(*layout.size)
            return (
                int(side.right),
                int(getattr(side, "cwidth", 0)),
                int(round(width)),
                int(round(height)),
            )

        return None

    # QA-only dynamic label coverage: record every v2.1 insert that the game
    # actually transfers control to. tools/v21_run_tests.py --label-file sets
    # V21_QA_LABEL_FILE for the whole run; the audit testcase at the end of the
    # regression suite asserts that all 23 inserts were traversed by real play.
    def v21_record_label(label, abnormal):
        import os
        path = os.environ.get("V21_QA_LABEL_FILE", "")
        if path and isinstance(label, str) and label.startswith("v21_"):
            try:
                with open(path, "a", encoding="utf-8") as f:
                    f.write(label + "\n")
            except Exception:
                pass

    def v21_audit_labels():
        import os
        path = os.environ.get("V21_QA_LABEL_FILE", "")
        expected = {
            "v21_prologue",
            "v21_chapter_01", "v21_chapter_02", "v21_chapter_03",
            "v21_chapter_04", "v21_chapter_05", "v21_chapter_06",
            "v21_ending_stable", "v21_ending_rising", "v21_ending_startup",
            "v21_sequel_prologue",
            "v21_sequel_chapter_01", "v21_sequel_chapter_02_spring",
            "v21_sequel_chapter_03_summer", "v21_sequel_chapter_04_autumn",
            "v21_sequel_chapter_05_winter",
            "v21_sequel_finale",
            "v21_sequel_ending_dana", "v21_sequel_ending_luna",
            "v21_sequel_ending_irene", "v21_sequel_ending_ruby",
            "v21_sequel_ending_return", "v21_sequel_ending_true",
        }
        assert path, "V21_QA_LABEL_FILE is not set; run through tools/v21_run_tests.py --label-file"
        with open(path, encoding="utf-8") as f:
            reached = {line.strip() for line in f if line.strip()}
        missing = sorted(expected - reached)
        assert not missing, "v2.1 insert labels not traversed: " + ", ".join(missing)
        assert len(expected) == 23

    if renpy.game.args.command == "test":
        config.label_callbacks.append(v21_record_label)


testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.02
        # The full sequel intentionally loads six 1920x1080 CGs. Give CI and
        # first-run texture decoding enough time without weakening assertions.
        $ _test.timeout = 60.0
        $ persistent.test_old_ending_route_backup = persistent.old_ending_route
        $ persistent.test_old_endings_seen_backup = list(persistent.old_endings_seen)

        if eval (not main_menu):
            run MainMenu(confirm=False)

    teardown:
        $ persistent.old_ending_route = persistent.test_old_ending_route_backup
        $ persistent.old_endings_seen = persistent.test_old_endings_seen_backup
        $ persistent.test_old_ending_route_backup = None
        $ persistent.test_old_endings_seen_backup = None
        $ renpy.save_persistent()
        exit


testcase full_flow_stable_ideal:
    click "旧篇：三个月，留下来"

    advance until screen "choice"
    click "把三个月的目标拆成行动清单。"
    advance until screen "choice"
    click "没事，我正好趁这个机会看看公司的数据。"
    advance until screen "choice"
    click "先自己跑一遍完整数据验证，确认后再汇报。"
    advance until screen "choice"
    click "才第四天，急什么。"
    advance until screen "choice"
    click "要不现在就去公司跑一遍数据？"
    advance until screen "choice"
    click "会后悄悄给她买一杯咖啡放在桌上。"
    advance until screen "choice"
    click "还是 AA 吧，我现在不富裕。"
    advance until screen "choice"
    click "不是不说，是时候没到。我已经保留了所有的原始文件和时间记录。"
    advance until screen "choice"
    click "我不介意功劳被分，但方案不能出错。下次有问题直接找我。"
    advance until screen "choice"
    click "签下公司的转正通知。"

    advance until "你终于开窍了。"
    assert eval (ending_route == "stable")
    assert eval (chapter_progress == 6)
    assert eval (ability >= 7 and affection >= 15)
    assert eval (story_arc == "old")
    assert eval (sequel_chapter_progress == 0 and sequel_route == "" and ruby_affection == 0 and dana_affection == 0 and luna_affection == 0 and irene_affection == 0)
    assert eval (sequel_insight == 0 and sequel_resolve == 0 and fragment_count() == 0)
    advance until eval (main_menu)


testcase rising_ideal:
    $ ability = 9
    $ affection = 12
    run Start("chapter_06")
    advance until screen "choice"
    click "接受另一家公司的 offer。"
    advance until "你以为就你有野心？走吧，一起。"
    assert eval (ending_route == "rising")
    advance until eval (main_menu)


testcase startup_ideal:
    $ ability = 8
    $ affection = 15
    $ money = 1800
    $ side_project_ready = True
    run Start("chapter_06")
    advance until screen "choice"
    click "拿起自己的项目企划书。"
    advance until "他们的第一个版本如期上线。"
    assert eval (ending_route == "startup")
    advance until eval (main_menu)


testcase stable_normal:
    $ ability = 2
    $ affection = 0
    run Start("ending_stable")
    advance until "庆祝你顺利转正。"
    advance until eval (main_menu)


testcase rising_normal:
    $ ability = 2
    $ affection = 0
    run Start("ending_rising")
    advance until "我暂时不去。不过，你到了那边别松懈。"
    advance until eval (main_menu)


testcase startup_normal:
    $ ability = 2
    $ affection = 0
    $ money = 100
    $ side_project_ready = False
    run Start("ending_startup")
    advance until "条件还不算充足"
    advance until eval (main_menu)


testcase save_load_smoke:
    click "旧篇：三个月，留下来"
    advance until screen "choice"
    click "把三个月的目标拆成行动清单。"
    assert eval (ability == 3)

    click "保存"
    assert screen "save"
    click "返回游戏"

    run FileSave(1, confirm=False, page="1")
    advance until screen "choice"
    click "没事，我正好趁这个机会看看公司的数据。"
    assert eval (ability == 4)

    click "读档"
    assert screen "load"
    click "返回游戏"
    run FileLoad(1, confirm=False, page="1")
    pause 1.0
    assert eval (ability == 3)
    run MainMenu(confirm=False)


testcase sequel_full_flow_true_ending:
    click "新篇：樱镜町"

    advance until screen "choice"
    click "逐项核对文件"
    advance until screen "choice"
    click "坦白自己是被银光带来"
    advance until screen "choice"
    click "立即与 Luna 核对"
    advance until screen "choice"
    click "先问 Dana 需要什么"
    advance until screen "choice"
    click "让每位见证者各自保存"
    advance until screen "choice"
    click "执行 Luna 的分组方案"
    advance until screen "choice"
    click "公开可复核证据"
    advance until screen "choice"
    click "让她把所有经过说完"
    advance until screen "choice"
    click "拒绝未经本人"
    advance until screen "choice"
    click "请她亲手写下名字"
    advance until screen "choice"
    click "尊重 Ruby 的决定"
    advance until screen "choice"
    click "让整个樱镜町共同记住"

    advance until "——真结局《四季同在》"
    assert eval (sequel_route == "true")
    assert eval (sequel_chapter_progress == 7)
    assert eval (sequel_luna_observation_outcome == "paper_tape")
    assert eval (sequel_truth_ready())
    assert eval (story_arc == "sequel")
    assert eval (affection == 0 and ability == 2 and money == 2300 and ending_route == "")
    advance until eval (main_menu)


testcase sequel_dana_ending:
    $ spring_fragment = True
    $ summer_fragment = True
    $ autumn_fragment = True
    $ winter_fragment = True
    $ dana_affection = 3
    run Start("sequel_finale")
    advance until screen "choice"
    assert eval (dana_affection == 3)
    click "与 Dana 一起守住"
    advance until "——Dana 结局《春日归邻》"
    assert eval (sequel_route == "dana")
    advance until eval (main_menu)


testcase sequel_luna_ending:
    $ spring_fragment = True
    $ summer_fragment = True
    $ autumn_fragment = True
    $ winter_fragment = True
    $ luna_affection = 3
    run Start("sequel_finale")
    advance until screen "choice"
    assert eval (luna_affection == 3)
    click "与 Luna 一起建立"
    advance until "——Luna 结局《盛夏坐标》"
    assert eval (sequel_route == "luna")
    advance until eval (main_menu)


testcase sequel_irene_ending:
    $ spring_fragment = True
    $ summer_fragment = True
    $ autumn_fragment = True
    $ winter_fragment = True
    $ irene_affection = 3
    run Start("sequel_finale")
    advance until screen "choice"
    assert eval (irene_affection == 3)
    click "与 Irene 一起重写"
    advance until "——Irene 结局《秋实之书》"
    assert eval (sequel_route == "irene")
    advance until eval (main_menu)


testcase sequel_ruby_ending:
    $ spring_fragment = True
    $ summer_fragment = True
    $ autumn_fragment = True
    $ winter_fragment = True
    $ ruby_affection = 3
    run Start("sequel_finale")
    advance until screen "choice"
    assert eval (ruby_affection == 3)
    click "陪 Ruby 记住"
    advance until "——Ruby 结局《冬夜来信》"
    assert eval (sequel_route == "ruby")
    advance until eval (main_menu)


testcase sequel_return_ending:
    $ spring_fragment = True
    $ summer_fragment = True
    $ autumn_fragment = True
    $ winter_fragment = True
    run Start("sequel_finale")
    advance until screen "choice"
    click "回到原来的世界"
    advance until "——返回结局《回到灯火》"
    assert eval (sequel_route == "return")
    advance until eval (main_menu)


testcase sequel_origin_rising_smoke:
    $ persistent.old_ending_route = "rising"
    run Start("sequel_start")
    assert eval (sequel_origin_ending == "rising")
    assert eval (story_arc == "sequel")
    run MainMenu(confirm=False)


# ===========================================================================
# v2.1 acceptance matrix additions (baseline 2.0 content, no v21 inserts yet)
#
# These routes exist so the matrix can state, per option and per ending gate,
# what is actually exercised today:
#   * every one of the 61 options is clicked by at least one testcase;
#   * old篇 normal/ideal for stable, rising, startup;
#   * sequel true ending positive and negative gates;
#   * history / auto-forward / skip / rollback / save-load UI.
# They intentionally assert concrete state (values, captions, markers) instead
# of only waiting on text, so a silently skipped click fails loudly.
# ===========================================================================

testcase full_flow_startup_ideal:
    # Natural startup ideal: same data/affection path as the stable ideal run,
    # but the money threshold is met through the chapter 5 bonus while still
    # paying for the coffee (-18) and the AA dinner (-50).
    click "旧篇：三个月，留下来"
    advance until screen "choice"
    click "把三个月的目标拆成行动清单。"
    advance until screen "choice"
    click "没事，我正好趁这个机会看看公司的数据。"
    advance until screen "choice"
    click "先自己跑一遍完整数据验证，确认后再汇报。"
    advance until screen "choice"
    click "才第四天，急什么。"
    advance until screen "choice"
    click "要不现在就去公司跑一遍数据？"
    advance until screen "choice"
    click "会后悄悄给她买一杯咖啡放在桌上。"
    advance until screen "choice"
    click "还是 AA 吧，我现在不富裕。"
    advance until screen "choice"
    click "不是不说，是时候没到。我已经保留了所有的原始文件和时间记录。"
    advance until screen "choice"
    click "我不介意功劳被分，但方案不能出错。下次有问题直接找我。"
    advance until screen "choice"
    click "拿起自己的项目企划书。"

    advance until "他们的第一个版本如期上线。"
    assert eval (ending_route == "startup")
    assert eval (chapter_progress == 6)
    assert eval (side_project_ready)
    assert eval (ability >= 8 and affection >= 15 and money >= 1800)
    assert eval (story_arc == "old")
    assert eval (sequel_route == "" and sequel_chapter_progress == 0)
    advance until eval (main_menu)


testcase full_flow_low_old:
    # Lowest-value route: covers the four "cold" answers and asserts the
    # normal stable ending branch (ability < 7).
    click "旧篇：三个月，留下来"
    advance until screen "choice"
    click "先确认住处和今天的预算。"
    advance until screen "choice"
    click "别提了，烦得要死。"
    advance until screen "choice"
    click "直接给主管发消息，报告数据异常。"
    advance until screen "choice"
    click "被赶走也不怕，大不了换个地方。"
    advance until screen "choice"
    click "这个你比我懂，你定就行。"
    advance until screen "choice"
    click "什么都没说，觉得这没什么。"
    advance until screen "choice"
    click "不用了，我回去还有事。"
    advance until screen "choice"
    click "无所谓，方案能跑通就行。"
    advance until screen "choice"
    click "什么都不说，坐回去继续处理数据。"
    advance until screen "choice"
    click "签下公司的转正通知。"

    advance until "庆祝你顺利转正。"
    assert eval (ending_route == "stable")
    assert eval (chapter_progress == 6)
    assert eval (ability == 5 and affection == -3 and money == 1900)
    assert eval (story_arc == "old")
    advance until eval (main_menu)


testcase full_flow_mid_old:
    # Remaining old options (杂活/观察/发报告/当面说/你请/说了又怎样/希望下次).
    # Ends on the normal rising branch: ability 8 < 9.
    click "旧篇：三个月，留下来"
    advance until screen "choice"
    click "把三个月的目标拆成行动清单。"
    advance until screen "choice"
    click "杂活也得有人干，先干着呗。"
    advance until screen "choice"
    click "直接给主管发消息，报告数据异常。"
    advance until screen "choice"
    click "你一直在观察我？"
    advance until screen "choice"
    click "我把数据报告发你，你先看，明天咱们碰。"
    advance until screen "choice"
    click "当面说：这次多亏你的策划。"
    advance until screen "choice"
    click "你请？那我不客气了。"
    advance until screen "choice"
    click "说了又怎样？主管会信我还是信他？"
    advance until screen "choice"
    click "希望下次你能用自己的方案。"
    advance until screen "choice"
    click "接受另一家公司的 offer。"

    advance until "我暂时不去。不过，你到了那边别松懈。"
    assert eval (ending_route == "rising")
    assert eval (chapter_progress == 6)
    assert eval (ability == 8 and affection == 12 and money == 1900)
    assert eval (not (ability >= 9 and affection >= 12))
    advance until eval (main_menu)


testcase sequel_low_trust_flow:
    # All "keep a distance" answers: no trust, no insight, no resolve. The
    # finale must offer only the return ending (true and character endings
    # gated out).
    click "新篇：樱镜町"
    advance until screen "choice"
    click "先确认住处，避免继续淋雨。"
    advance until screen "choice"
    click "暂时沿用材料中的转学生说法。"
    advance until screen "choice"
    click "先完成报到，等拿到更多权限再查。"
    advance until screen "choice"
    click "直接接过名单，替 Dana 指挥所有人。"
    advance until screen "choice"
    click "把全部记录交给 Dana，由她一个人保管。"
    advance until screen "choice"
    click "离开安全绳，直接冲向更近的三号设备。"
    advance until screen "choice"
    click "立刻上传全部原始资料，让异常引发全镇关注。"
    advance until screen "choice"
    click "当面指出她没有权力替所有人决定。"
    advance until screen "choice"
    click "接受她的安排，先让小镇稳定下来。"
    advance until screen "choice"
    click "承诺无论发生什么，自己都不会忘记她。"
    advance until screen "choice"
    click "抢过钥印，试图代替她成为承载者。"
    advance until screen "choice"

    assert eval (sequel_insight == 0 and sequel_resolve == 0)
    assert eval (dana_affection == 0 and luna_affection == 0 and irene_affection == 0 and ruby_affection == 0)
    # Summer M05 fact: leaving the safety rope aborts the observation.
    assert eval (sequel_luna_observation_outcome == "aborted")
    assert eval (fragment_count() == 4)
    assert eval (not sequel_truth_ready())
    assert eval (v21_choice_captions() == ["回到原来的世界，带走这里真实存在过的证据。"])
    click "回到原来的世界"
    advance until "——返回结局《回到灯火》"
    assert eval (sequel_route == "return")
    advance until eval (main_menu)


testcase sequel_partial_trust_flow:
    # Third options in spring/summer (no trust), full trust in autumn/winter.
    # The finale must offer exactly Irene, Ruby and the return ending.
    click "新篇：樱镜町"
    advance until screen "choice"
    click "逐项核对文件、日期和签名。"
    advance until screen "choice"
    click "坦白自己是被银光带来，身份材料也不是本人办理。"
    advance until screen "choice"
    click "立即与 Luna 核对录入时间、账号和签名。"
    advance until screen "choice"
    click "建议立刻解散活动，所有人各自回家。"
    advance until screen "choice"
    click "由王不稳建立一份唯一的总档案。"
    advance until screen "choice"
    click "立即撤离，放弃全部现场数据。"
    advance until screen "choice"
    click "暂时封锁消息，只让五个人保留记录。"
    advance until screen "choice"
    click "让她把所有经过说完，再逐页核对证据。"
    advance until screen "choice"
    click "拒绝未经本人和众人同意的牺牲。"
    advance until screen "choice"
    click "请她亲手写下名字和意愿，让所有人共同读出。"
    advance until screen "choice"
    click "尊重 Ruby 的决定，与其他三人共同扶住钥印。"
    advance until screen "choice"

    assert eval (sequel_insight == 4 and sequel_resolve == 3)
    assert eval (dana_affection == 0 and luna_affection == 0)
    assert eval (irene_affection == 3 and ruby_affection == 4)
    # Summer M05 fact: immediate evacuation keeps an incomplete offline backup.
    assert eval (sequel_luna_observation_outcome == "evacuated")
    assert eval (not sequel_truth_ready())
    assert eval (v21_choice_captions() == ["留下来，与 Irene 一起重写不再封闭的档案。", "留下来，陪 Ruby 记住每一个冬夜的名字。", "回到原来的世界，带走这里真实存在过的证据。"])
    click "与 Irene 一起重写"
    advance until "——Irene 结局《秋实之书》"
    assert eval (sequel_route == "irene")
    advance until eval (main_menu)


testcase sequel_true_gate_insight_short:
    # Positive gate needs insight >= 6; hold everything else and assert the
    # true option is not even offered.
    $ spring_fragment = True
    $ summer_fragment = True
    $ autumn_fragment = True
    $ winter_fragment = True
    $ dana_affection = 3
    $ luna_affection = 3
    $ irene_affection = 3
    $ ruby_affection = 3
    $ sequel_insight = 5
    $ sequel_resolve = 4
    run Start("sequel_finale")
    advance until screen "choice"
    assert eval (not sequel_truth_ready())
    assert eval ("让整个樱镜町共同记住四季。" not in v21_choice_captions())
    assert eval (len(v21_choice_captions()) == 6 - 1)
    click "回到原来的世界"
    advance until "——返回结局《回到灯火》"
    advance until eval (main_menu)


testcase sequel_true_gate_missing_fragment:
    # Positive gate needs all four fragments; winter is missing here.
    $ spring_fragment = True
    $ summer_fragment = True
    $ autumn_fragment = True
    $ winter_fragment = False
    $ dana_affection = 3
    $ luna_affection = 3
    $ irene_affection = 3
    $ ruby_affection = 3
    $ sequel_insight = 8
    $ sequel_resolve = 6
    run Start("sequel_finale")
    advance until screen "choice"
    assert eval (not sequel_truth_ready())
    assert eval (fragment_count() == 3)
    assert eval ("让整个樱镜町共同记住四季。" not in v21_choice_captions())
    click "回到原来的世界"
    advance until "——返回结局《回到灯火》"
    advance until eval (main_menu)


testcase ui_features_smoke:
    # Rollback / history / auto-forward / skip / save-load reachability.
    click "旧篇：三个月，留下来"
    advance until screen "choice"
    click "把三个月的目标拆成行动清单。"
    assert eval (ability == 3)

    # Rollback returns to the choice interaction and restores the pre-choice
    # state (ability 2), then the choice can be taken again.
    click "回退"
    assert eval (ability == 2)
    assert screen "choice"
    click "把三个月的目标拆成行动清单。"
    assert eval (ability == 3)

    # History lists the line that was just read. config.history_length is 250
    # (game/options.rpy), so the 历史 screen must show the stored dialogue.
    click "历史"
    assert screen "history"
    assert eval (renpy.config.history_length == 250)
    assert eval (any("先把能做的事列清楚" in (h.what or "") for h in _history_list))
    click "返回游戏"
    assert eval (renpy.get_screen("history") is None)

    # Auto-forward is a persistent preference that can be toggled both ways.
    # The quick-menu caption is 自动, but its accessible text comes from the
    # Preference action and is currently the untranslated "Auto forward"
    # (see qa/defects.md, low severity); find_focus matches that text.
    click "Auto forward"
    assert eval (preferences.afm_enable)
    click "Auto forward"
    assert eval (not preferences.afm_enable)

    # Skip runs dialogue until the next menu, stopping on the choice screen.
    # The default preference only skips already-seen text; this is a fresh
    # playthrough, so enable skip_unseen for the check and restore it after.
    $ preferences.skip_unseen = True
    click "快进"
    pause 0.3 until screen "choice"
    $ preferences.skip_unseen = False
    assert eval (chapter_progress == 1)
    assert eval (renpy.get_screen("choice") is not None)
    assert eval (renpy.config.skipping is None)
    run MainMenu(confirm=False)


testcase settings_smoke_main_menu_and_in_game:
    # Main menu -> preferences: both real sliders are rendered with the fixed
    # 28 px track (not the old full-height blank), dragging changes the text
    # speed / auto-forward preferences, and Esc / 返回 close back to the main
    # menu instead of falling through to start.
    assert eval (main_menu)
    assert eval (renpy.get_screen("main_menu") is not None)
    click "系统设置"
    advance until screen "preferences"
    assert eval (main_menu)
    assert eval (renpy.get_screen("main_menu") is None)

    $ _v21_text_rect = v21_pref_slider_rect("text_cps")
    $ _v21_afm_rect = v21_pref_slider_rect("afm_time")
    assert eval (_v21_text_rect[3] == 28 and _v21_afm_rect[3] == 28)
    # The two slider rows must stay adjacent; the native bug inserted ~565 px
    # of blank space between them and clipped the auto-forward control.
    assert eval (0 < _v21_afm_rect[1] - _v21_text_rect[1] < 200)
    assert eval (_v21_afm_rect[1] + _v21_afm_rect[3] <= renpy.config.screen_height)

    $ _v21_saved_text_cps = preferences.text_cps
    $ _v21_saved_afm_time = preferences.afm_time
    # Hover first so the bar is focused before the synthetic button-down;
    # test input posts motion and press in the same frame otherwise.
    move pos v21_pref_slider_point("text_cps", 0.5)
    pause 0.1
    drag pos v21_pref_slider_point("text_cps", 0.5) to pos v21_pref_slider_point("text_cps", 0.2)
    pause 0.1
    assert eval (preferences.text_cps != _v21_saved_text_cps)
    move pos v21_pref_slider_point("afm_time", 0.5)
    pause 0.1
    drag pos v21_pref_slider_point("afm_time", 0.5) to pos v21_pref_slider_point("afm_time", 0.2)
    pause 0.1
    assert eval (preferences.afm_time != _v21_saved_afm_time)

    keysym "K_ESCAPE"
    pause 0.3 until screen "main_menu"
    assert eval (renpy.get_screen("preferences") is None)
    assert eval (main_menu)
    assert eval (not renpy.get_screen("say") and not renpy.get_screen("choice"))

    # The visible 返回 control in the main-menu game menu takes the same exit.
    click "系统设置"
    advance until screen "preferences"
    click "返回"
    pause 0.3 until screen "main_menu"
    assert eval (main_menu and renpy.get_screen("preferences") is None)

    # In-game preferences must return to the exact saved statement, not start
    # a new game or reset the progress just made.
    click "旧篇：三个月，留下来"
    advance until screen "choice"
    click "把三个月的目标拆成行动清单。"
    assert eval (story_arc == "old" and ability == 3)
    $ _v21_progress_node = renpy.game.context().current
    $ _v21_progress_chapter = chapter_progress
    $ _v21_progress_ability = ability

    click "设置"
    advance until screen "preferences"
    assert eval (not main_menu)
    assert eval (v21_pref_slider_rect("text_cps")[3] == 28)

    keysym "K_ESCAPE"
    pause 0.3 until screen "say"
    assert eval (renpy.get_screen("preferences") is None)
    assert eval (not main_menu)
    assert eval (renpy.get_screen("choice") is None)
    assert eval (renpy.game.context().current == _v21_progress_node)
    assert eval (chapter_progress == _v21_progress_chapter)
    assert eval (ability == _v21_progress_ability)

    $ preferences.text_cps = _v21_saved_text_cps
    $ preferences.afm_time = _v21_saved_afm_time
    run MainMenu(confirm=False)


testcase old_chapter_02_public_evidence:
    # Covers the remaining "公开指出问题" chapter-2 option: it raises evidence
    # immediately but with a smaller affection gain than the private report.
    click "旧篇：三个月，留下来"
    advance until screen "choice"
    click "把三个月的目标拆成行动清单。"
    advance until screen "choice"
    click "没事，我正好趁这个机会看看公司的数据。"
    advance until screen "choice"
    click "发到工作群里公开指出问题。"
    assert eval (chapter_progress == 2)
    assert eval (ability == 5 and affection == 4)
    assert eval (evidence_ready)
    run MainMenu(confirm=False)


testcase history_panel_visible_text:
    # Regression for the native 2.1 history panel that stayed blank while
    # _history_list had entries (tech/history-native-fix.md): the vertical
    # scrollbar was measured at the full `side` width, so the dialogue column
    # shrank to 0 and nothing was drawn. This drives the real 历史 screen and
    # inspects the live side()/viewport geometry plus the Layout the history
    # Text was rendered with; a string only present in _history_list is not
    # enough.
    click "旧篇：三个月，留下来"
    advance until screen "choice"
    click "把三个月的目标拆成行动清单。"
    assert eval (ability == 3)
    # Passive wait: `advance until` would click and could skip the very line
    # this test needs in the history. The say is up once its history entry is
    # recorded, and it is the last entry at this point in the prologue.
    pause 0.2 until eval (any("先把能做的事列清楚" in (h.what or "") for h in _history_list)) timeout 10.0
    assert screen "say" timeout 2.0
    assert eval (any("先把能做的事列清楚" in (h.what or "") for h in _history_list))

    click "历史"
    assert screen "history"
    pause 0.2 until eval (v21_history_metrics("先把能做的事列清楚") is not None) timeout 10.0
    $ _v21_history_bar_width, _v21_history_center_width, _v21_history_text_width, _v21_history_text_height = v21_history_metrics("先把能做的事列清楚")

    # vscrollbar_xsize 18 keeps the bar a narrow track; the full 1160 px frame
    # used to be handed to it instead and pushed the centre column to zero.
    assert eval (0 < _v21_history_bar_width <= 64)
    assert eval (_v21_history_center_width >= 900)
    # The stored line must be laid out at real text width and height inside the
    # live panel (about 400 px at gui.text_size 34), not a zero-width column.
    assert eval (_v21_history_text_width >= 200)
    assert eval (0 < _v21_history_text_height <= 400)

    click "返回游戏"
    assert eval (renpy.get_screen("history") is None)
    run MainMenu(confirm=False)


testcase auto_forward_advances_by_default:
    # Regression for the v2.1 default that read `afm_time` (SDK name) while the
    # game set a misspelled field: afm_enable could be switched on, but the
    # SayBehavior delay stayed 0 (renpy/display/behavior.py: SayBehavior.event),
    # so nothing advanced. This asserts a positive default and then a real
    # advance to the next line with no further input.
    assert eval (preferences.afm_time > 0)

    # Keep the wait dominated by afm_time, not by the typewriter: instant text
    # removes Text.get_time() from the SayBehavior delay. Auto-forward starts
    # off so the toggle below is the only thing that enables it. All three
    # preferences are restored at the end and none of them is game progress.
    $ _v21_saved_text_cps = preferences.text_cps
    $ _v21_saved_afm_enable = preferences.afm_enable
    $ preferences.text_cps = 0
    $ preferences.afm_enable = False

    click "旧篇：三个月，留下来"
    advance until screen "choice"
    click "把三个月的目标拆成行动清单。"
    assert eval (ability == 3)
    # Passive wait for the say (an `advance until` here could skip it).
    pause 0.2 until eval (any("先把能做的事列清楚" in (h.what or "") for h in _history_list)) timeout 10.0
    assert screen "say" timeout 2.0

    $ _v21_afm_node = id(renpy.game.context().current)
    $ _v21_afm_history = len(_history_list)

    # Real quick-menu control (caption 自动, Preference alt text "Auto forward").
    # Hover first so the button owns the focus before the synthetic press; a
    # click while the say is focused would dismiss the line and, with
    # using_afm_enable, switch auto-forward back off in SayBehavior.event.
    move "Auto forward"
    pause 0.1
    click "Auto forward"
    assert eval (preferences.afm_enable)

    # No further input from here on: the next line must arrive by itself.
    pause 0.2 until eval (len(_history_list) > _v21_afm_history) timeout 25.0

    assert screen "say" timeout 2.0
    assert eval (id(renpy.game.context().current) != _v21_afm_node)
    assert eval (len(_history_list) == _v21_afm_history + 1)
    assert eval ("楼道里的感应灯坏了三盏" in (_history_list[-1].what or ""))
    assert eval (preferences.afm_enable)
    assert eval (renpy.config.skipping is None)

    $ preferences.afm_enable = False
    $ preferences.text_cps = _v21_saved_text_cps
    $ preferences.afm_enable = _v21_saved_afm_enable
    run MainMenu(confirm=False)


testcase v21_label_traversal_audit:
    # Runs last in `global`: every v2.1 insert must have been reached by real
    # play in this run (not by calling the label directly).
    $ v21_audit_labels()
    assert eval (True)


# ===========================================================================
# 2.0 compatibility fixtures (capture only; not part of `global`)
#
# These testcases are run on the frozen 2.0 baseline to produce the save files
# stored in the main repository at .work/v21/compat-v20. Each one reaches the
# target menu through the real main-menu entry and real choices (no Start()
# shortcuts, no pre-set variables), then writes slot 1 of page 1 and dumps the
# store state next to it. tools/v21_capture_fixtures.py runs them under the
# shared GUI lock with an isolated saves root.
# ===========================================================================

testsuite fixtures:
    enabled False

    before testcase:
        $ _test.transition_timeout = 0.02
        $ _test.timeout = 60.0

    teardown:
        $ renpy.save_persistent()
        exit


    testcase capture_v20_old_chapter01_menu:
        click "旧篇：三个月，留下来"
        advance until screen "choice"
        click "把三个月的目标拆成行动清单。"
        assert eval (ability == 3)
        advance until screen "choice"
        assert eval (chapter_progress == 1 and money == 1100 and affection == 0)

        run FileSave(1, confirm=False, page="1")
        pause 0.3
        $ v21_capture_state("v20_old_chapter01_menu")
        run MainMenu(confirm=False)


    testcase capture_v20_old_chapter06_menu:
        click "旧篇：三个月，留下来"
        advance until screen "choice"
        click "把三个月的目标拆成行动清单。"
        advance until screen "choice"
        click "没事，我正好趁这个机会看看公司的数据。"
        advance until screen "choice"
        click "先自己跑一遍完整数据验证，确认后再汇报。"
        advance until screen "choice"
        click "才第四天，急什么。"
        advance until screen "choice"
        click "要不现在就去公司跑一遍数据？"
        advance until screen "choice"
        click "会后悄悄给她买一杯咖啡放在桌上。"
        advance until screen "choice"
        click "还是 AA 吧，我现在不富裕。"
        advance until screen "choice"
        click "不是不说，是时候没到。我已经保留了所有的原始文件和时间记录。"
        advance until screen "choice"
        click "我不介意功劳被分，但方案不能出错。下次有问题直接找我。"
        advance until screen "choice"
        assert eval (chapter_progress == 6 and ability == 13 and affection == 27 and money == 1832)

        run FileSave(1, confirm=False, page="1")
        pause 0.3
        $ v21_capture_state("v20_old_chapter06_menu")
        run MainMenu(confirm=False)


    testcase capture_v20_sequel_first_menu:
        click "新篇：樱镜町"
        advance until screen "choice"
        assert eval (story_arc == "sequel")
        assert eval (sequel_insight == 0 and dana_affection == 0 and luna_affection == 0)
        assert eval (irene_affection == 0 and ruby_affection == 0 and sequel_origin_ending == "unknown")

        run FileSave(1, confirm=False, page="1")
        pause 0.3
        $ v21_capture_state("v20_sequel_first_menu")
        run MainMenu(confirm=False)


    testcase capture_v20_sequel_finale_menu:
        click "新篇：樱镜町"
        advance until screen "choice"
        click "逐项核对文件、日期和签名。"
        advance until screen "choice"
        click "坦白自己是被银光带来，身份材料也不是本人办理。"
        advance until screen "choice"
        click "立即与 Luna 核对录入时间、账号和签名。"
        advance until screen "choice"
        click "先问 Dana 需要什么，再按她的方案分工。"
        advance until screen "choice"
        click "让每位见证者各自保存一小段，再互相核对。"
        advance until screen "choice"
        click "执行 Luna 的分组方案，带回二号点原始纸带。"
        advance until screen "choice"
        click "公开可复核证据，并邀请见证者补充各自记录。"
        advance until screen "choice"
        click "让她把所有经过说完，再逐页核对证据。"
        advance until screen "choice"
        click "拒绝未经本人和众人同意的牺牲。"
        advance until screen "choice"
        click "请她亲手写下名字和意愿，让所有人共同读出。"
        advance until screen "choice"
        click "尊重 Ruby 的决定，与其他三人共同扶住钥印。"
        advance until screen "choice"
        assert eval (sequel_chapter_progress == 6 and fragment_count() == 4)
        assert eval (sequel_truth_ready())

        run FileSave(1, confirm=False, page="1")
        pause 0.3
        $ v21_capture_state("v20_sequel_finale_menu")
        run MainMenu(confirm=False)


# ===========================================================================
# 2.0 save compatibility acceptance (run by tools/v21_compat_check.py)
#
# Each testcase loads a fixture from .work/v21/compat-v20 into an isolated
# saves root, re-enters the saved menu and re-asserts the state recorded at
# capture time. On 2.1 the same testcases must pass unchanged: old values are
# preserved, the saved menu is still reachable, and inserted content must not
# change these numbers. New 2.1 variables are only allowed to appear with
# their `default` values (checked for sequel_luna_observation_outcome).
# ===========================================================================

testsuite compat:
    enabled False

    before testcase:
        $ _test.transition_timeout = 0.02
        $ _test.timeout = 60.0

    teardown:
        $ renpy.save_persistent()
        exit


    testcase compat_v20_old_chapter01_menu:
        run FileLoad(1, confirm=False, page="1")
        advance until screen "choice"
        assert eval (story_arc == "old")
        assert eval (chapter_progress == 1 and ability == 3 and money == 1100 and affection == 0)
        assert eval (ending_route == "")
        assert eval (sequel_chapter_progress == 0 and sequel_insight == 0 and sequel_resolve == 0)
        assert eval (getattr(renpy.store, "sequel_luna_observation_outcome", "unknown") == "unknown")
        $ v21_capture_state("compat_v20_old_chapter01_menu")
        run MainMenu(confirm=False)


    testcase compat_v20_old_chapter06_menu:
        run FileLoad(1, confirm=False, page="1")
        advance until screen "choice"
        assert eval (story_arc == "old")
        assert eval (chapter_progress == 6 and ability == 13 and affection == 27 and money == 1832)
        assert eval (side_project_ready and evidence_ready)
        assert eval (v21_choice_captions() == ["签下公司的转正通知。", "接受另一家公司的 offer。", "拿起自己的项目企划书。"])
        $ v21_capture_state("compat_v20_old_chapter06_menu")
        run MainMenu(confirm=False)


    testcase compat_v20_sequel_first_menu:
        run FileLoad(1, confirm=False, page="1")
        advance until screen "choice"
        assert eval (story_arc == "sequel")
        assert eval (sequel_chapter_progress == 0)
        assert eval (sequel_insight == 0 and sequel_resolve == 0 and sequel_route == "")
        assert eval (dana_affection == 0 and luna_affection == 0 and irene_affection == 0 and ruby_affection == 0)
        assert eval (fragment_count() == 0)
        assert eval (getattr(renpy.store, "sequel_luna_observation_outcome", "unknown") == "unknown")
        $ v21_capture_state("compat_v20_sequel_first_menu")
        run MainMenu(confirm=False)


    testcase compat_v20_sequel_finale_menu:
        run FileLoad(1, confirm=False, page="1")
        advance until screen "choice"
        assert eval (story_arc == "sequel")
        assert eval (sequel_chapter_progress == 6)
        assert eval (fragment_count() == 4 and sequel_insight == 6 and sequel_resolve == 5)
        assert eval (dana_affection == 3 and luna_affection == 3 and irene_affection == 3 and ruby_affection == 4)
        assert eval (sequel_truth_ready())
        assert eval (len(v21_choice_captions()) == 6)
        assert eval ("让整个樱镜町共同记住四季。" in v21_choice_captions())
        $ v21_capture_state("compat_v20_sequel_finale_menu")
        run MainMenu(confirm=False)
