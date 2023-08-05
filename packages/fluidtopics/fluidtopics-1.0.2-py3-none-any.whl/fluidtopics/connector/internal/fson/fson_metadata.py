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
from typing import List

from autovalue import autovalue

from fluidtopics.connector.model.metadata import Metadata, Snapshot, DEFAULT_PRODUCER, \
    SemanticMetadata, is_simple_value, is_string_value


class FsonMetadataType(Enum):
    STRING = 1
    STRING_TREE = 2


@autovalue
class FsonSnapshot:
    def __init__(self, mtype: FsonMetadataType, key: str,
                 values: List[List[str]], producer: str, comment: str = None):
        self.mtype = mtype
        self.key = key
        self.values = values
        self.producer = producer
        self.comment = comment


@autovalue
class FsonJournal:
    def __init__(self, snapshots: List[FsonSnapshot]):
        self.snapshots = snapshots

    def add(self, snapshot: FsonSnapshot) -> 'FsonJournal':
        snapshots = self.snapshots.copy()
        snapshots.append(snapshot)
        return FsonJournal(snapshots)

    @classmethod
    def empty(cls) -> 'FsonJournal':
        return cls([])


@autovalue
class FsonMetadata:
    def __init__(self, key: str, producer: str, values: List[str] = None,
                 hierarchical_values: List[List[str]] = None,
                 comment: str = None, journal: FsonJournal = None):
        self.key = key
        self.producer = producer
        self.values = values
        self.hierarchical_values = hierarchical_values
        self.comment = comment
        self.journal = journal if journal is not None else FsonJournal.empty()

    @staticmethod
    def title(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.TITLE, producer, values=[value], comment=comment)

    @staticmethod
    def last_edition(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.LAST_EDITION, producer, values=[value], comment=comment)

    @staticmethod
    def locale(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.LOCALE, producer, values=[value], comment=comment)

    @staticmethod
    def base_id(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.BASE_ID, producer, values=[value], comment=comment)

    @staticmethod
    def cluster_id(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.CLUSTER_ID, producer, values=[value], comment=comment)

    @staticmethod
    def open_mode(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.OPEN_MODE, producer, values=[value], comment=comment)

    @staticmethod
    def origin_url(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.ORIGIN_URL, producer, values=[value], comment=comment)

    @staticmethod
    def description(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.DESCRIPTION, producer, values=[value], comment=comment)

    @staticmethod
    def pretty_url(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.PRETTY_URL, producer, values=[value], comment=comment)

    @staticmethod
    def editorial_type(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'FsonMetadata':
        return FsonMetadata(SemanticMetadata.EDITORIAL_TYPE, producer, values=[value], comment=comment)


class MetadataConverter:
    def convert_metadata_list(self, metadata: List[Metadata]) -> List[FsonMetadata]:
        return [self.convert_metadata(m) for m in metadata]

    def convert_metadata(self, meta: Metadata) -> FsonMetadata:
        journal = self._convert_journal(meta.journal)
        values = tree_values = None
        if is_simple_value(meta.value):
            values = [meta.value]
        elif is_string_value(meta.value):
            values = list(sorted(meta.value))
        else:
            tree_values = list(sorted(list(value) for value in meta.value))
        return FsonMetadata(meta.key, meta.producer, values, tree_values, meta.comment, journal)

    def _convert_journal(self, journal: List[Snapshot]) -> FsonJournal:
        snaps = [self._convert_snapshot(snap) for snap in journal]
        return FsonJournal(snaps)

    def _convert_snapshot(self, snapshot: Snapshot) -> FsonSnapshot:
        if is_simple_value(snapshot.value):
            values = [[snapshot.value]]
            meta_type = FsonMetadataType.STRING
        elif is_string_value(snapshot.value):
            values = list([v] for v in sorted(snapshot.value))
            meta_type = FsonMetadataType.STRING
        else:
            values = list(sorted(list(value) for value in snapshot.value))
            meta_type = FsonMetadataType.STRING_TREE
        return FsonSnapshot(meta_type, snapshot.key, values, snapshot.producer, snapshot.comment)
