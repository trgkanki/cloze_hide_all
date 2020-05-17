# -*- coding: utf-8 -*-
#
# addon_template v20.5.4i8
#
# Copyright: trgk (phu54321@naver.com)
# License: GNU AGPL, version 3 or later;
# See http://www.gnu.org/licenses/agpl.html

# -*- mode: Python ; coding: utf-8 -*-
#
# Cloze (Hide All) - v6
#   Adds a new card type "Cloze (Hide All)", which hides all clozes on its
#   front and optionally on the back.
#
# Changelog
#  v6: support anki 2.1
#  v5 : DOM-boundary crossing clozes will be handled properly
#  .1 : More rubust DOM boundary handling
#        Compatiable with addon 719871418
#  v4 : Prefixing cloze content with ! will make it visibile on other clozes.
#        Other hidden content's size will be fixed. (No automatic update)
#  .1 : Fixed bug when editing notes (EditCurrent hook, better saveNow hook)
#       Fixed issues where wrong fields are marked as 'sticky'
#  v3 : Fixed issues which caused text to disappear on the mac version,
#        Added option to hide other clozes on the back.
#  v2 : Support clozes with hint
#  v1 : Initial release
#
# Copyright © 2019 Hyun Woo Park (phu54321@naver.com)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Lots of code from
#   - Cloze overlapper (by Glutaminate)
#   - Batch Note Editing (by Glutaminate)
#

import re

from aqt.editor import Editor
from aqt.browser import ChangeModel
from aqt.utils import askUser
from anki.hooks import addHook, wrap
from anki import version

from anki.consts import MODEL_CLOZE
from aqt import mw

from .applyClozeHide import (
    tokenizeHTML,
    optimizeChunks
)

from .updateScriptBlock import (
    ScriptBlock,
    removeScriptBlock
)

from .utils.resource import readResource

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ TEMPALTES

model_name = u"Cloze (Hide all)"

oldScriptBlockHeader = '/* --- DO NOT DELETE OR EDIT THIS SCRIPT --- */'

revealClozeScript = ScriptBlock('409cac4f6e95b12d', readResource('scriptBlock/revealCurrentCloze.js'))
scrollToClozeSiteScript = ScriptBlock('1f91af7729e984b8', readResource('scriptBlock/scrollToCurrentCloze.js'))

card_front = """
<style>
cloze2 {
    display: none;
}

cloze2_w {
    display: inline-block;
    width: 5em;
    height: 1em;
    background-color: #ffeba2;
}
</style>

{{cloze:Text}}
"""

card_back = """
{{cloze:Text}}
{{#Extra}}
<hr>
{{Extra}}
{{/Extra}}
"""

card_css = """
.card {
    font-family: Arial;
    font-size: 20px;
    color: black;
    background-color: white;
}

.cloze {
    font-weight: bold;
    color: blue;
}

cz_hide {
    display: none;
}
"""

hideback_caption = u"Hide others on the back side"

hideback_html = """<style>
cloze2 {
    display: none;
}

cloze2_w {
    display: inline-block;
    width: 5em;
    height: 1em;
    background-color: #ffeba2;
}

.cloze cloze2 {
    display: inline;
}

.cloze cloze2_w {
    display: none;
}

cloze2.reveal-cloze2 {
    display: inline;
}

cloze2_w.reveal-cloze2 {
    display: none;
}

.cloze2-toggle {
    -webkit-appearance: none;
    display: block;
    font-size: 1.3em;
    height: 2em;
    background-color: #ffffff;
    width: 100%;
    margin-top: 20px;
}

.cloze2-toggle:active {
    background-color: #ffffaa;
}
</style>

<script>
function toggle() {
var elements = document.querySelectorAll('cloze2, cloze2_w');
    for(var i = 0 ; i < elements.length ; i++) {
        elements[i].classList.toggle('reveal-cloze2');
    }
}
</script>

<button class='cloze2-toggle' onclick='toggle()'>Toogle mask</button>"""

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ TEMPALTES


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# Main code
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


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

    if templateUpdated[0]:
        models.save()


def registerClozeModel():
    """Prepare note type"""
    if not mw.col.models.byName(model_name):
        addClozeModel(mw.col)
    updateClozeModel(mw.col)


addHook("profileLoaded", registerClozeModel)

# Editor


def stripClozeHelper(html):
    return re.sub(
        r"</?(cz_hide|cloze2|cloze2_w)>|"
        + r"<(cloze2_w|cloze2) class=(\"|')cz-\d+(\"|')>|"
        + r"<script( class=(\"|')cz-\d+(\"|'))?>_czha\(\d+\)</script>",
        "",
        html,
    )


def wrapClozeTag(segment, clozeId):
    """
    Cloze may span across DOM boundary. This ensures that clozed text
    in elements different from starting element to be properly hidden
    by enclosing them by <cloze2>
    """

    output = ["<cloze2_w class='cz-%d'></cloze2_w>" % clozeId]
    cloze_header = "<cloze2 class='cz-%d'>" % clozeId
    cloze_footer = "</cloze2>"

    chunks = tokenizeHTML(segment)
    chunks = optimizeChunks(chunks)

    for chunk in chunks:
        if chunk[0] == 'raw':
            output.append(cloze_header)
            output.append(chunk[1])
            output.append(cloze_footer)
        else:
            output.append(chunk[1])

    return "".join(output)


def makeClozeCompatiable(html):
    html = re.sub(
        r"\{\{c(\d+)::([^!]([^:}]|:[^:}])*?)\}\}",
        lambda match: "{{c%s::%s}}"
        % (match.group(1), wrapClozeTag(match.group(2), int(match.group(1)))),
        html,
    )
    html = re.sub(
        r"\{\{c(\d+)::([^!]([^:}]|:[^:}])*?)::(([^:}]|:[^:}])*?)\}\}",
        lambda match: "{{c%s::%s::%s}}"
        % (
            match.group(1),
            wrapClozeTag(match.group(2), int(match.group(1))),
            match.group(4),
        ),
        html,
    )
    html = re.sub(r"\{\{c(\d+)::!", "{{c\\1::<cz_hide>!</cz_hide>", html)
    return html


def updateNote(note):
    for key in note.keys():
        html = note[key]
        html = stripClozeHelper(html)
        html = makeClozeCompatiable(html)
        note[key] = html


def beforeSaveNow(self, callback, keepFocus=False, *, _old):
    """Automatically generate overlapping clozes before adding cards"""

    def newCallback():
        # self.note may be None when editor isn't yet initialized.
        # ex: entering browser
        if self.note and self.note.model()["name"] == model_name:
            updateNote(self.note)
            if not self.addMode:
                self.note.flush()
                self.mw.requireReset()
        callback()

    return _old(self, newCallback, keepFocus)


Editor.saveNow = wrap(Editor.saveNow, beforeSaveNow, "around")

# Batch change node types on card type change


def applyClozeFormat(browser, nids):
    mw = browser.mw
    mw.checkpoint("Note type change to cloze (reveal one)")
    mw.progress.start()
    browser.model.beginReset()
    for nid in nids:
        note = mw.col.getNote(nid)
        updateNote(note)
        note.flush()
    browser.model.endReset()
    mw.requireReset()
    mw.progress.finish()
    mw.reset()


def onChangeModel(self):
    if self.targetModel["name"] == model_name:
        applyClozeFormat(self.browser, self.nids)


ChangeModel.accept = wrap(ChangeModel.accept, onChangeModel, "before")
