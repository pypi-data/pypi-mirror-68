# Copyright 2019 Antidot opensource@antidot.net
#
# This file is part of Fluid-Topics python API
#
# Fluid-Topics python API is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# Fluid-Topics python API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from enum import Enum
from typing import List, Iterable

from autovalue import autovalue
from deprecated.sphinx import deprecated
from pyckson import caseinsensitive


@caseinsensitive
@deprecated(reason='Prefer using metadata with content access right')
class AccessLevel(Enum):
    """Determine the access level of a Rights object.

    PUBLIC is accessible to everybody.
    AUTHENTICATED is accessible to logged in users.
    RESTRICTED is accessible to users in specific groups."""
    PUBLIC = 1
    AUTHENTICATED = 2
    RESTRICTED = 3


@autovalue
@deprecated(reason='Prefer using metadata with content access right')
class Rights:
    """Determine arbitrarily the access level of a publication.

    This access level override content access right rule.
    Specify groups field when you use RESTRICTED access level.
    You can use public(), authenticated(), restricted(['user-group']) to create
    Rights of the corresponding access level."""
    def __init__(self, access_level: AccessLevel = AccessLevel.PUBLIC, groups: List[str] = None):
        self.access_level = access_level
        self.groups = groups if groups is not None else []

    @staticmethod
    def public() -> 'Rights':
        """Create a public Rights.

        The Publication will be visible by everybody."""
        return Rights(AccessLevel.PUBLIC)

    @staticmethod
    def authenticated() -> 'Rights':
        """Create an authenticated Rights.

        The Publication will only be visible by authenticated users."""
        return Rights(AccessLevel.AUTHENTICATED)

    @staticmethod
    def restricted(groups: Iterable[str]) -> 'Rights':
        """Create a Rights restricted to some groups.

        The Publication will only be visible by users which belong to one of the
        specified groups.
        :param groups: Groups allowed to see the Publication."""
        return Rights(AccessLevel.RESTRICTED, list(groups))
