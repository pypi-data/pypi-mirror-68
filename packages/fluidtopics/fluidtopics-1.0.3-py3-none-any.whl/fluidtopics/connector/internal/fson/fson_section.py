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

from typing import List, Optional

from autovalue import autovalue
from injector import inject

from fluidtopics.connector.internal.fson.fson_body import FsonBody, BodyConverter
from fluidtopics.connector.internal.fson.fson_metadata import FsonMetadata, MetadataConverter
from fluidtopics.connector.model.topic import Topic


@autovalue
class FsonSection:
    def __init__(self, id: str, title: str = None, body: FsonBody = None,
                 children: List['FsonSection'] = None,
                 metadata: List[FsonMetadata] = None, base_id: str = None,
                 variant_selector: Optional[str] = None,
                 description: Optional[str] = None,
                 pretty_url: Optional[str] = None):
        self.id = id
        self.title = title
        self.body = body if body is not None else FsonBody.none()
        self.metadata = metadata if metadata is not None else []
        self.children = children if children is not None else []
        self.base_id = base_id
        self.variant_selector = variant_selector
        self.description = description
        self.pretty_url = pretty_url


class SectionConverter:
    @inject
    def __init__(self, body_converter: BodyConverter, metadata_converter: MetadataConverter):
        self._body_converter = body_converter
        self._metadata_converter = metadata_converter

    def convert_topic(self, topic: Topic) -> FsonSection:
        body = self._body_converter.convert_body(topic.body)
        section_metadata = self._metadata_converter.convert_metadata_list(topic.metadata.values())
        children = self.convert_topics(topic.children)
        return FsonSection(
            id=topic.topic_id,
            title=None,
            body=body,
            children=children,
            metadata=section_metadata,
            base_id=None,
            variant_selector=None,
            description=None,
            pretty_url=None
        )

    def convert_topics(self, toc: List[Topic]) -> List[FsonSection]:
        return [self.convert_topic(topic) for topic in toc]
