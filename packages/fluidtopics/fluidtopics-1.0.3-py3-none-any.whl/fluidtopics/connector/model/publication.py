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

from collections import OrderedDict
from enum import Enum
from typing import Optional, Union, List, Iterable

from autovalue import autovalue
from deprecated.sphinx import deprecated

from fluidtopics.connector.internal.utils import Utils
from fluidtopics.connector.model.metadata import Metadata, SemanticMetadata
from fluidtopics.connector.model.resource import Resource
from fluidtopics.connector.model.right import Rights
from fluidtopics.connector.model.topic import Topic


@autovalue
class TocNode:
    """Node in a table of content of a Publication. It contains the topic and
    its sub-topics."""

    def __init__(self, topic: Topic, children: List['TocNode'] = None):
        self.topic = topic
        self.children = children if children is not None else []


class EditorialType(Enum):
    """Editorial type of the Publication. It will determine the value of {}
    metadata.

    Reserved to StructuredContent.
    BOOK: Topics can be find and accessed directly through the search
    ARTICLE: The publication is "atomic": you can only access the top of the publication
    """.format(SemanticMetadata.EDITORIAL_TYPE)
    DEFAULT = 0
    BOOK = 1
    ARTICLE = 2


@autovalue
class StructuredContent:
    """Content of a structured publication."""

    def __init__(self, toc: List[TocNode], editorial_type: EditorialType = EditorialType.DEFAULT):
        """Create a StructuredContent.

        :param toc: Table Of Content of the Publication
        :param editorial_type: Specify if the Publication is a BOOK or an ARTICLE"""
        self.toc = toc
        self.editorial_type = editorial_type


@autovalue
class UnstructuredContent:
    """Content of an unstructured Publication."""

    def __init__(self, resource_reference: str):
        """Create an UnstructuredContent.

        :param resource_reference: Resource ID of the Resource object which is the content of this UD."""
        self.resource_reference = resource_reference


@autovalue
class AttachmentLink:
    """Declare a Resource in the ResourceBank as a map attachment for the Publication."""

    def __init__(self, resource_id: str, tags: List[str], title: str = None):
        """Create an AttachmentLink.

        :param resource_id: ID of the Resource in ResourceBank of the Publication
        :param tags: Useless but "it can be useful later"... T.T
        :param title: Title of the attachment. It is the name displayed on the link to the attachment in reader.
                      Fallback to resource filename if not specified."""
        self.resource_id = resource_id
        self.tags = tags
        self.title = title


@autovalue
class Publication:
    """Publication is the element which is published to Fluid Topics.

    It can be structured (a map), or not (an Unstructured Document).
    It is recommended to use PublicationBuilder to create it."""

    def __init__(self, id: str, title: Optional[str], lang: Optional[str],
                 content: Union[StructuredContent, UnstructuredContent],
                 rights: Optional[Rights],
                 metadata: Optional[List[Metadata]],
                 base_id: Optional[str],
                 variant_selector: Optional[str],
                 resources: Optional[List[Resource]],
                 attachments: Optional[List[AttachmentLink]] = None,
                 business_id: Optional[str] = None,
                 description: Optional[str] = None,
                 pretty_url: Optional[str] = None):
        """Prefer using PublicationBuilder to create a Publication.

        :param id: Origin ID. It should be unique for a given source.
        :param title: Title of the Publication
        :param content: Content of the Publication. If the Publication is an UD, use an UnstructuredContent,
                        if it is a map use a StructuredContent
        :param rights: Deprecated (put None and use Content Access Right). Access rights on the Publication.
                       It overrides rules set in Content Access Right administration page
        :param metadata: List of Metadata
        :param base_id: Publications with the same base_id are clustered in search page and cross-book links.
                        Fallback to id if None. Can be override by {cluster_id} metadata for search page clustering.
        :param variant_selector: Deprecated (it's here for compatibility but no longer used. Put None)
        :param resources: List of Resources used in the Publication (also called Resource Bank).
                          It should contains map attachments, resources in Topics (like images), UD content, ...
        :param attachments: List of attachments. Attachment contents should be declared as Resource in resources param.
        :param business_id: Name displayed in publishing report. Fallback to id if None.
        :param description: Description displayed in search page. Set {description} metadata.
        :param pretty_url: Pretty name used to build a pretty URL. Set {pretty_url} metadata.""".format(
            cluster_id=SemanticMetadata.CLUSTER_ID,
            description=SemanticMetadata.DESCRIPTION,
            pretty_url=SemanticMetadata.PRETTY_URL)
        self.id = id
        self.title = title
        self.lang = lang
        self.metadata = metadata
        self.rights = rights
        self.content = content
        self.base_id = base_id
        self.variant_selector = variant_selector
        self.resources = resources
        self.attachments = attachments if attachments is not None else []
        self.business_id = business_id
        self.description = description
        self.pretty_url = pretty_url

    def __eq__(self, other):
        """Return self==other."""
        return Utils.objects_are_equals(self, other, 'metadata', 'resources')

    def get_title(self) -> str:
        """Helper to get title of the Publication."""
        meta_title = self._get_metadata(SemanticMetadata.TITLE)
        return next(iter(meta_title.values))[0] if meta_title is not None else self.title

    def get_lang(self) -> str:
        """Helper to get locale of the Publication."""
        meta_lang = self._get_metadata(SemanticMetadata.LOCALE)
        return next(iter(meta_lang.values))[0] if meta_lang is not None else self.lang

    def _get_metadata(self, key: str) -> Optional[Metadata]:
        meta = self.metadata if self.metadata is not None else []
        return next((m for m in meta if m.key == key), None)

    def get_business_id(self) -> str:
        """Helper to get business ID of the Publication."""
        if self.business_id is not None:
            return self.business_id
        return self.id


class _ResourceBankBuilder:
    def __init__(self, resources: List[Resource] = None):
        self.resources = OrderedDict()
        if resources:
            self.add_all(resources)

    def add(self, resource: Resource) -> '_ResourceBankBuilder':
        """Add/update a Resource to the Publication.

        Update fields of the Resource if the Publication already contains a
        Resource with the same ID."""
        if resource.id in self.resources:
            existing_resource = self.resources[resource.id]
            if resource != existing_resource:
                resource = self._merge(resource, existing_resource)
        self.resources[resource.id] = resource
        return self

    def add_all(self, resources: Iterable[Resource]) -> '_ResourceBankBuilder':
        """Add/update Resources to the Publication."""
        for resource in resources:
            self.add(resource)
        return self

    def build(self) -> List[Resource]:
        """Create the Resource bank of the Publication."""
        return list(self.resources.values())

    def _merge(self, r1: Resource, r2: Resource) -> Resource:
        return Resource(
            r1.id,
            r1.content or r2.content,
            r1.filename or r2.filename,
            r1.mime_type or r2.mime_type,
            r1.indexable_content or r2.indexable_content,
            r1.url or r2.url)


class InvalidPublication(Exception):
    pass


class PublicationBuilder:
    """Helper to create a valid Publication."""

    def __init__(self, publication: Publication = None):
        """Create a PublicationBuilder.

        :param publication: Built Publication will have same fields than
                            publication except if you update them."""
        resources = publication.resources if publication else []
        self._resource_bank_builder = _ResourceBankBuilder(resources)
        self._id = publication.id if publication else None
        self._business_id = publication.business_id if publication else None
        self._title = publication.title if publication else None
        self._description = publication.description if publication else None
        self._lang = publication.lang if publication else None
        self._metadata = publication.metadata if publication else None
        self._attachments = publication.attachments if publication else None
        self._rights = publication.rights if publication else None
        self._content = publication.content if publication else StructuredContent(toc=[])
        self._base_id = publication.base_id if publication else None
        self._variant_selector = publication.variant_selector if publication else None
        self._pretty_url = publication.pretty_url if publication else None

    def id(self, id: str) -> 'PublicationBuilder':
        """Set the ID of the Publication. It should be unique for a given source."""
        self._id = id
        return self

    def business_id(self, business_id: str) -> 'PublicationBuilder':
        """Set the business ID which is displayed in publishing report. Fallback to publication id if not set."""
        self._business_id = business_id
        return self

    def title(self, title: Union[str, Metadata]) -> 'PublicationBuilder':
        """Set the title of the Publication.

        :param title: Can be a string or a {title} Metadata
        :raises:
            InvalidPublication: Metadata key is not {title}""".format(title=SemanticMetadata.TITLE)
        if isinstance(title, Metadata):
            self._add_semantic_metadata(SemanticMetadata.TITLE, title)
        else:
            self._title = title
        return self

    def description(self, description: Union[str, Metadata]) -> 'PublicationBuilder':
        """Set the description which is displayed in search page.

        :param description: Can be a string or a {description} Metadata
        :raises:
            InvalidPublication: Metadata key is not {description}""".format(description=SemanticMetadata.DESCRIPTION)
        if isinstance(description, Metadata):
            self._add_semantic_metadata(SemanticMetadata.DESCRIPTION, description)
        else:
            self._description = description
        return self

    def pretty_url(self, pretty_url: Union[str, Metadata]) -> 'PublicationBuilder':
        """Set the pretty name which is used to build a pretty URL.

        :param pretty_url: Can be a string or a {pretty} Metadata
        :raises:
            InvalidPublication: Metadata key is not {pretty}""".format(pretty=SemanticMetadata.PRETTY_URL)
        if isinstance(pretty_url, Metadata):
            self._add_semantic_metadata(SemanticMetadata.PRETTY_URL, pretty_url)
        else:
            self._pretty_url = pretty_url
        return self

    def lang(self, lang: Union[str, Metadata]) -> 'PublicationBuilder':
        """Set the locale of the Publication.

        :param lang: Can be a string or a {lang} Metadata
        :raises:
            InvalidPublication: Metadata key is not {lang}""".format(lang=SemanticMetadata.LOCALE)
        if isinstance(lang, Metadata):
            self._add_semantic_metadata(SemanticMetadata.LOCALE, lang)
        else:
            try:
                self._lang = Utils.parse_ietf_language_tag(lang)
            except ValueError as e:
                msg = 'Error building publication (id={}). {}'
                raise InvalidPublication(msg.format(self._id, e))
        return self

    def add_metadata(self, *metadata: Metadata) -> 'PublicationBuilder':
        """Add Metadata to the Publication."""
        if self._metadata is None:
            self._metadata = []
        self._metadata.extend(metadata)
        return self

    def add_attachment(self, resource: Resource, tags: List[str] = None, title: str = None) -> 'PublicationBuilder':
        """Add attachment to the Publication.

        :param resource: Attachment content
        :param tags: Useless but "it can be useful later"... T.T
        :param title: Title of the attachment. Fallback to filename if None"""
        if self._attachments is None:
            self._attachments = []
        link = AttachmentLink(resource.id, tags or [], title)
        self._attachments.append(link)
        self.resource_bank().add(resource)
        return self

    @deprecated(reason='Prefer using metadata with content access right to specify rights')
    def rights(self, rights: Rights) -> 'PublicationBuilder':
        """Set rights of the Publication. It override rules set in Content Access Rights."""
        self._rights = rights
        return self

    def content(self, content: Union[StructuredContent, UnstructuredContent]) -> 'PublicationBuilder':
        """Set content of the Publication. If the Publication is an UD, use an UnstructuredContent,
         if it is a map use a StructuredContent."""
        self._content = content
        return self

    def base_id(self, base_id: Union[str, Metadata]) -> 'PublicationBuilder':
        """Set the base ID of the Publication.

        Publications with the same base_id are clustered in search page and cross-book links.
        Fallback to id if None. Can be override by {cluster_id} metadata for search page clustering
        :param base_id: Can be a string or a {base_id} Metadata
        :raises:
            InvalidPublication: Metadata key is not {base_id}
        """.format(base_id=SemanticMetadata.BASE_ID, cluster_id=SemanticMetadata.CLUSTER_ID)
        if isinstance(base_id, Metadata):
            self._add_semantic_metadata(SemanticMetadata.BASE_ID, base_id)
        else:
            self._base_id = base_id
        return self

    @deprecated(reason='Variant selector value is ignored.But this method is kept for compatibility.')
    def variant_selector(self, variant_selector: str) -> 'PublicationBuilder':
        self._variant_selector = variant_selector
        return self

    def resource_bank(self) -> '_ResourceBankBuilder':
        """Return a helper to build the resource bank of the Publication."""
        return self._resource_bank_builder

    def _metadata_for_a_key(self, key: str) -> List[Metadata]:
        meta = self._metadata if self._metadata is not None else []
        return [m for m in meta if m.key == key]

    def _add_semantic_metadata(self, key: str, metadata: Metadata) -> 'PublicationBuilder':
        if metadata.key == key:
            self.add_metadata(metadata)
        else:
            raise InvalidPublication('Expected {} metadata, actual metadata: {}'.format(key, metadata.key))
        return self

    def build(self) -> Publication:
        """Build the Publication from information specified before.

        ID and title are mandatory.
        :raises:
            InvalidPublication: One of the requirement is not fulfilled."""
        if not self._id:
            raise InvalidPublication('Missing id when building publication')

        if not self._title:
            title_metadata = self._metadata_for_a_key(SemanticMetadata.TITLE)
            pattern = '{} title when building publication {}'
            if not title_metadata:
                raise InvalidPublication(pattern.format('Missing', self._id))
            elif len(title_metadata) > 1:
                raise InvalidPublication(pattern.format('Multiple', self._id))

        return Publication(
            id=self._id,
            title=self._title,
            lang=self._lang,
            content=self._content,
            rights=self._rights,
            metadata=self._metadata,
            base_id=self._base_id,
            variant_selector=self._variant_selector,
            resources=self._resource_bank_builder.build(),
            attachments=self._attachments,
            business_id=self._business_id,
            description=self._description,
            pretty_url=self._pretty_url
        )
