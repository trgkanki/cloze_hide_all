from aqt import mw
from aqt.qt import QAction
from aqt.utils import askUser, tooltip

from .utils.configrw import getConfig
from .model.consts import model_name

from .model.migrator import updateClozeModel
from .model.create import createClozeHideAllModel
from .model.reset import resetClozeHideModel


def registerClozeModel():
    if getConfig("noModelMigration"):
        return

    """Prepare note type"""
    if not mw.col.models.byName(model_name):
        createClozeHideAllModel(mw.col)
    updateClozeModel(mw.col)


## Reset button for template reset
def addResetModelButton():
    def _():
        # This could happen on environment like macOS, where menu item can be
        # clicked without main window being visible (e.g: no profile loaded)
        if not mw.col:
            return

        if askUser(
            "Really reset the model template? This will wipe all your UI customization."
        ):
            resetClozeHideModel(mw.col)
            mw.reset()
            tooltip("Template reset")

    action = QAction("(Warning) Reset template of Cloze (Hide All)", mw)
    action.triggered.connect(_)
    mw.form.menuHelp.addAction(action)


addResetModelButton()
