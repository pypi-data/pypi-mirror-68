from multipart.multipart import parse_options_header
from urllib.parse import parse_qsl
from enum import Enum
import inspect
import multipart
import typing

from yaat.components import Form, Headers, UploadFile
from yaat.constants import ENCODING_METHOD


class FormParser:
    def __init__(self, body: bytes):
        self.body = body

    async def parse(self) -> Form:
        body_data = await self.body()
        body_data = body_data.decode(ENCODING_METHOD)
        form_data = [] if body_data == "" else parse_qsl(body_data)
        form_data = [(item[0], item[1]) for item in form_data]
        return Form(form_data)


class MultiPartParser:
    class MultiPartMessage(Enum):
        PART_BEGIN = 1
        PART_DATA = 2
        PART_END = 3
        HEADER_FIELD = 4
        HEADER_VALUE = 5
        HEADER_END = 6
        HEADERS_FINISHED = 7
        END = 8

    def __init__(
        self, headers: Headers, stream: typing.AsyncGenerator[bytes, None]
    ):
        self.headers = headers
        self.stream = stream
        self.messages = []

    def __user_safe_decode(self, src: bytes, codec: str) -> str:
        try:
            return src.decode(codec)
        except (UnicodeDecodeError, LookupError):
            return src.decode(ENCODING_METHOD)

    async def parse(self) -> Form:
        events = self.MultiPartMessage

        # Parse the Content-Type header to get the multipart boundary.
        content_type, params = parse_options_header(
            self.headers.get("content-type")
        )
        charset = params.get(b"charset", "utf-8")
        if type(charset) == bytes:
            charset = charset.decode(ENCODING_METHOD)
        boundary = params.get(b"boundary")

        # Callbacks dictionary.
        callbacks = {
            "on_part_begin": lambda: self.messages.append(
                (events.PART_BEGIN, b"")
            ),
            "on_part_data": lambda data, start, end: self.messages.append(
                (events.PART_DATA, data[start:end])
            ),
            "on_part_end": lambda: self.messages.append(
                (events.PART_END, b"")
            ),
            "on_header_field": lambda data, start, end: self.messages.append(
                (events.HEADER_FIELD, data[start:end])
            ),
            "on_header_value": lambda data, start, end: self.messages.append(
                (events.HEADER_VALUE, data[start:end])
            ),
            "on_header_end": lambda: self.messages.append(
                (events.HEADER_END, b"")
            ),
            "on_headers_finished": lambda: self.messages.append(
                (events.HEADERS_FINISHED, b"")
            ),
            "on_end": lambda: self.messages.append((events.END, b"")),
        }

        # Create the parser.
        parser = multipart.MultipartParser(boundary, callbacks)
        header_field = b""
        header_value = b""
        content_disposition = None
        content_type = b""
        field_name = ""
        data = b""
        file = None

        items = (
            # typing.List[typing.Tuple[str, typing.Union[str, UploadFile]]]
            []
        )

        # Data from the request
        async for chunk in self.stream:
            parser.write(chunk)
            messages = list(self.messages)
            self.messages.clear()

            for message_type, message_bytes in messages:
                if message_type == events.PART_BEGIN:
                    content_disposition = None
                    content_type = b""
                    data = b""

                elif message_type == events.HEADER_FIELD:
                    header_field += message_bytes

                elif message_type == events.HEADER_VALUE:
                    header_value += message_bytes

                elif message_type == events.HEADER_END:
                    field = header_field.lower()

                    if field == b"content-disposition":
                        content_disposition = header_value
                    elif field == b"content-type":
                        content_type = header_value

                    header_field = b""
                    header_value = b""

                elif message_type == events.HEADERS_FINISHED:
                    disposition, options = parse_options_header(
                        content_disposition
                    )
                    field_name = self.__user_safe_decode(
                        options[b"name"], charset
                    )

                    if b"filename" in options:
                        filename = self.__user_safe_decode(
                            options[b"filename"], charset
                        )
                        file = UploadFile(
                            name=filename,
                            content_type=content_type.decode(ENCODING_METHOD),
                        )
                    else:
                        file = None

                elif message_type == events.PART_DATA:
                    if file is None:
                        data += message_bytes
                    else:
                        await file.write(message_bytes)

                elif message_type == events.PART_END:
                    if file is None:
                        items.append(
                            (
                                field_name,
                                self.__user_safe_decode(data, charset),
                            )
                        )
                    else:
                        await file.seek(0)
                        items.append((field_name, file))

                elif message_type == events.END:
                    pass

        parser.finalize()
        return Form(items)


class UrlParamParser:
    """
    To convert URL parameter datatypes to what annotation defines
    """

    def __init__(
        self,
        handler: typing.Callable,
        kwargs: typing.Dict[str, str],
        is_class: bool,
    ):
        specs = inspect.getfullargspec(handler)
        # if class, ignore first 2 params (self, request) else 1 (request)
        args_index = 2 if is_class else 1

        self.convertors = {
            "int": self.to_interger,
            "float": self.to_float,
            "str": self.to_string,
        }
        self.args = specs.args[args_index:]
        self.annotations = specs.annotations
        self.kwargs = kwargs

        self.parse()

    def get(self) -> typing.Dict[str, typing.Any]:
        return self.kwargs

    def parse(self):
        kwargs = self.kwargs

        # convert to the datatype annoation defined
        for param, dtype in self.annotations.items():
            if param in kwargs.keys():
                value = kwargs[param]
                convertor = self.convertors.get(dtype.__name__, self.to_string)
                kwargs[param] = convertor(value)

        self.kwargs = kwargs

    def to_interger(self, value: str) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return value

    def to_float(self, value: str) -> int:
        try:
            return float(value)
        except (TypeError, ValueError):
            return value

    def to_string(self, value: typing.Any) -> str:
        return str(value)
