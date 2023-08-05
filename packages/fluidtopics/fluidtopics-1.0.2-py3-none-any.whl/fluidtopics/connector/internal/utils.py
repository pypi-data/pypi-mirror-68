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

import re
from os.path import basename
from typing import Tuple

import requests

IETF_LOCALE_TAG_REGEX = re.compile(r'^[a-z]{2}(?:-[A-Z]{2})?$')
URL_REGEX = re.compile(r'^https?://.+')


class Utils:
    @staticmethod
    def parse_ietf_locale_tag(locale_tag: str) -> str:
        locale_separator = '-'
        if locale_tag is not None:
            normalized_locale_tag = locale_tag.replace('_', locale_separator).lower()
            if locale_separator in normalized_locale_tag:
                country, region = normalized_locale_tag.split(locale_separator, maxsplit=1)
                normalized_locale_tag = locale_separator.join([country, region.upper()])
            if IETF_LOCALE_TAG_REGEX.match(normalized_locale_tag):
                return normalized_locale_tag

        raise ValueError('Invalid ISO code "{}". Expect valid ISO 639 locale (like "en-US").'.format(locale_tag))

    @staticmethod
    def extract_from(uri: str) -> Tuple[str, bytes]:
        filename = basename(uri)
        if URL_REGEX.match(uri):
            response = requests.get(uri)
            content = response.content
        else:
            with open(uri, 'rb') as file:
                content = file.read()
        return filename, content
