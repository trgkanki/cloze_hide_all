from aqt.utils import showInfo

from ...markerReplacer import (
    ScriptBlock,
    ReplaceBlock,
    removeScriptBlock,
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig


###############################################################################
# Script blocks
revealCurrentClozeScript = ScriptBlock("409cac4f6e95b12d", "revealCurrentCloze.js")
scrollToClozeSiteScript = ScriptBlock("1f91af7729e984b8", "scrollToCurrentCloze.js")


###############################################################################
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
