# Copyright 2020 Antidot opensource@antidot.net
#
# This file is part of Fluid Topics python API
#
# Fluid Topics python API is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# Fluid Topics python API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from enum import Enum
from typing import List

from autovalue import autovalue
from pyckson import caseinsensitive


@caseinsensitive
class FsonAccessLevel(Enum):
    PUBLIC = 1
    AUTHENTICATED = 2
    RESTRICTED = 3


@autovalue
class FsonRights:
    def __init__(self, access_level: FsonAccessLevel = FsonAccessLevel.PUBLIC, groups: List[str] = None):
        self.access_level = access_level
        self.groups = groups or []

    @staticmethod
    def public():
        return FsonRights(FsonAccessLevel.PUBLIC)

    @staticmethod
    def authenticated():
        return FsonRights(FsonAccessLevel.AUTHENTICATED)

    @staticmethod
    def restricted(groups: List[str]):
        return FsonRights(FsonAccessLevel.RESTRICTED, groups)
