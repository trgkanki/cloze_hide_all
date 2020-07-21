from html.parser import HTMLParser
import re
import json


_voidElements = {
    "area",
    "base",
    "basefont",
    "bgsound",
    "br",
    "col",
    "command",
    "embed",
    "frame",
    "hr",
    "image",
    "img",
    "input",
    "isindex",
    "keygen",
    "link",
    "menuitem",
    "meta",
    "nextid",
    "param",
    "source",
    "track",
    "wbr",
}


def tokenizeHTML(s):
    """
    Using html.parser is surprisingly hard...
    Really.
    """
    PARSE_DATA = 0
    PARSE_TAG = 1
    mode = PARSE_DATA

    dataCh = []
    tagCh = []

    chunks = []

    def emitData():
        data = "".join(dataCh)
        dataCh[:] = []

        if not data:
            return

        chunks.append(("raw", data))

    def emitTag():
        tag = "".join(tagCh)
        tagCh[:] = []

        # Process starting tag & Ending tag
        tagStartMatch = re.match("<\s*([a-zA-Z0-9]+)", tag)
        tagEndMatch = re.match("<\s*/\s*([a-zA-Z0-9]+)", tag)

        if tagStartMatch:
            chunks.append(("tstart", tag, tagStartMatch.group(1).lower()))

        elif tagEndMatch:
            chunks.append(("tend", tag, tagEndMatch.group(1).lower()))

    for ch in s:
        if mode == PARSE_DATA:
            # Tag start/end -> switch to tag parsing mode
            if ch == "<":
                mode = PARSE_TAG
                emitData()
                tagCh.append("<")

            # Emit character as-is
            else:
                dataCh.append(ch)

        elif mode == PARSE_TAG:
            tagCh.append(ch)

            if ch == ">":
                mode = PARSE_DATA
                emitTag()

    # Rest of the data
    if mode == PARSE_DATA:
        emitData()
    else:
        emitTag()

    return chunks


def transform_removeEmptyChunk(chunks):
    newChunks = []
    for chunk in chunks:
        if not chunk[1]:
            continue
        newChunks.append(chunk)

    return newChunks


def transform_concatAdjacentData(chunks):
    newChunks = []
    for chunk in chunks:
        if chunk[0] == "raw" and newChunks and newChunks[-1][0] == "raw":
            newChunks[-1] = ("raw", newChunks[-1][1] + chunk[1])
        else:
            newChunks.append(chunk)

    return newChunks


def transform_concatProperlyClozedTag(chunks):
    newChunks = []
    for chunk in chunks:
        newChunks.append(chunk)

        if (
            len(newChunks) >= 3
            and newChunks[-3][0] == "tstart"
            and newChunks[-2][0] == "raw"
            and newChunks[-1][0] == "tend"
            and newChunks[-1][2] == newChunks[-3][2]
        ):
            ts, r, te = newChunks[-3:]
            newRaw = ts[1] + r[1] + te[1]
            newChunks[-3:] = [("raw", newRaw)]

    return newChunks


def transform_rawifyVoidElements(chunks):
    newChunks = []
    for chunk in chunks:
        if chunk[0] == "tstart" and chunk[2] in _voidElements:
            newChunks.append(("raw", chunk[1]))
        else:
            newChunks.append(chunk)

    return newChunks


def optimizeChunks(chunks):
    chunks = transform_rawifyVoidElements(chunks)
    while True:
        oldChunks = chunks
        chunks = transform_concatProperlyClozedTag(chunks)
        chunks = transform_concatAdjacentData(chunks)
        chunks = transform_removeEmptyChunk(chunks)
        if jsonEq(oldChunks, chunks):
            break

    return chunks


def jsonEq(o1, o2):
    """ Simple json-based comparator of procratinator. Anyway it works """
    return json.dumps(o1) == json.dumps(o2)


if __name__ == "__main__":
    segment = 'wow<div><br></div><div><img src="paste-535b9586ebd2de4bc5837f1a5c51de8d95e847b9.png">'
    chunks = tokenizeHTML(segment)
    chunks = optimizeChunks(chunks)
    assert len(chunks) == 3
    print(chunks)

    segment = "<i>test</i>"
    chunks = tokenizeHTML(segment)
    chunks = optimizeChunks(chunks)
    assert len(chunks) == 1
    print(chunks)
