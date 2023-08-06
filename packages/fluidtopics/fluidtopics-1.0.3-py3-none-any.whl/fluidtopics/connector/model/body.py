# Copyright 2019 Antidot opensource@antidot.net
#
# This file is part of Fluid-Topics python API
#
# Fluid-Topics python API is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# Fluid-Topics python API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import List

from autovalue import autovalue
from lxml import etree


FT_LINK_TYPE_ATTR = 'data-ft-link-type'
FT_LINK_TYPE_BASE_ID = 'baseId'

EXPANDING_BLOCK_LINK_CLASS = 'ft-expanding-block-link'
EXPANDING_BLOCK_TARGET_ID_ATTR = 'data-target-id'
EXPANDING_BLOCK_CONTENT_CLASS = 'ft-expanding-block-content'
EXPANDING_BLOCK_INLINE_CONTENT_CLASS = 'ft-expanding-block-inline-content'


class ExpandingBlock:
    """Helper to generate expanding block HTML."""
    def __init__(self, id: str):
        """Create an ExpandingBlock which contains a topic.
        :param id: ID of the topic in the expanding block"""
        self.id = id

    def get_link(self, text: str = '', children: List[etree.Element] = None, tail: str = '') -> etree.Element:
        """Get the HTML link of the expanding block."""
        link = etree.Element('span')
        link.set('class', EXPANDING_BLOCK_LINK_CLASS)
        link.set(EXPANDING_BLOCK_TARGET_ID_ATTR, self.id)
        return self._fill_element(link, text, children, tail)

    def get_block_content(self, text: str = '', children: List[etree.Element] = None, tail: str = '') -> etree.Element:
        """Get the HTML <div> where the topic content will be expanded."""
        div = etree.Element('div')
        div.set('class', EXPANDING_BLOCK_CONTENT_CLASS)
        div.set('id', self.id)
        return self._fill_element(div, text, children, tail)

    def get_inline_content(self, text: str = '', children: List[etree.Element] = None, tail: str = '') -> etree.Element:
        """Get the HTML <span> where the topic content will be expanded."""
        span = etree.Element('span')
        span.set('class', EXPANDING_BLOCK_INLINE_CONTENT_CLASS)
        span.set('id', self.id)
        return self._fill_element(span, text, children, tail)

    def _fill_element(self, element, text, children, tail) -> etree.Element:
        element.text = text
        element.extend(children if children is not None else [])
        element.tail = tail
        return element


@autovalue
class Body:
    """Body of a Topic"""
    def __init__(self, html: str = None, resource_reference: str = None):
        """Create a Body. It is advise to use none(), html() or file() to create a Body
        instead of using constructor.

        :param html: HTML content of the body
        :param resource_reference: Resource ID"""
        self.html = html
        self.resource_reference = resource_reference

    @staticmethod
    def none() -> 'Body':
        """Create empty Body."""
        return Body()

    @staticmethod
    # pylint: disable=method-hidden
    def html(html: str) -> 'Body':
        """Create HTML Body."""
        return Body(html=html)

    @staticmethod
    def file(resource_reference: str) -> 'Body':
        """Create file Body.

        :param resource_reference: ID of the resource"""
        return Body(resource_reference=resource_reference)
