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

from ..consts import hideback_caption
from .common import revealCurrentClozeScript, hidebackStyleBlock
from .utils.removeCSSContainingSelector import removeCSSRuleContainingSelectorFromHtml

hidebackBlockHeader = "{{#%s}}\n" % hideback_caption
hidebackBlockFooter = "{{/%s}}\n" % hideback_caption
hidebackCommentedHeader = "<!-- (Always) #%s -->\n" % hideback_caption
hidebackCommentedFooter = "<!-- (Always) /%s -->\n" % hideback_caption


def migrateBackSide(backSide, templateUpdated=[False]):
    oldBackSide = backSide

    # remove legacy script block
    backSide = removeScriptBlock(
        backSide, "/* --- DO NOT DELETE OR EDIT THIS SCRIPT --- */"
    )

    # Bad code killer (Issue #35)
    backSide = removeCSSRuleContainingSelectorFromHtml(backSide, "cloze2")
    backSide = removeCSSRuleContainingSelectorFromHtml(backSide, "cloze2_w")
    backSide = hidebackStyleBlock.remove(backSide)
    backSide = revealCurrentClozeScript.remove(backSide)
    backSide = re.sub("<style>\s*</style>", "", backSide)  # Empty stylesheet remove

    # Code normalization
    backSide = backSide.replace("\r", "")  # Possible windows dirt

    # Hideback code applier
    backSide = backSide.replace(hidebackCommentedHeader, hidebackBlockHeader)
    backSide = backSide.replace(hidebackCommentedFooter, hidebackBlockFooter)

    if hidebackBlockHeader in backSide:
        # TODO: <style> should preferrably be before the card content. Dunno if this is possible.
        backSide = backSide.replace(
            hidebackBlockHeader,
            "%s<style>\n%s\n</style>\n\n%s\n\n"
            % (
                hidebackBlockHeader,
                hidebackStyleBlock.blockRaw,
                revealCurrentClozeScript.blockRaw,
            ),
        )
    else:
        # User might just have removed '{{#..}}' and '{{/..}}`, so that condition
        # always evaluates to true and other clozes won't be shown regardless
        # of {hideback_caption} field.
        backSide = "<style>\n%s\n</style>\n\n%s\n\n%s" % (
            hidebackStyleBlock.blockRaw,
            revealCurrentClozeScript.blockRaw,
            backSide,
        )

    backSide = re.sub(r"\n{3,}", "\n\n", backSide)

    if getConfig("alwaysHideback"):
        backSide = backSide.replace(hidebackBlockHeader, hidebackCommentedHeader)
        backSide = backSide.replace(hidebackBlockFooter, hidebackCommentedFooter)

    if oldBackSide != backSide:
        templateUpdated[0] = True

    return backSide
