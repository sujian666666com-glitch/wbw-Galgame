# v2.1 固定资源。九张文件稍后生成，此处只声明路径，不放占位图。
# 立绘站位沿用 game/core/images.rpy 里对应 normal。
# 时段变体只对已有背景做 TintMatrix / BrightnessMatrix，不改旧文件。

image dana worried:
    "images/v21/characters/dana_worried.png"
    xalign 0.34
    yalign 1.0

image luna soft:
    "images/v21/characters/luna_soft.png"
    xalign 0.50
    yalign 1.0

image irene shaken:
    "images/v21/characters/irene_shaken.png"
    xalign 0.66
    yalign 1.0

image irene relieved:
    "images/v21/characters/irene_relieved.png"
    xalign 0.66
    yalign 1.0

image ruby resolute:
    "images/v21/characters/ruby_resolute.png"
    xalign 0.84
    yalign 1.0

image bg v21_train_interior_dusk = "images/v21/backgrounds/bg_train_interior_dusk.png"
image bg v21_old_house_mirror = "images/v21/backgrounds/bg_old_house_mirror.png"
image cg v21_xuwanqing_rain_close = "images/v21/cg/cg_xuwanqing_rain_close.png"
image cg v21_ruby_ending_kiss = "images/v21/cg/cg_ruby_ending_kiss.png"

image bg v21_time_company_street_rain:
    "bg company_street_night"
    matrixcolor TintMatrix("#b7c6d8") * BrightnessMatrix(-0.06)

image bg v21_time_company_street_dusk:
    "bg company_street_night"
    matrixcolor TintMatrix("#ffc49a") * BrightnessMatrix(0.12)

image bg v21_time_startup_morning:
    "bg startup_studio"
    matrixcolor TintMatrix("#ffe4c2") * BrightnessMatrix(0.10)

image bg v21_time_spring_garden_evening:
    "bg spring_garden"
    matrixcolor TintMatrix("#e09a62") * BrightnessMatrix(-0.16)

image bg v21_time_archive_evening:
    "bg archive_autumn"
    matrixcolor TintMatrix("#e7b07a") * BrightnessMatrix(-0.08)

image bg v21_time_archive_night:
    "bg archive_autumn"
    matrixcolor TintMatrix("#8d97b8") * BrightnessMatrix(-0.24)

image bg v21_time_lighthouse_dawn:
    "bg lighthouse_night"
    matrixcolor TintMatrix("#ffd0b0") * BrightnessMatrix(0.28)

image bg v21_time_station_first_snow:
    "bg sakurakagami_station_winter"
    matrixcolor TintMatrix("#d7e6f6") * BrightnessMatrix(0.08)

image bg v21_time_station_boundary:
    "bg sakurakagami_station_rain"
    matrixcolor TintMatrix("#e4d4ef") * BrightnessMatrix(0.04)
