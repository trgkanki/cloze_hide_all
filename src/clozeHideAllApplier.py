import re

from .htmlChunker import tokenizeHTML, optimizeChunks


def stripClozeHelper(html):
    return re.sub(
        r"</?(cz_hide|cloze2|cloze2_w)[^>]*?>|"
        + r"<(cloze2_w|cloze2)[^>]*?class=(\"|')cz-\d+(\"|')[^>]*?>|"
        + r"<script( class=(\"|')cz-\d+(\"|'))?>_czha\(\d+\)</script>",
        "",
        html,
    )


def wrapClozeTag(segment, clozeId):
    """
    Cloze may span across DOM boundary. This ensures that clozed text
    in elements different from starting element to be properly hidden
    by enclosing them by <cloze2>
    """

    output = ["<cloze2_w class='cz-%d'></cloze2_w>" % clozeId]
    cloze_header = "<cloze2 class='cz-%d'>" % clozeId
    cloze_footer = "</cloze2>"

    chunks = tokenizeHTML(segment)
    chunks = optimizeChunks(chunks)

    for chunk in chunks:
        if chunk[0] == "raw":
            output.append(cloze_header)
            output.append(chunk[1])
            output.append(cloze_footer)
        else:
            output.append(chunk[1])

    return "".join(output)


def makeClozeCompatible(html):
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
