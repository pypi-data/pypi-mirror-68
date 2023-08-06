#encoding=utf-8
from __future__ import unicode_literals, print_function

# use "".format() insted ""%()
# use six.text_type insted basestring
import types
import cchardet, traceback

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

from codecs import open
import six



def encode_get(s, to_lower=False):
    if not isinstance(s, six.string_types):
        return None

    if not s:
        return "unicode"
    if isinstance(s, six.text_type):
        return "unicode"
    else:
        codeType = cchardet.detect(s).get('encoding', None)
        if to_lower and isinstance(codeType, basestring):
            codeType = codeType.lower()
        return codeType  # s==''时，会return None

def encode_toCn(s):
    if (not isinstance(s, six.string_types)): return s
    if (encode_get(s) in ['unicode', 'utf-8']):
        ret = s.encode('GBK')
        return ret
    else:
        try:
            ret = s.decode('GBK').encode('GBK')
        except Exception as eObj:
            # print(six.binary_type(eObj))
            raise Exception("encode_toCn: {%s}.decode('GBK').encode('GBK'), error={%s}" % (s, eObj))
        return ret


def encode_to(s, typeNew='utf-8', __Encoding__=''):
    if not isinstance(s, six.string_types):
        return s
    typeNew = __Encoding__ or typeNew
    typeOld = encode_get(s)
    if not typeOld or typeOld==typeNew:
        return s

    if typeOld != 'unicode':
        s = encode_toU(s)

    try:
        ret = s.encode(typeNew)
    except Exception as eObj:
        errDetail = traceback.format_exc()
        raise Exception("encode_toU: {%s}.decode(%s), error={%s}" % (s, typeNew, eObj))
    return ret

def encode_toU(s, notForce=True):
    codeType = ''
    try:
        if not isinstance(s, six.string_types):
            if notForce or isinstance(s, (int, long, float)):
                return s
            s_bak = s
            try:
                s = six.binary_type(s)
            except Exception as errObj:
                s = six.text_type(s)
        codeType = encode_get(s)
        if not codeType:
            return codeType  # return ''
        if codeType in ['unicode']:
            return s

        ret = s.decode(codeType)
        return ret
    except Exception as eObj:
        errDetail = traceback.format_exc()
        raise Exception(b"encode_toU: {%s}.decode(%s), error={%s}" % (s, codeType, eObj))


def str_fmt(fmt=None, *args, **kwargs):
    try:
        if not args and not kwargs:
            ret = '{}'.format(encode_toU(fmt, notForce=False))
        elif args:
            ret = fmt.format(*[encode_toU(i, notForce=False) for i in args])
        else:
            kwargsNew = {}
            # e.g.  "{x}, {self.XXX}".format(self=self, x=self)  => dict(x=encode_toU(x), self=self)
            for k, v in kwargs.items():
                if fmt.find('{%s}' % (k, )) != -1:
                    kwargsNew[k] = encode_toU(v, notForce=False)
                else:
                    kwargsNew[k] = v
            ret = fmt.format(**kwargsNew)
        return ret
    except Exception as errObj:
        raise errObj

def str_fmtB(fmt=None, *args, **kwargs):
    __Encoding__ = 'utf-8'
    if kwargs.has_key('__Encoding__'):
        __Encoding__ = kwargs.pop('__Encoding__')
    strFmt = str_fmt(fmt, *args, **kwargs)
    return encode_to(strFmt, __Encoding__=__Encoding__)

def printB(fmt=None, *args, **kwargs):
    if not isinstance(fmt, six.string_types):
        msg = fmt
    else:
        strFmtB = str_fmtB(fmt, *args, **kwargs)
        msg = (strFmtB)

    try:
        print(msg)
    except BaseException as errObj:
        pass # TODO: skip error("IOError: [Errno 22] Invalid argument") at ansitowin32.py: