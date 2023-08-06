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
from fluidtopics.connector.model.attachment import Attachment


class IdProvider:
    def ud_resource_id(self, publication_id: str) -> str:
        return '{}_content'.format(publication_id)

    def attachment_id(self, map_id: str, attachment: Attachment) -> str:
        return attachment.attachment_id or '{}-{}'.format(map_id, attachment.filename)
