from ....utils.resource import readResource


class ReplaceBlock:
    def __init__(self, startMarker, endMarker, script):
        self.startMarker = startMarker
        self.endMarker = endMarker
        self.script = script
        self.blockRaw = "%s%s%s" % (startMarker, self.script, endMarker)

    def included(self, targetString):
        return self.blockRaw in targetString

    def remove(self, targetString):
        return removeReplaceBlock(targetString, self.startMarker, self.endMarker)

    def apply(self, targetString, *, updated=None, position="after"):
        oldTargetString = targetString

        try:
            start = targetString.index(self.startMarker)
            end = targetString.index(self.endMarker, start + 1)
            targetString = (
                targetString[:start]
                + self.blockRaw
                + self.remove(targetString[end + len(self.endMarker) :])
            )
        except ValueError:
            if position == "after":
                targetString = targetString + "\n\n" + self.blockRaw
            elif position == "before":
                targetString = self.blockRaw + "\n\n" + targetString
            else:
                raise RuntimeError("Invalid argument %s to position" % position)

        if updated and oldTargetString != targetString:
            updated[0] = True

        return targetString


def removeReplaceBlock(targetString, startMarker, endMarker, *, updated=None):
    oldTargetString = targetString
    while True:
        try:
            start = targetString.index(startMarker)
            end = targetString.index(endMarker, start + 1)
            targetString = (
                targetString[:start] + targetString[end + len(endMarker) :]
            ).strip()
        except ValueError:
            break

    if updated and oldTargetString != targetString:
        updated[0] = True

    return targetString


# Helper function


def ScriptBlock(blockHeader, scriptPath):
    script = readResource("scriptBlock/%s" % scriptPath)
    blockHeader = "/* --- DO NOT DELETE OR EDIT THIS SCRIPT (%s) --- */" % blockHeader
    startMarker = "<script>\n%s\n" % blockHeader
    endMarker = "\n%s\n</script>" % blockHeader
    return ReplaceBlock(startMarker, endMarker, script)


def removeScriptBlock(targetString, blockHeader, *, updated=None):
    startMarker = "<script>\n%s\n" % blockHeader
    endMarker = "\n%s\n</script>" % blockHeader
    return removeReplaceBlock(targetString, startMarker, endMarker, updated=updated)


if __name__ == "__main__":
    sb = ScriptBlock("test", "1+1 = 2")
    segment = "wow"
    assert not sb.included(segment)

    # Test: segment applied well
    segment2 = sb.apply(segment)
    print("segment2", segment2)
    assert sb.included(segment2)

    # Test: updated field when really updated
    updated = [False]
    segment2 = sb.apply(segment, updated=updated)
    assert updated[0]

    # Test: segment applied to already-include string won't cause issues
    segment3 = sb.apply(segment2)
    assert segment2 == segment3

    # Test: updated field when really updated
    updated = [False]
    segment3 = sb.apply(segment2, updated=updated[0])
    assert not updated[0]

    # Test: clean up erroneously added multiple script blocks
    segment4 = """wow
<script>
/* --- DO NOT DELETE OR EDIT THIS SCRIPT (test) --- */
1+1 = 2
/* --- DO NOT DELETE OR EDIT THIS SCRIPT (test) --- */
</script>

<script>
/* --- DO NOT DELETE OR EDIT THIS SCRIPT (test) --- */
aa
/* --- DO NOT DELETE OR EDIT THIS SCRIPT (test) --- */
</script>"""
    segment4 = sb.apply(segment4)
    print("segment4", segment4)
    assert sb.apply(segment4) == segment2
