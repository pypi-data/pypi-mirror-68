__doc__='''
A unicodeconvert for demo.
USAGE:
\'\'\'do you want to print idle a smily face(emoji)?maybe u tried this:
print(\'\\U0001F600\')
but you got this:
Traceback (most recent call last):
  File "<pyshell#29>", line 1, in <module>
    print(\'\\U0001F600\')
UnicodeEncodeError: 'UCS-2' codec can't encode character \'\\U0001f600\' in position 0: Non-BMP character not supported in Tk
>>>
\'\'\'
#try this:
nonBMPtoBMP('\U0001F600')
ok,have fun!
'''
class UnicodeConvertError(BaseException):
    pass
def nonBMPtoBMP_e(up):
    u=ord(up)
    vc = u - 0x10000
    vh = (vc & 0xFFC00) >>10
    vl = vc & 0x3FF
    w1 = 0xD800
    w2 = 0xDC00
    w1 = w1|vh
    w2 = w2|vl
    return chr(w1)+chr(w2)
import unicodedata
def UnicodetoASCII(s):
    return unicodedata.normalize('NFKD',s).encode('ascii','ignore')
def ASCIItoUnicode(s):
    return chr(ord(s))
def nonBMPtoBMP(up):
    u=ord(up)
    if u<=0xFFFF:
        raise UnicodeConvertError('The arg shouldn\'t be lesser than 0x10000.')
    else:
        return nonBMPtoBMP_e(up)

def toUTF16(u):
    if u<=0xFFFF:
        return u
    else:
        return nonBMPtoBMP_e(u)

