import re
from aqt.utils import showInfo


from ...markerReplacer import (
    ReplaceBlock,
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig
from ...utils.cssHelper import minifyCSS

# Customizable cloze styles
try:
    hiddenClozeStyle = getConfig("hiddenClozeStyle")
    clozeHiddenContent = readResource(
        "template/clozeHiddenUI/%s.css" % hiddenClozeStyle
    )
except IOError:
    showInfo("Cloze (Hide all) - Hidden cloze style %s not exists!" % hiddenClozeStyle)
    clozeHiddenContent = readResource("template/clozeHiddenUI/yellowBox.css")

clozeFrontCSS = readResource("template/clozeFront.css")
hidebackStyleBlock = ReplaceBlock(
    "/* !-- a81b1bee0481ede2 */",
    "/* a81b1bee0481ede2 --! */",
    "\n" + clozeHiddenContent + clozeFrontCSS + "\n",
)


def migrateModelCSS(css, templateUpdated=[False]):
    oldCSS = css
    css = removeReplaceBlock(
        css, hidebackStyleBlock.startMarker, hidebackStyleBlock.endMarker
    )
    css = re.sub(r"cloze2 \{(.|\n)*?\}", "", css)

    # add .nightMode .cloze selector if appliable
    minifiedCSS = minifyCSS(css)
    if (
        ".nightMode" not in minifiedCSS
        and ".night_mode" not in minifiedCSS
        and "cloze{font-weight:bold;color:blue}"  # CSS doesn't care night mode
        in minifiedCSS  # User haven't touched the cloze styling
    ):
        css += """\


.nightMode .cloze {
    color: lightblue;
}
"""

    css = css.replace("\r", "")
    css = re.sub(r"\n{3,}", "\n\n", css)
    if oldCSS != css:
        templateUpdated[0] = True

    return css
