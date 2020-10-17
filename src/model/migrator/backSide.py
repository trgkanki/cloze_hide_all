import re
from aqt.utils import showInfo


from ...markerReplacer import (
    ScriptBlock,
    ReplaceBlock,
    removeScriptBlock,
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig


hideback_caption = u"Hide others on the back side"
hideback_block_header = "{{#%s}}\n" % hideback_caption
hideback_block_footer = "{{/%s}}\n" % hideback_caption
hideback_commented_header = "<!-- (Always) #%s -->\n" % hideback_caption
hideback_commented_footer = "<!-- (Always) /%s -->\n" % hideback_caption

oldScriptBlockHeader = "/* --- DO NOT DELETE OR EDIT THIS SCRIPT --- */"

revealClozeScript = ScriptBlock("409cac4f6e95b12d", "revealCurrentCloze.js")


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


def migrateBackSide(backSide, templateUpdated=[False]):
    oldBackSide = backSide

    backSide = removeScriptBlock(backSide, oldScriptBlockHeader)
    backSide = revealClozeScript.apply(backSide)

    backSide = backSide.replace(
        hideback_commented_header, hideback_block_header
    ).replace(hideback_commented_footer, hideback_block_footer)

    backSide = removeReplaceBlock(backSide, "cloze2 {", "}")
    backSide = removeReplaceBlock(backSide, "cloze2_w {", "}")
    backSide = removeReplaceBlock(
        backSide, clozeHideAllBlock.startMarker, clozeHideAllBlock.endMarker
    )
    backSide = re.sub("<style>\s*</style>", "", backSide)

    if (hideback_block_header) in backSide:
        # TODO: <style> should preferrably be before the card content. Dunno if this is possible.
        backSide = backSide.replace(
            hideback_block_header,
            "%s<style>\n%s\n</style>\n"
            % (hideback_block_header, clozeHideAllBlock.blockRaw),
        )
    else:
        # User might just have removed '{{#..}}' and '{{/..}}`, so that condition
        # always evaluates to true and other clozes won't be shown regardless
        # of {hideback_caption} field.
        backSide = "<style>\n%s\n</style>\n\n%s" % (
            clozeHideAllBlock.blockRaw,
            backSide,
        )

    backSide = backSide.replace("\r", "")
    backSide = re.sub(r"\n{3,}", "\n\n", backSide)

    if getConfig("alwaysHideback"):
        backSide = backSide.replace(
            hideback_block_header, hideback_commented_header
        ).replace(hideback_block_footer, hideback_commented_footer)

    if oldBackSide != backSide:
        templateUpdated[0] = True

    return backSide
