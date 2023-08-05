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

from typing import Optional

from autovalue import autovalue
from injector import inject

from fluidtopics.connector.internal.id_provider import IdProvider
from fluidtopics.connector.model.attachment import Attachment
from fluidtopics.connector.model.external_document import ExternalDocument
from fluidtopics.connector.model.resource import Resource
from fluidtopics.connector.model.unstructured_document import UnstructuredDocument

EXTERNAL_DOCUMENT_FILENAME = 'external_document'


@autovalue
class FsonResource:
    def __init__(self, id: str, filename: str,
                 mime_type: str = None, description: str = None,
                 indexable_content: str = None, url: str = None):
        self.id = id
        self.filename = filename
        self.mime_type = mime_type
        self.description = description
        self.indexable_content = indexable_content
        self.url = url


class ResourceConverter:
    @inject
    def __init__(self, id_provider: IdProvider):
        self._id_provider = id_provider

    def convert_resource(self, resource: Resource, description: Optional[str] = None) -> FsonResource:
        return FsonResource(
            id=resource.resource_id,
            filename=resource.filename,
            mime_type=resource.mime_type,
            description=description)

    def convert_content(self, ud: UnstructuredDocument) -> FsonResource:
        return FsonResource(
            id=self._id_provider.ud_resource_id(ud.document_id),
            filename=ud.filename,
            mime_type=ud.mime_type,
            indexable_content=ud.indexable_content)

    def convert_external_content(self, external: ExternalDocument) -> FsonResource:
        return FsonResource(
            id=self._id_provider.ud_resource_id(external.document_id),
            filename=EXTERNAL_DOCUMENT_FILENAME,
            mime_type=external.mime_type,
            indexable_content=external.indexable_content)

    def convert_attachment(self, attachment: Attachment, map_id: str) -> FsonResource:
        return FsonResource(
            id=self._id_provider.attachment_id(map_id, attachment),
            filename=attachment.filename,
            mime_type=attachment.mime_type,
            url=attachment.url)
