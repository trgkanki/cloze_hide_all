import re
from aqt.utils import showInfo


from .utils.markerReplacer import (
    ReplaceBlock,
    removeReplaceBlock,
)

from ...utils.resource import readResource
from ...utils.configrw import getConfig
from ...utils.cssHelper import minifyCSS
from .utils.removeCSSContainingSelector import removeRuleContainingSelectorFromCSS

from .common import hiddenClozeStyle


def migrateModelCSS(css, templateUpdated, warnUserUpdate):
    oldCSS = css

    css = css.replace("\r", "")  # Windows compat

    # Remove obsolete hidebackStyleBlock
    css = hiddenClozeStyle.remove(css)

    # cloze2 / cloze2_w tag styling is embedded directly in front/back template
    # remove such styling on css part
    css = removeRuleContainingSelectorFromCSS(css, "cloze2")
    css = removeRuleContainingSelectorFromCSS(css, "cloze2_w")

    # add .nightMode .cloze selector if appliable
    minifiedCSS = minifyCSS(css)
    if (
        ".nightMode" not in minifiedCSS
        and ".night_mode" not in minifiedCSS
        and "cloze{font-weight:bold;color:blue}"  # CSS doesn't care night mode
        in minifiedCSS  # User haven't touched the cloze styling
    ):
        css += """\


.nightMode .cloze {
    color: lightblue;
}
"""

    css = re.sub(r"\n{3,}", "\n\n", css)  # normalize multi-line newlines
    if oldCSS != css:
        templateUpdated[0] = True

    return css
