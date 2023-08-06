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

from typing import List

from autovalue import autovalue

from fluidtopics.connector.model.metadata import Metadata


class MetadataAction(Enum):
    """Specify what to do with metadata in PublicationMetadata.

    REPLACE: replace all metadata by these specified in PublicationMetadata
    UPDATE: Add metadata or update their values if they already exists"""
    REPLACE = 1
    UPDATE = 2


@autovalue
class PublicationMetadata:
    """Specify metadata update to do for a given publication."""
    def __init__(self, pub_id: str, action: MetadataAction, meta: List[Metadata]):
        """Create a PublicationMetadata.

        :param pub_id: Khub ID of the publication
        :param action: UPDATE or REPLACE metadata for this publication
        :param meta: List of updated metadata (metadata journal is ignored)"""
        self.pub_id = pub_id
        self.action = action
        self.meta = meta

    def __eq__(self, other: 'PublicationMetadata') -> bool:
        return self is not None and self.pub_id == other.pub_id \
               and self.action == other.action \
               and len(self.meta) == len(other.meta) \
               and all(m in other.meta for m in self.meta) \
               and all(m in self.meta for m in other.meta)


@autovalue
class MetadataUpdates:
    """List of all metadata update to do."""
    def __init__(self, updates: List[PublicationMetadata]):
        self.updates = updates
