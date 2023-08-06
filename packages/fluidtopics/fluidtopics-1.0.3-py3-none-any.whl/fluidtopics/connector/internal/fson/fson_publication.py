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
from typing import List, Optional, Union

from autovalue import autovalue
from injector import inject

from fluidtopics.connector.internal.fson.fson_metadata import FsonMetadata, MetadataConverter
from fluidtopics.connector.internal.fson.fson_right import FsonRights
from fluidtopics.connector.internal.fson.fson_section import FsonSection, SectionConverter
from fluidtopics.connector.internal.id_provider import IdProvider
from fluidtopics.connector.model.attachment import Attachment
from fluidtopics.connector.model.document import Document
from fluidtopics.connector.model.external_document import ExternalDocument
from fluidtopics.connector.model.structured_document import StructuredDocument
from fluidtopics.connector.model.unstructured_document import UnstructuredDocument


@autovalue
class FsonAttachmentLink:
    def __init__(self, resource_id: str, title: str = None, tags: List[str] = None):
        self.resource_id = resource_id
        self.title = title
        self.tags = tags or []


class FsonEditorialType(Enum):
    DEFAULT = 0
    ARTICLE = 1
    BOOK = 2


@autovalue
class FsonStructured:
    def __init__(self, sections: List[FsonSection], editorial_type: FsonEditorialType):
        self.sections = sections
        self.editorial_type = editorial_type


@autovalue
class FsonUnstructured:
    def __init__(self, resource_reference: str):
        self.resource_reference = resource_reference


@autovalue
class FsonContent:
    def __init__(self, structured: FsonStructured = None,
                 unstructured: FsonUnstructured = None):
        self.structured = structured
        self.unstructured = unstructured

    @staticmethod
    def structured_content(structured_content: FsonStructured) -> 'FsonContent':
        return FsonContent(structured=structured_content)

    @staticmethod
    def unstructured_content(resource_reference: str) -> 'FsonContent':
        return FsonContent(unstructured=FsonUnstructured(resource_reference))


@autovalue
class FsonPublication:
    def __init__(self, id: str,
                 content: FsonContent,
                 lang: str = None,
                 title: str = None,
                 rights: Optional[FsonRights] = None,
                 metadata: List[FsonMetadata] = None,
                 base_id: str = None,
                 variant_selector: Optional[str] = None,
                 attachments: List[FsonAttachmentLink] = None,
                 description: Optional[str] = None,
                 pretty_url: Optional[str] = None):
        self.id = id
        self.content = content
        self.lang = lang
        self.title = title
        self.rights = rights
        self.metadata = metadata
        self.base_id = base_id
        self.variant_selector = variant_selector
        self.attachments = attachments if attachments is not None else []
        self.description = description
        self.pretty_url = pretty_url

    @property
    def sections(self):
        return self.content.structured.sections


class PublicationConverter:
    @inject
    def __init__(self, section_converter: SectionConverter,
                 metadata_converter: MetadataConverter,
                 id_provider: IdProvider):
        self._section_converter = section_converter
        self._metadata_converter = metadata_converter
        self._id_provider = id_provider

    def convert_structured_document(self, document: StructuredDocument) -> FsonPublication:
        content = self._convert_structured_content(document)
        attachments = self._convert_attachment_links(document.document_id, document.attachments)
        return self._convert_publication(document, content, attachments)

    def convert_unstructured_document(self, ud: Union[UnstructuredDocument, ExternalDocument]) -> FsonPublication:
        content = self._convert_unstructured_content(ud.document_id)
        return self._convert_publication(ud, content)

    def _convert_unstructured_content(self, document_id: str) -> FsonContent:
        resource_id = self._id_provider.ud_resource_id(document_id)
        return FsonContent.unstructured_content(resource_id)

    def _convert_structured_content(self, document: StructuredDocument) -> FsonContent:
        sections = self._section_converter.convert_topics(document.toc)
        return FsonContent.structured_content(FsonStructured(sections, FsonEditorialType.DEFAULT))

    def _convert_publication(self, document: Document,
                             content: FsonContent,
                             attachments: List[FsonAttachmentLink] = None) -> FsonPublication:
        publication_metadata = self._metadata_converter.convert_metadata_list(document.metadata.values())
        attachments = attachments or []
        return FsonPublication(
            id=document.document_id,
            title=None,
            lang=None,
            content=content,
            rights=None,
            metadata=publication_metadata,
            base_id=None,
            variant_selector=None,
            attachments=attachments,
            description=None,
            pretty_url=None
        )

    def _convert_attachment_links(self, map_id: str, attachments: List[Attachment]) -> List[FsonAttachmentLink]:
        return [FsonAttachmentLink(self._id_provider.attachment_id(map_id, a), a.title) for a in attachments]
