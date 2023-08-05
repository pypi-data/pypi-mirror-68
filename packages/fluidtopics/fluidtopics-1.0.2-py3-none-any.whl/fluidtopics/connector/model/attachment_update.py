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

from typing import List, Optional, Union

from autovalue import autovalue


@autovalue
class Attachment:
    """A map Attachment is a file resource which is linked to a Publication."""

    def __init__(self, id: str = None, filename: str = None, title: str = None,
                 mime_type: str = None, content: bytes = None, url: str = None,
                 source_id: str = None, khub_id: str = None, file_path: str = None):
        """Prefer using AttachmentBuilder to create an Attachment.

        :param id: Origin ID of the Attachment. It should be unique for a given source.
        :param filename: Name used when the Attachment is downloaded. Extracted from URL of file path if not set.
        :param title: Title of the attachment. It is the name displayed on the link to the attachment in reader (if not
                      overridden by AttachmentLink or AttachCommand title).
                      Fallback to attachment filename if not specified.
        :param mime_type: MIME type of the Attachment. Guessed from the content if not set.
        :param content: Binary content. Not mandatory if you specify an URL.
        :param url: If specified, the Attachment become an URL attachment. Accessing it redirect to this URL.
        :param source_id: ID of the source which contains the attachment.
                          Only specify this parameter to reference an existing Attachment.
        :param khub_id: Khub ID of the Attachment. Can be used instead of origin ID / source ID,
                        to reference an existing Attachment.
        :param file_path: Path of a file in the archive."""
        self.id = id
        self.source_id = source_id
        self.khub_id = khub_id
        self.filename = filename
        self.title = title
        self.mime_type = mime_type
        self.file_path = file_path
        self.content = content
        self.url = url


class InvalidAttachment(Exception):
    def __init__(self, attachment: Attachment):
        msg = '{} is missing origin or khub ID'.format(attachment)
        super(InvalidAttachment, self).__init__(msg)


def _check_attachment(attachment: Attachment):
    if attachment.id is None and attachment.khub_id is None:
        raise InvalidAttachment(attachment)


class AttachmentBuilder:
    """Helper to build a valid Attachment."""

    def __init__(self, attachment: Optional[Attachment] = None):
        """Create an AttachmentBuilder.

        :param attachment: Built Attachment will have same fields than
                           attachment except if you update them."""
        self._id = attachment.id if attachment else None
        self._source_id = attachment.source_id if attachment else None
        self._khub_id = attachment.khub_id if attachment else None
        self._filename = attachment.filename if attachment else None
        self._file_path = attachment.file_path if attachment else None
        self._title = attachment.title if attachment else None
        self._mime_type = attachment.mime_type if attachment else None
        self._content = attachment.content if attachment else None
        self._url = attachment.url if attachment else None

    def id(self, id: Optional[str]) -> 'AttachmentBuilder':
        """Origin ID of the Attachment. It should be unique for a given source."""
        self._id = id
        return self

    def source_id(self, source_id: Optional[str]) -> 'AttachmentBuilder':
        """ID of the source which contains the attachment.
        Only specify this parameter to reference an existing Attachment."""
        self._source_id = source_id
        return self

    def khub_id(self, khub_id: Optional[str]) -> 'AttachmentBuilder':
        """Khub ID of the Attachment.
        Can be used instead of origin ID / source ID, to reference an existing Attachment."""
        self._khub_id = khub_id
        return self

    def filename(self, filename: Optional[str]) -> 'AttachmentBuilder':
        """Name used when the Attachment is downloaded. Extracted from URL of file path if not set."""
        self._filename = filename
        return self

    def file_path(self, file_path: Optional[str]) -> 'AttachmentBuilder':
        """Path of a file in the archive."""
        self._file_path = file_path
        return self

    def title(self, title: Optional[str]) -> 'AttachmentBuilder':
        """Title of the attachment. It is the name displayed on the link to the attachment in reader.
        Fallback to attachment filename if not specified."""
        self._title = title
        return self

    def mime_type(self, mime_type: Optional[str]) -> 'AttachmentBuilder':
        """MIME type of the Attachment. Guessed from the content if not set."""
        self._mime_type = mime_type
        return self

    def content(self, content: Optional[bytes]) -> 'AttachmentBuilder':
        """Binary content. Not mandatory if you specify an URL."""
        self._content = content
        return self

    def url(self, url: Optional[str]) -> 'AttachmentBuilder':
        """If specified, the Attachment become an URL attachment. Accessing it redirect to this URL."""
        self._url = url
        return self

    def build(self) -> Attachment:
        """Build the Attachment from information specified before.

        Attachment should have an ID or a khub ID.
        :raises:
            InvalidAttachment: One of the requirement is not fulfilled."""
        attachment = Attachment(self._id, self._filename, self._title,
                                self._mime_type, self._content, self._url,
                                self._source_id, self._khub_id, self._file_path)
        _check_attachment(attachment)
        return attachment


@autovalue
class AttachCommand:
    """Relation to create between an Attachment and a Publication.
    This object is only used for asynchronous update.
    You can directly add an Attachment to a Publication by adding AttachmentLink to it."""

    def __init__(self, pub_id: str = None, attachment_id: str = None,
                 tags: List[str] = None, title: str = None, insert_at: int = None,
                 pub_khub_id: str = None, attachment_source_id: str = None,
                 attachment_khub_id: str = None):
        """Prefer using AttachCommandBuilder to create a valid AttachCommand.

        Publication and Attachment can be referenced by their origin ID / source ID, or by their khub ID.
        :param pub_id: Origin ID of the target Publication.
        :param attachment_id: Origin ID of the Attachment.
        :param tags: Useless but "it can be useful later"... T.T
        :param title: Title of the attachment for this Publication.
                      It is the name displayed on the link to the attachment in reader.
                      Fallback to Attachment title if not specified.
        :param insert_at: Position in the Attachment list of the Publication where this Attachment will be inserted.
                          Start at 0.
        :param pub_khub_id: Khub ID of the target Publication.
        :param attachment_source_id: Source ID of the Attachment.
        :param attachment_khub_id: Khub ID of the Attachment."""
        self.pub_id = pub_id
        self.pub_khub_id = pub_khub_id
        self.attachment_id = attachment_id
        self.attachment_source_id = attachment_source_id
        self.attachment_khub_id = attachment_khub_id
        self.tags = tags if tags is not None else list()
        self.title = title
        self.insert_at = insert_at


class AttachCommandBuilder:
    """Helper to build a valid AttachCommand.

    Publication and Attachment can be referenced by their origin ID / source ID, or by their khub ID."""

    def __init__(self, attach_command: Optional[AttachCommand] = None):
        """Create an AttachCommandBuilder.

        :param attach_command: Built AttachCommand will have same fields than
                               attach_command except if you update them."""
        self._pub_id = attach_command.pub_id if attach_command else None
        self._pub_khub_id = attach_command.pub_khub_id if attach_command else None
        self._attachment_id = attach_command.attachment_id if attach_command else None
        self._attachment_source_id = attach_command.attachment_source_id if attach_command else None
        self._attachment_khub_id = attach_command.attachment_khub_id if attach_command else None
        self._tags = attach_command.tags if attach_command else None
        self._title = attach_command.title if attach_command else None
        self._insert_at = attach_command.insert_at if attach_command else None

    def pub_id(self, pub_id: Optional[str]) -> 'AttachCommandBuilder':
        """Origin ID of the target Publication."""
        self._pub_id = pub_id
        return self

    def pub_khub_id(self, pub_khub_id: Optional[str]) -> 'AttachCommandBuilder':
        """Khub ID of the target Publication."""
        self._pub_khub_id = pub_khub_id
        return self

    def attachment_id(self, attachment_id: Optional[str]) -> 'AttachCommandBuilder':
        """Origin ID of the Attachment."""
        self._attachment_id = attachment_id
        return self

    def attachment_source_id(self, attachment_source_id: Optional[str]) -> 'AttachCommandBuilder':
        """Source ID of the Attachment."""
        self._attachment_source_id = attachment_source_id
        return self

    def attachment_khub_id(self, attachment_khub_id: Optional[str]) -> 'AttachCommandBuilder':
        """Khub ID of the Attachment."""
        self._attachment_khub_id = attachment_khub_id
        return self

    def title(self, title: Optional[str]) -> 'AttachCommandBuilder':
        """Title of the attachment for this Publication.
           It is the name displayed on the link to the attachment in reader.
           Fallback to Attachment title if not specified."""
        self._title = title
        return self

    def insert_at(self, insert_at: Optional[int]) -> 'AttachCommandBuilder':
        """Position in the Attachment list of the Publication where this Attachment will be inserted. Start at 0."""
        self._insert_at = insert_at
        return self

    def build(self) -> AttachCommand:
        """Build the AttachCommand from information specified before.

        Publication and Attachment can be referenced by their origin ID / source ID, or by their khub ID.
        :raises:
            InvalidCommand: One of the requirement is not fulfilled."""
        command = AttachCommand(self._pub_id, self._attachment_id, self._tags,
                                self._title, self._insert_at, self._pub_khub_id,
                                self._attachment_source_id, self._attachment_khub_id)
        _check_command(command)
        return command


@autovalue
class DetachCommand:
    """Relation to remove between an Attachment and a Publication."""

    def __init__(self, pub_id: str = None, attachment_id: str = None,
                 pub_khub_id: str = None, attachment_source_id: str = None,
                 attachment_khub_id: str = None):
        """Prefer using DetachCommandBuilder to create a valid DetachCommand.

        Publication and Attachment can be referenced by their origin ID / source ID, or by their khub ID.
        :param pub_id: Origin ID of the target Publication.
        :param attachment_id: Origin ID of the Attachment.
        :param pub_khub_id: Khub ID of the target Publication.
        :param attachment_source_id: Source ID of the Attachment.
        :param attachment_khub_id: Khub ID of the Attachment."""
        self.pub_id = pub_id
        self.pub_khub_id = pub_khub_id
        self.attachment_id = attachment_id
        self.attachment_source_id = attachment_source_id
        self.attachment_khub_id = attachment_khub_id


class InvalidCommand(Exception):
    def __init__(self, command: Union[AttachCommand, DetachCommand]):
        msg = '{} is missing publication or attachment IDs'.format(command)
        super(InvalidCommand, self).__init__(msg)


def _check_command(command: Union[AttachCommand, DetachCommand]):
    if (command.attachment_id is None and command.attachment_khub_id is None) \
            or (command.pub_id is None and command.pub_khub_id is None):
        raise InvalidCommand(command)


class DetachCommandBuilder:
    """Helper to build a valid DetachCommand.

    Publication and Attachment can be referenced by their origin ID / source ID, or by their khub ID."""

    def __init__(self, detach_command: Optional[DetachCommand] = None):
        """Create a DetachCommandBuilder.

            :param detach_command: Built DetachCommand will have same fields than
                       detach_command except if you update them."""

        self._pub_id = detach_command.pub_id if detach_command else None
        self._pub_khub_id = detach_command.pub_khub_id if detach_command else None
        self._attachment_id = detach_command.attachment_id if detach_command else None
        self._attachment_source_id = detach_command.attachment_source_id if detach_command else None
        self._attachment_khub_id = detach_command.attachment_khub_id if detach_command else None

    def pub_id(self, pub_id: Optional[str]) -> 'DetachCommandBuilder':
        """Origin ID of the target Publication."""
        self._pub_id = pub_id
        return self

    def pub_khub_id(self, pub_khub_id: Optional[str]) -> 'DetachCommandBuilder':
        """Khub ID of the target Publication."""
        self._pub_khub_id = pub_khub_id
        return self

    def attachment_id(self, attachment_id: Optional[str]) -> 'DetachCommandBuilder':
        """Origin ID of the Attachment."""
        self._attachment_id = attachment_id
        return self

    def attachment_source_id(self, attachment_source_id: Optional[str]) -> 'DetachCommandBuilder':
        """Source ID of the Attachment."""
        self._attachment_source_id = attachment_source_id
        return self

    def attachment_khub_id(self, attachment_khub_id: Optional[str]) -> 'DetachCommandBuilder':
        """Khub ID of the Attachment."""
        self._attachment_khub_id = attachment_khub_id
        return self

    def build(self) -> DetachCommand:
        """Build the DetachCommand from information specified before.

        Publication and Attachment can be referenced by their origin ID / source ID, or by their khub ID.
        :raises:
            InvalidCommand: One of the requirement is not fulfilled."""
        command = DetachCommand(self._pub_id, self._attachment_id, self._pub_khub_id,
                                self._attachment_source_id, self._attachment_khub_id)
        _check_command(command)
        return command


@autovalue
class AttachmentsUpdate:
    """List of all attachment updates to do."""

    def __init__(self, attachments: List[Attachment],
                 attach: List[AttachCommand],
                 detach: List[DetachCommand]):
        """Prefer using AttachmentUpdateBuilder to create a valid AttachmentUpdate.

        :param attachments: All attachments that will be created/updated.
        :param attach: All attach commands to execute. Corresponding Attachment should be in attachments
                       if it doesn't already exist in khub.
        :param  detach: All detach command to execute."""
        self.attachments = attachments
        self.attach = attach
        self.detach = detach


class AttachmentsUpdateBuilder:
    """Helper to build a valid AttachmentsUpdate."""
    def __init__(self, update: Optional[AttachmentsUpdate] = None):
        self._attachments = update.attachments if update else []
        self._attach = update.attach if update else []
        self._detach = update.detach if update else []

    def attachment(self, id: str, filename: str, title: str = None,
                   mime_type: str = None, content: bytes = None,
                   url: str = None) -> 'AttachmentsUpdateBuilder':
        """Add an attachment to the Attachment list.

        :param id: Origin ID of the Attachment. It should be unique for a given source.
        :param filename: Name used when the Attachment is downloaded. Extracted from URL of file path if not set.
        :param title: Title of the attachment. It is the name displayed on the link to the attachment in reader (if not
                      overridden by AttachCommand title).
                      Fallback to attachment filename if not specified.
        :param mime_type: MIME type of the Attachment. Guessed from the content if not set.
        :param content: Binary content. Not mandatory if you specify an URL.
        :param url: If specified, the Attachment become an URL attachment. Accessing it redirect to this URL."""
        attachment = Attachment(id, filename, title, mime_type, content, url)
        self._attachments.append(attachment)
        return self

    def add_attachments(self, *attachments: Attachment) -> 'AttachmentsUpdateBuilder':
        """Add attachments to the Attachment list.

        :raises:
            InvalidAttachment: An Attachment is not valid."""
        for attachment in attachments:
            _check_attachment(attachment)
        self._attachments.extend(attachments)
        return self

    def attach(self, pub_id: str, attachment_id: str, title: str = None,
               insert_at: int = None) -> 'AttachmentsUpdateBuilder':
        """Add an attach command.

        :param pub_id: Origin ID of the target Publication.
        :param attachment_id: Origin ID of the Attachment.
        :param title: Title of the attachment for this Publication.
                      It is the name displayed on the link to the attachment in reader.
                      Fallback to Attachment title if not specified.
        :param insert_at: Position in the Attachment list of the Publication where this Attachment will be inserted.
                          Start at 0."""
        command = AttachCommand(pub_id, attachment_id, title=title, insert_at=insert_at)
        self._attach.append(command)
        return self

    def add_attach_commands(self, *commands: AttachCommand) -> 'AttachmentsUpdateBuilder':
        """Add attach commands.

        :raises:
            InvalidCommand: An AttachCommand is not valid."""
        for command in commands:
            _check_command(command)
        self._attach.extend(commands)
        return self

    def detach(self, pub_id: str, attachment_id: str) -> 'AttachmentsUpdateBuilder':
        """Add a detach command.

        :param pub_id: Origin ID of the target Publication.
        :param attachment_id: Origin ID of the Attachment."""
        command = DetachCommand(pub_id, attachment_id)
        self._detach.append(command)
        return self

    def add_detach_commands(self, *commands: DetachCommand) -> 'AttachmentsUpdateBuilder':
        """Add detach commands.

        :raises:
            InvalidCommand: A DetachCommand is not valid."""
        for command in commands:
            _check_command(command)
        self._detach.extend(commands)
        return self

    def build(self) -> AttachmentsUpdate:
        """Build the AttachmentsUpdate from information specified before."""
        return AttachmentsUpdate(self._attachments, self._attach, self._detach)
