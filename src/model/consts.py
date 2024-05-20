from ..utils.resource import readResource

model_name = "Cloze (Hide all)"

card_front = readResource("template/qSide.html")
card_back = readResource("template/aSide.html")
card_css = readResource("template/style.css")
hideback_caption = "Hide others on the back side"

hidebackBlockHeader = "{{#%s}}" % hideback_caption
hidebackBlockFooter = "{{/%s}}" % hideback_caption
hidebackCommentedHeader = "<!-- (Always) #%s -->" % hideback_caption
hidebackCommentedFooter = "<!-- (Always) /%s -->" % hideback_caption
