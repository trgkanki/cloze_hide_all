from ..consts import model_name, hideback_caption
from .frontSide import migrateFrontSide
from .backSide import migrateBackSide
from .css import migrateModelCSS


def updateClozeModel(col, warnUserUpdate=True):
    models = col.models
    clozeModel = col.models.byName(model_name)
    template = clozeModel["tmpls"][0]
    templateUpdated = [False]

    # update cloze box related stylings
    template["qfmt"] = migrateFrontSide(template["qfmt"], templateUpdated)
    template["afmt"] = migrateBackSide(clozeModel, template["afmt"], templateUpdated)
    clozeModel["css"] = migrateModelCSS(clozeModel["css"], templateUpdated)

    if templateUpdated[0]:
        models.save(clozeModel)
