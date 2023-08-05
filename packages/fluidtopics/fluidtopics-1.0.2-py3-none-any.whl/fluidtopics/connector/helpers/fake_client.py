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

from assertpy import assert_that
from injector import singleton

from fluidtopics.connector.client import Client
from fluidtopics.connector.model.document import Document


@singleton
class FakeClient(Client):
    """FakeClient is a helper to mock a Client in tests."""

    def __init__(self):
        self.publications = []
        self.publish_name = None

    def publish(self, *publications: Document, publish_name: str = 'publish.zip'):
        """Publish a Document to Fluid Topics.

        Published documents can be found in `.publications` list field.
        It is also possible to access a specific published document with
        `.publication('document_id')`.

        :param publications: Documents to publish.
        :param publish_name: Name of this publish run in Fluid Topics Knowledge Hub > Process Content.
        :raises: KeyError: A Document or Resource is published twice.
        """
        self.publish_name = publish_name
        self.publications.extend(publications)

    def publication(self, pub_id: str) -> Document:
        """Returns the last Document with corresponding ID.

        :param pub_id: ID of the expected document.
        :return: Last Document with the given ID.
        :raises: AssertionError: No Publication was published with this ID.
        """
        publication = self._find_publication(pub_id)
        assert_that(publication).described_as('{} not found in published publications: {}'
                                              .format(pub_id, [pub.document_id for pub in self.publications])) \
            .is_not_none()
        return publication

    def assert_not_published(self, pub_id: str):
        """Asserts that no document has been published with this ID.

        :param pub_id: ID of the Document which should not be published.
        :raises: AssertionError: A Document has been published with this ID.
        """
        publication = self._find_publication(pub_id)
        assert_that(publication).described_as('{} is published'.format(pub_id)) \
            .is_none()

    def _find_publication(self, pub_id: str) -> Optional[Document]:
        return next((pub for pub in reversed(self.publications) if pub.document_id == pub_id), None)
