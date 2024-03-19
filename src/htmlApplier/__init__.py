## Module for appling CHA-related html modification to note templates


import re

from .wrapClozeTags import wrapClozeTag
from .stripClozeTags import stripClozeTags


def applyClozeTags(html):
    def _(match):
        clozeNumber = int(match.group(1))
        clozeContent: str = match.group(2)
        clozeCaption: str = match.group(3) or ""

        # Empty cloze - just passthrough
        if not clozeContent:
            return "{{c%d::%s%s}}" % (clozeNumber, clozeContent, clozeCaption)

        # Always-shown cloze - just passthrough
        if clozeContent[0] in ("!", "?"):
            clozePrefix = clozeContent[0]
            clozeContent = clozeContent[1:]
            return "{{c%d::<cz_hide class='cz-%d'>%s</cz_hide>%s%s}}" % (
                clozeNumber,
                clozeNumber,
                clozePrefix,
                clozeContent,
                clozeCaption,
            )

        return "{{c%d::%s%s}}" % (
            clozeNumber,
            wrapClozeTag(clozeContent, int(clozeNumber)),
            clozeCaption,
        )

    html = re.sub(
        r"\{\{"  # starting {{
        r"c(\d+)::"  # c1::
        r"((?:[^:}]|:[^:}])*?)"  # cloze content
        r"(::(?:(?:[^:}]|:[^:}])*?))?"  # cloze caption
        r"\}\}",  # ending "}}"
        _,
        html,
    )

    return html
