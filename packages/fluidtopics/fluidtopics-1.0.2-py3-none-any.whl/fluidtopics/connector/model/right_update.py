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

from typing import List

from autovalue import autovalue
from deprecated.sphinx import deprecated

from fluidtopics.connector.model.right import Rights


@autovalue
class PublicationRights:
    """Specify rights update to do for a given publication."""

    def __init__(self, pub_id: str, rights: Rights):
        """Create a PublicationRights.

        :param pub_id: Khub ID of the publication.
        :param rights: Rights to apply to the publication."""
        self.pub_id = pub_id
        self.rights = rights


@autovalue
@deprecated(reason='Prefer using metadata with content access right')
class RightsUpdates:
    """List all of right update to do."""

    def __init__(self, updates: List[PublicationRights]):
        self.updates = updates
