from urllib.parse import parse_qsl, urlparse
import tempfile
import typing

from yaat.constants import ENCODING_METHOD
from yaat.concurrency import run_in_threadpool
from yaat.typing import Scope


class DictMapper(dict):
    def __cmp__(self, dict_: typing.Dict):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item: typing.Any) -> bool:
        return item in self.__dict__

    def __delitem__(self, key: str):
        del self.__dict__[key]

    def __getitem__(self, key: str):
        return self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __setitem__(self, key: str, item: typing.Any):
        self.__dict__[key] = item

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def get(self, key: str, default: typing.Any = None):
        return self.__dict__.get(key, default)

    def has_key(self, k: str):
        return k in self.__dict__

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def values(self):
        return self.__dict__.values()


class URL:
    def __init__(self, url: str = "", scope: Scope = None):
        if scope is not None:
            assert not url, 'Cannot set both "url" and "scope".'

            self.scheme = scope.get("scheme", "http")
            self.server = scope.get("server", None)
            self.path = scope.get("root_path", "") + scope["path"]
            self.query = scope.get("query_string", b"")
            self.host_header = scope["headers"]
        else:
            assert not scope, 'Cannot set both "url" and "scope".'

            components = urlparse(url)
            netloc = components.netloc.split(":")

            self.scheme = components.scheme
            self.server = (netloc[0], netloc[1] if len(netloc) > 1 else None)
            self.path = components.path
            self.query = components.query
            self.host_header = []
            self.fragment = components.fragment

        # init url
        self.__init_url()

    @property
    def scheme(self) -> str:
        return self.__scheme

    @scheme.setter
    def scheme(self, scheme: str):
        self.__scheme = scheme

    @property
    def server(self) -> typing.Tuple[str, int]:
        return self.__server

    @server.setter
    def server(self, server: typing.Tuple[str, int]):
        self.__server = server  # ip and port

    @property
    def netloc(self) -> str:
        if self.port:
            return f"{self.host}:{self.port}"
        else:
            return self.host

    @property
    def host(self) -> str:
        if not hasattr(self, "_host"):
            self.__host = None

            if self.server:
                host, port = self.server
                self._host = host
        return self._host

    @property
    def port(self) -> int:
        if not hasattr(self, "_port"):
            self._port = None

            if self.server:
                host, port = self.server
                self._port = int(port) if port else None
        return self._port

    @property
    def query(self) -> str:
        return self.__query

    @query.setter
    def query(self, query: bytes):
        try:
            self.__query = query.decode(ENCODING_METHOD)
        except (AttributeError, UnicodeDecodeError):
            self.__query = query

    @property
    def host_header(self) -> str:
        return self.__host_header

    @host_header.setter
    def host_header(self, headers: typing.Dict[str, str]):
        host_header = None
        for key, value in headers:
            if key == b"host":
                host_header = value.decode(ENCODING_METHOD)
                break
        self.__host_header = host_header

    @property
    def fragment(self) -> str:
        return self.__fragment

    @fragment.setter
    def fragment(self, fragment: str):
        self.__fragment = fragment

    @property
    def url(self) -> str:
        return self.__url

    def __init_url(self):
        if self.host_header is not None:
            url = f"{self.scheme}://{self.host_header}{self.path}"
        elif self.server is None:
            url = self.path
        else:
            host, port = self.server
            default_port = {"http": 80, "https": 443, "ws": 80, "wss": 443}[
                self.scheme
            ]
            if port == default_port:
                url = f"{self.scheme}://{host}{self.path}"
            else:
                url = f"{self.scheme}://{host}:{port}{self.path}"

        if self.query:
            url += "?" + self.query

        self.__url = url

    def is_secure(self) -> bool:
        return self.scheme in ("https", "wss")

    def __eq__(self, other: typing.Any) -> bool:
        return str(self) == str(other)

    def __str__(self) -> str:
        return self.__url


class Address:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, host: str):
        self.__host = str(host)

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, port: int):
        self.__port = int(port) if port else None

    def __str__(self) -> str:
        if self.host and self.port:
            return f"{self.host}:{self.port}"
        return self.host


class Headers(DictMapper):
    def __init__(self, raw_headers: typing.List[typing.Tuple[bytes, bytes]]):
        self.__dict__ = {
            key.decode(ENCODING_METHOD): value.decode(ENCODING_METHOD)
            for key, value in raw_headers
        }


class QueryParams(DictMapper):
    def __init__(self, raw_query: bytes):
        try:
            query_str = raw_query.decode(ENCODING_METHOD)
        except (AttributeError, UnicodeDecodeError):
            query_str = raw_query
        # parse the query string
        query_list = parse_qsl(query_str, keep_blank_values=True)

        for qs in query_list:
            key = qs[0]
            value = qs[1]

            if key not in self.__dict__:
                self.__dict__[key] = value
                continue

            # if key exists, store multiple values in list
            values = self.__dict__[key]
            # convert to list if not a list already
            if type(values) != list:
                values = [values]
            values.append(value)
            self.__dict__[key] = values

    def __str__(self) -> str:
        query_string = None

        for key, value in self.items():
            # if no value, just add back key
            if not value:
                query_string = (
                    f"{key}" if not query_string else f"{query_string}&{key}"
                )
            # if list, iterate and add back
            elif type(value) == list:
                for each in value:
                    query_string = (
                        f"{key}={each}"
                        if not query_string
                        else f"{query_string}&{key}={each}"
                    )
            # just add
            else:
                query_string = (
                    f"{key}={value}"
                    if not query_string
                    else f"{query_string}&{key}={value}"
                )

        return query_string


class Form(DictMapper):
    def __init__(self, form_data: typing.List[typing.Tuple[str, str]] = None):
        if not form_data:
            form_data = []

        for item in form_data:
            key = item[0]
            value = item[1]

            if key not in self.__dict__:
                self.__dict__[key] = value
                continue

            # if key exists, store multiple values in list
            values = self.__dict__[key]
            # convert to list if not a list already
            if type(values) != list:
                values = [values]
            values.append(value)
            self.__dict__[key] = values


class UploadFile:
    SPOOL_MAX_SIZE = 1024 * 1024

    def __init__(
        self, name: str, file: typing.IO = None, content_type: str = ""
    ):
        self.name = name
        self.content_type = content_type
        if file is None:
            file = tempfile.SpooledTemporaryFile(max_size=self.SPOOL_MAX_SIZE)
        self.file = file

    async def write(self, data: typing.Union[bytes, str]):
        await run_in_threadpool(self.file.write, data)

    async def read(self, size: int = None) -> typing.Union[bytes, str]:
        return await run_in_threadpool(self.file.read, size)

    async def seek(self, offset: int):
        await run_in_threadpool(self.file.seek, offset)

    async def close(self):
        await run_in_threadpool(self.file.close)
