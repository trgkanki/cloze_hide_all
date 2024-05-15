from ....utils.resource import readResource, updateMedia
from aqt import mw, gui_hooks


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
                targetString = targetString + "\n" + self.blockRaw
            elif position == "before":
                targetString = self.blockRaw + "\n" + targetString
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
_updateMediaList = []


def updateMediaOnProfileLoad(path, content):
    _updateMediaList.append((path, content))
    if mw.col:
        updateMedia(path, content)


def _updateProfileLoadPendingMedias():
    for path, content in _updateMediaList:
        updateMedia(path, content)


gui_hooks.profile_did_open.append(_updateProfileLoadPendingMedias)


def ScriptBlock(identifier, scriptPath, scriptContent=None):
    if scriptContent is None:
        scriptContent = readResource("assets/%s" % scriptPath)
    if type(scriptContent) is str:
        scriptContent = scriptContent.encode("utf-8")
    updateMediaOnProfileLoad(f"_cha_{scriptPath}", scriptContent)
    return ReplaceBlock(
        f"<!-- # {identifier} -->",
        f"<!-- / {identifier} -->",
        f'<script src="_cha_{scriptPath}"></script>',
    )


def StyleBlock(identifier, stylePath, styleContent=None):
    if styleContent is None:
        styleContent = readResource("assets/%s" % stylePath)
    if type(styleContent) is str:
        styleContent = styleContent.encode("utf-8")
    updateMediaOnProfileLoad(f"_cha_{stylePath}", styleContent)

    return ReplaceBlock(
        f"<!-- # {identifier} -->",
        f"<!-- / {identifier} -->",
        f'<link rel="stylesheet" type="text/css" href="_cha_{stylePath}">',
    )
