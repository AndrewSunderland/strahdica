# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define strahd_char = Character("Strahd", color="#f52916")
define anastrasius_char = Character("Anastrasius", color="#470202")
define escher_char = Character("Escher", color="#959193")
define ludmilla_char = Character("Ludmilla", color="#f0b411")
define volenta_char = Character("Volenta", color="#20c120")

# player characters
define corin_char = Character("Corin", color="#067e1c")
define bridget_char = Character("Bridget", color="#e921d5")
define jacira_char = Character("Jacira", color="#f4f410")
define kokali_char = Character("Kokali", color="#059fbe")
define taniel_char = Character("Taniel", color="#f5bb9a")

default player_char = None
default player_prefix = None
default hovered_character = None


init -4 python:
    # Locations:
    interior_entrance_day = "backgrounds/interior_entrance_day.png"
    mansion_front_nightd = "backgrounds/mansion_front_nightd.png"
    misty_forest = "Locations/MistyForest.jpg"
    
    # Character sprites:
    char_descriptions = {
        "corin": "Corin was raised as a baker's son but was cast out at twelve " +
            "after a youthful mistake. His village was later attacked by a wendigo " + 
            "and he was saved by the monster hunter Ezmerelda, who trained him to " + 
            "fight and raised him. After her mysterious disappearance at seventeen, " + 
            "Corin worked at Bev and Bab's in Waterdeep to regain his footing. At " + 
            "nineteen he leaves the bakery to find Ezmerelda and prove himself.",
        "bridget": "Bridget had dreams of traveling the world as a great bard, " + 
            "but they were cut short by an unexpected pregnancy and whirlwind " + 
            "marriage in her youth.  Now she has six kids and a husband who has " + 
            "abandoned her to raise them on her own.  Looking for a fresh start " + 
            "and some much-needed relaxation, Bridget heads off on a trip with her " + 
            "friend Kokali.",
        "jacira": "Jacira - A young dusk elf warlock with a dark past. She is trying to escape her cultlike upbringing and find her own path.",
        "kokali": "Kokali was raised in the feywilds but left when a suitor, named " + 
            "Kuzco, drew him in with a promise of a library of their desires.  He " + 
            "failed to be a dutiful husband and courtier when he saw how terrible " + 
            "his husband treated his people. Kokali left at the age of 125 with " + 
            "only a parting gift of warlock patronage and a desire to be better.",
        "taniel": "Taniel - A charming dhampir rogue. He is trying to discover his origins as half vampire and half vistani.",
    }

# New styles that reuse the game's dialogue look.
style char_desc_window is window
    # Optional tweaks (uncomment to adjust):
    # padding (30, 15, 30, 18)
    # background Frame("gui/window.png", 40, 40)  # Already default in most themes

style char_desc_text is say_dialogue:
    yalign 0.2
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

