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
from typing import Union, Dict

from fluidtopics.connector.model.has_metadata import HasMetadata
from fluidtopics.connector.model.metadata import Metadata, SemanticMetadata, InvalidMetadata


class InvalidDocument(ValueError):
    pass


class Document(HasMetadata):
    """Document is an abstract class for elements which can be published to Fluid Topics.

    Known implementations are:
    * StructuredDocument for a standard document, made up of topics
    * UnstructuredDocument for an arbitrary binary file (PDF, image, Word document, ...)
    * ExternalDocument for a document hosted outside of Fluid Topics
    """

    def __init__(self, document_id: str,
                 metadata: Dict[str, Metadata] = None):
        if not document_id:
            raise InvalidDocument('Document ID is mandatory: "{}" is not a valid ID.'.format(document_id))
        try:
            super().__init__(metadata)
            self._check_mandatory_metadata(metadata, SemanticMetadata.LOCALE)
        except InvalidMetadata as e:
            raise InvalidDocument('Invalid document "{}": {}'.format(document_id, e))
        self.document_id = document_id

    @property
    def locale(self) -> str:
        """Access Document locale stored in ft:locale Metadata."""
        # noinspection PyTypeChecker
        # By design, locale is always present in the metadata dict
        return self._get_metadata_value(SemanticMetadata.LOCALE)

    def update_locale(self, new_locale: Union[str, Metadata]) -> 'Document':
        """Create a copy of this Document with the new locale.

        Previous locale value is not stored in Metadata journal.
        """
        return self._update_semantic_metadata(new_locale, Metadata.locale)

    def _update_metadata(self, new_metadata: Dict[str, Metadata]) -> 'Document':
        raise NotImplementedError
