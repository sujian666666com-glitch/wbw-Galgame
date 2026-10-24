label prologue:
    $ chapter_progress = 0
    $ notify_change("章节进度：序章")

    scene bg subway_exit_rain with fade
    show wangbuwen normal

    narrator "大城市地铁站出口，雨后傍晚，地面湿漉漉的，霓虹灯倒映在水洼里。"
    narrator "王不稳拖着行李箱走出地铁站。口袋里只剩 2300 块。"
    narrator "电话响起。"
    narrator "电话里的亲戚说：小王啊，你一个普通学校的，别太挑了，有班上就不错了，知道吧？"
    wbw "……我知道。"
    narrator "挂掉电话，王不稳看着远处高楼的灯光，打开手机备忘录，打下一行字——三个月，留下来。"

    scene cg subway_meeting with dissolve
    show xuwanqing normal
    xw "目标写得挺狠，就是字有点丑。"
    wbw "……"
    narrator "王不稳回头——一个撑着伞的女生站在旁边，长发被雨雾染上一层湿意，正低头看着他的手机屏幕。"
    wbw "你谁啊？"
    xw "和你一样，刚到这儿的人。"
    narrator "她收了伞，甩了甩水，转身走了。风衣下摆扫过水洼，带起一点细碎的光。"
    hide xuwanqing

    $ notify_change("许晚晴好感度 +0")

    menu:
        "面对这个陌生城市，王不稳决定先做什么？"

        "把三个月的目标拆成行动清单。":
            $ ability += 1
            $ notify_change("能力 +1")
            show wangbuwen confident
            wbw "先把能做的事列清楚。"

        "先确认住处和今天的预算。":
            $ notify_change("资金保持不变")
            wbw "先安顿下来，别乱花钱。"

    call v21_prologue

    jump chapter_01
