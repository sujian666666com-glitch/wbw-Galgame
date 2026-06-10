testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.02
        $ _test.timeout = 8.0

        if eval (not main_menu):
            run MainMenu(confirm=False)

    teardown:
        exit


testcase full_flow_stable_ideal:
    click "开始游戏"

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

    assert eval (ending_route == "stable")
    assert eval (chapter_progress == 6)
    assert eval (ability >= 7 and affection >= 15)
    advance until "你终于开窍了。"
    advance until eval (main_menu)


testcase rising_ideal:
    $ ability = 9
    $ affection = 12
    run Start("chapter_06")
    advance until screen "choice"
    click "接受另一家公司的 offer。"
    assert eval (ending_route == "rising")
    advance until "你以为就你有野心？走吧，一起。"
    advance until eval (main_menu)


testcase startup_ideal:
    $ ability = 8
    $ affection = 15
    $ money = 1800
    $ side_project_ready = True
    run Start("chapter_06")
    advance until screen "choice"
    click "拿起自己的项目企划书。"
    assert eval (ending_route == "startup")
    advance until "他们的第一个版本如期上线。"
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
    click "开始游戏"
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
    exit
