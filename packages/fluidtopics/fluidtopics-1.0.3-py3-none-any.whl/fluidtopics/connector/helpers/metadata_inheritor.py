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

from typing import List, Dict, Union, Iterable, Tuple

from fluidtopics.connector.model.metadata import SemanticMetadata, Metadata, ValueType, is_simple_value, \
    is_hierarchical_value
from fluidtopics.connector.model.structured_document import StructuredDocument
from fluidtopics.connector.model.topic import Topic

PRODUCER = 'Normalizer'
INHERIT_MESSAGE = 'Inherited from parent metadata'
ENRICH_MESSAGE = 'Enriched from parent metadata'


class MetadataInheritor:
    """Helper to inherit metadata in a StructuredDocument.

    Book (book_meta)
    | - Topic (topic_meta)
        | - Sub-topic (sub_topic_meta)

    will become

    Book (book_meta)
    | - Topic (topic_meta, book_meta)
        | - Sub-topic (sub_topic_meta, topic_meta, book_meta)

    Semantic metadata are not inherited.
    """

    def __init__(self, ignored_keys: List[str] = None):
        """Create a MetadataInheritor.

        :param ignored_keys: Metadata keys that should not be inherited.
        """
        ignored_keys = ignored_keys or []
        self.ignored_keys = {*ignored_keys, *SemanticMetadata.ALL}

    def inherit_metadata(self, document: StructuredDocument) -> StructuredDocument:
        """Inherits metadata in the StructuredDocument.

        If a topic inherits metadata it already has, values are merged.
        Example:
            Metadata('version', '1') inherits from Metadata('version', '2')
                => Metadata('version', {'1', '2'})
        If one of the merged Metadata values is hierarchical, the merged value is
        hierarchical.
        Example:
            Metadata('version', [['2.x', '2.3']]) inherits from Metadata('version', 'latest')
                => Metadata('version', {('2.x', '2.3'), ('latest',)}
        Merged Metadata keep their previous values in the Metadata journal.

        :param document: The StructuredDocument to apply metadata inheritance on.
        :return: Copy of the given StructuredDocument with metadata inheritance applied.
        """
        metadata = self._filter_ignored_metadata(document.metadata)
        topics = self._inherit_metadata_for_topics(document.toc, metadata)
        return document.update(toc=topics)

    def _filter_ignored_metadata(self, metadata: Dict[str, Metadata]) -> Dict[str, Metadata]:
        return {k: m for k, m in metadata.items() if k not in self.ignored_keys}

    def _inherit_metadata_for_topics(self, topics: List[Topic], metadata: Dict[str, Metadata]) -> List[Topic]:
        return [self._inherit_metadata_for_topic(n, metadata) for n in topics]

    def _inherit_metadata_for_topic(self, topic: Topic, metadata: Dict[str, Metadata]) -> Topic:
        merged_metadata = self._merge_metadata(topic.metadata, metadata)
        metadata_to_transmit = self._filter_ignored_metadata(merged_metadata)
        children = self._inherit_metadata_for_topics(topic.children, metadata_to_transmit)
        return topic.update(metadata=merged_metadata, children=children)

    def _merge_metadata(self, metadata: Dict[str, Metadata], to_merge: Dict[str, Metadata]) -> Dict[str, Metadata]:
        merged_metadata = dict(**metadata)
        for key, meta in to_merge.items():
            if key in merged_metadata:
                merged_metadata[key] = self._merge_meta(merged_metadata[key], meta)
            else:
                merged_metadata[key] = Metadata(key=meta.key,
                                                value=meta.value,
                                                producer=PRODUCER,
                                                comment=INHERIT_MESSAGE)
        return merged_metadata

    def _merge_meta(self, old_meta: Metadata, new_meta: Metadata) -> Metadata:
        if old_meta.value != new_meta.value:
            values = self._merge_values(old_meta.value, new_meta.value)
            merged_meta = Metadata(old_meta.key, values, PRODUCER, ENRICH_MESSAGE)
            return old_meta.update_from(merged_meta)
        return old_meta

    def _merge_values(self, old_value: ValueType, new_value: ValueType) -> ValueType:
        if is_hierarchical_value(old_value) or is_hierarchical_value(new_value):
            return {*self._get_hierarchical_value(old_value), *self._get_hierarchical_value(new_value)}
        else:
            return {*self._get_string_value(old_value), *self._get_string_value(new_value)}

    def _get_hierarchical_value(self, value: ValueType) -> Tuple[str]:
        if is_hierarchical_value(value):
            yield from value
        else:
            yield from ((v,) for v in self._get_string_value(value))

    def _get_string_value(self, value: Union[str, Iterable[str]]) -> str:
        if is_simple_value(value):
            yield value
        else:
            yield from value
