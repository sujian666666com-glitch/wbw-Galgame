label chapter_05:
    $ chapter_progress = 5
    $ notify_change("章节进度：第五章")

    scene bg office with fade

    narrator "办公区气氛凝重。公司最重要的一个客户项目出了问题，方案执行偏差太大，客户直接投诉。"

    wl "怎么回事？谁负责的？"

    zh "这个……数据那边好像有点问题……"

    narrator "所有人开始互相推卸。张浩把矛头指向数据组，数据组指向策划，策划指向执行。"
    narrator "会议陷入僵局，没人能拿出解决方案。王不稳站了起来。"

    wbw "我有一个方案。"

    narrator "所有人看着他。"

    wbw "我重新跑了一遍数据，问题出在投放策略和用户画像的偏差上。我准备了一套修正方案，预估能在三天内挽回流失。"

    narrator "他打开电脑，把完整的分析报告投到屏幕上。数据清晰，逻辑完整，每一步都有依据。"

    wl "这个……你什么时候做的？"

    wbw "之前做活动的时候，顺便把整个客户项目的数据也过了一遍。"

    zh "你——"

    narrator "张浩刚想说什么，许晚晴站了起来。"

    xw "我补充一下。这次活动方案的原始版本，包括客户项目的数据优化思路，最早的文件记录都在这里——"

    narrator "她把一组文件记录投到屏幕上。时间戳、修改记录、原始作者，全部指向王不稳。"

    xw "谁做的，记录写得很清楚。"

    narrator "会议室安静了几秒。王磊的脸色很复杂。张浩低下了头。"

    if evidence_ready:
        narrator "完整的证据链让这次翻盘再没有争辩的余地。"

    $ ability += 2
    $ money += 800
    $ notify_change("能力 +2")
    $ notify_change("项目奖金 +800")

    menu:
        "我不介意功劳被分，但方案不能出错。下次有问题直接找我。":
            $ affection += 4
            $ ability += 1
            $ notify_change("许晚晴好感度 +4")
            $ notify_change("能力 +1")

            narrator "许晚晴看着王不稳。这个时候，他仍然保持着风度。"

        "什么都不说，坐回去继续处理数据。":
            $ affection += 2
            $ notify_change("许晚晴好感度 +2")

            narrator "许晚晴看着他的背影，没说话。"

        "希望下次你能用自己的方案。":
            $ affection += 3
            $ notify_change("许晚晴好感度 +3")

            narrator "张浩脸色铁青，会议室气氛更紧张了。"

    scene bg rooftop_sunset with dissolve

    xw "你早就准备好了。"

    wbw "准备了，但不确定什么时候能用上。"

    xw "你真的很能忍。"

    wbw "不是忍，是等。忍是憋着，等是有计划的。"

    xw "……你这个人，真的挺可怕的。"

    wbw "可怕？"

    xw "可怕的好。"

    narrator "风吹过来，吹乱了她的头发。她伸手别了一下，看着远处的天际线。"

    xw "王不稳。"

    wbw "嗯？"

    xw "三个月的期限，快到了。"

    wbw "嗯。"

    xw "留下来了吗？"

    wbw "还在选。"

    call v21_chapter_05

    jump chapter_06
