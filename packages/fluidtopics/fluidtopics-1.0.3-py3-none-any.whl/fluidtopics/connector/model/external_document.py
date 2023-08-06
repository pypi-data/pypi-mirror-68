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
from typing import Dict, Union, Optional, Iterable

from autovalue import autovalue

from fluidtopics.connector.model.document import Document, InvalidDocument
from fluidtopics.connector.model.has_metadata import build_metadata_map
from fluidtopics.connector.model.metadata import DEFAULT_LOCALE, Metadata


class InvalidExternalDocument(ValueError):
    pass


@autovalue
class ExternalDocument(Document):
    """Document hosted outside of Fluid Topics through its URL.

    An ExternalDocument object is immutable: once created, it is not possible to modify it.
    To create another ExternalDocument object from this one, use `.update()` method.
    Example:
    >>> document = ExternalDocument.create('id', 'title', 'http://url', mime_type='mime/type')
    >>> document.update(mime_type='new/type', indexable_content='to index')
    ExternalDocument(document_id=id, title=title, url=http://url, mime_type=new/type, indexable_content=to index)

    `.update()` only works for ExternalDocument object attributes. To update semantic metadata (base ID, locale, ...),
    use corresponding `.update_*()` method.
    Example:
    >>> document = ExternalDocument.create('id', 'title', 'http://url', base_id='baseId')
    >>> document.update_base_id('newBaseId')
    ExternalDocument(document_id=id, title=title, url=http://url, base_id=newBaseId)
    """

    def __init__(self, document_id: str,
                 metadata: Dict[str, Metadata] = None,
                 indexable_content: Optional[str] = None,
                 mime_type: Optional[str] = None):
        """Create an ExternalDocument. It is recommended to use `ExternalDocument.create()` instead.

        :param document_id: Origin ID of the document. Should not be empty.
        :param metadata: Metadata of the document indexed by key. Contains client and semantic Metadata.
        :param indexable_content: Text to index for this document.
        :param mime_type: Standard IANA media type. Detected automatically in Fluid Topics when not specified.
        :raises: InvalidExternalDocument: Data integrity criteria are not respected.
        """
        try:
            super().__init__(
                document_id=document_id,
                metadata=metadata)
        except InvalidDocument as e:
            raise InvalidExternalDocument(e)
        self.mime_type = mime_type
        self.indexable_content = indexable_content

    @staticmethod
    def create(document_id: str,
               title: str,
               url: str,
               locale: Union[str, Metadata] = DEFAULT_LOCALE,
               base_id: Optional[Union[str, Metadata]] = None,
               description: Optional[Union[str, Metadata]] = None,
               last_edition: Optional[Union[str, Metadata]] = None,
               pretty_url: Optional[Union[str, Metadata]] = None,
               metadata: Iterable[Metadata] = None,
               mime_type: Optional[str] = None,
               indexable_content: Optional[str] = None) -> 'ExternalDocument':
        """Create an ExternalDocument.

        :param document_id: Origin ID of the document. Should not be empty.
        :param title: Title of the document.
        :param url: Destination of the document when opened. Set ft:originUrl Metadata.
        :param locale: ISO locale code of the document. Set ft:locale Metadata. Default: `en-US`.
        :param base_id: ID used to link this document and cluster it.
            Set ft:baseId Metadata. Fallback to document_id when not specified.
        :param description: Description used for search engines. Set ft:description Metadata.
        :param last_edition: Last time this document was modified. Should respect YYYY-MM-DD format.
            Set ft:lastEdition Metadata. Fallback to publication date when not specified.
        :param pretty_url: Set ft:prettyUrl Metadata.
            For more information about pretty URLs: https://doc.antidot.net/go/FT/37/Pretty_URL.
        :param metadata: Metadata of the document. When multiple Metadata have the same key, the last one
            is used and others are stored in Metadata journal. Semantic Metadata overrides corresponding
            attributes. For example: ft:title Metadata override given title (which is stored in Metadata journal).
        :param mime_type: Standard IANA media type. Detected automatically in Fluid Topics when not specified.
        :param indexable_content: Text to index for this document.
        :raises: InvalidExternalDocument: Data integrity criteria are not respected.
        """
        metadata_map = build_metadata_map(
            object_id=document_id,
            title=title,
            base_id=base_id,
            locale=locale,
            description=description,
            last_edition=last_edition,
            pretty_url=pretty_url,
            origin_url=url,
            metadata=metadata)
        return ExternalDocument(
            document_id=document_id,
            mime_type=mime_type,
            metadata=metadata_map,
            indexable_content=indexable_content)

    def _update_metadata(self, new_metadata: Dict[str, Metadata]) -> 'Document':
        return self.update(metadata=new_metadata)
