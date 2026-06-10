default affection = 0
default ability = 2
default money = 2300
default chapter_progress = 0
default ending_route = ""
default evidence_ready = False
default side_project_ready = False

init python:
    def notify_change(message):
        renpy.notify(message)

    def affection_level():
        if affection >= 15:
            return "彼此信任"
        if affection >= 8:
            return "逐渐靠近"
        if affection >= 3:
            return "初步了解"
        return "保持距离"
