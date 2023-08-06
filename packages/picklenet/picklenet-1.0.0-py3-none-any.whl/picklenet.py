import io as _io
import tempfile

import clr as _clr
_clr.AddReference('System')
_clr.AddReference('System.Runtime')
_clr.AddReference('System.Runtime.Serialization')
_clr.AddReference('System.Runtime.Serialization.Formatters')
import System as _sysnet
import System.IO as _ionet
import System.Runtime.Serialization as _ser
import System.Runtime.Serialization.Formatters.Binary as _bin

IFormatter = _ser.IFormatter
BinaryFormatter = _bin.BinaryFormatter


def _get_class_from_protocol(protocol):
    if protocol == 'binary' or protocol == 'bin':
        return BinaryFormatter
    else:
        raise NotImplementedError('unsupported protocol %r' % protocol)


def get_formatter(protocol_or_class_or_formatter='binary'):
    if isinstance(protocol_or_class_or_formatter, str):
        return _get_class_from_protocol(protocol_or_class_or_formatter)()
    elif isinstance(protocol_or_class_or_formatter, type):
        return protocol_or_class_or_formatter()
    else:
        return protocol_or_class_or_formatter


def dump(obj, fp, formatter='binary') -> None:
    name = tempfile.mktemp()
    outfp = _ionet.FileStream(name, 2, 3)
    formatter = get_formatter(formatter)
    formatter.Serialize(outfp, obj)
    outfp.Flush()
    fp.write(open(name, 'rb').read())


def dumps(obj, formatter='binary') -> bytes:
    stream = _io.BytesIO()
    dump(obj, stream, formatter)
    return stream.getvalue()


def load(fp, formatter='binary'):
    name = tempfile.mktemp()
    open(name, 'wb').write(fp.read())
    fp = _ionet.FileStream(name, 3, 1)
    formatter = get_formatter(formatter)
    return formatter.Deserialize(fp)


def loads(data, formatter='binary'):
    stream = _io.BytesIO(data)
    return load(stream, formatter)
