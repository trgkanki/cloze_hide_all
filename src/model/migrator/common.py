from aqt.utils import showInfo

from .utils.markerReplacer import (
    ScriptBlock,
    ReplaceBlock,
    removeScriptBlock,
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig
from ..consts import hideback_html, hidebackBlockHeader, hidebackBlockFooter

###############################################################################
# Script blocks
unused_revealCurrentClozeScriptBlock = ReplaceBlock(
    "<script>\n/* --- DO NOT DELETE OR EDIT THIS SCRIPT (409cac4f6e95b12d) --- */\n",
    "\n/* --- DO NOT DELETE OR EDIT THIS SCRIPT (409cac4f6e95b12d) --- */\n</script>",
    "",
)  # Exists only for removal of old template clutters.
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
hiddenClozeStyleBuggy = ReplaceBlock(
    "/* !-- a81b1bee0481ede2 */",
    "/* a81b1bee0481ede2 --! */",
    "\n" + clozeHiddenContent + clozeFrontCSS + "\n",
)

hiddenClozeStyle = ReplaceBlock(
    "<!-- # 24402e41168547b6 -->",
    "<!-- / 24402e41168547b6 --!>",
    "\n<style>" + clozeHiddenContent + clozeFrontCSS + "</style>\n",
)

hidebackBlock = ReplaceBlock(
    hidebackBlockHeader,
    hidebackBlockFooter,
    "\n\n<style>\n%s\n%s\n</style>\n\n%s\n\n"
    % (clozeHiddenContent, clozeFrontCSS, hideback_html),
)
