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
from .utils.cssHelper import minifyCSS
from .consts import model_name

from .model.migrator.frontSide import migrateFrontSide
from .model.migrator.backSide import migrateBackSide
from .model.migrator.css import migrateModelCSS

import re

############################# Templates

card_front = readResource("template/qSide.html")
card_back = readResource("template/aSide.html")
card_css = readResource("template/style.css")
hideback_caption = u"Hide others on the back side"
hideback_html = readResource("template/hideback.html")

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

    # update cloze box related stylings
    template["qfmt"] = migrateFrontSide(template["qfmt"], templateUpdated)
    template["afmt"] = migrateBackSide(template["afmt"], templateUpdated)
    clozeModel["css"] = migrateModelCSS(clozeModel["css"], templateUpdated)

    if templateUpdated[0]:
        models.save(clozeModel)


def registerClozeModel():
    if getConfig("noModelMigration"):
        return

    """Prepare note type"""
    if not mw.col.models.byName(model_name):
        createClozeHideAllModel(mw.col)
    updateClozeModel(mw.col)
