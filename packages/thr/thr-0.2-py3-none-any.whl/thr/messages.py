import secrets
from typing import Optional
import json
from .crypto import SYMMETRIC_KEY_LENGTH


def generate_padding(length: Optional[int] = None) -> bytes:
    '''
    Generates a padding with a random length or the specified length if the
    parameter `length` is used.
    '''
    if length < 0 or length > 255:
        raise ValueError("length must be between 0 and 255 (inclusive).")
    if length is None:
        length = secrets.randbelow(256)
    padding = length.to_bytes(1, byteorder='big')
    return padding * length


class Message:
    '''
    Base class for messages.
    '''
    type_byte: bytes

    def get_data(self) -> bytes:
        '''
        Returns the binary representation without padding bytes.
        '''
        raise NotImplementedError()

    def to_bytes(self, padding_length=None) -> bytes:
        '''
        Get the message in binary representation with padding bytes.

        If the padding_length is not set or set to None, a random padding length will be chosen.
        '''
        return self.type_byte + self.get_data() + generate_padding(length=padding_length)


class TextMessage(Message):
    '''
    A text message can take up to 3500 bytes.
    '''
    type_byte = b'\x01'

    def __init__(self, content: str):
        self.content = content

    def get_data(self) -> bytes:
        data = self.content.encode('utf-8')
        if len(data) > 3500:
            raise ValueError("content may only be 3500 UTF-8 bytes long")
        return data


def _require_size(name, value, size):
    if len(value) != size:
        raise ValueError(f"{name} needs size of {size}")
    return value


class ImageMessage(Message):
    '''
    An image message contains the "blob identifier" to a image resource.
    '''
    type_byte = b'\x02'

    def __init__(self, blob_id: str, size: int, nonce: bytes):
        self.blob_id = blob_id
        self.size = size
        self.nonce = nonce

    def get_data(self) -> bytes:
        data = self.blob_id.encode(
            'ascii') + self.size.to_bytes(4, "big") + self.nonce
        if len(data) != 44:
            raise ValueError("Size of data is not 44 it's " + len(data))
        return data


class FileMessage(Message):
    '''
    A file message references an uploaded "blob" which can be an arbitrary
    file type.
    '''
    type_byte = b'\x17'

    def __init__(self, blob_id: bytes, size: int, key: bytes, mime_type: str,
                 filename: str = None, thumbnail_blob_id=None, description=None):
        self.blob_id = blob_id
        self.size = size
        self.key = _require_size("key", key, SYMMETRIC_KEY_LENGTH)
        self.mime_type = mime_type
        self.filename = filename
        self.thumbnail_blob_id = thumbnail_blob_id
        self.description = description

    def get_data(self) -> bytes:
        value = {
            'b': self.blob_id.hex(),
            'k': self.key.hex(),
            'm': self.mime_type,
            's': self.size,
            'i': 0
        }

        if self.description is not None:
            value['d'] = self.description

        if self.filename is not None:
            value['n'] = self.filename

        if self.thumbnail_blob_id is not None:
            value['t'] = self.thumbnail_blob_id.hex()
        result = json.dumps(value, separators=(',', ':')).encode('utf-8')
        print(result)
        return result
