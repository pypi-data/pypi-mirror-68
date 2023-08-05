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

from typing import List, Optional

from assertpy import assert_that

from fluidtopics.connector.model.body import Body
from fluidtopics.connector.model.metadata import Metadata
from fluidtopics.connector.model.publication import Publication, AttachmentLink, EditorialType, StructuredContent, \
    UnstructuredContent, TocNode
from fluidtopics.connector.model.resource import Resource
from fluidtopics.connector.model.right import AccessLevel, Rights


class MetadataChecker:
    """Helper to check a Metadata."""

    def __init__(self, metadata: Metadata):
        """Create a MetadataChecker.

        :param metadata: Metadata to check."""
        self.metadata = metadata

    def __repr__(self):
        return 'MetadataChecker({})'.format(self.metadata)

    def has_key(self, key: str) -> 'MetadataChecker':
        assert self.metadata.key == key
        return self

    def has_value(self, value: str) -> 'MetadataChecker':
        assert len(self.metadata.values) == 1
        assert len(next(iter(self.metadata.values))) == 1
        assert self.metadata.first_value == value
        return self

    def has_values(self, *values: str) -> 'MetadataChecker':
        values = {(v,) for v in values}
        assert values == self.metadata.values, 'Metadata values {} are not {}'.format(self.metadata.values, values)
        return self

    def has_hierarchical_value(self, value: List[str]) -> 'MetadataChecker':
        assert len(self.metadata.values) == 1
        hierarchical_value = self.metadata.first_hierarchical_value
        err_msg = '{} and {} are not equivalent'.format(hierarchical_value, value)
        assert len(hierarchical_value) == len(value), err_msg
        for i, value_part in enumerate(value):
            assert hierarchical_value[i] == value_part, err_msg
        return self

    def has_hierarchical_values(self, *values: List[str]) -> 'MetadataChecker':
        values = {tuple(value) for value in values}
        assert values == self.metadata.values, 'Metadata values {} are not {}'.format(self.metadata.values, values)
        return self

    def has_producer(self, producer: str) -> 'MetadataChecker':
        assert self.metadata.producer == producer, 'Expected producer: {}, actual: {}' \
            .format(producer, self.metadata.producer)
        return self

    def has_comment(self, comment: str) -> 'MetadataChecker':
        assert self.metadata.comment == comment
        return self


class RightsChecker:
    """Helper to check Rights."""

    def __init__(self, rights: Rights):
        """Create a RightsChecker.

        :param rights: Rights to check."""
        self.rights = rights

    def __repr__(self):
        return 'RightsChecker({})'.format(self.rights)

    def has_access_level(self, level: AccessLevel) -> 'RightsChecker':
        assert self.rights.access_level == level
        return self

    def has_groups(self, *groups: str) -> 'RightsChecker':
        assert_that(self.rights.groups).contains_only(*groups)
        return self


class TopicChecker:
    """Helper to check a TocNode."""

    def __init__(self, toc_node: TocNode):
        """Create a TopicChecker.

        :param toc_node: TocNode to check."""
        self.toc_node = toc_node

    def __repr__(self):
        return 'TopicChecker({})'.format(self.toc_node)

    def has_id(self, id: str) -> 'TopicChecker':
        assert self.toc_node.topic.id == id
        return self

    def has_title(self, title: str) -> 'TopicChecker':
        assert self.toc_node.topic.get_title() == title
        return self

    def has_base_id(self, base_id: str) -> 'TopicChecker':
        assert self.toc_node.topic.base_id == base_id
        return self

    def has_no_body(self) -> 'TopicChecker':
        assert self.toc_node.topic.body == Body.none()
        return self

    def has_html_body(self, body: str) -> 'TopicChecker':
        assert self.toc_node.topic.body.html == body, 'Expected body: {}, actual: {}' \
            .format(body, self.toc_node.topic.body.html)
        return self

    def has_html_body_which_contains(self, extract: str) -> 'TopicChecker':
        assert extract in self.toc_node.topic.body.html
        return self

    def children(self) -> List['TopicChecker']:
        """Return checkers on all sub TocNode of this TocNode."""
        return [TopicChecker(topic) for topic in self.toc_node.children]

    def child(self, topic_id: str) -> 'TopicChecker':
        """Return a checker on a specific TocNode.

        :param topic_id: ID of the Topic contained in the TocNode to check.
        :raises:
            AssertionError: No Topic with this ID has been found."""
        topic = next((TopicChecker(t) for t in self.toc_node.children if t.topic.id == topic_id), None)
        assert topic is not None, \
            'Topic {} not found in {}'.format(topic_id, [t.topic.id for t in self.toc_node.children])
        return topic

    def metadata(self) -> List[MetadataChecker]:
        """Return checkers on all Metadata of the Topic in this TocNode."""
        return [MetadataChecker(m) for m in self.toc_node.topic.metadata]

    def meta(self, meta_key: str) -> MetadataChecker:
        """Return a checker on a specific Metadata of the Topic in this TocNode.

        :param meta_key: Key of the Metadata to check.
        :raises:
            AssertionError: No Metadata with this key has been found in the current Topic."""
        meta = next((MetadataChecker(m) for m in self.toc_node.topic.metadata if m.key == meta_key), None)
        assert meta is not None, \
            'Metadata {} not found in {}'.format(meta_key, [m.key for m in self.toc_node.topic.metadata])
        return meta


class ResourceChecker:
    """Helper to check a Resource."""

    def __init__(self, resource: Resource):
        """Create a ResourceChecker.

        :param resource: Resource to check."""
        self.resource = resource

    def __repr__(self):
        return 'ResourceChecker({})'.format(self.resource)

    def has_id(self, resource_id: str) -> 'ResourceChecker':
        assert resource_id == self.resource.id, \
            'Expected: {}, actual: {}'.format(resource_id, self.resource.resource_id)
        return self

    def has_content(self, content: bytes) -> 'ResourceChecker':
        assert content == self.resource.content, \
            'Expected: {}, actual: {}'.format(content, self.resource.content)
        return self

    def has_no_content(self) -> 'ResourceChecker':
        assert not self.resource.content
        return self

    def has_filename(self, filename: str) -> 'ResourceChecker':
        assert filename == self.resource.filename, \
            'Expected: {}, actual: {}'.format(filename, self.resource.filename)
        return self

    def has_mime_type(self, mime_type: str) -> 'ResourceChecker':
        assert mime_type == self.resource.mime_type, \
            'Expected: {}, actual: {}'.format(mime_type, self.resource.mime_type)
        return self

    def has_indexable_content(self, indexable_content: str) -> 'ResourceChecker':
        assert indexable_content == self.resource.indexable_content, \
            'Expected: {}, actual: {}'.format(indexable_content, self.resource.indexable_content)
        return self

    def has_no_indexable_content(self) -> 'ResourceChecker':
        assert not self.resource.indexable_content
        return self

    def has_url(self, url: str) -> 'ResourceChecker':
        assert url == self.resource.url, \
            'Expected: {}, actual: {}'.format(url, self.resource.url)
        return self

    def has_no_url(self) -> 'ResourceChecker':
        assert not self.resource.url
        return self


class AttachmentLinkChecker:
    """Helper to check an AttachmentLink."""

    def __init__(self, attachment_link: AttachmentLink):
        """Create an AttachmentLinkChecker.

        :param attachment_link: AttachmentLink to check."""
        self.attachment_link = attachment_link

    def has_resource_id(self, resource_id: str) -> 'AttachmentLinkChecker':
        assert_that(self.attachment_link).has_resource_id(resource_id)
        return self

    def has_tags(self, tags: List[str]) -> 'AttachmentLinkChecker':
        assert_that(self.attachment_link).has_tags(tags)
        return self

    def has_title(self, title: str) -> 'AttachmentLinkChecker':
        assert_that(self.attachment_link).has_title(title)
        return self


class PublicationChecker:
    """Helper to check a Publication."""

    def __init__(self, publication: Publication):
        """Create a PublicationChecker.

        :param publication: Publication to check."""
        self.publication = publication

    def __repr__(self):
        return 'PublicationChecker({})'.format(self.publication)

    def has_title(self, title: str) -> 'PublicationChecker':
        assert self.publication.get_title() == title, \
            'Expected: {}, actual: {}'.format(title, self.publication.title)
        return self

    def has_id(self, publication_id: str) -> 'PublicationChecker':
        assert self.publication.id == publication_id, \
            'Expected: {}, actual: {}'.format(publication_id, self.publication.id)
        return self

    def has_base_id(self, base_id: str) -> 'PublicationChecker':
        assert self.publication.base_id == base_id, \
            'Expected: {}, actual: {}'.format(base_id, self.publication.base_id)
        return self

    def has_variant_selector(self, variant_selector: str) -> 'PublicationChecker':
        assert self.publication.variant_selector == variant_selector, \
            'Expected: {}, actual: {}'.format(variant_selector, self.publication.variant_selector)
        return self

    def has_no_variant_selector(self) -> 'PublicationChecker':
        assert not self.publication.variant_selector
        return self

    def has_lang(self, lang: str) -> 'PublicationChecker':
        assert self.publication.get_lang() == lang, \
            'Expected: {}, actual: {}'.format(lang, self.publication.lang)
        return self

    def is_structured_content(self) -> 'PublicationChecker':
        assert isinstance(self.publication.content, StructuredContent)
        return self

    def is_unstructured_content(self) -> 'PublicationChecker':
        assert isinstance(self.publication.content, UnstructuredContent)
        return self

    def has_editorial_type(self, editorial_type: EditorialType) -> 'PublicationChecker':
        """Check the editorial type of the Publication.
        An Unstructured Publication will always fail."""
        self.is_structured_content()
        assert self.publication.content.editorial_type == editorial_type
        return self

    def has_public_rights(self) -> 'PublicationChecker':
        """Check that the Publication has public access rights.
        This only verify rights directly set to the Publication. It does not concern content access rights."""
        assert self.publication.rights == Rights.public()
        return self

    def has_authenticated_rights(self) -> 'PublicationChecker':
        """Check that the Publication has authenticated access rights.
        This only verify rights directly set to the Publication. It does not concern content access rights."""
        assert self.publication.rights == Rights.authenticated()
        return self

    def has_restricted_rights(self, *groups: str) -> 'PublicationChecker':
        """Check that the Publication has restricted access rights.
        This only verify rights directly set to the Publication. It does not concern content access rights."""
        assert self.publication.rights == Rights.restricted(groups)
        return self

    def has_no_content(self) -> 'PublicationChecker':
        if isinstance(self.publication.content, StructuredContent):
            assert_that(self.publication.content.toc).described_as('Publication toc is empty').is_empty()
        elif isinstance(self.publication.content, UnstructuredContent):
            assert self.publication.content.resource_reference, 'Publication as no resource reference'
        return self

    def topics(self) -> List[TopicChecker]:
        """Return checkers on all top level TocNode of the Publication.
        :raises:
            AssertionError: The Publication is not structured."""
        self.is_structured_content()
        return [TopicChecker(topic) for topic in self.publication.content.toc]

    def topic(self, topic_id: str) -> TopicChecker:
        """Return a checker on a specific top level TocNode of the Publication.

        :param topic_id: ID of the Topic to check.
        :raises:
            AssertionError: The Publication is not structured, or no Topic with this ID has been found."""
        self.is_structured_content()
        topic = self._topic_checker(topic_id)
        assert topic is not None, \
            'Topic {} not found in {}'.format(topic_id, [t.topic.id for t in self.publication.content.toc])
        return topic

    def has_no_topic(self, *topic_ids: str):
        """Check that the Publication does not contain these top level Topics.

        :param topic_ids: ID of Topics that should not be in Publication top level Topics.
        :raises:
            AssertionError: The Publication is not structured, or a Topic with this ID has been found."""
        self.is_structured_content()
        found_ids = [topic_id for topic_id in topic_ids if self._topic_checker(topic_id)]
        assert_that(found_ids).described_as('Topics {} found in publication'.format(found_ids)) \
            .is_empty()

    def _topic_checker(self, topic_id) -> Optional[TopicChecker]:
        return next((TopicChecker(t) for t in self.publication.content.toc if t.topic.id == topic_id), None)

    def has_no_metadata(self) -> 'PublicationChecker':
        assert self.publication.metadata
        return self

    def metadata(self) -> List[MetadataChecker]:
        """Return checkers on all Metadata of the Publication."""
        return [MetadataChecker(m) for m in self.publication.metadata]

    def meta(self, meta_key: str) -> MetadataChecker:
        """Return a checker on a specific Metadata of the Publication.

        :param meta_key: Key of the Metadata to check.
        :raises:
            AssertionError: No Metadata with this key has been found in the Publication."""
        meta = next((MetadataChecker(m) for m in self.publication.metadata if m.key == meta_key), None)
        assert meta is not None, \
            'Metadata {} not found in {}'.format(meta_key, [m.key for m in self.publication.metadata])
        return meta

    def resources(self) -> List[ResourceChecker]:
        """Return checkers on all Resources of the Publication."""
        return [ResourceChecker(resource) for resource in self.publication.resources]

    def resource(self, resource_id: str) -> ResourceChecker:
        """Return a checker on a specific Resource of the Publication.

        :param resource_id: ID of the Resource to check.
        :raises:
            AssertionError: No Resource with this ID has been found."""
        resource = next((r for r in self.publication.resources if r.id == resource_id), None)
        assert resource is not None, \
            'Resource {} not found in {}'.format(resource_id, [r.id for r in self.publication.resources])
        return ResourceChecker(resource)

    def attachments(self) -> List[AttachmentLinkChecker]:
        """Return checker on all AttachmentLink of the Publication."""
        return [AttachmentLinkChecker(a) for a in self.publication.attachments]

    def attachment(self, resource_id: str) -> AttachmentLinkChecker:
        """Return a checker on a specific AttachmentLink.

        :param resource_id: ID of the Attachment concerned by the AttachmentLink to check.
        :raises:
            AssertionError: No AttachmentLink about the Attachment with this ID has been found."""
        attachment_link = next((a for a in self.publication.attachments if a.resource_id == resource_id), None)
        assert attachment_link is not None, 'Attachment link {} not found in {}' \
            .format(resource_id, [a.resource_id for a in self.publication.attachments])
        return AttachmentLinkChecker(attachment_link)
