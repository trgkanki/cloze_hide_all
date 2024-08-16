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

        while True:
            # Always-shown cloze - just passthrough
            if clozeContent[0] in ("!", "?"):
                clozeRevealCondition = clozeContent[0]
                clozeContent = clozeContent[1:]

                # NOTE: this requires special treatment:
                # People may don't want any model migration,
                # (`noModelMigration` set to true)
                # Emit old-style always-shown cloze code for backward compatibility.
                return "{{c%d::<cz_hide>%s</cz_hide>%s%s}}" % (
                    clozeNumber,
                    clozeRevealCondition,
                    clozeContent,
                    clozeCaption,
                )

            # Cloze number conditional cloze
            # {{c1::<1!content}}  ← show when current cloze number < 1
            match = re.match(
                r"^(" + r"(?:(?:<|>|&lt;|&gt;)=?|=|==)" + r"\d*[!?]" + r")(.+)$",
                clozeContent,
            )
            if match:
                clozeRevealCondition = match.group(1)
                clozeContent = match.group(2)
                break

            # other case
            clozeRevealCondition = None
            break

        output = ["{{c%d::" % clozeNumber]
        if clozeRevealCondition:
            output.append(
                "<cz_hide class='cz-%d'>%s</cz_hide>"
                % (clozeNumber, clozeRevealCondition)
            )
            clozeRevealCondition = clozeRevealCondition[:-1]  # strip last ! or ?
        output.append(wrapClozeTag(clozeContent, clozeNumber, clozeRevealCondition))
        output.append(clozeCaption)
        output.append("}}")
        return "".join(output)

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
