default affection = 0
default ability = 2
default money = 2300
default chapter_progress = 0
default ending_route = ""
default evidence_ready = False
default side_project_ready = False

default story_arc = "old"
default sequel_chapter_progress = 0
default sequel_route = ""
default sequel_origin_ending = "unknown"
default ruby_affection = 0
default dana_affection = 0
default luna_affection = 0
default irene_affection = 0
default sequel_insight = 0
default sequel_resolve = 0
default spring_fragment = False
default summer_fragment = False
default autumn_fragment = False
default winter_fragment = False

default persistent.old_ending_route = None
default persistent.old_endings_seen = []

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

    def fragment_count():
        return sum((
            spring_fragment,
            summer_fragment,
            autumn_fragment,
            winter_fragment,
        ))

    def sequel_truth_ready():
        return (
            spring_fragment
            and summer_fragment
            and autumn_fragment
            and winter_fragment
            and sequel_insight >= 6
            and sequel_resolve >= 4
            and ruby_affection >= 3
            and dana_affection >= 3
            and luna_affection >= 3
            and irene_affection >= 3
        )
