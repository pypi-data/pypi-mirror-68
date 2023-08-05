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

from fluidtopics.connector.internal.utils import Utils


class InvalidAttachment(ValueError):
    pass


@autovalue
class Attachment:
    """Attachment of a StructuredDocument (also called map attachment).

    An Attachment object is immutable: once created, it is not possible to modify it.
    To create another Attachment object from this one, use `.update()` method.
    Example:
    >>> attachment = Attachment('filename', b'content')
    >>> attachment.update(filename='new_filename', title='Title')
    Attachment(filename='new_filename', content=b'content', title='Title')
    """

    def __init__(self, filename: str,
                 content: bytes = None,
                 title: str = None,
                 attachment_id: Optional[str] = None,
                 mime_type: Optional[str] = None,
                 url: Optional[str] = None):
        """Create an Attachment.

        :param filename: Filename of the Attachment when downloaded. Should not be empty.
        :param content: Binary content of the Attachment. Should be specified when url is not specified.
        :param title: Name displayed in the Attachment tab. Fallback to filename when not specified.
        :param attachment_id: Origin ID of the Attachment. Fallback to filename + document ID when not specified.
        :param mime_type: Standard IANA media type. Detected automatically in Fluid Topics when not specified.
        :param url: URL of the external Attachment. Should be specified when content is not specified.
        :raises: InvalidAttachment: Data integrity criteria are not respected.
        """
        if not filename:
            raise InvalidAttachment('Attachment should have a filename.')
        if not content and not url:
            raise InvalidAttachment('Attachment {} should have content or a URL'.format(filename))
        self.attachment_id = attachment_id
        self.filename = filename
        self.title = title or filename
        self.mime_type = mime_type
        self.content = content
        self.url = url

    @staticmethod
    def from_uri(uri: str,
                 filename: str = None,
                 attachment_id: str = None,
                 title: str = None,
                 mime_type: str = None) -> 'Attachment':
        """Create an Attachment from its URI.

        URI can be a file path or a URL.

        :param uri: Path of the Attachment file.
        :param filename: Filename of the Attachment. Deduced from uri if not specified.
        :param attachment_id: Origin ID of the Attachment. Fallback to filename + document ID when not specified.
        :param title: Name displayed in the Attachment tab. Fallback to filename when not specified.
        :param mime_type: Standard IANA media type. Detected automatically in Fluid Topics when not specified.
        :raises: InvalidAttachment: Data integrity criteria are not respected.
        """
        extracted_filename, content = Utils.extract_from(uri)
        return Attachment(
            filename=filename or extracted_filename,
            content=content,
            attachment_id=attachment_id,
            title=title,
            mime_type=mime_type)
