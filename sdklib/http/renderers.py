import json
try:
    from exceptions import BaseException
except:
    pass
from urllib3.filepost import encode_multipart_formdata
from urllib3.fields import RequestField, guess_content_type

from sdklib.util.files import guess_filename_stream
from sdklib.util.structures import to_key_val_list, to_key_val_dict
from sdklib.compat import urlencode, quote_plus, basestring, str


java_strings = {"true": "true", "false": "false", "null": "null"}
python_strings = {"true": "True", "false": "False", "null": "None"}
csharp_strings = {"true": "True", "false": "False", "null": "Null"}


def to_string(value, lang='javascript'):
    if lang in ['javascript', 'java', 'php']:
        return get_primitive_as_string(java_strings, value)
    elif lang in ['python']:
        return get_primitive_as_string(python_strings, value)
    elif lang in ['csharp', 'dotnet']:
        return get_primitive_as_string(csharp_strings, value)
    else:
        return get_primitive_as_string(python_strings, value)


def get_primitive_as_string(strings_dict, value):
    if isinstance(value, bool) and value:
        return strings_dict["true"]
    elif isinstance(value, bool):
        return strings_dict["false"]
    elif value is None:
        return strings_dict["null"]
    else:
        return str(value)


class BaseRenderer(object):

    DEFAULT_CONTENT_TYPE = ""

    def encode_params(self, data=None, **kwargs):
        """
        Build the body for a request.
        """
        raise BaseException("Not implemented yet")


def guess_file_name_stream_type_header(args):
    """
    Guess filename, file stream, file type, file header from args.

    :param args: may be string (filepath), 2-tuples (filename, fileobj), 3-tuples (filename, fileobj,
    contentype) or 4-tuples (filename, fileobj, contentype, custom_headers).
    :return: filename, file stream, file type, file header
    """
    ftype = None
    fheader = None
    if isinstance(args, (tuple, list)):
        if len(args) == 2:
            fname, fstream = args
        elif len(args) == 3:
            fname, fstream, ftype = args
        else:
            fname, fstream, ftype, fheader = args
    else:
        fname, fstream = guess_filename_stream(args)
        ftype = guess_content_type(fname)

    if isinstance(fstream, (str, bytes, bytearray)):
        fdata = fstream
    else:
        fdata = fstream.read()
    return fname, fdata, ftype, fheader


class MultiPartRenderer(BaseRenderer):

    def __init__(self, boundary="----------ThIs_Is_tHe_bouNdaRY", output_str='javascript'):
        self.boundary = boundary
        self.output_str = output_str

    def encode_params(self, data=None, files=None, **kwargs):
        """
        Build the body for a multipart/form-data request.
        Will successfully encode files when passed as a dict or a list of
        tuples. Order is retained if data is a list of tuples but arbitrary
        if parameters are supplied as a dict.
        The tuples may be string (filepath), 2-tuples (filename, fileobj), 3-tuples (filename, fileobj, contentype)
        or 4-tuples (filename, fileobj, contentype, custom_headers).
        """
        if isinstance(data, basestring):
            raise ValueError("Data must not be a string.")

        # optional args
        boundary = kwargs.get("boundary", None)
        output_str = kwargs.get("output_str", self.output_str)

        new_fields = []
        fields = to_key_val_list(data or {})
        files = to_key_val_list(files or {})

        for field, value in fields:
            ctype = None
            if isinstance(value, (tuple, list)) and len(value) == 2:
                val, ctype = value
            else:
                val = value

            if isinstance(val, basestring) or not hasattr(val, '__iter__'):
                val = [val]
            for v in val:
                # Don't call str() on bytestrings: in Py3 it all goes wrong.
                if not isinstance(v, bytes):
                    v = to_string(v, lang=output_str)

                field = field.decode('utf-8') if isinstance(field, bytes) else field
                v = v.encode('utf-8') if isinstance(v, str) else v

                rf = RequestField(name=field, data=v)
                rf.make_multipart(content_type=ctype)
                new_fields.append(rf)

        for (k, v) in files:
            fn, fdata, ft, fh = guess_file_name_stream_type_header(v)
            rf = RequestField(name=k, data=fdata, filename=fn, headers=fh)
            rf.make_multipart(content_type=ft)
            new_fields.append(rf)

        if boundary is None:
            boundary = self.boundary
        body, content_type = encode_multipart_formdata(new_fields, boundary=boundary)

        return body, content_type


class FormRenderer(BaseRenderer):

    VALID_COLLECTION_FORMATS = ['multi', 'csv', 'ssv', 'tsv', 'pipes', 'encoded']
    COLLECTION_SEPARATORS = {"csv": ",", "ssv": " ", "tsv": "\t", "pipes": "|"}
    DEFAULT_CONTENT_TYPE = "application/x-www-form-urlencoded"

    def __init__(self, collection_format='multi', output_str='javascript', sort=False):
        self.content_type = self.DEFAULT_CONTENT_TYPE
        self.collection_format = collection_format
        self.output_str = output_str
        self.sort = sort

    @property
    def collection_format(self):
        return self._collection_format

    @collection_format.setter
    def collection_format(self, value):
        assert value in self.VALID_COLLECTION_FORMATS
        self._collection_format = value

    def encode_params(self, data=None, **kwargs):
        """
        Encode parameters in a piece of data.
        Will successfully encode parameters when passed as a dict or a list of
        2-tuples. Order is retained if data is a list of 2-tuples but arbitrary
        if parameters are supplied as a dict.
        """
        collection_format = kwargs.get("collection_format", self.collection_format)
        output_str = kwargs.get("output_str", self.output_str)
        sort = kwargs.get("sort", self.sort)

        if data is None:
            return "", self.content_type
        elif isinstance(data, (str, bytes)):
            return data, self.content_type
        elif hasattr(data, 'read'):
            return data, self.content_type
        elif collection_format == 'multi' and hasattr(data, '__iter__'):
            result = []
            for k, vs in to_key_val_list(data, sort=sort):
                if isinstance(vs, basestring) or not hasattr(vs, '__iter__'):
                    vs = [vs]
                for v in vs:
                    result.append(
                        (k.encode('utf-8') if isinstance(k, str) else k,
                         v.encode('utf-8') if isinstance(v, str) else to_string(v, lang=output_str)))
            return urlencode(result, doseq=True), self.content_type
        elif collection_format == 'encoded' and hasattr(data, '__iter__'):
            return urlencode(data, doseq=False), self.content_type
        elif hasattr(data, '__iter__'):
            results = []
            for k, vs in to_key_val_dict(data).items():
                if isinstance(vs, list):
                    v = self.COLLECTION_SEPARATORS[collection_format].join(quote_plus(e) for e in vs)
                    key = k + '[]'
                else:
                    v = quote_plus(vs)
                    key = k
                results.append("%s=%s" % (key, v))

            return '&'.join(results), self.content_type
        else:
            return data, self.content_type


class PlainTextRenderer(BaseRenderer):
    VALID_COLLECTION_FORMATS = ['multi', 'csv', 'ssv', 'tsv', 'pipes', 'plain']
    COLLECTION_SEPARATORS = {"csv": ",", "ssv": " ", "tsv": "\t", "pipes": "|"}

    def __init__(self, charset='utf-8', collection_format='multi', output_str='javascript'):
        self.charset = charset
        self.collection_format = collection_format
        self.output_str = output_str

    @property
    def collection_format(self):
        return self._collection_format

    @collection_format.setter
    def collection_format(self, value):
        assert value in self.VALID_COLLECTION_FORMATS

        self._collection_format = value

    def get_content_type(self, charset=None):
        if charset is None:
            charset = self.charset
        if charset:
            return "text/plain; charset=%s" % self.charset
        return 'text/plain'

    @staticmethod
    def _encode(data, charset=None, output_str='javascript'):
        return to_string(data, lang=output_str).encode(charset) if charset else to_string(data, lang=output_str).encode()

    def encode_params(self, data=None, **kwargs):
        """
        Build the body for a text/plain request.
        Will successfully encode parameters when passed as a dict or a list of
        2-tuples. Order is retained if data is a list of 2-tuples but arbitrary
        if parameters are supplied as a dict.
        """
        charset = kwargs.get("charset", self.charset)
        collection_format = kwargs.get("collection_format", self.collection_format)
        output_str = kwargs.get("output_str", self.output_str)

        if data is None:
            return "", self.get_content_type(charset)
        elif isinstance(data, (str, bytes)):
            return data, self.get_content_type(charset)
        elif hasattr(data, 'read'):
            return data, self.get_content_type(charset)
        elif collection_format == 'multi' and hasattr(data, '__iter__'):
            result = []
            for k, vs in to_key_val_list(data):
                if isinstance(vs, basestring) or not hasattr(vs, '__iter__'):
                    vs = [vs]
                for v in vs:
                    result.append(b"=".join([self._encode(k, charset), self._encode(v, charset, output_str)]))
            return b'\n'.join(result), self.get_content_type(charset)
        elif collection_format == 'plain' and hasattr(data, '__iter__'):
            results = []
            for k, vs in to_key_val_dict(data).items():
                results.append(b"=".join([self._encode(k, charset), self._encode(vs, charset, output_str)]))

            return b'\n'.join(results), self.get_content_type(charset)
        elif hasattr(data, '__iter__'):
            results = []
            for k, vs in to_key_val_dict(data).items():
                if isinstance(vs, list):
                    v = self.COLLECTION_SEPARATORS[collection_format].join(e for e in vs)
                    key = k + '[]'
                else:
                    v = vs
                    key = k
                results.append(b"=".join([self._encode(key, charset), self._encode(v, charset, output_str)]))

            return b"\n".join(results), self.get_content_type(charset)
        else:
            return str(data).encode(charset) if charset else str(data), self.get_content_type(charset)


class JSONRenderer(BaseRenderer):

    DEFAULT_CONTENT_TYPE = "application/json"

    def __init__(self):
        self.content_type = self.DEFAULT_CONTENT_TYPE

    def encode_params(self, data=None, **kwargs):
        """
        Build the body for a application/json request.
        """
        if isinstance(data, basestring):
            raise ValueError("Data must not be a string.")
        if data is None:
            return b"", self.content_type

        try:
            fields = to_key_val_dict(data)
        except:
            fields = data

        try:
            body = json.dumps(fields)
        except:
            body = json.dumps(fields, encoding='latin-1')

        return str(body).encode(), self.content_type


class XMLRenderer(BaseRenderer):

    DEFAULT_CONTENT_TYPE = "application/xml"

    def __init__(self):
        self.content_type = self.DEFAULT_CONTENT_TYPE

    def encode_params(self, data=None, **kwargs):
        """
        Build the body for a application/xml request.
        """
        raise BaseException("Not implemented yet")


class CustomRenderer(BaseRenderer):

    def __init__(self, content_type):
        self.content_type = content_type

    def encode_params(self, data=None, **kwargs):
        """
        Build the body for a custom request.
        """
        return data, self.content_type


default_renderer = JSONRenderer()


def get_renderer(name=None, mime_type=None):
    if name == 'json' or mime_type == JSONRenderer.DEFAULT_CONTENT_TYPE:
        return JSONRenderer()
    elif name == 'form' or mime_type == FormRenderer.DEFAULT_CONTENT_TYPE:
        return FormRenderer()
    elif name == 'multipart' or mime_type == MultiPartRenderer.DEFAULT_CONTENT_TYPE:
        return MultiPartRenderer()
    elif name == 'plain' or mime_type == PlainTextRenderer.DEFAULT_CONTENT_TYPE:
        return PlainTextRenderer()
    else:
        return default_renderer


def url_encode(params, sort=False):
    r = get_renderer('form')
    return r.encode_params(params, sort=sort)[0]
