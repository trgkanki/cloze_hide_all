from anki.consts import MODEL_CLOZE

from .consts import model_name, hideback_caption, card_front, card_back, card_css
from .migrator import updateClozeModel
from ..utils.configrw import setConfig


def resetClozeHideModel(col):
    models = col.models
    clozeModel = col.models.byName(model_name)
    template = clozeModel["tmpls"][0]
    template["qfmt"] = card_front
    template["afmt"] = card_back
    clozeModel["css"] = card_css
    updateClozeModel(col, False)
    models.save(clozeModel)

    # Set alwaysHideBack to true for new users
    setConfig("alwaysHideback", True)

    return clozeModel
