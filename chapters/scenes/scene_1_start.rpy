label scene_1_start:
    scene expression interior_entrance_day

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "strahd happy.png" to the images
    # directory.

    show strahd base at Transform(xalign=1.0, yalign=0.5, zoom=0.70)

    # These display lines of dialogue.

    strahd_char "I am Strahd blah blah blah."

    show expression "{} base".format(player_prefix) at Transform(xalign=0.0, yalign=0.5, zoom=1.5)
    player_char "Hello Strahd, I am [player_char.name]."

    show strahd happy at Transform(xalign=1.0, yalign=0.5, zoom=0.70)

    strahd_char "How dare you make me angry! I'll rip your arm off!"

    show strahd neutral at Transform(xalign=0.5, yalign=0.5, zoom=2.5)

    strahd_char "I'm sorry. Please don't be angry."

    menu: 
        "How do you respond?"
        "Wtf man my arm!":
            show strahd angry at Transform(xalign=0.5, yalign=0.5, zoom=2.5)
            strahd_char "How dare you! I kill you now!"
            jump bad_end
        "Oh yes thank you for my lesson":
            show strahd happy at Transform(xalign=0.5, yalign=0.5, zoom=2.5)
            strahd_char "That's good lets fuck now!"
            jump good_end

label bad_end:
    scene black
    show text "You have made a grave mistake. Strahd kills you." at truecenter with dissolve
    pause 2
    return

label good_end:
    scene black
    show text "Strahd fucks you silly and you die." at truecenter with dissolve
    pause 2
    return
    # This ends the game.

    return
