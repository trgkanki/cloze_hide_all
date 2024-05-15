import re
from aqt.utils import showInfo


from .utils.markerReplacer import (
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig

from .common import (
    removeObsoleteBlocks,
    scrollToClozeSiteScript,
    hiddenClozeStyleBlock,
    revealConditionalBlock,
)


def migrateFrontSide(frontSide, templateUpdated, warnUserUpdate):
    oldFrontSide = frontSide

    # update cloze box related stylings
    frontSide = frontSide.replace("\r", "")
    frontSide = removeReplaceBlock(frontSide, "cloze2 {", "}")
    frontSide = removeReplaceBlock(frontSide, "cloze2_w {", "}")
    frontSide = removeObsoleteBlocks(frontSide)
    frontSide = hiddenClozeStyleBlock.apply(frontSide, position="before")
    frontSide = re.sub("<style>\s*</style>", "", frontSide)
    frontSide = frontSide.strip()
    frontSide = re.sub(r"\n{3,}", "\n\n", frontSide)

    # functions
    frontSide = revealConditionalBlock.apply(frontSide)
    frontSide = scrollToClozeSiteScript.apply(frontSide)

    if oldFrontSide != frontSide:
        templateUpdated[0] = True

    return frontSide
