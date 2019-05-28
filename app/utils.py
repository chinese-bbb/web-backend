def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def fun(d):
    if 'KeyNo' in d:
        yield d['KeyNo']
    for k in d:
        if isinstance(d[k], list):
            for i in d[k]:
                for j in fun(i):
                    yield j

