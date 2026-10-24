label start:
    jump sequel_start


label original_story_start:
    $ story_arc = "old"
    jump prologue


label sequel_start:
    $ story_arc = "sequel"
    $ sequel_origin_ending = persistent.old_ending_route or "unknown"
    jump sequel_prologue
