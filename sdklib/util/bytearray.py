import time


def timestamp_to_ticks(t=None):
    if t is None:
        t = time.time()
    return int(t * (10**7)) + 621355968000000000


def dotnet_datetime_to_binary(ticks, kind):
    return ticks | ( kind << 62 )


def xor_string(string1, string2):
    return [ord(a) ^ ord(b) for a,b in zip(string1, string2)]


def string_to_bytearray(string):
    byte_array = [ord(a) for a in string]
    to_return = []
    for elem in byte_array:
        to_return.append(elem)
        to_return.append(0)
    return to_return


def long_to_bytearray(long):
    to_return = []
    for i in range(0,8):
        to_return.append(int((long >> i*8) & 255))
    return to_return


def xor_bytearray(byteArray1, byteArray2):
    return [a ^ b for a,b in zip(byteArray1, byteArray2)]


def bytearray_to_string(byteArray):
    chr_list = [chr(a) for a in byteArray]
    return ''.join(chr_list)
