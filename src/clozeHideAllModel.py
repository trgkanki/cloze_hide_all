from aqt import mw
from anki.consts import MODEL_CLOZE
from aqt.utils import askUser, showInfo

from .markerReplacer import (
    ScriptBlock,
    ReplaceBlock,
    removeScriptBlock,
    removeReplaceBlock
)

from .utils.resource import readResource
from .utils.configrw import getConfig
from .consts import model_name

import re

############################# Templates

oldScriptBlockHeader = '/* --- DO NOT DELETE OR EDIT THIS SCRIPT --- */'

revealClozeScript = ScriptBlock('409cac4f6e95b12d', readResource('scriptBlock/revealCurrentCloze.js'))
scrollToClozeSiteScript = ScriptBlock('1f91af7729e984b8', readResource('scriptBlock/scrollToCurrentCloze.js'))

card_front = readResource('template/qSide.html')
card_back = readResource('template/aSide.html')
card_css = readResource('template/style.css')
hideback_caption = u"Hide others on the back side"
hideback_html = readResource('template/hideback.html')

# Customizable cloze styles
try:
    hiddenClozeStyle = getConfig('hiddenClozeStyle')
    clozeHiddenContent = readResource('template/clozeHiddenUI/%s.css' % hiddenClozeStyle)
except IOError:
    showInfo('Cloze (Hide all) - Hidden cloze style %s not exists!' % hiddenClozeStyle)
    clozeHiddenContent = readResource('template/clozeHiddenUI/yellowBox.css')

cloze_css = ReplaceBlock('/* !-- a81b1bee0481ede2 */\n', '\n/* a81b1bee0481ede2 --! */', clozeHiddenContent)


###################################################################


def addClozeModel(col):
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
    return clozeModel


warningMsg = (
    "ClozeHideAll will update its card template. "
    "Sync your deck to AnkiWeb before pressing OK"
)


def updateClozeModel(col, warnUserUpdate=True):
    models = col.models
    clozeModel = mw.col.models.byName(model_name)

    # Add hideback caption
    if hideback_caption not in models.fieldNames(clozeModel):
        if warnUserUpdate and not askUser(warningMsg):
            return
        warnUserUpdate = False
        fld = models.newField(hideback_caption)
        fld["sticky"] = True
        models.addField(clozeModel, fld)

        template = clozeModel["tmpls"][0]
        template["afmt"] += "\n{{#%s}}\n%s\n{{/%s}}" % (
            hideback_caption,
            hideback_html,
            hideback_caption,
        )

        models.save()

    template = clozeModel["tmpls"][0]
    templateUpdated = [False]
    template["afmt"] = removeScriptBlock(template["afmt"], oldScriptBlockHeader, updated=templateUpdated)
    template["afmt"] = revealClozeScript.apply(template["afmt"], updated=templateUpdated)
    template["qfmt"] = scrollToClozeSiteScript.apply(template["qfmt"], updated=templateUpdated)

    # update cloze box related stylings
    oldQfmt = template['qfmt']
    template['qfmt'] = removeReplaceBlock(template['qfmt'], '\ncloze2 {', '}')
    template['qfmt'] = removeReplaceBlock(template['qfmt'], '\ncloze2_w {', '}')
    template['qfmt'] = re.sub('<style>\s*</style>', '', template['qfmt'])
    if oldQfmt != template['qfmt']:
        templateUpdated[0] = True

    oldAfmt = template['afmt']
    template['afmt'] = removeReplaceBlock(template['afmt'], '\ncloze2 {', '}')
    template['afmt'] = removeReplaceBlock(template['afmt'], '\ncloze2_w {', '}')
    template['afmt'] = re.sub('<style>\s*</style>', '', template['afmt'])
    if oldAfmt != template['afmt']:
        templateUpdated[0] = True

    # Apply css of hidden clozes
    clozeModel["css"] = cloze_css.apply(clozeModel["css"], updated=templateUpdated)

    # Apply css of <cloze2> element (should be hidden by default)
    try:
        clozeModel["css"].index('cloze2 {\n')
    except ValueError:
        clozeModel["css"] += '\ncloze2 {\n  display: none;\n}'
        templateUpdated[0] = True

    if templateUpdated[0]:
        models.save()


def registerClozeModel():
    """Prepare note type"""
    if not mw.col.models.byName(model_name):
        addClozeModel(mw.col)
    updateClozeModel(mw.col)
