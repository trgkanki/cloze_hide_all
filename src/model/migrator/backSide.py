import re
from aqt.utils import showInfo


from .utils.markerReplacer import (
    ScriptBlock,
    ReplaceBlock,
    removeScriptBlock,
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig

from ..consts import hideback_caption, hidebackBlockHeader, hidebackBlockFooter
from .common import (
    hidebackBlock,
    hiddenClozeStyle,
    scrollToClozeSiteScript,
    unused_revealCurrentClozeScriptBlock,
)
from .utils.removeCSSContainingSelector import removeCSSRuleContainingSelectorFromHtml

hidebackCommentedHeader = "<!-- (Always) #%s -->\n" % hideback_caption
hidebackCommentedFooter = "<!-- (Always) /%s -->\n" % hideback_caption

# Anki replaces {{#~~}} to {{^~~}} after the field is removed.
# THIS IS UNDOCUMENTED FEATURE :(
hidebackBlockHeaderAfterFieldDelete = "{{^%s}}" % hideback_caption


def migrateBackSide(model, backSide, templateUpdated, warnUserUpdate):
    oldBackSide = backSide

    # remove legacy script block
    backSide = removeScriptBlock(
        backSide, "/* --- DO NOT DELETE OR EDIT THIS SCRIPT --- */"
    )

    # Bad code killer (Issue #35)
    backSide = removeCSSRuleContainingSelectorFromHtml(backSide, "cloze2")
    backSide = removeCSSRuleContainingSelectorFromHtml(backSide, "cloze2_w")
    backSide = hiddenClozeStyle.remove(backSide)
    backSide = unused_revealCurrentClozeScriptBlock.remove(backSide)
    backSide = re.sub("<style>\s*</style>", "", backSide)  # Empty stylesheet remove

    # Code normalization
    backSide = backSide.replace("\r", "")  # Possible windows dirt

    # Hideback code applier
    backSide = backSide.replace(hidebackCommentedHeader, hidebackBlockHeader)
    backSide = backSide.replace(hidebackCommentedFooter, hidebackBlockFooter)

    # Some user simply have removed hideback field. OMG please.
    backSide = backSide.replace(
        hidebackBlockHeaderAfterFieldDelete, hidebackBlockHeader
    )

    if hidebackBlockHeader not in backSide:
        if warnUserUpdate:
            showInfo(
                'Due to migration script refactoring, you cannot just remove "%s"~"%s" block from back template. Use "alwaysHideBack" addon config instead.'
                % (hidebackBlockHeader, hidebackBlockFooter)
            )

    backSide = hidebackBlock.apply(backSide)

    backSide = re.sub(r"\n{3,}", "\n\n", backSide)

    if getConfig("alwaysHideback"):
        backSide = backSide.replace(hidebackBlockHeader, hidebackCommentedHeader)
        backSide = backSide.replace(hidebackBlockFooter, hidebackCommentedFooter)

    # Revert to `{{^` syntax...
    if not any(fld["name"] == hideback_caption for fld in model["flds"]):
        backSide = backSide.replace(
            hidebackBlockHeader, hidebackBlockHeaderAfterFieldDelete
        )

    # Functions
    backSide = scrollToClozeSiteScript.apply(backSide)

    if oldBackSide != backSide:
        templateUpdated[0] = True

    return backSide
