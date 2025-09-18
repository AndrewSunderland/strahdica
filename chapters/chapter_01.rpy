label chapter_01:
    # Order the scenes for this chapter.
    call screen character_select    # call selection screen (will Jump to scene_1_start on selection)
    # If you prefer selection only once, replace with calls to scenes directly:
    call chapter_01_scene_01
    call chapter_01_scene_02
    # call scene_2_start
    return