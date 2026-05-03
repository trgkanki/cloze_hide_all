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
import os
import time
import traceback

from aqt.editor import Editor
from aqt.reviewer import Reviewer
from aqt import gui_hooks
from anki.hooks import wrap
from anki import hooks
from anki.notes import Note

from typing import List

from .htmlApplier import stripClozeTags, applyClozeTags, ClozeIdState
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
from .utils import debugLog

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# Main code
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

gui_hooks.profile_did_open.append(registerClozeModel)


## Hooks


def isNoteClozeHideAllType(note):
    noteModelName = note.model()["name"]
    extraModelNames = getConfig("clozeHideAllModelNames")
    return noteModelName == model_name or noteModelName in extraModelNames


def beforeNoteFlush(note):
    useCHA = False
    if isNoteClozeHideAllType(note):
        useCHA = "note_type"
    else:
        for key in note.keys():
            if "cha-enable" in note[key]:
                useCHA = "card"
                break

    state = ClozeIdState()

    if useCHA:
        for key in note.keys():
            html = note[key]
            html = stripClozeTags(html)
            html = applyClozeTags(html, state)

            if useCHA == "card":
                html = hidebackBlock.remove(html)
                html = stripChaScriptToHTML(html)
                html = applyChaScriptToHTML(html)
                if html:
                    html = hidebackBlock.apply(html)

            note[key] = html
    else:
        for key in note.keys():
            html = note[key]
            html = stripClozeTags(html)
            html = stripChaScriptToHTML(html)
            html = hidebackBlock.remove(html)
            note[key] = html


hooks.note_will_flush.append(beforeNoteFlush)


## Support for 'reveal' shortcut
def newShortuts(self, *, _old):
    def _():
        self.web.eval("toggleCHA()")

    shortcuts = _old(self)
    shortcuts.append((getConfig("shortcutToggleMask", "ctrl+r"), _))
    return shortcuts


Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, newShortuts, "around")

## "Cloze hide all" button


def _add_cloze_hide_all_marker(editor: Editor) -> None:
    editor.web.eval("setFormat('inserthtml', '<img src=_cha_cha-enable.png>');")


def _add_conditional_visible_cloze_area(editor: Editor) -> None:
    editor.web.eval("wrap('<div class=\"cz_on_active\">', '</div>');")


def add_buttons(buttons: List[str], editor: Editor) -> None:
    buttons.append(
        editor.addButton(
            icon=None,
            cmd=f"add_cloze_hide_all_marker",
            func=_add_cloze_hide_all_marker,
            tip="Add CHA reveal button here (%s)" % getConfig("cha_marker_shortcut"),
            label="█ CHA",
        )
    )

    buttons.append(
        editor.addButton(
            icon=None,
            cmd=f"add_conditional_visible_cloze_area",
            func=_add_conditional_visible_cloze_area,
            tip="Add conditional CHA visible area (%s)"
            % getConfig("cha_conditional_zone_shortcut"),
            label="『cond』",
        )
    )


def setup_shortcuts(shortcuts, editor):
    shortcuts.append(
        (getConfig("cha_marker_shortcut"), lambda: _add_cloze_hide_all_marker(editor))
    )
    shortcuts.append(
        (
            getConfig("cha_conditional_zone_shortcut"),
            lambda: _add_conditional_visible_cloze_area(editor),
        )
    )


gui_hooks.editor_did_init_buttons.append(add_buttons)
gui_hooks.editor_did_init_shortcuts.append(setup_shortcuts)


# code from https://github.com/ijgnd/anki__editor__apply__font_color__background_color__custom_class__custom_style/blob/master/src/editor/webview.py#L6
def append_css_to_editor(js, note, editor) -> str:
    return js + readResource("assets/editorAddActiveOnlyCSS.js")


gui_hooks.editor_will_load_note.append(append_css_to_editor)
