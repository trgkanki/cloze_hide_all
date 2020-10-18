from aqt import mw
from .utils.configrw import getConfig
from .model.consts import model_name

from .model.migrator import updateClozeModel
from .model.create import createClozeHideAllModel


def registerClozeModel():
    if getConfig("noModelMigration"):
        return

    """Prepare note type"""
    if not mw.col.models.byName(model_name):
        createClozeHideAllModel(mw.col)
    updateClozeModel(mw.col)
