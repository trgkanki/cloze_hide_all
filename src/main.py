# Copyright (C) 2020 Hyun Woo Park
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
#
# cloze_hide_all v20.9.26i168
#
# Copyright: trgk (phu54321@naver.com)
# License: GNU AGPL, version 3 or later;
# See http://www.gnu.org/licenses/agpl.html

import re

from aqt.editor import Editor
from aqt.reviewer import Reviewer
from aqt import gui_hooks, mw
from anki.hooks import wrap
from aqt.utils import tooltip

from typing import List

from .htmlApplier import stripClozeTags, applyClozeTags
from .clozeHideAllModel import registerClozeModel
from .model.consts import model_name
from .model.migrator.common import (
    stripChaScriptToHTML,
    applyChaScriptToHTML,
    hidebackBlock,
)
from .utils.resource import readResource
from .utils.configrw import getConfig
from .utils import openChangelog
from .utils import uuid  # duplicate UUID checked here


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# Main code
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

gui_hooks.profile_did_open.append(registerClozeModel)


## Hooks

# Hide 'hideback' field on note load


def isNoteClozeHideAllType(note):
    noteModelName = note.model()["name"]
    extraModelNames = getConfig("clozeHideAllModelNames")
    return noteModelName == model_name or noteModelName in extraModelNames


def onSetNote(self, note, hide=True, focus=False):
    if not self.web:
        return

    if self.note and isNoteClozeHideAllType(self.note):
        if getConfig("alwaysHideback"):
            hidebackJS = readResource("assets/hideHidebackField.js")
            self.web.eval(hidebackJS)


if hasattr(Editor, "set_note"):  # 2.1.46+ fix
    Editor.set_note = wrap(Editor.set_note, onSetNote, "after")
    Editor.setNote = Editor.set_note
else:
    Editor.setNote = wrap(Editor.setNote, onSetNote, "after")

# Apply CHA code before save


def findFieldsInTemplate(template: str) -> List[str]:
    fields: List[str] = []
    for m in re.findall(r"\{\{(?:.+?::?)?(.+?)\}\}", template):
        # skip conditional rendering
        if m[0] == "#" or m[0] == "/":
            continue
        fields.append(m)
    return fields


def beforeSaveNow(self, callback, keepFocus=False, *, _old):
    def newCallback():
        # self.note may be None when editor isn't yet initialized.
        # ex: entering browser
        note = self.note
        if note and not keepFocus:
            useCHA = False
            if isNoteClozeHideAllType(note):
                useCHA = "note_type"
            else:
                for key in note.keys():
                    if "cha-enable" in note[key]:
                        useCHA = "card"
                        break

            if useCHA:
                qFields: List[str] = []
                aFields: List[str] = []
                if useCHA == "card":
                    model = mw.col.models.get(note.mid)
                    template = model["tmpls"][0]
                    qFields = findFieldsInTemplate(template["qfmt"])
                    aFields = findFieldsInTemplate(template["afmt"])

                for key in note.keys():
                    html = note[key]
                    html = stripClozeTags(html)
                    html = applyClozeTags(html)

                    if useCHA == "card":
                        html = applyChaScriptToHTML(html)
                        if key in aFields and key not in qFields:
                            html = hidebackBlock.apply(html)

                    note[key] = html
            else:
                for key in note.keys():
                    html = note[key]
                    html = stripClozeTags(html)
                    html = stripChaScriptToHTML(html)
                    html = hidebackBlock.remove(html)
                    note[key] = html

            if not self.addMode:
                note.flush()
                self.mw.requireReset()

        callback()

    return _old(self, newCallback, keepFocus)


if hasattr(Editor, "call_after_note_saved"):  # 2.1.46+ fix
    Editor.call_after_note_saved = wrap(
        Editor.call_after_note_saved, beforeSaveNow, "around"
    )
    Editor.saveNow = Editor.call_after_note_saved

else:
    Editor.saveNow = wrap(Editor.saveNow, beforeSaveNow, "around")


#### Hook for HTML edit


def _newOnHtmlEdit(self, field, *, _old):
    # Temporarily strip CHA-related tags
    self.note.fields[field] = stripClozeTags(self.note.fields[field])
    ret = _old(self, field)
    self.note.fields[field] = applyClozeTags(self.note.fields[field])
    return ret


# Fix for 2.1.46+ needed.
Editor._onHtmlEdit = wrap(Editor._onHtmlEdit, _newOnHtmlEdit, "around")


## Support for 'reveal' shortcut
def newShortuts(self, *, _old):
    def _():
        self.web.eval("toggle()")

    shortcuts = _old(self)
    shortcuts.append((getConfig("shortcutToggleMask", "ctrl+r"), _))
    return shortcuts


Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, newShortuts, "around")

## "Cloze hide all" button


def add_buttons(buttons: List[str], editor: Editor) -> None:
    shortcut = "Ctrl+Alt+Shift+H"

    def _(editor: Editor) -> None:
        editor.web.eval("setFormat('inserthtml', '<img src=_cha_cha-enable.png>');")

    buttons.append(
        editor.addButton(
            icon=None,
            cmd=f"add_cloze_hide_all_marker",
            func=_,
            tip="Make this note like 'Cloze (Hide All)'",
            label="█ CHA",
            keys=shortcut,
        )
    )


gui_hooks.editor_did_init_buttons.append(add_buttons)
