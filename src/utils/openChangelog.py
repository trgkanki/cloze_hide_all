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

from aqt import mw
from aqt.utils import askUser, showText, showInfo

import os

from .configrw import getCurrentAddonName, setConfig
from .resource import readResource, getResourcePath
from .MiniBrowser import MiniBrowser


def getCurrentAddonVersion():
    return readResource("VERSION")


def showChangelogOnUpdate():
    addonVersion = getCurrentAddonVersion()
    addonName = getCurrentAddonName()

    addonMeta = mw.addonManager.addonMeta(addonName)
    if addonMeta.get("human_version", None) != addonVersion:
        if askUser(
            """IMPORTANT!!

This addon has a history of breaking user cards during migration steps.\
If your addon is working well, ***We recommend just pressing YES here***.

But if your addon doesn't, new addon *might* contain a migration to fix\
your current issue, so we recommend presssing *no* here.

Would you like to prevent addon from auto-migrating your templates?
"""
        ):
            showInfo(
                "You can always issue migration on addon config. Check out the `noModelMigration` option."
            )
            setConfig("noModelMigration", True)

        addonMeta["human_version"] = addonVersion
        mw.addonManager.writeAddonMeta(addonName, addonMeta)

        changelogPath = getResourcePath("CHANGELOG.html")
        if os.path.exists(changelogPath):
            dlg = MiniBrowser(None, "CHANGELOG.html")
            dlg.exec()


showChangelogOnUpdate()
