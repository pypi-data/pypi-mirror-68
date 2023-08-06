from .messages import Message, TextMessage, FileMessage
from .crypto import PublicKey, SecretKey, box_encrypt, encrypt_file, encrypt_thumbnail
from .utils import hash_email, hash_phone
import requests
import urllib.parse
from collections import namedtuple
from typing import Text, Union, Optional
import mimetypes
import os

__version__ = '0.3'


class ApiException(Exception):
    pass


class NotFoundException(ApiException):
    pass


class IdentityNotFound(NotFoundException):
    def __init__(self, identity):
        super().__init__(f"Identity '{identity}' was not found")
        self.identity = identity


def _url_join(base_url, *parts):
    return base_url + '/'.join(map(urllib.parse.quote, parts))


def _check_identity(identity):
    if len(identity) != 8:
        raise ValueError("identity must be 8 characters long")


RemoteBlob = namedtuple("RemoteBlob", ["id", "key"])


class Contact:
    '''
    A contact represents a fully resolved recipient.

    This includes a identity and the public key.
    '''

    def __init__(self, identity: str, public_key: PublicKey):
        _check_identity(identity)
        self.identity = identity
        self.public_key = public_key

    def __str__(self) -> str:
        encoded_pk = self.public_key.hex_pk().decode('ascii')
        return f"Contact(identity={self.identity}, public_key={encoded_pk})"


class Threema:
    '''
    The Threema Gateway API client. 

    This is the main entry point to communicate to the gateway API.
    '''

    key: SecretKey

    # exact version should is not included
    user_agent = "python-thr/0"

    def __init__(self, identity: str, secret, key, base_url="https://msgapi.threema.ch/"):
        if not isinstance(key, SecretKey):
            if len(key) == 32:
                key = SecretKey(key)
            elif len(key) == 64:
                key = SecretKey(bytes.fromhex(key))
            else:
                raise ValueError("Invalid key length. Expected 64 for hex")

        _check_identity(identity)
        self.identity = identity
        self.secret = secret
        self.key = key
        self.base_url = base_url

    @classmethod
    def from_environment(cls) -> 'Threema':
        secret = os.environ.get("THREEMA_SECRET")
        if secret is None:
            raise ValueError("THREEMA_SECRET is not set")

        identity = os.environ.get("THREEMA_IDENTITY")
        if identity is None:
            raise ValueError("THREEMA_IDENTITY is not set")

        key = os.environ.get("THREEMA_KEY")
        if key is None:
            raise ValueError("THREEMA_KEY is not set")

        return cls(identity=identity, secret=secret, key=key)

    def _query(self, method, *url_parts, **kwargs):
        headers = {
            "User-Agent": self.user_agent,
        }
        url = _url_join(self.base_url, *url_parts)
        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code == 404:
            raise NotFoundException("Ressource not found")
        response.raise_for_status()
        return response

    def _query_text(self, method, *url_parts, **kwargs):
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/plain",
        }
        url = _url_join(self.base_url, *url_parts)
        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code == 404:
            raise NotFoundException("Ressource not found")
        response.raise_for_status()
        return response.text

    def lookup_identity_by_email(self, email) -> str:
        identity = self._query_text("GET", "lookup", "email_hash", hash_email(email), params={
            'from': self.identity,
            'secret': self.secret
        })
        _check_identity(identity)
        return identity

    def lookup_identity_by_phone(self, phone) -> str:
        '''
        Retrieves the identity based pon the phone number.

        The phone number will be hashed prior to querrying the API.
        '''
        identity = self._query_text("GET", "lookup", "phone_hash", hash_phone(phone), params={
            'from': self.identity,
            'secret': self.secret
        })
        _check_identity(identity)
        return identity

    def lookup_pubkey(self, identity: str) -> PublicKey:
        '''
        Queries the API for the public key of the specified identity.

        Raises IdentityNotFound if the identity doesn't exist.
        '''
        _check_identity(identity)
        try:
            hex_pubkey = self._query_text("GET", 'pubkeys', identity, params={
                'from': self.identity,
                'secret': self.secret
            })
        except NotFoundException:
            raise IdentityNotFound(identity)
        return PublicKey(bytes.fromhex(hex_pubkey))

    def get_credits(self) -> int:
        credits = self._query_text("GET", "credits", params={
            'from': self.identity,
            'secret': self.secret
        })
        return int(credits)

    def lookup(self, identity: str) -> Contact:
        public_key = self.lookup_pubkey(identity)
        return Contact(identity=identity, public_key=public_key)

    def upload_raw_blob(self, data: bytes) -> bytes:
        '''
        Uploads a blob and returns the blob ID in binary form.
        '''
        hex_blob_id = self._query_text("POST", 'upload_blob', params={
            'from': self.identity,
            'secret': self.secret
        }, files={'blob': ('blob', data, 'application/octet-stream')})
        return bytes.fromhex(hex_blob_id)

    def upload_blob(self, data: bytes, key=None) -> RemoteBlob:
        '''
        Encrypt and upload binary data. If the key is None, a random key will be generated
        '''
        encrypted = encrypt_file(content=data, key=key)
        identifier = self.upload_raw_blob(encrypted.data)
        return RemoteBlob(id=identifier, key=encrypted.key)

    def send_message(self, message: Message, recipient: Contact):
        '''
        Send an end-to-end encrypted message
        '''
        encrypted = box_encrypt(
            content=message.to_bytes(),
            secret_key=self.key,
            public_key=recipient.public_key)

        response = self._query("POST", "send_e2e", data={
            'nonce': encrypted.nonce.hex(),
            'box': encrypted.data.hex(),
            'secret': self.secret,
            'from': self.identity,
            'to': recipient.identity
        }, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        return response.text

    def send_text_message(self, recipient: str, content: str):
        message = TextMessage(content)
        return self.send_message(
            message=message,
            recipient=recipient)

    def upload_file(self, filename: Optional[Text] = None, 
                    content: Optional[bytes] = None, 
                    mimetype=None, key=None) -> FileMessage:
        '''
        Upload a file and prepare a file message for it.

        This function will pre-fill the following fields:
         * size
         * mime_type
         * blob_id
         * key
         * filename
        '''
        if filename is not None:
            with open(filename, 'rb') as infile:
                content = infile.read()

            filename = os.path.basename(filename)
        elif content is None:
            raise ValueError("Either content or filename has to be provided")

        if mimetype is None and filename is not None:
            mimetype, _ = mimetypes.guess_type(filename) or 'application/octet-stream'

        blob = self.upload_blob(data=content, key=key)

        return FileMessage(blob_id=blob.id, key=blob.key, mime_type=mimetype, 
                           size=len(content), filename=filename)

    def upload_thumbnail(self, content: bytes, key) -> bytes:
        '''
        Uploads a thumbnail, encrypted with the specified key.

        The key must be the same as the one used to encrytp the file
        for the thumbnail to work.

        Returns the blob ID of the thumbnail.
        '''
        encrypted = encrypt_thumbnail(content=content, key=key)
        return self.upload_raw_blob(encrypted.data)
