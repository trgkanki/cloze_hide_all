from .htmlChunker import tokenizeHTML, optimizeChunks
import html


class ClozeIdState:
    def __init__(self):
        self._id = 0

    def next(self):
        self._id += 1
        return self._id  # starting with 1


def wrapClozeTag(segment, clozeNo, clozeIdState: ClozeIdState, revealCondition=None):
    """
    Cloze may span across DOM boundary. This ensures that clozed text
    in elements different from starting element to be properly hidden
    by enclosing them by <cloze2>
    """

    clozeId = clozeIdState.next()

    if revealCondition is None:
        dataRevealCondition = ""
    else:
        dataRevealCondition = f" data-reveal-condition='{html.escape(revealCondition)}'"
    output = [
        "<cloze2_w class='cz-%d' data-cloze-id='%d'%s></cloze2_w>"
        % (clozeNo, clozeId, dataRevealCondition)
    ]
    cloze_header = "<cloze2 class='cz-%d czi-%d'>" % (clozeNo, clozeId)

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
