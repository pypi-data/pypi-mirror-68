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

from typing import Optional, List

from assertpy import assert_that

from fluidtopics.connector.model.attachment_update import Attachment, AttachCommand, DetachCommand


class AttachmentChecker:
    """Helper to check an Attachment."""

    def __init__(self, attachment: Attachment):
        """Create an AttachmentChecker.

        :param attachment: Attachment to check."""
        self._attachment = attachment

    def has_id(self, attachment_id: Optional[str]) -> 'AttachmentChecker':
        assert_that(self._attachment).has_id(attachment_id)
        return self

    def has_source_id(self, source_id: Optional[str]) -> 'AttachmentChecker':
        assert_that(self._attachment).has_source_id(source_id)
        return self

    def has_khub_id(self, khub_id: Optional[str]) -> 'AttachmentChecker':
        assert_that(self._attachment).has_khub_id(khub_id)
        return self

    def has_filename(self, filename: Optional[str]) -> 'AttachmentChecker':
        assert_that(self._attachment).has_filename(filename)
        return self

    def has_title(self, title: Optional[str]) -> 'AttachmentChecker':
        assert_that(self._attachment).has_title(title)
        return self

    def has_mime_type(self, mime_type: Optional[str]) -> 'AttachmentChecker':
        assert_that(self._attachment).has_mime_type(mime_type)
        return self

    def has_content(self, content: Optional[bytes]) -> 'AttachmentChecker':
        assert_that(self._attachment).has_content(content)
        return self

    def has_url(self, url: Optional[str]) -> 'AttachmentChecker':
        assert_that(self._attachment).has_url(url)
        return self


class AttachCommandChecker:
    """Helper to check an AttachCommand."""

    def __init__(self, attach_cmd: AttachCommand):
        """Create an AttachCommandChecker.

        :param attach_cmd: AttachCommand to check."""
        self._attach_cmd = attach_cmd

    def has_pub_id(self, pub_id: Optional[str]) -> 'AttachCommandChecker':
        assert_that(self._attach_cmd).has_pub_id(pub_id)
        return self

    def has_pub_khub_id(self, pub_khub_id: Optional[str]) -> 'AttachCommandChecker':
        assert_that(self._attach_cmd).has_pub_khub_id(pub_khub_id)
        return self

    def has_attachment_id(self, attachment_id: Optional[str]) -> 'AttachCommandChecker':
        assert_that(self._attach_cmd).has_attachment_id(attachment_id)
        return self

    def has_attachment_source_id(self, attachment_source_id: Optional[str]) -> 'AttachCommandChecker':
        assert_that(self._attach_cmd).has_attachment_source_id(attachment_source_id)
        return self

    def has_attachment_khub_id(self, attachment_khub_id: Optional[str]) -> 'AttachCommandChecker':
        assert_that(self._attach_cmd).has_attachment_khub_id(attachment_khub_id)
        return self

    def has_tags(self, tags: List[str]) -> 'AttachCommandChecker':
        assert_that(self._attach_cmd).has_tags(tags)
        return self

    def has_title(self, title: Optional[str]) -> 'AttachCommandChecker':
        assert_that(self._attach_cmd).has_title(title)
        return self

    def has_insert_at(self, insert_at: Optional[int]) -> 'AttachCommandChecker':
        assert_that(self._attach_cmd).has_insert_at(insert_at)
        return self


class DetachCommandChecker:
    """Helper to check an DetachCommand."""

    def __init__(self, detach_cmd: DetachCommand):
        """Create a DetachCommandChecker.

        :param detach_cmd: DetachCommand to check."""
        self._detach_cmd = detach_cmd

    def has_pub_id(self, pub_id: Optional[str]) -> 'DetachCommandChecker':
        assert_that(self._detach_cmd).has_pub_id(pub_id)
        return self

    def has_pub_khub_id(self, pub_khub_id: Optional[str]) -> 'DetachCommandChecker':
        assert_that(self._detach_cmd).has_pub_khub_id(pub_khub_id)
        return self

    def has_attachment_id(self, attachment_id: Optional[str]) -> 'DetachCommandChecker':
        assert_that(self._detach_cmd).has_attachment_id(attachment_id)
        return self

    def has_attachment_source_id(self, attachment_source_id: Optional[str]) -> 'DetachCommandChecker':
        assert_that(self._detach_cmd).has_attachment_source_id(attachment_source_id)
        return self

    def has_attachment_khub_id(self, attachment_khub_id: Optional[str]) -> 'DetachCommandChecker':
        assert_that(self._detach_cmd).has_attachment_khub_id(attachment_khub_id)
        return self
