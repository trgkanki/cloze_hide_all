from aqt.utils import showInfo

from .utils.markerReplacer import (
    ScriptBlock,
    StyleBlock,
    ReplaceBlock,
    updateMediaOnProfileLoad,
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig
from ..consts import hideback_html, hidebackBlockHeader, hidebackBlockFooter

###############################################################################
# Script blocks
scrollToClozeSiteScript = ScriptBlock("1f91af7729e984b8", "scrollToCurrentCloze.js")

###############################################################################
# Customizable cloze styles
try:
    _hiddenClozeStyle = getConfig("hiddenClozeStyle")
    _clozeHiddenContent = readResource(
        "template/clozeHiddenUI/%s.css" % _hiddenClozeStyle
    )
except IOError:
    showInfo("Cloze (Hide all) - Hidden cloze style %s not exists!" % _hiddenClozeStyle)
    _clozeHiddenContent = readResource("template/clozeHiddenUI/yellowBox.css")

_clozeFrontCSS = readResource("template/clozeFront.css")

_obsoleteBlocks = [
    # legacy script block
    ReplaceBlock(
        "<script>\n/* --- DO NOT DELETE OR EDIT THIS SCRIPT --- */",
        "/* --- DO NOT DELETE OR EDIT THIS SCRIPT --- */\n</script>",
        "",
    ),
    # hiddenClozeStyle (1)
    ReplaceBlock("/* !-- a81b1bee0481ede2 */", "/* a81b1bee0481ede2 --! */", ""),
    # hiddenClozeStyle (2)
    ReplaceBlock(
        "<!-- # 24402e41168547b6 -->", "<!-- / 24402e41168547b6 --!>", ""
    ),  # apparently --!> was a bug...
    # unused_revealCurrentClozeScriptBlock
    ReplaceBlock(
        "<script>\n/* --- DO NOT DELETE OR EDIT THIS SCRIPT (409cac4f6e95b12d) --- */\n",
        "\n/* --- DO NOT DELETE OR EDIT THIS SCRIPT (409cac4f6e95b12d) --- */\n</script>",
        "",
    ),
    # old revealConditionalBlock
    ReplaceBlock(
        "<script>\n/* --- DO NOT DELETE OR EDIT THIS SCRIPT (5c19f7715c0d9480) --- */\n",
        "\n/* --- DO NOT DELETE OR EDIT THIS SCRIPT (5c19f7715c0d9480) --- */\n</script>",
        "",
    ),
    # old scrollToClozeSizeScript
    ReplaceBlock(
        "<script>\n/* --- DO NOT DELETE OR EDIT THIS SCRIPT (1f91af7729e984b8) --- */",
        "/* --- DO NOT DELETE OR EDIT THIS SCRIPT (1f91af7729e984b8) --- */\n</script>",
        "",
    ),
]


def removeObsoleteBlocks(code):
    for block in _obsoleteBlocks:
        code = block.remove(code)
    return code


hiddenClozeStyleBlock = StyleBlock(
    "f71d5f0dc9ead165", "hiddenClozeStyle.css", _clozeHiddenContent + _clozeFrontCSS
)
revealConditionalBlock = ScriptBlock("ba699a36f501800d", "revealConditional.js")


hidebackBlock = ReplaceBlock(
    hidebackBlockHeader,
    hidebackBlockFooter,
    '\n<link rel="stylesheet" type="text/css" href="_cha_hiddenClozeStyle.css">\n<script src="_cha_revealHideback.js"></script>\n%s\n'
    % (hideback_html),
)
updateMediaOnProfileLoad(
    "_cha_revealHideback.js", readResource("scriptBlock/revealHideBack.js", binary=True)
)
