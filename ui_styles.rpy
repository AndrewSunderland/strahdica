# Dialogue, namebox, description alignment
style window is default:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Frame("gui/window_base.png", 48, 48)
    xpadding 54
    ypadding 36
    bottom_padding 140

style say_dialogue is default:
    size 26
    color "#D8C9B0"
    line_spacing 2
    outlines [(2, "#00000080", 0, 0)]

style say_label is default:
    size 32
    color "#C48A32"
    bold True
    outlines [(2, "#000000AA", 0, 0)]

style namebox is default:
    background Frame("gui/namebox.png", 24, 24)
    padding (22, 10, 22, 12)

style char_desc_window is window
style char_desc_text is say_dialogue:
    size 26

style choice_vbox:
    spacing 12
    xalign 0.5
    # y alignment handled in screen

# Compact choice styles
style menu_caption is default:
    properties gui.text_properties("dialogue")
    size 28
    color "#D8C9B0"
    outlines [(2, "#00000080", 0, 0)]
    xalign 0.0
    xsize gui.dialogue_width

style choice_button is default:
    # smaller visuals: reduce padding and height
    background Frame("gui/choice_idle.png", 18, 18)
    hover_background Frame("gui/choice_hover.png", 18, 18)
    xmaximum gui.dialogue_width
    yminimum 36
    padding (15, 5, 15, 5)

style choice_button_text is default:
    size 26
    color "#EDE0C9"
    outlines [(2, "#000000AA", 0, 0)]
# ...existing code...



# Quick menu styles
style quick_button:
    background Solid("#2A0E1250")
    hover_background Solid("#5C1A1F90")
    padding (20, 12, 20, 14)
    yoffset -6

style quick_button_text:
    size 24
    color "#C9B99F"
    hover_color "#F2E6D2"
    selected_color "#C48A32"
    
# Main menu styles
style mm_root_frame:
    background None
    xfill True
    yfill True
    padding (0, 0, 0, 0)

style mm_vbox:
    spacing 18
    xalign 0.02
    yalign 0.55

style mm_button:
    background Frame("gui/choice_idle.png", 28, 28)
    hover_background Frame("gui/choice_hover.png", 28, 28)
    padding (36, 18, 36, 20)
    xminimum 380

style mm_button_text:
    size 34
    color "#C9B99F"
    hover_color "#F2E6D2"
    selected_color "#C48A32"
    outlines [(2, "#000000AA", 0, 0)]


# Title text style (replace logo image with text)
style logo_text is default:
    font "gui/fonts/EBGaramond-Regular.ttf"
    size 96
    color "#F2E6D2"
    outlines [(4, "#000000CC", 0, 0)]
    xalign 0.5

# Small "drip" glyph style (we use repeated vertical bars as drops)
style drip_text is default:
    font "gui/fonts/AtkinsonHyperlegible-Regular.ttf"
    size 36
    color "#8A0B0B"             # blood color
    outlines [(2, "#2A0E12AA", 0, 0)]
    antialias True