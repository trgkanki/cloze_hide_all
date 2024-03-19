## Module for appling CHA-related html modification to note templates


import re

from .wrapClozeTags import wrapClozeTag
from .stripClozeTags import stripClozeTags


def applyClozeTags(html):
    def _(match):
        clozeNumberString: str = match.group(1)
        clozeContent: str = match.group(2)
        clozeCaption: str = match.group(3) or ""

        # Empty cloze - just passthrough
        if not clozeContent:
            return "{{c%s::%s%s}}" % (clozeNumberString, clozeContent, clozeCaption)

        # Always-shown cloze - just passthrough
        if clozeContent[0] in ("!", "?"):
            clozePrefix = clozeContent[0]
            clozeContent = clozeContent[1:]
            return "{{c%s::<cz_hide>%s</cz_hide>%s%s}}" % (
                clozeNumberString,
                clozePrefix,
                clozeContent,
                clozeCaption,
            )

        return "{{c%s::%s%s}}" % (
            clozeNumberString,
            wrapClozeTag(clozeContent, int(clozeNumberString)),
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
