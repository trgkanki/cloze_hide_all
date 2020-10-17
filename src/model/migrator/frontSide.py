import re
from aqt.utils import showInfo


from ...markerReplacer import (
    ScriptBlock,
    ReplaceBlock,
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig


scrollToClozeSiteScript = ScriptBlock("1f91af7729e984b8", "scrollToCurrentCloze.js")

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
clozeHideAllBlock = ReplaceBlock(
    "/* !-- a81b1bee0481ede2 */",
    "/* a81b1bee0481ede2 --! */",
    "\n" + clozeHiddenContent + clozeFrontCSS + "\n",
)


def migrateFrontSide(frontSide, templateUpdated=[False]):
    oldFrontSide = frontSide

    frontSide = scrollToClozeSiteScript.apply(frontSide)

    # update cloze box related stylings
    frontSide = removeReplaceBlock(frontSide, "cloze2 {", "}")
    frontSide = removeReplaceBlock(frontSide, "cloze2_w {", "}")
    frontSide = removeReplaceBlock(
        frontSide, clozeHideAllBlock.startMarker, clozeHideAllBlock.endMarker
    )
    frontSide = re.sub("<style>\s*</style>", "", frontSide)
    frontSide = frontSide.strip()
    frontSide = "<style>\n%s\n</style>\n\n%s" % (
        clozeHideAllBlock.blockRaw,
        frontSide,
    )
    frontSide = frontSide.replace("\r", "")
    frontSide = re.sub(r"\n{3,}", "\n\n", frontSide)

    if oldFrontSide != frontSide:
        templateUpdated[0] = True

    return frontSide
