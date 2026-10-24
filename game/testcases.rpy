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
