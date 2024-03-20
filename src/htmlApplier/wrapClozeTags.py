from .htmlChunker import tokenizeHTML, optimizeChunks
from .xorshift16 import xorshift16Step
import random
import html

clozeId = random.randint(1, 0xFFFF)


def wrapClozeTag(segment, clozeNo, revealCondition=None):
    """
    Cloze may span across DOM boundary. This ensures that clozed text
    in elements different from starting element to be properly hidden
    by enclosing them by <cloze2>
    """

    global clozeId

    if revealCondition is None:
        dataRevealCondition = ""
    else:
        dataRevealCondition = f" data-reveal-condition='{html.escape(revealCondition)}'"
    output = [
        "<cloze2_w class='cz-%d' data-cloze-id='%04x'%s></cloze2_w>"
        % (clozeNo, clozeId, dataRevealCondition)
    ]
    cloze_header = "<cloze2 class='cz-%d czi-%04x'>" % (clozeNo, clozeId % 0xFFFF)

    cloze_footer = "</cloze2>"
    clozeId = xorshift16Step(clozeId)

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
