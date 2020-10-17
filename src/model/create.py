from anki.consts import MODEL_CLOZE

from ..utils.configrw import setConfig

from .consts import model_name, card_front, card_back, card_css, hideback_caption
from .migrator import updateClozeModel


def createClozeHideAllModel(col):
    models = col.models
    clozeModel = models.new(model_name)
    clozeModel["type"] = MODEL_CLOZE

    # Add fields
    for fieldName in ("Text", "Extra"):
        fld = models.newField(fieldName)
        models.addField(clozeModel, fld)

    fld = models.newField(hideback_caption)
    fld["sticky"] = True
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
