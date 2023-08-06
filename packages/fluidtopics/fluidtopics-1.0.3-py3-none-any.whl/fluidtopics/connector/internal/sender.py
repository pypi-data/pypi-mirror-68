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

from typing import Dict, Optional

import requests
from requests import Response

UPLOAD_ID_FIELD = 'uploadId'

SOURCE_TYPE = 'External'


class SenderError(Exception):
    def __init__(self, msg: str,
                 verb: str = None,
                 url: Optional[str] = None,
                 response: Optional[Response] = None):
        super().__init__(msg)
        self.verb = verb or response.request.method
        self.url = url or response.request.url
        self.status_code = response.status_code if response is not None else None
        self.response = response.text if response is not None else None

    def __str__(self):
        msg = '{} {} fails: {}'.format(self.verb, self.url, super().__str__())
        if self.status_code is not None:
            msg += '\nResponse: {}'.format(self.status_code)
            if self.response:
                msg += ' - {}'.format(self.response)
        return msg


class RemoteSender:
    def __init__(self, url: str, auth: str, source_id: str):
        self.url = url[:-1] if url.endswith('/') else url
        self.auth = auth
        self.source_id = source_id

    def publish(self, data: bytes, filename: str) -> str:
        response = self._send(
            method='POST',
            url=self._upload_endpoint(),
            files={filename: data},
            error_msg='publish fail')
        try:
            return response.json()[UPLOAD_ID_FIELD]
        except ValueError:
            msg = 'publish succeed but response is not JSON valid'
            raise SenderError(msg, response=response)
        except KeyError:
            msg = 'publish succeed but response does not contain {}'.format(UPLOAD_ID_FIELD)
            raise SenderError(msg, response=response)

    def create_source(self, name: str = None, description: str = '') -> bool:
        body = {
            'name': name or self.source_id,
            'type': SOURCE_TYPE,
            'description': description
        }
        response = self._send(
            method='PUT',
            url=self._source_endpoint(),
            json=body,
            error_msg='source creation fail')
        return response.status_code == 201

    def _get_header(self) -> Dict[str, str]:
        return {'Authorization': 'Basic {}'.format(self.auth)}

    def _upload_endpoint(self) -> str:
        return '{}/api/admin/khub/sources/{}/upload'.format(self.url, self.source_id)

    def _source_endpoint(self) -> str:
        return '{}/api/admin/khub/sources/{}'.format(self.url, self.source_id)

    def _send(self, method: str,
              url: str,
              error_msg: str,
              json: dict = None,
              files: Dict[str, bytes] = None) -> Response:
        try:
            response = requests.request(
                method=method,
                url=url,
                json=json,
                files=files,
                headers=self._get_header())
        except requests.exceptions.ConnectionError:
            raise SenderError('connection to server fail, check URL validity', verb='POST', url=url)
        if not response.ok:
            raise SenderError(error_msg, response=response)
        return response
