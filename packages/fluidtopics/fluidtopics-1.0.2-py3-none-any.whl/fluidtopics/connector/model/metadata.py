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
from time import strptime
from typing import Set, Optional, List, Iterable, Union, Tuple, Callable

from autovalue import autovalue

from fluidtopics.connector.internal.utils import Utils

DEFAULT_LOCALE = 'en-US'
DEFAULT_PRODUCER = 'Data'
ValueType = Union[str, Iterable[str], Iterable[Iterable[str]]]


def is_simple_value(value: ValueType) -> bool:
    return isinstance(value, str)


def is_string_value(value: ValueType) -> bool:
    return isinstance(next(iter(value)), str)


def is_hierarchical_value(value: ValueType) -> bool:
    return not is_string_value(value)


class SemanticMetadata:
    """Semantic metadata keys.

    SemanticMetadata.ALL is a set which returns all semantic metadata keys.
    """
    TITLE = 'ft:title'
    LOCALE = 'ft:locale'
    BASE_ID = 'ft:baseId'
    CLUSTER_ID = 'ft:clusterId'
    OPEN_MODE = 'ft:openMode'
    ORIGIN_URL = 'ft:originUrl'
    EDITORIAL_TYPE = 'ft:editorialType'
    LAST_EDITION = 'ft:lastEdition'
    DESCRIPTION = 'ft:description'
    PRETTY_URL = 'ft:prettyUrl'

    ALL = {
        BASE_ID,
        CLUSTER_ID,
        DESCRIPTION,
        EDITORIAL_TYPE,
        LAST_EDITION,
        LOCALE,
        OPEN_MODE,
        ORIGIN_URL,
        PRETTY_URL,
        TITLE,
    }


class OpenMode(Enum):
    """Possible values for ft:openMode Metadata.

    `FLUIDTOPICS`: Document is consulted in Fluid Topics (default).
    `EXTERNAL`: Document is consulted outside of Fluid Topics (destination is defined in ft:originUrl Metadata).
    """
    FLUIDTOPICS = 'fluidtopics'
    EXTERNAL = 'external'


class EditorialType(Enum):
    """Possible values for ft:editorialType Metadata.

    Reserved for StructuredDocument.
    BOOK: Topics can be accessed directly through the search.
    ARTICLE: Only the beginning of the document can be accessed through the search.
    """
    BOOK = 'book'
    ARTICLE = 'article'


@autovalue
class Snapshot:
    """Snapshot of a Metadata state in the Journal.

    Prefer using `.update()` / `.update_from()` to build the Metadata journal than creating it manually.
    """

    def __init__(self, key: str,
                 value: ValueType,
                 producer: str,
                 comment: Optional[str] = None):
        self.key = key
        self.value = value
        self.producer = producer
        self.comment = comment

    @staticmethod
    def from_meta(meta: 'Metadata') -> 'Snapshot':
        return Snapshot(meta.key, meta.value, meta.producer, meta.comment)


class InvalidMetadata(ValueError):
    pass


@autovalue
class Metadata:
    """Metadata are an association of a key with one or multiple values. There are two types of Metadata: string and
    hierarchical.

    Simple string Metadata have one value:
        value='metadata value'
    Multivalued string Metadata have more than one value, stored in a set:
        value={'value1', 'value2'}
    Hierarchical Metadata have one or more values (stored in a set) composed of one or more parts (stored in tuples):
        value={('hierarchical', 'value'), ('hierarchical', 'value 2')}

    A Metadata object is immutable: once created, it is not possible to modify it.
    To create another Metadata object from this one, use `.update()` method.
    Example:
    >>> metadata = Metadata('version', 'v3.8')
    >>> metadata.update(value='3.8', producer='Normalizer', comment='Normalize version')
    Metadata(
        key=version,
        value=3.8,
        producer=Normalizer,
        comment=Normalize version,
        journal=[Snapshot(key=version, value=v3.8, producer=Data)])

    A detailed record of the steps the Metadata took to arrive to its current state is available in the Metadata
    journal. This journal allows the technical writer to understand how the `lang=English` metadata was changed by the
    connector.
    Example of a Metadata journal:
    >>> lang = Metadata('lang', 'English', comment='Lang read from data')
    >>> locale = lang.update(SemanticMetadata.LOCALE, 'en', 'Semantic finder', 'Transform into FT locale')
    >>> normalized_locale = locale.update(value='en-US', producer='Normalizer', comment='Add region code to locale')
    >>> normalized_locale.key
    ft:locale
    >>> normalized_locale.value
    en-US
    >>> normalized_locale.journal
    [Snapshot(key=lang, value=English, producer=Data, comment=Lang read from data),
     Snapshot(key=ft:locale, value=en, producer=Semantic finder, comment=Transform into FT locale)]
    """

    def __init__(self, key: str,
                 value: ValueType,
                 producer: str = DEFAULT_PRODUCER,
                 comment: Optional[str] = None,
                 journal: List[Snapshot] = None):
        """Create Metadata.

        :param key: Metadata key. Should not be empty.
        :param value: Value associated with the key. `value` type determines Metadata type:
            * str => simple string Metadata
            * Iterable[str] => multivalued string Metadata
            * Iterable[Iterable[str]] => hierarchical Metadata
            Value parts, values, and the value list cannot be empty.
        :param producer: What produces this Metadata (Data, Normalizer, ...). Displayed in FT Metadata journal.
        :param comment: More details about Metadata states. Displayed in FT Metadata journal.
        :param journal: Previous states of this Metadata. Use `.update()`and `.update_from()` to modify Metadata state
            and add current state to journal. Journal snapshots are in chronological order.
        """
        if not key:
            raise InvalidMetadata('Invalid metadata: key should not be empty')
        if key in SemanticMetadata.ALL and not is_simple_value(value):
            msg = 'Invalid "{}" metadata: semantic metadata cannot have multiple values ({})'
            raise InvalidMetadata(msg.format(key, value))
        try:
            self.value = self._compute_value(value, set)
        except InvalidMetadata as e:
            raise InvalidMetadata('Invalid "{}" metadata: {}'.format(key, e))
        self.key = key
        self.producer = producer
        self.comment = comment
        self.journal = journal or []

    def is_equivalent_to(self, other: 'Metadata') -> bool:
        """Compare two Metadata ignoring their Journal."""
        return (other is not None
                and self.key == other.key
                and self.value == other.value
                and self.producer == other.producer)

    @staticmethod
    def title(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:title Metadata."""
        return Metadata(SemanticMetadata.TITLE, value, producer, comment)

    @staticmethod
    def last_edition(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:lastEdition Metadata.

        The value should match the format YYYY-MM-DD.
        """
        try:
            strptime(value, '%Y-%m-%d')
        except ValueError:
            raise InvalidMetadata('Invalid last edition date "{}", expected format "YYYY-MM-DD"'.format(value))
        return Metadata(SemanticMetadata.LAST_EDITION, value, producer, comment)

    @staticmethod
    def locale(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:locale Metadata.

        The value should be a valid ISO code (example: en-US, fr-FR)."""
        try:
            value = Utils.parse_ietf_locale_tag(value)
            return Metadata(SemanticMetadata.LOCALE, value, producer, comment)
        except ValueError as e:
            raise InvalidMetadata('"{}" is not a valid locale: {}'.format(value, e))

    @staticmethod
    def base_id(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:baseId Metadata."""
        return Metadata(SemanticMetadata.BASE_ID, value, producer, comment)

    @staticmethod
    def cluster_id(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:clusterId Metadata."""
        return Metadata(SemanticMetadata.CLUSTER_ID, value, producer, comment)

    @staticmethod
    def open_mode(mode: OpenMode, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:openMode Metadata."""
        return Metadata(SemanticMetadata.OPEN_MODE, mode.value, producer, comment)

    @staticmethod
    def origin_url(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:originUrl Metadata."""
        return Metadata(SemanticMetadata.ORIGIN_URL, value, producer, comment)

    @staticmethod
    def description(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:description Metadata."""
        return Metadata(SemanticMetadata.DESCRIPTION, value, producer, comment)

    @staticmethod
    def pretty_url(value: str, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:prettyUrl Metadata."""
        return Metadata(SemanticMetadata.PRETTY_URL, value, producer, comment)

    @staticmethod
    def editorial_type(type: EditorialType, producer: str = DEFAULT_PRODUCER, comment: str = None) -> 'Metadata':
        """Create ft:prettyUrl Metadata."""
        return Metadata(SemanticMetadata.EDITORIAL_TYPE, type.value, producer, comment)

    def update(self, key: str = None,
               value: ValueType = None,
               producer: str = None,
               comment: str = None):
        """Update the Metadata state (key, values, producer, comment).

        It is advised to use this method to update any aspect of the Metadata.
        Example:
        >>> old = Metadata('version', 'v1.0')
        >>> updated = old.update(value='1.0', producer='Normalizer', comment='Normalize version')
        >>> updated.value
        1.0
        >>> updated.producer
        Normalizer
        >>> updated.journal[0].value
        v1.0

        Returns the current Metadata if self and new state are equivalent, without updating journal.

        :param key: New Metadata key. Keep the current key if not defined.
        :param value: New Metadata value. Keep the current value if not defined.
        :param producer: New Metadata producer. Keep the current producer if not defined.
        :param comment: New Metadata comment. Keep the current comment if not defined.
        :return: New Metadata with updated state and a journal which contains the state of the current Metadata.
        """
        new_metadata = Metadata(
            key=key if key is not None else self.key,
            value=value if value is not None else self.value,
            producer=producer if producer is not None else self.producer,
            comment=comment)
        return self.update_from(new_metadata)

    def update_from(self, metadata: 'Metadata') -> 'Metadata':
        """Update the Metadata state from the state of another Metadata.

        Equivalent to `.update(metadata.key, metadata.value, metadata.producer, metadata.comment)`.
        Example:
        >>> old = Metadata('version', 'v1.0')
        >>> new = Metadata('version', '1.0', 'NORMALIZER', 'Normalize version')
        >>> updated = old.update_from(new)
        >>> updated.value
        1.0
        >>> updated.producer
        Normalizer
        >>> updated.journal[0].value
        v1.0

        Returns the current Metadata if self and Metadata are equivalent, without updating journal.

        :param metadata: New state of the Metadata. Journal of this Metadata is ignored.
        :return: New Metadata with updated state and a journal which contains the state of the current Metadata.
        """
        if self.is_equivalent_to(metadata):
            return self
        return Metadata(
            key=metadata.key,
            value=metadata.value,
            producer=metadata.producer,
            comment=metadata.comment,
            journal=self._update_journal())

    def _compute_value(self, value: ValueType, collection_type: Callable) -> Union[str, Set[str], Set[Tuple[str]]]:
        if not value:
            raise InvalidMetadata('invalid value \'{}\''.format(value))
        if isinstance(value, str):
            return value
        try:
            return collection_type(self._compute_value(v, tuple) for v in value)
        except InvalidMetadata as e:
            raise InvalidMetadata('{} in {}'.format(e, value))

    def _update_journal(self) -> List[Snapshot]:
        snapshot = Snapshot.from_meta(self)
        return [*self.journal, snapshot]
