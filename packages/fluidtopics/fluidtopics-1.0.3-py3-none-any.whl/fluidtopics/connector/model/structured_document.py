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
from typing import List, Iterable, Union, Optional, Dict

from autovalue import autovalue

from fluidtopics.connector.model.attachment import Attachment
from fluidtopics.connector.model.document import Document, InvalidDocument
from fluidtopics.connector.model.has_metadata import build_metadata_map
from fluidtopics.connector.model.metadata import Metadata, EditorialType, InvalidMetadata, DEFAULT_LOCALE, \
    SemanticMetadata
from fluidtopics.connector.model.resource import Resource
from fluidtopics.connector.model.topic import Topic


class InvalidStructuredDocument(ValueError):
    pass


@autovalue
class StructuredDocument(Document):
    """Standard Document, made up of topics organized in a table of contents (TOC).

    A StructuredDocument object is immutable: once created, it is not possible to modify it.
    To create another StructuredDocument objectobject  from this one, use `.update()` method.
    Example:
    >>> document = StructuredDocument.create('id', 'title', [])
    >>> document.update(document_id='new_id', resources=[Resource('rid', b'')])
    StructuredDocument(document_id=new_id, title=title, toc=[], resources=[Resource(resource_id=rid, content=b'')])

    `.update()` only works for StructuredDocument object attributes. To update semantic Metadata (base ID, locale, ...),
    use corresponding `.update_*()` method.
    Example:
    >>> document = StructuredDocument.create('id', 'title', [], base_id='baseId')
    >>> document.update_base_id('newBaseId')
    StructuredDocument(document_id=id, title=title, toc=[], base_id=newBaseId)
    """

    def __init__(self, document_id: str,
                 toc: List[Topic],
                 metadata: Dict[str, Metadata] = None,
                 resources: Iterable[Resource] = None,
                 attachments: Iterable[Attachment] = None):
        """Create a StructuredDocument. It is recommended to use `StructuredDocument.create()` instead.

        :param document_id: Origin ID of the document. Should not be empty.
        :param toc: Table of contents. List of document root topics (sub-topics are stored in Topic `.children` field).
        :param metadata: Metadata of the document indexed by key. Contains client and semantic Metadata.
        :param resources: Resources used in topic HTML.
        :param attachments: Map attachment of the document.
        :raises: InvalidStructuredDocument: Data integrity criteria are not respected.
        """
        try:
            super().__init__(
                document_id=document_id,
                metadata=metadata)
        except InvalidDocument as e:
            raise InvalidStructuredDocument(e)
        resources = resources or set()
        attachments = attachments or set()
        resource_ids = [r.resource_id for r in resources]
        if len(resource_ids) != len(set(resource_ids)):
            raise InvalidStructuredDocument('Resource list should not contains duplicate IDs')
        attachment_filenames = [a.filename for a in attachments]
        if len(attachment_filenames) != len(set(attachment_filenames)):
            raise InvalidStructuredDocument('Attachment list should not contains duplicate filenames')
        self.toc = toc
        self.resources = set(resources)
        self.attachments = set(attachments)

    @staticmethod
    def create(document_id: str,
               title: Union[str, Metadata],
               toc: List[Topic],
               locale: Union[str, Metadata] = DEFAULT_LOCALE,
               base_id: Optional[Union[str, Metadata]] = None,
               description: Optional[Union[str, Metadata]] = None,
               last_edition: Optional[Union[str, Metadata]] = None,
               pretty_url: Optional[Union[str, Metadata]] = None,
               editorial_type: Union[EditorialType, Metadata] = EditorialType.BOOK,
               metadata: Iterable[Metadata] = None,
               resources: Iterable[Resource] = None,
               attachments: Iterable[Attachment] = None) -> 'StructuredDocument':
        """Create a StructuredDocument.

        :param document_id: Origin ID of the document. Should not be empty.
        :param title: Title of the document.
        :param toc: Table of contents. List of document root topics (sub-topics are stored in Topic `.children` field).
        :param locale: ISO locale code of the document. Set ft:locale Metadata. Default: `en-US`.
        :param base_id: ID used to link this document and cluster it.
            Set ft:baseId Metadata. Fallback to document_id when not specified.
        :param description: Description used for search engines. Set ft:description Metadata.
        :param last_edition: Last time this document was modified. Should respect YYYY-MM-DD format.
            Set ft:lastEdition Metadata. Fallback to publication date when not specified.
        :param pretty_url: Set ft:prettyUrl Metadata.
            For more information about pretty URLs: https://doc.antidot.net/go/FT/37/Pretty_URL.
        :param editorial_type: Defines if the document is a book or an article. Set ft:editorialType Metadata.
        :param metadata: Metadata of the document. When multiple Metadata have the same key, the last one
            is used and others are stored in Metadata journal. Semantic Metadata overrides corresponding
            attributes. For example: ft:title Metadata overrides given title (which is stored in Metadata journal).
        :param resources: Resources used in topic HTML.
        :param attachments: Map attachment of the document.
        :raises: InvalidStructuredDocument: Data integrity criteria are not respected.
        """
        try:
            metadata_map = build_metadata_map(
                object_id=document_id,
                title=title,
                base_id=base_id,
                locale=locale,
                description=description,
                last_edition=last_edition,
                pretty_url=pretty_url,
                editorial_type=editorial_type,
                metadata=metadata)
        except InvalidMetadata as e:
            raise InvalidStructuredDocument('Invalid structured document "{}": {}'.format(document_id, e))
        return StructuredDocument(
            document_id=document_id,
            toc=toc,
            metadata=metadata_map,
            resources=resources,
            attachments=attachments)

    @property
    def editorial_type(self) -> EditorialType:
        """Access editorial type stored in ft:editorialType Metadata."""
        str_type = self._get_metadata_value(SemanticMetadata.EDITORIAL_TYPE)
        return EditorialType(str_type)

    def update_editorial_type(self, editorial_type: Union[EditorialType, Metadata]) -> 'StructuredDocument':
        """Create a copy of this object with the new editorial type.

        Previous editorial type value is not stored in Metadata journal.
        """
        return self._update_semantic_metadata(editorial_type, Metadata.editorial_type)

    def _update_metadata(self, new_metadata: Dict[str, Metadata]) -> 'StructuredDocument':
        return self.update(metadata=new_metadata)
