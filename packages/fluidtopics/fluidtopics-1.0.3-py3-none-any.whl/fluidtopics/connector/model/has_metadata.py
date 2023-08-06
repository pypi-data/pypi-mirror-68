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
from typing import Union, Optional, Iterable, Dict

from fluidtopics.connector.model.metadata import InvalidMetadata, Metadata, SemanticMetadata, EditorialType, OpenMode

CONNECTOR_PRODUCER = 'Connector'
OPEN_MODE_COMMENT = 'Set by connector API because origin URL is specified'


def build_metadata_map(object_id: str,
                       title: Union[str, Metadata],
                       base_id: Optional[Union[str, Metadata]] = None,
                       locale: Union[str, Metadata] = None,
                       description: Optional[Union[str, Metadata]] = None,
                       last_edition: Optional[Union[str, Metadata]] = None,
                       pretty_url: Optional[Union[str, Metadata]] = None,
                       editorial_type: Optional[Union[EditorialType, Metadata]] = None,
                       origin_url: Optional[Union[str, Metadata]] = None,
                       metadata: Iterable[Metadata] = None) -> Dict[str, Metadata]:
    metadata = metadata or []
    metadata_map = _build_semantic_metadata_map(
        title=title,
        locale=locale,
        base_id=base_id or object_id,
        description=description,
        pretty_url=pretty_url,
        editorial_type=editorial_type,
        origin_url=origin_url,
        last_edition=last_edition)
    for meta in metadata:
        if meta.key in metadata_map:
            metadata_map[meta.key] = metadata_map[meta.key].update_from(meta)
        else:
            metadata_map[meta.key] = meta
    return metadata_map


def _build_semantic_metadata_map(title: Union[str, Metadata],
                                 base_id: Union[str, Metadata],
                                 locale: Optional[Union[str, Metadata]],
                                 description: Optional[Union[str, Metadata]],
                                 last_edition: Optional[Union[str, Metadata]],
                                 pretty_url: Optional[Union[str, Metadata]],
                                 editorial_type: Optional[Union[EditorialType, Metadata]],
                                 origin_url: Optional[Union[str, Metadata]]) -> Dict[str, Metadata]:
    metadata_map = {
        SemanticMetadata.TITLE: _build_metadata(title, Metadata.title),
        SemanticMetadata.BASE_ID: _build_metadata(base_id, Metadata.base_id)
    }
    if locale:
        metadata_map[SemanticMetadata.LOCALE] = _build_metadata(locale, Metadata.locale)
    if description:
        metadata_map[SemanticMetadata.DESCRIPTION] = _build_metadata(description, Metadata.description)
    if last_edition:
        metadata_map[SemanticMetadata.LAST_EDITION] = _build_metadata(last_edition, Metadata.last_edition)
    if pretty_url:
        metadata_map[SemanticMetadata.PRETTY_URL] = _build_metadata(pretty_url, Metadata.pretty_url)
    if editorial_type:
        metadata_map[SemanticMetadata.EDITORIAL_TYPE] = _build_metadata(editorial_type, Metadata.editorial_type)
    if origin_url:
        metadata_map[SemanticMetadata.OPEN_MODE] = Metadata.open_mode(
            mode=OpenMode.EXTERNAL,
            producer=CONNECTOR_PRODUCER,
            comment=OPEN_MODE_COMMENT)
        metadata_map[SemanticMetadata.ORIGIN_URL] = _build_metadata(origin_url, Metadata.origin_url)
    return metadata_map


def _build_metadata(metadata: Union[str, Enum, Metadata], constructor) -> Metadata:
    return metadata if isinstance(metadata, Metadata) else constructor(metadata)


class HasMetadata:
    """Mixin for classes with Metadata."""

    def __init__(self, metadata: Dict[str, Metadata] = None):
        metadata = metadata or {}
        self._check_metadata(metadata)
        self.metadata = metadata

    @property
    def title(self) -> str:
        """Access title stored in ft:title Metadata."""
        # noinspection PyTypeChecker
        # By design, title is always present in the metadata dict
        return self._get_metadata_value(SemanticMetadata.TITLE)

    def update_title(self, new_title: Union[str, Metadata]) -> 'HasMetadata':
        """Create a copy of this object with the new title.

        Previous title value is not stored in Metadata journal.
        """
        return self._update_semantic_metadata(new_title, Metadata.title)

    @property
    def base_id(self) -> str:
        """Access base ID stored in ft:baseId Metadata."""
        # noinspection PyTypeChecker
        # By design, base ID is always present in the metadata dict
        return self._get_metadata_value(SemanticMetadata.BASE_ID)

    def update_base_id(self, new_base_id: Union[str, Metadata]) -> 'HasMetadata':
        """Create a copy of this object with the new base ID.

        Previous base ID value is not stored in Metadata journal.
        """
        return self._update_semantic_metadata(new_base_id, Metadata.base_id)

    @property
    def description(self) -> Optional[str]:
        """Access description stored in ft:description Metadata."""
        return self._get_metadata_value(SemanticMetadata.DESCRIPTION)

    def update_description(self, new_description: Union[str, Metadata]) -> 'HasMetadata':
        """Create a copy of this object with the new description.

        Previous description value is not stored in Metadata journal.
        """
        return self._update_semantic_metadata(new_description, Metadata.description)

    @property
    def last_edition(self) -> Optional[str]:
        """Access last edition date stored in ft:lastEdition Metadata."""
        return self._get_metadata_value(SemanticMetadata.LAST_EDITION)

    def update_last_edition(self, new_last_edition: Union[str, Metadata]) -> 'HasMetadata':
        """Create a copy of this object with the new last edition date.

        Previous last edition date value is not stored in Metadata journal.
        """
        return self._update_semantic_metadata(new_last_edition, Metadata.last_edition)

    @property
    def pretty_url(self) -> Optional[str]:
        """Access pretty URL stored in ft:prettyUrl Metadata."""
        return self._get_metadata_value(SemanticMetadata.PRETTY_URL)

    def update_pretty_url(self, new_pretty_url: Union[str, Metadata]) -> 'HasMetadata':
        """Create a copy of this object with the new pretty URL.

        Previous pretty URL value is not stored in Metadata journal.
        """
        return self._update_semantic_metadata(new_pretty_url, Metadata.pretty_url)

    @property
    def open_mode(self) -> Optional[OpenMode]:
        """Access open mode stored in ft:openMode Metadata."""
        str_mode = self._get_metadata_value(SemanticMetadata.OPEN_MODE)
        return OpenMode(str_mode)

    def update_open_mode(self, new_open_mode: Union[OpenMode, Metadata]) -> 'HasMetadata':
        """Create a copy of this object with the new open mode.

        Previous open mode value is not stored in Metadata journal.
        """
        return self._update_semantic_metadata(new_open_mode, Metadata.open_mode)

    @property
    def origin_url(self) -> Optional[str]:
        """Access origin URL stored in ft:originUrl Metadata."""
        return self._get_metadata_value(SemanticMetadata.ORIGIN_URL)

    def update_origin_url(self, new_origin_url: Union[str, Metadata]) -> 'HasMetadata':
        """Create a copy of this object with the new origin URL.

        Previous origin URL value is not stored in Metadata journal.
        """
        return self._update_semantic_metadata(new_origin_url, Metadata.origin_url)

    @property
    def client_metadata(self) -> Dict[str, Metadata]:
        """Access non-semantic Metadata, indexed by key."""
        return {key: metadata for key, metadata in self.metadata.items() if not key.startswith('ft:')}

    def _check_metadata(self, metadata: Dict[str, Metadata]):
        self._check_mandatory_metadata(metadata, SemanticMetadata.TITLE)
        self._check_mandatory_metadata(metadata, SemanticMetadata.BASE_ID)
        for key, meta in metadata.items():
            if key != meta.key:
                msg = 'metadata dictionary key {} does not match metadata key {}'
                raise InvalidMetadata(msg.format(key, meta))

    def _check_mandatory_metadata(self, metadata: Dict[str, Metadata], key: str):
        if key not in metadata:
            msg = 'metadata dictionary should contain {} metadata'
            raise InvalidMetadata(msg.format(key))

    def _get_metadata_value(self, key: str) -> Optional[str]:
        metadata = self.metadata.get(key)
        return metadata.value if metadata else None

    def _update_semantic_metadata(self, value: Union[str, Enum, Metadata], constructor) -> 'HasMetadata':
        metadata = dict(**self.metadata)
        meta = _build_metadata(value, constructor)
        metadata[meta.key] = meta
        return self._update_metadata(metadata)

    def _update_metadata(self, new_metadata: Dict[str, Metadata]) -> 'HasMetadata':
        raise NotImplementedError
