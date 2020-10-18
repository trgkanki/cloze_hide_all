## Module for appling CHA-related html modification to note templates


import re

from .wrapClozeTags import wrapClozeTag
from .stripClozeTags import stripClozeTags


def applyClozeTags(html):
    html = re.sub(
        r"\{\{c(\d+)::([^!?]([^:}]|:[^:}])*?)\}\}",
        lambda match: "{{c%s::%s}}"
        % (match.group(1), wrapClozeTag(match.group(2), int(match.group(1)))),
        html,
    )
    html = re.sub(
        r"\{\{c(\d+)::([^!?]([^:}]|:[^:}])*?)::(([^:}]|:[^:}])*?)\}\}",
        lambda match: "{{c%s::%s::%s}}"
        % (
            match.group(1),
            wrapClozeTag(match.group(2), int(match.group(1))),
            match.group(4),
        ),
        html,
    )
    html = re.sub(r"\{\{c(\d+)::([!?])", "{{c\\1::<cz_hide>\\2</cz_hide>", html)
    return html
