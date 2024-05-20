import re
from aqt.utils import showInfo

from ...utils.configrw import getConfig

from ..consts import (
    hideback_caption,
    hidebackBlockHeader,
    hidebackBlockFooter,
    hidebackCommentedHeader,
    hidebackCommentedFooter,
)
from .common import (
    removeObsoleteBlocks,
    hidebackBlock,
    applyChaScriptToHTML,
)
from .utils.removeCSSContainingSelector import removeCSSRuleContainingSelectorFromHtml

# Anki replaces {{#~~}} to {{^~~}} after the field is removed.
# THIS IS UNDOCUMENTED FEATURE :(
hidebackBlockHeaderAfterFieldDelete = "{{^%s}}" % hideback_caption


def migrateBackSide(model, backSide, templateUpdated, warnUserUpdate):
    oldBackSide = backSide

    # code normalization
    backSide = backSide.replace("\r", "")  # Possible windows dirt

    # remove legacy blocks
    backSide = removeObsoleteBlocks(backSide)
    backSide = removeCSSRuleContainingSelectorFromHtml(backSide, "cloze2")
    backSide = removeCSSRuleContainingSelectorFromHtml(backSide, "cloze2_w")
    backSide = re.sub("<style>\s*</style>", "", backSide)  # Empty stylesheet remove

    backSide = re.sub(r"\n{3,}", "\n\n", backSide)

    # support for 'alwaysHideback'
    backSide = backSide.replace(hidebackBlockHeader, hidebackCommentedHeader)
    backSide = backSide.replace(hidebackBlockFooter, hidebackCommentedFooter)

    # Some user simply have removed hideback field. OMG please.
    backSide = backSide.replace(
        hidebackBlockHeaderAfterFieldDelete, hidebackBlockHeader
    )
    if hidebackCommentedHeader not in backSide:
        if warnUserUpdate:
            showInfo(
                'Due to migration script refactoring, you cannot just remove "%s"~"%s" block from back template. Use "alwaysHideBack" addon config instead.'
                % (hidebackBlockHeader, hidebackBlockFooter)
            )

    # This is where the main substitution happens.
    if True:
        backSide = applyChaScriptToHTML(backSide)
        backSide = hidebackBlock.apply(backSide)

    # support for 'alwaysHideback'
    if not getConfig("alwaysHideback"):
        backSide = backSide.replace(hidebackCommentedHeader, hidebackBlockHeader)
        backSide = backSide.replace(hidebackCommentedFooter, hidebackBlockFooter)

    # Revert to `{{^` syntax...
    if not any(fld["name"] == hideback_caption for fld in model["flds"]):
        backSide = backSide.replace(
            hidebackBlockHeader, hidebackBlockHeaderAfterFieldDelete
        )

    if oldBackSide != backSide:
        templateUpdated[0] = True

    return backSide
