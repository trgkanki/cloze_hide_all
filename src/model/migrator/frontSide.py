import re
from aqt.utils import showInfo


from .utils.markerReplacer import (
    ScriptBlock,
    ReplaceBlock,
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig

from .common import scrollToClozeSiteScript, hidebackStyleBlock


def migrateFrontSide(frontSide, templateUpdated=[False]):
    oldFrontSide = frontSide

    frontSide = scrollToClozeSiteScript.apply(frontSide)

    # update cloze box related stylings
    frontSide = removeReplaceBlock(frontSide, "cloze2 {", "}")
    frontSide = removeReplaceBlock(frontSide, "cloze2_w {", "}")
    frontSide = removeReplaceBlock(
        frontSide, hidebackStyleBlock.startMarker, hidebackStyleBlock.endMarker
    )
    frontSide = re.sub("<style>\s*</style>", "", frontSide)
    frontSide = frontSide.strip()
    frontSide = "<style>\n%s\n</style>\n\n%s" % (
        hidebackStyleBlock.blockRaw,
        frontSide,
    )
    frontSide = frontSide.replace("\r", "")
    frontSide = re.sub(r"\n{3,}", "\n\n", frontSide)

    if oldFrontSide != frontSide:
        templateUpdated[0] = True

    return frontSide
