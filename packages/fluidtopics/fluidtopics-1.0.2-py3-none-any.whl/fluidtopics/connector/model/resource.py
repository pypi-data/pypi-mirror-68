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
from os.path import basename
from typing import Optional

from autovalue import autovalue

from fluidtopics.connector.internal.utils import Utils


class InvalidResource(ValueError):
    pass


@autovalue
class Resource:
    """Binary files used in HTML content of Topics.

    A Resource can be an image. It is referred to as `<img src="resource_id"/>` in HTML.
    A Resource can also be an arbitrary binary file. It is referred to as `<a href="resource_id"/> in HTML.

    A Resource object is immutable: once created, it is not possible to modify it.
    To create another Resource object from this one, use `.update()` method.
    Example:
    >>> resource = Resource('id', b'content')
    >>> resource.update(content=b'new content', filename='filename')
    Resource(resource_id=id, content=b'new content', filename=filename)
    """

    def __init__(self, resource_id: str,
                 content: bytes,
                 filename: str = None,
                 mime_type: Optional[str] = None):
        """Create a Resource.

        :param resource_id: ID of the Resource. It should be unique. Should not be empty.
        :param content: Binary content.
        :param filename: Name used when the resource is downloaded. Fallback to the resource_id when not specified.
        :param mime_type: Standard IANA media type. Detected automatically in Fluid Topics when not specified.
        :raises: InvalidResource: Data integrity criteria are not respected.
        """
        if not resource_id:
            raise InvalidResource('Resource should have an id')
        self.resource_id = resource_id
        self.content = content
        self.filename = filename or basename(resource_id)
        self.mime_type = mime_type

    @staticmethod
    def from_uri(resource_id: str,
                 uri: str,
                 mime_type: Optional[str] = None) -> 'Resource':
        """Create a Resource from its URI.

        URI can be a file path or a URL.

        :param resource_id: ID of the Resource. It should be unique. Should not be empty.
        :param uri: Path of the resource file.
        :param mime_type: Standard IANA media type. Detected automatically in Fluid Topics when not specified.
        :raises: InvalidResource: Data integrity criteria are not respected.
        """
        filename, content = Utils.extract_from(uri)
        return Resource(
            resource_id=resource_id,
            content=content,
            filename=filename,
            mime_type=mime_type)
