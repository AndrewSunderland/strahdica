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
        background misty_forest
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
                            Jump("scene_1_start")
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