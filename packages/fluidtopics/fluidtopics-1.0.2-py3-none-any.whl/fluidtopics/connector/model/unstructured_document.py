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
from os.path import basename
from typing import Optional, Union, Iterable, Dict

from autovalue import autovalue

from fluidtopics.connector.internal.utils import Utils
from fluidtopics.connector.model.document import Document, InvalidDocument
from fluidtopics.connector.model.metadata import Metadata, InvalidMetadata, DEFAULT_LOCALE
from fluidtopics.connector.model.has_metadata import build_metadata_map


class InvalidUnstructuredDocument(ValueError):
    pass


@autovalue
class UnstructuredDocument(Document):
    """A document that is self-sufficient and is not in a structured format, like a PDF file, or a JPG image.

    An UnstructuredDocument object is immutable: once created, it is not possible to modify it.
    To create another UnstructuredDocument object from this one, use `.update()` method.
    Example:
    >>> ud = UnstructuredDocument.create('id', b'content')
    >>> ud.update(content=b'new content', filename='filename')
    UnstructuredDocument(document_id=id, content=b'new content', filename=filename)

    `.update()` only works for UnstructuredDocument object attributes. To update semantic Metadata
    (base ID, locale, ...), use corresponding `.update_*()` method.
    Example:
    >>> ud = UnstructuredDocument.create('id', b'content', base_id='baseId')
    >>> ud.update_base_id('newBaseId')
    UnstructuredDocument(document_id=id, content=b'content', base_id=newBaseId)
    """

    def __init__(self, document_id: str,
                 content: bytes,
                 filename: str = None,
                 metadata: Dict[str, Metadata] = None,
                 mime_type: Optional[str] = None,
                 indexable_content: Optional[str] = None):
        """Create an UnstructuredDocument. It is recommended to use `UnstructuredDocument.create()` instead.

        :param document_id: Origin ID of the document. Should not be empty.
        :param content: Binary content of the UnstructuredDocument.
        :param filename: Filename of the UnstructuredDocument when downloaded. Fallback to ID when not specified.
        :param metadata: Metadata of the document indexed by key. Contains client and semantic Metadata.
        :param mime_type: Standard IANA media type. Detected automatically in Fluid Topics when not specified.
        :param indexable_content: Text to index for this document.
        :raises: InvalidUnstructuredContent: Data integrity criteria are not respected.
        """
        try:
            super().__init__(
                document_id=document_id,
                metadata=metadata)
        except InvalidDocument as e:
            raise InvalidUnstructuredDocument(e)
        final_filename = UnstructuredDocument._build_filename(filename, document_id)
        self.filename = final_filename
        self.content = content
        self.mime_type = mime_type
        self.indexable_content = indexable_content

    @staticmethod
    def create(document_id: str,
               content: bytes,
               filename: str = None,
               title: Union[str, Metadata] = None,
               locale: Union[str, Metadata] = DEFAULT_LOCALE,
               base_id: Optional[Union[str, Metadata]] = None,
               description: Optional[Union[str, Metadata]] = None,
               last_edition: Optional[Union[str, Metadata]] = None,
               pretty_url: Optional[Union[str, Metadata]] = None,
               metadata: Iterable[Metadata] = None,
               mime_type: Optional[str] = None,
               indexable_content: Optional[str] = None) -> 'UnstructuredDocument':
        """Create an UnstructuredDocument.

        :param document_id: Origin ID of the document. Should not be empty.
        :param content: Binary content of the UnstructuredDocument.
        :param filename: Filename of the UnstructuredDocument when downloaded. Fallback to ID when not specified.
        :param title: Title of the document.  Fallback to filename when not specified.
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
            attributes. For example: ft:title Metadata overrides given title (which is stored in Metadata journal).
        :param mime_type: Standard IANA media type. Detected automatically in Fluid Topics when not specified.
        :param indexable_content: Text to index for this document.
        :raises: InvalidUnstructuredDocument: Data integrity criteria are not respected.
        """
        final_filename = UnstructuredDocument._build_filename(filename, document_id)
        try:
            metadata_map = build_metadata_map(
                object_id=document_id,
                title=title or final_filename,
                locale=locale,
                description=description,
                pretty_url=pretty_url,
                base_id=base_id,
                last_edition=last_edition,
                metadata=metadata)
        except InvalidMetadata as e:
            raise InvalidUnstructuredDocument('Invalid unstructured document "{}": {}'.format(document_id, e))
        return UnstructuredDocument(
            document_id=document_id,
            content=content,
            filename=filename,
            mime_type=mime_type,
            metadata=metadata_map,
            indexable_content=indexable_content)

    @staticmethod
    def from_uri(document_id: str,
                 uri: str,
                 title: Union[str, Metadata] = None,
                 locale: Union[str, Metadata] = DEFAULT_LOCALE,
                 base_id: Optional[Union[str, Metadata]] = None,
                 description: Optional[Union[str, Metadata]] = None,
                 last_edition: Optional[Union[str, Metadata]] = None,
                 pretty_url: Optional[Union[str, Metadata]] = None,
                 metadata: Iterable[Metadata] = None,
                 mime_type: Optional[str] = None,
                 indexable_content: Optional[str] = None) -> 'UnstructuredDocument':
        """Create an UnstructuredDocument from its URI.

        URI can be a file path or a URL.

        :param document_id: Origin ID of the document. Should not be empty.
        :param uri: Path of the document file.
        :param title: Title of the document.
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
            attributes. For example: ft:title Metadata overrides given title (which is stored in Metadata journal).
        :param mime_type: Standard IANA media type. Detected automatically in Fluid Topics when not specified.
        :param indexable_content: Text to index for this document.
        :raises: InvalidUnstructuredDocument: Data integrity criteria are not respected.
        """
        filename, content = Utils.extract_from(uri)
        return UnstructuredDocument.create(
            document_id=document_id,
            title=title,
            locale=locale,
            base_id=base_id,
            description=description,
            last_edition=last_edition,
            pretty_url=pretty_url,
            metadata=metadata,
            filename=filename,
            content=content,
            mime_type=mime_type,
            indexable_content=indexable_content)

    @staticmethod
    def _build_filename(filename: str, document_id: Optional[str]) -> str:
        return filename or basename(document_id)

    def _update_metadata(self, new_metadata: Dict[str, Metadata]) -> 'UnstructuredDocument':
        return self.update(metadata=new_metadata)
