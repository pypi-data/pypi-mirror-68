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

from fluidtopics.connector.client import Client, RemoteClient, Authentication, Base64Authentication, \
    LoginAuthentication, RemoteClientError
from fluidtopics.connector.helpers.fake_client import FakeClient
from fluidtopics.connector.helpers.metadata_inheritor import MetadataInheritor
from fluidtopics.connector.model.attachment import Attachment, InvalidAttachment
from fluidtopics.connector.model.document import Document, InvalidDocument
from fluidtopics.connector.model.external_document import ExternalDocument
from fluidtopics.connector.model.has_metadata import HasMetadata
from fluidtopics.connector.model.metadata import SemanticMetadata, OpenMode, Snapshot, Metadata, InvalidMetadata, \
    DEFAULT_PRODUCER, EditorialType, DEFAULT_LOCALE
from fluidtopics.connector.model.resource import Resource, InvalidResource
from fluidtopics.connector.model.structured_document import StructuredDocument, InvalidStructuredDocument
from fluidtopics.connector.model.topic import Topic, InvalidTopic
from fluidtopics.connector.model.unstructured_document import UnstructuredDocument, InvalidUnstructuredDocument

__all__ = [
    'DEFAULT_LOCALE',
    'DEFAULT_PRODUCER',
    'Attachment',
    'Base64Authentication',
    'Client',
    'EditorialType',
    'ExternalDocument',
    'FakeClient',
    'HasMetadata',
    'InvalidAttachment',
    'InvalidDocument',
    'InvalidMetadata',
    'InvalidResource',
    'InvalidStructuredDocument',
    'InvalidTopic',
    'InvalidUnstructuredDocument',
    'LoginAuthentication',
    'Metadata',
    'MetadataInheritor',
    'OpenMode',
    'Document',
    'RemoteClient',
    'RemoteClientError',
    'Resource',
    'SemanticMetadata',
    'Snapshot',
    'StructuredDocument',
    'Topic',
    'UnstructuredDocument',
]
