import re
from aqt.utils import showInfo


from .utils.markerReplacer import (
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig

from .common import (
    removeObsoleteBlocks,
    applyChaScriptToHTML,
)


def migrateFrontSide(frontSide, templateUpdated, warnUserUpdate):
    oldFrontSide = frontSide

    # remove obsolete blocks
    frontSide = frontSide.replace("\r", "")
    frontSide = removeObsoleteBlocks(frontSide)
    frontSide = removeReplaceBlock(frontSide, "cloze2 {", "}")
    frontSide = removeReplaceBlock(frontSide, "cloze2_w {", "}")
    frontSide = re.sub("<style>\s*</style>", "", frontSide)
    frontSide = re.sub(r"\n{3,}", "\n\n", frontSide)
    frontSide = frontSide.strip()

    # functions
    frontSide = applyChaScriptToHTML(frontSide)

    if oldFrontSide != frontSide:
        templateUpdated[0] = True

    return frontSide
