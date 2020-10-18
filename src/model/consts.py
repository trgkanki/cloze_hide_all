from ..utils.resource import readResource

model_name = u"Cloze (Hide all)"

card_front = readResource("template/qSide.html")
card_back = readResource("template/aSide.html")
card_css = readResource("template/style.css")
hideback_caption = u"Hide others on the back side"
hideback_html = readResource("template/hideback.html")

hidebackBlockHeader = "{{#%s}}" % hideback_caption
hidebackBlockFooter = "{{/%s}}" % hideback_caption
