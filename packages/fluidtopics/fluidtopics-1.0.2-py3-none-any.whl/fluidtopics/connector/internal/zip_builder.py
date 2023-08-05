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

from base64 import b64encode
from io import BytesIO
from typing import Optional
from zipfile import ZipFile, ZIP_DEFLATED

import pyckson

from fluidtopics.connector.internal.constants import VERSION_FILE
from fluidtopics.connector.internal.fson.fson_publication import FsonPublication
from fluidtopics.connector.internal.fson.fson_resource import FsonResource
from fluidtopics.connector.internal.fson.fson_version import FsonVersion


class ZipBuilder:
    def __init__(self):
        self.file = BytesIO()
        self.zip_file = ZipFile(self.file, 'w', ZIP_DEFLATED)

    def add_file(self, filename: str, data: bytes) -> 'ZipBuilder':
        if not filename:
            raise ValueError('Filename cannot be empty')
        if filename not in self.zip_file.namelist():
            self.zip_file.writestr(filename, data, ZIP_DEFLATED)
        else:
            raise KeyError('File {} already exists in zip ({})'
                           .format(filename, self.zip_file.namelist()))
        return self

    def build(self) -> bytes:
        self.zip_file.close()
        self.file.seek(0)
        data = self.file.read()
        return data

    def build_zip(self) -> ZipFile:
        return self.zip_file


class FsonZipBuilder:
    PUBLICATIONS_DIR = 'publications'
    RESOURCES_DIR = 'resources'
    MAPPING_FILE = 'fluid_debug.b64_mapping.txt'

    def __init__(self):
        self.zip_builder = ZipBuilder()
        self.add_data(VERSION_FILE, FsonVersion('2'))
        self.b64_mapping = ''

    def add_data(self, filename: str, data) -> 'FsonZipBuilder':
        if isinstance(data, bytes):
            self.zip_builder.add_file(filename, data)
        elif isinstance(data, str):
            self.zip_builder.add_file(filename, data.encode('UTF-8'))
        else:
            self.zip_builder.add_file(filename, pyckson.dumps(data))
        return self

    def add_publication(self, publication: FsonPublication) -> 'FsonZipBuilder':
        b64_name = b64encode(publication.id.encode(), altchars=b'AB').decode()
        data_file_path = '{}/{}'.format(self.PUBLICATIONS_DIR, b64_name)
        try:
            self.add_data(data_file_path, publication)
        except KeyError:
            raise KeyError('A Publication with id "{}" has already been added.'.format(publication.id))
        self._register_new_b64_mapping(publication.id, data_file_path)
        return self

    def add_resource(self, file: FsonResource, data: Optional[bytes]) -> 'FsonZipBuilder':
        b64_name = b64encode(file.id.encode(), altchars=b'AB').decode()
        meta_file_path = '{}/{}.meta'.format(self.RESOURCES_DIR, b64_name)
        try:
            self.add_data(meta_file_path, file)
        except KeyError:
            raise KeyError('A Resource with id "{}" has already been added.'.format(file.id))
        if data is not None:
            data_file_path = '{}/{}.bin'.format(self.RESOURCES_DIR, b64_name)
            self.add_data(data_file_path, data)
            self._register_new_b64_mapping(file.id, '{} and {}'.format(data_file_path, meta_file_path))
        else:
            self._register_new_b64_mapping(file.id, '{} (no content)'.format(meta_file_path))
        return self

    def _register_new_b64_mapping(self, _from: str, to: str):
        self.b64_mapping += '{} => {}\n'.format(_from, to)

    def _add_mapping(self):
        if self.b64_mapping:
            self.add_data(self.MAPPING_FILE, self.b64_mapping)

    def build(self) -> bytes:
        self._add_mapping()
        return self.zip_builder.build()

    def build_zip(self) -> ZipFile:
        self._add_mapping()
        return self.zip_builder.build_zip()
