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

import base64

from injector import Injector

from fluidtopics.connector.internal.fson.fson_publication import PublicationConverter
from fluidtopics.connector.internal.fson.fson_resource import ResourceConverter
from fluidtopics.connector.internal.sender import RemoteSender, SenderError
from fluidtopics.connector.internal.zip_builder import FsonZipBuilder
from fluidtopics.connector.model.document import Document
from fluidtopics.connector.model.external_document import ExternalDocument
from fluidtopics.connector.model.structured_document import StructuredDocument
from fluidtopics.connector.model.unstructured_document import UnstructuredDocument


class Client:
    """Interface which enables interaction with Fluid Topics."""

    def publish(self, *publications: Document, publish_name: str = 'publish.zip'):
        """Publish a Document to Fluid Topics

        :param publications: Documents to publish.
        :param publish_name: Name of this publish run in Fluid Topics Knowledge Hub > Process Content.
        """
        raise NotImplementedError()


class Authentication:
    """Authentication interface for the RemoteClient."""

    def basic_authentication(self) -> str:
        raise NotImplementedError(
            "Please provide an object with the attribute 'basic_authentication' that returns 'login:password'"
            'encoded as base 64. See : https:/'
            '/www.ibm.com/support/knowledgecenter/en/SSGMCP_5.1.0/com.ibm.cics.ts.internet.doc/topics/dfhtl2a.html'
        )


class LoginAuthentication(Authentication):
    """Authentication using login/password for the RemoteClient."""

    def __init__(self, login: str = 'root@fluidtopics.com', password: str = 'change_it'):
        self.login = login
        self.password = password

    def basic_authentication(self) -> str:
        bytes_encoded = bytes('{}:{}'.format(self.login, self.password), 'utf-8')
        b64_encoded = base64.b64encode(bytes_encoded)
        return b64_encoded.decode('utf-8')


class Base64Authentication(Authentication):
    """Authentication method which directly sets the value of the Authorization http header."""

    def __init__(self, basic_authentication: str):
        self._authentication = basic_authentication

    def basic_authentication(self) -> str:
        return self._authentication


class RemoteClientError(Exception):
    pass


class RemoteClient(Client):
    """Implementation of the Client interface which uses Fluid Topics web services."""

    def __init__(self, url: str, authentication: Authentication, source_id: str):
        """Create a RemoteClient.

        :param url: URL of the Fluid Topics server (like "http://doc.antidot.net").
        :param authentication: User (with KHUB_ADMIN rights) used to call web services.
        :param source_id: ID of the external source to publish into in Fluid Topics.
        """
        self._sender = RemoteSender(url, authentication.basic_authentication(), source_id)
        injector = Injector()
        self._publication_converter = injector.get(PublicationConverter)
        self._resource_converter = injector.get(ResourceConverter)

    def __repr__(self):
        return 'RemoteClient:[url={}, source_id={}]'.format(self._sender.url, self._sender.source_id)

    def publish(self, *publications: Document, publish_name: str = 'publish.zip') -> str:
        """Publish a Document to Fluid Topics

        :param publications: Documents to publish.
        :param publish_name: Name of this publish process in Fluid Topics Knowledge Hub > Process Content.
        :return: Upload ID of this publish run.
        :raises: RemoteClientError: Publish web service call failed.
        :raises: KeyError: A Document or a Resource is published twice.
        """
        zip_builder = FsonZipBuilder()
        self._populate_zip(zip_builder, *publications)
        try:
            return self._sender.publish(zip_builder.build(), publish_name)
        except SenderError as e:
            raise RemoteClientError(str(e))

    def create_source(self, name: str = None, description: str = ''):
        """Create an external source corresponding to the RemoteClient source ID.
        Does nothing if the source already exists.

        :param name: Name of the created source. If not specified, source ID is used.
        :param description: Description of the created source.
        :raises: RemoteClientError: Source creation web service call failed.
        """
        try:
            self._sender.create_source(name, description)
        except SenderError as e:
            raise RemoteClientError(str(e))

    def _populate_zip(self, fson_zip: FsonZipBuilder, *documents: Document):
        for document in documents:
            if isinstance(document, StructuredDocument):
                self._populate_zip_with_structured_document(fson_zip, document)
            elif isinstance(document, UnstructuredDocument):
                self._populate_zip_with_unstructured_document(fson_zip, document)
            elif isinstance(document, ExternalDocument):
                self._populate_zip_with_external_document(fson_zip, document)

    def _populate_zip_with_structured_document(self, fson_zip: FsonZipBuilder, document: StructuredDocument):
        fson_publication = self._publication_converter.convert_structured_document(document)
        fson_zip.add_publication(fson_publication)
        for attachment in document.attachments:
            fson_resource = self._resource_converter.convert_attachment(attachment, document.document_id)
            fson_zip.add_resource(fson_resource, attachment.content)
        for resource in document.resources:
            fson_resource = self._resource_converter.convert_resource(resource)
            fson_zip.add_resource(fson_resource, resource.content)

    def _populate_zip_with_unstructured_document(self, fson_zip: FsonZipBuilder, document: UnstructuredDocument):
        fson_publication = self._publication_converter.convert_unstructured_document(document)
        fson_zip.add_publication(fson_publication)
        fson_resource = self._resource_converter.convert_content(document)
        fson_zip.add_resource(fson_resource, document.content)

    def _populate_zip_with_external_document(self, fson_zip: FsonZipBuilder, document: ExternalDocument):
        fson_publication = self._publication_converter.convert_unstructured_document(document)
        fson_zip.add_publication(fson_publication)
        fson_resource = self._resource_converter.convert_external_content(document)
        fson_zip.add_resource(fson_resource, None)
