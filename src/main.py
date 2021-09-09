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

from anki.hooks import addHook, wrap

from .htmlApplier import stripClozeTags, applyClozeTags
from .clozeHideAllModel import registerClozeModel
from .model.consts import model_name
from .utils.resource import readResource
from .utils.configrw import getConfig
from .utils import openChangelog
from .utils import uuid  # duplicate UUID checked here


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# Main code
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

addHook("profileLoaded", registerClozeModel)


def updateNote(note):
    for key in note.keys():
        html = note[key]
        html = stripClozeTags(html)
        html = applyClozeTags(html)
        note[key] = html


## Hooks

# Hide 'hideback' field on note load


def onSetNote(self, note, hide=True, focus=False):
    if not self.web:
        return

    if self.note and self.note.model()["name"] == model_name:
        if getConfig("alwaysHideback"):
            hidebackJS = readResource("scriptBlock/hideHidebackField.js")
            self.web.eval(hidebackJS)


if hasattr(Editor, "set_note"):  # 2.1.46+ fix
    Editor.set_note = wrap(Editor.set_note, onSetNote, "after")
    Editor.setNote = Editor.set_note
else:
    Editor.setNote = wrap(Editor.setNote, onSetNote, "after")

# Apply CHA code before save


def beforeSaveNow(self, callback, keepFocus=False, *, _old):
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
