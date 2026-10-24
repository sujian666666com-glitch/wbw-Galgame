init offset = -2

init python:
    gui.init(1920, 1080)

define config.check_conflicting_properties = True

define gui.text_font = "fonts/SourceHanSansLite.ttf"
define gui.name_text_font = "fonts/SourceHanSansLite.ttf"
define gui.interface_text_font = "fonts/SourceHanSansLite.ttf"

define gui.text_size = 34
define gui.name_text_size = 38
define gui.interface_text_size = 30
define gui.label_text_size = 40
define gui.title_text_size = 72

define gui.accent_color = "#e6b7da"
define gui.idle_color = "#d8d8e8"
define gui.idle_small_color = "#b8b8c8"
define gui.hover_color = "#ffffff"
define gui.selected_color = "#f4cfe8"
define gui.insensitive_color = "#88889988"
define gui.muted_color = "#5e5574"
define gui.hover_muted_color = "#81769b"
define gui.text_color = "#ffffff"
define gui.interface_text_color = "#ffffff"

define gui.main_menu_background = "images/backgrounds/bg_main_menu_cover_wide.jpg"
define gui.game_menu_background = Solid("#171625ee")

define gui.dialogue_xpos = 330
define gui.dialogue_ypos = 840
define gui.dialogue_width = 1260
define gui.dialogue_text_xalign = 0.0

define gui.name_xpos = 350
define gui.name_ypos = 780
define gui.name_xalign = 0.0
define gui.namebox_width = 330
define gui.namebox_height = 72

define gui.choice_button_width = 1050
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(28, 18, 28, 18)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = 32
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = "#eeeeff"
define gui.choice_button_text_hover_color = "#ffffff"

define gui.button_text_font = gui.interface_text_font
define gui.button_text_size = gui.interface_text_size
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color
define gui.button_text_xalign = 0.5
