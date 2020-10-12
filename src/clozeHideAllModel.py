from aqt import mw
from anki.consts import MODEL_CLOZE
from aqt.utils import askUser, showInfo

from .markerReplacer import (
    ScriptBlock,
    ReplaceBlock,
    removeScriptBlock,
    removeReplaceBlock,
)

from .utils.resource import readResource
from .utils.configrw import getConfig, setConfig
from .consts import model_name
from .minifyCSS import minifyCSS

import re

############################# Templates

oldScriptBlockHeader = "/* --- DO NOT DELETE OR EDIT THIS SCRIPT --- */"

revealClozeScript = ScriptBlock(
    "409cac4f6e95b12d", readResource("scriptBlock/revealCurrentCloze.js")
)
scrollToClozeSiteScript = ScriptBlock(
    "1f91af7729e984b8", readResource("scriptBlock/scrollToCurrentCloze.js")
)

card_front = readResource("template/qSide.html")
card_back = readResource("template/aSide.html")
card_css = readResource("template/style.css")
hideback_caption = u"Hide others on the back side"
hideback_html = readResource("template/hideback.html")

# Customizable cloze styles
try:
    hiddenClozeStyle = getConfig("hiddenClozeStyle")
    clozeHiddenContent = readResource(
        "template/clozeHiddenUI/%s.css" % hiddenClozeStyle
    )
except IOError:
    showInfo("Cloze (Hide all) - Hidden cloze style %s not exists!" % hiddenClozeStyle)
    clozeHiddenContent = readResource("template/clozeHiddenUI/yellowBox.css")

clozeFrontCSS = readResource("template/clozeFront.css")
clozeHideAllBlock = ReplaceBlock(
    "/* !-- a81b1bee0481ede2 */\n",
    "\n/* a81b1bee0481ede2 --! */",
    clozeHiddenContent + clozeFrontCSS,
)


###################################################################


def createClozeHideAllModel(col):
    models = col.models
    clozeModel = models.new(model_name)
    clozeModel["type"] = MODEL_CLOZE

    # Add fields
    for fieldName in ("Text", "Extra"):
        fld = models.newField(fieldName)
        models.addField(clozeModel, fld)

    # Add template
    template = models.newTemplate("Cloze (Hide all)")
    template["qfmt"] = card_front
    template["afmt"] = card_back
    clozeModel["css"] = card_css
    models.addTemplate(clozeModel, template)
    models.add(clozeModel)
    updateClozeModel(col, False)

    # Set alwaysHideBack to true for new users
    setConfig("alwaysHideback", True)

    return clozeModel


warningMsg = (
    "ClozeHideAll will update its card template. "
    "Sync your deck to AnkiWeb before pressing OK"
)


def updateClozeModel(col, warnUserUpdate=True):
    models = col.models
    clozeModel = mw.col.models.byName(model_name)

    hideback_block_header = "{{#%s}}\n" % hideback_caption
    hideback_block_footer = "{{/%s}}\n" % hideback_caption
    hideback_commented_header = "<!-- (Always) #%s -->\n" % hideback_caption
    hideback_commented_footer = "<!-- (Always) /%s -->\n" % hideback_caption

    # Add hideback caption
    if hideback_caption not in models.fieldNames(clozeModel):
        if warnUserUpdate and not askUser(warningMsg):
            return
        warnUserUpdate = False
        fld = models.newField(hideback_caption)
        fld["sticky"] = True
        models.addField(clozeModel, fld)

        template = clozeModel["tmpls"][0]
        template["afmt"] += "\n%s%s%s" % (
            hideback_block_header,
            hideback_html,
            hideback_block_footer,
        )

        models.save(clozeModel)

    template = clozeModel["tmpls"][0]
    templateUpdated = [False]
    template["afmt"] = removeScriptBlock(
        template["afmt"], oldScriptBlockHeader, updated=templateUpdated
    )
    template["afmt"] = revealClozeScript.apply(
        template["afmt"], updated=templateUpdated
    )
    template["qfmt"] = scrollToClozeSiteScript.apply(
        template["qfmt"], updated=templateUpdated
    )

    # update cloze box related stylings
    oldQfmt = template["qfmt"]
    template["qfmt"] = removeReplaceBlock(template["qfmt"], "\ncloze2 {", "}")
    template["qfmt"] = removeReplaceBlock(template["qfmt"], "\ncloze2_w {", "}")
    template["qfmt"] = removeReplaceBlock(
        template["qfmt"], clozeHideAllBlock.startMarker, clozeHideAllBlock.endMarker
    )
    template["qfmt"] = re.sub("<style>\s*</style>", "", template["qfmt"])
    template["qfmt"] = template["qfmt"].strip()
    template["qfmt"] = "<style>\n%s\n</style>\n\n%s" % (
        clozeHideAllBlock.blockRaw,
        template["qfmt"],
    )
    template["qfmt"] = template["qfmt"].replace("\r", "\n")
    template["qfmt"] = re.sub(r"\n{3,}", "\n\n", template["qfmt"])
    if oldQfmt != template["qfmt"]:
        templateUpdated[0] = True

    oldAfmt = template["afmt"]

    template["afmt"] = (
        template["afmt"]
        .replace(hideback_commented_header, hideback_block_header)
        .replace(hideback_commented_footer, hideback_block_footer)
    )

    template["afmt"] = removeReplaceBlock(template["afmt"], "\ncloze2 {", "}")
    template["afmt"] = removeReplaceBlock(template["afmt"], "\ncloze2_w {", "}")
    template["afmt"] = removeReplaceBlock(
        template["afmt"], clozeHideAllBlock.startMarker, clozeHideAllBlock.endMarker
    )
    template["afmt"] = re.sub("<style>\s*</style>", "", template["afmt"])

    if (hideback_block_header) in template["afmt"]:
        # TODO: <style> should preferrably be before the card content. Dunno if this is possible.
        template["afmt"] = template["afmt"].replace(
            hideback_block_header,
            "%s<style>\n%s\n</style>\n"
            % (hideback_block_header, clozeHideAllBlock.blockRaw),
        )
    else:
        # User might just have removed '{{#..}}' and '{{/..}}`, so that condition
        # always evaluates to true and other clozes won't be shown regardless
        # of {hideback_caption} field.
        template["afmt"] = "<style>\n%s\n</style>\n\n%s" % (
            clozeHideAllBlock.blockRaw,
            template["afmt"],
        )

    template["afmt"] = template["afmt"].replace("\r", "\n")
    template["afmt"] = re.sub(r"\n{3,}", "\n\n", template["afmt"])

    if getConfig("alwaysHideback"):
        template["afmt"] = (
            template["afmt"]
            .replace(hideback_block_header, hideback_commented_header)
            .replace(hideback_block_footer, hideback_commented_footer)
        )

    if oldAfmt != template["afmt"]:
        templateUpdated[0] = True

    # Remove cloze css on 'css' section. Cloze hide all related CSS except 'cz-hide'
    # moved to front & back template.
    oldCSS = clozeModel["css"]
    clozeModel["css"] = removeReplaceBlock(
        clozeModel["css"], clozeHideAllBlock.startMarker, clozeHideAllBlock.endMarker
    )
    clozeModel["css"] = re.sub(r"cloze2 \{(.|\n)*?\}", "", clozeModel["css"])

    # add .nightMode .cloze selector if appliable
    minifiedCSS = minifyCSS(clozeModel["css"])
    if (
        ".nightMode" not in minifiedCSS
        and ".night_mode" not in minifiedCSS
        and "cloze{font-weight:bold;color:blue}"  # CSS doesn't care night mode
        in minifiedCSS  # User haven't touched the cloze styling
    ):
        clozeModel[
            "css"
        ] += """\


.nightMode .cloze {
    color: lightblue;
}
"""

    clozeModel["css"] = clozeModel["css"].replace("\r", "\n")
    clozeModel["css"] = re.sub(r"\n{3,}", "\n\n", clozeModel["css"])
    if oldCSS != clozeModel["css"]:
        templateUpdated[0] = True

    if templateUpdated[0]:
        models.save(clozeModel)


def registerClozeModel():
    if getConfig("noModelMigration"):
        return

    """Prepare note type"""
    if not mw.col.models.byName(model_name):
        createClozeHideAllModel(mw.col)
    updateClozeModel(mw.col)
