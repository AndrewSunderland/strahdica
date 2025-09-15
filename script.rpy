# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define strahd_char = Character("Strahd", color="#f52916")

# player characters
define corin_char = Character("Corin", color="#067e1c")
define bridget_char = Character("Bridget", color="#21b7e9")
define jacira_char = Character("Jacira", color="#8f8f07")
define kokali_char = Character("Kokali", color="#be05be")
define taniel_char = Character("Taniel", color="#902206")

default player_char = None
default player_prefix = None
default hovered_character = None


init python:
    interior_entrance_day = "backgrounds/interior_entrance_day.png"
    mansion_front_nightd = "backgrounds/mansion_front_nightd.png"
    char_descriptions = {
        "corin": "Corin - A precious human ranger boy who loves to bake. He is looking for his teacher who taught him how to fight monsters.",
        "bridget": "Bridget - A witty gnome bard with a talent for storytelling. She left her kids behind to go on an adventure of self-discovery.",
        "jacira": "Jacira - A young dusk elf warlock with a dark past. She is trying to escape her cultlike upbringing and find her own path.",
        "kokali": "Kokali - A wise elf warlock. They seek knowledge and reading but want to escape their pact with an abusive ex.",
        "taniel": "Taniel - A charming dhampir rogue. He is trying to discover his origins as half vampire and half vistani.",
    }

# style char_desc_frame:
#     background Solid("#00000080")
#     padding (20, 12, 20, 16)
#     xfill True

# style char_desc_text:
#     color "#FFFFFF"
#     size 24
#     line_spacing 2
# New styles that reuse the game's dialogue look.
style char_desc_window is window
    # Optional tweaks (uncomment to adjust):
    # padding (30, 15, 30, 18)
    # background Frame("gui/window.png", 40, 40)  # Already default in most themes
    

style char_desc_text is say_dialogue
    # Optional: make slightly smaller than dialogue
    # size 34


transform thumb_base:
    zoom 0.25
    alpha 1.0
    on hover:
        # Bounce style: grow, slight shrink, settle
        ease 0.14 zoom 0.34
        ease 0.08 zoom 0.33
    on idle:
        ease 0.18 zoom 0.25

transform thumb_dim:
    zoom 0.25
    alpha 0.45
    on hover:
        ease 0.14 zoom 0.34 alpha 1.0
        ease 0.08 zoom 0.33
    on idle:
        ease 0.18 zoom 0.25 alpha 0.45


screen character_select:
    default characters = [
        ("corin", "PCs/Corin/corin base.png", corin_char),
        ("bridget", "PCs/Bridget/bridget base.png", bridget_char),
        ("jacira", "PCs/Jacira/jacira base.png", jacira_char),
        ("kokali", "PCs/Kokali/kokali base.png", kokali_char),
        ("taniel", "PCs/Taniel/taniel base.png", taniel_char),
    ]
    tag menu
    
    # Fullscreen container
    frame:
        background mansion_front_nightd
        xfill True
        yfill True

        # Character row (centered)
        hbox:
            spacing 40
            pos (0.5, 0.5)
            anchor (0.5, 0.5)

            for name, img, char in characters:
                $ use_dim = (hovered_character is not None and hovered_character != name)
                $ current_tf = thumb_dim if use_dim else thumb_base
                
                fixed:
                    xsize 330
                    ysize 510

                    imagebutton:
                        idle im.Scale(img, 1024, 1536)
                        hover im.Scale(img, 1024, 1536)
                        at current_tf
                        xpos 0.5
                        xanchor 0.5
                        ypos 0.5
                        yanchor 0.5
                        focus_mask True
                        action [
                            SetVariable("player_char", char),
                            SetVariable("player_prefix", name),
                            Jump("after_select")
                        ]
                        hovered SetVariable("hovered_character", name)
                        unhovered SetVariable("hovered_character", None)

        # Description box using dialogue window styling
        window:
            style "char_desc_window"
            xfill True
            ypos 1.0
            yanchor 1.0
            text char_descriptions.get(
                hovered_character,
                "Hover over a character to see their description."
            ) style "char_desc_text"  
    use quick_menu

            

# The game starts here.

label start:

    call screen character_select

label after_select:
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
