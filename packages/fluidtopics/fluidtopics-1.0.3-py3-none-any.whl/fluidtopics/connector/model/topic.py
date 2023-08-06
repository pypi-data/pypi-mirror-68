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
import re
from typing import List, Optional, Dict, Iterable, Union

from autovalue import autovalue

from fluidtopics.connector.model.has_metadata import build_metadata_map, HasMetadata
from fluidtopics.connector.model.metadata import Metadata, InvalidMetadata

DIV_REGEX = re.compile(r'<(div[^>]*)|(/div)>')
START_DIV = re.compile('<div[^>]*>')
ENDED_DIV = re.compile('<div[^>/]*/>')
END_DIV = '</div>'
END_DIV_LEN = len(END_DIV)


class InvalidTopic(ValueError):
    pass


@autovalue
class Topic(HasMetadata):
    """A Topic is a section in the table of contents of a StructuredDocument.
    It is composed of a title, an HTML body, and subtopics (subsections in the table of contents).

    A Topic object is immutable: once created, it is not possible to modify it.
    To create another Topic object from this one, use `.update()` method.
    Example:
    >>> topic = Topic.create('id', 'title')
    >>> topic.update(document_id='new_id', body='<div>HTML body</div>')
    Topic(topic_id=new_id, title=title, body=<div>HTML body</div>)

    `.update()` only works for Topic object attributes. To update semantic Metadata (base ID, description, ...),
    use corresponding `.update_*()` method.
    Example:
    >>> topic = Topic.create('id', 'title', base_id='baseId')
    >>> topic.update_base_id('newBaseId')
    Topic(topic_id=id, title=title, base_id=newBaseId)
    """
    def __init__(self, topic_id: str,
                 metadata: Dict[str, Metadata] = None,
                 body: Optional[str] = None,
                 children: List['Topic'] = None):
        """Create a Topic. It is recommended to use `Topic.create()` instead.

        :param topic_id: Origin ID of the topic. Should not be empty.
        :param metadata: Metadata of the topic indexed by key. Contains client and semantic Metadata.
        :param body: HTML body of the topic. It is wrapped in a <div> if it is not already the case.
        :param children: Subtopics of the current topic in the table of contents.
        :raises: InvalidTopic: Data integrity criteria are not respected.
        """
        if not topic_id:
            raise InvalidTopic('Topic ID is mandatory: "{}" is not a valid ID.'.format(topic_id))
        try:
            super().__init__(metadata)
        except InvalidMetadata as e:
            raise InvalidTopic('Invalid "{}" topic: {}'.format(topic_id, e))
        self.topic_id = topic_id
        self.body = self._wrap_body(body) if body else None
        self.children = children or []

    @staticmethod
    def create(topic_id: str,
               title: Union[str, Metadata],
               body: Optional[str] = None,
               base_id: Optional[Union[str, Metadata]] = None,
               description: Optional[Union[str, Metadata]] = None,
               last_edition: Optional[Union[str, Metadata]] = None,
               pretty_url: Optional[Union[str, Metadata]] = None,
               metadata: Iterable[Metadata] = None,
               children: List['Topic'] = None) -> 'Topic':
        """Create a Topic.

        :param topic_id: Origin ID of the topic. Should not be empty.
        :param title: Title of the topic.
        :param body: HTML content of the topic. It is wrapped in a <div> if it is not already the case.
        :param base_id: ID used to link this topic and cluster it.
            Set ft:baseId Metadata. Fallback to document_id when not specified.
        :param description: Description used for search engines. Set ft:description Metadata.
        :param last_edition: Last time this topic was modified. Should respect YYYY-MM-DD format.
            Set ft:lastEdition Metadata. Fallback to publication date when not specified.
        :param pretty_url: Set ft:prettyUrl Metadata.
            For more information about pretty URLs: https://doc.antidot.net/go/FT/37/Pretty_URL.
        :param metadata: Metadata of the topic. When multiple Metadata have the same key, the last one
            is used and others are stored in Metadata journal. Semantic Metadata overrides corresponding
            attributes. For example: ft:title Metadata overrides given title (which is stored in Metadata journal).
        :param children: Subtopics of the current topic in the table of contents.
        :raises: InvalidTopic: Data integrity criteria are not respected.
        """
        metadata = metadata or []
        try:
            metadata_map = build_metadata_map(
                object_id=topic_id,
                title=title,
                base_id=base_id,
                description=description,
                last_edition=last_edition,
                pretty_url=pretty_url,
                metadata=metadata)
        except InvalidMetadata as e:
            raise InvalidTopic('Invalid topic "{}": {}'.format(topic_id, e))
        return Topic(topic_id, metadata_map, body, children or [])

    def _wrap_body(self, body: str) -> str:
        body = body.strip()
        return '<div>{}</div>'.format(body) if not self._is_wrapped(body) else body

    def _is_wrapped(self, body: str) -> bool:
        start_match = START_DIV.match(body)
        return start_match \
            and body.endswith(END_DIV)\
            and self._are_sub_div_closed(body[start_match.end():-END_DIV_LEN]) \
            or ENDED_DIV.fullmatch(body)

    def _are_sub_div_closed(self, body: str) -> bool:
        divs = DIV_REGEX.findall(body)
        matching_count = 0
        for div in divs:
            if div[0]:
                matching_count += 1
            elif div[1]:
                matching_count -= 1
            if matching_count < 0:
                return False
        return matching_count == 0

    def _update_metadata(self, new_metadata: Dict[str, Metadata]) -> 'HasMetadata':
        return self.update(metadata=new_metadata)
