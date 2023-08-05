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

from assertpy import assert_that

from fluidtopics.connector.helpers.publication_checker import MetadataChecker
from fluidtopics.connector.model.metadata_update import PublicationMetadata, MetadataAction


class PublicationMetadataChecker:
    """Helper to check a PublicationMetadata."""

    def __init__(self, metadata_update: PublicationMetadata):
        """Create a PublicationMetadataChecker.

        :param metadata_update: PublicationMetadata to check."""
        self.metadata_update = metadata_update

    def __repr__(self):
        return 'MetadataChecker({})'.format(self.metadata_update)

    def has_publication_id(self, publication_id: str) -> 'PublicationMetadataChecker':
        assert_that(self.metadata_update).has_pub_id(publication_id)
        return self

    def has_action(self, action: MetadataAction) -> 'PublicationMetadataChecker':
        assert_that(self.metadata_update).has_action(action)
        return self

    def metadata(self) -> List[MetadataChecker]:
        """Return checkers on all updated metadata."""
        return [MetadataChecker(m) for m in self.metadata_update.meta]

    def meta(self, meta_key: str) -> MetadataChecker:
        """Return a checker on a specific metadata.

        :param meta_key: Key of the specific metadata.
        :raises:
            AssertionError: No Metadata with this key has been updated"""
        meta = next((MetadataChecker(m) for m in self.metadata_update.meta if m.key == meta_key), None)
        assert_that(meta) \
            .described_as('Metadata {} not found in {}'.format(meta_key, [m.key for m in self.metadata_update.meta])) \
            .is_not_none()
        return meta
