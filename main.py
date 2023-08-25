import cv2

charList = [chr(i) for i in range(32, 125)]

def getIndex(char):
    return charList.index(char)

def removeSpace(text):
    return text.replace(" ", "")

def addSpace(text1, text2):
    text1 = list(text1)
    for i, char in enumerate(text2):
        if char == " ":
            text1.insert(i, " ")
    return "".join(text1)

def encrypt(raw, key):
    txt = removeSpace(raw)
    result = ""
    key += txt
    for i, char in enumerate(txt):
        if char not in charList or key[i] not in charList:
            tempchar = char
        else:
            tempchar = charList[(getIndex(char) + getIndex(key[i])) % 93]
        result += tempchar
    result = addSpace(result, raw)
    return result

def decrypt(raw, key):
    txt = removeSpace(raw)
    keylen = len(key)
    result = ""
    for i, char in enumerate(txt[:keylen]):
        if char not in charList or key[i] not in charList:
            tempchar = char
        else:
            if getIndex(char) < getIndex(key[i]):
                tempchar = charList[93 + getIndex(char) - getIndex(key[i])]
            else:
                tempchar = charList[getIndex(char) - getIndex(key[i])]
        result += tempchar
    key = result
    for i, char in enumerate(txt[keylen:]):
        if char not in charList or key[i] not in charList:
            tempchar = char
        else:
            if getIndex(char) < getIndex(key[i]):
                tempchar = charList[93 + getIndex(char) - getIndex(key[i])]
            else:
                tempchar = charList[getIndex(char) - getIndex(key[i])]
        key += tempchar
        result += tempchar
    result = addSpace(result, raw)
    return result

def add_filler(bits,dim):
    for i in range((dim-(len(bits))*8)//8):
        bits.insert(0,'00000000')
    bits[0] == '00000000'
    return bits

def convert_to_bits(text,filler = False, dim = 0):
    bits = []
    for i in text:
        bits.append(format(ord(i),'08b'))
    if filler:
        bits = add_filler(bits,dim)
    return bits

def hide(im, text, keyword):
    dim = im.shape
    text = encrypt(text,keyword)
    len_bits = convert_to_bits(str(len(text)),filler=True, dim=dim[1]*3)
    text = len_bits + convert_to_bits(text)
    text_length = len(text)*8
    # print(dim)#1536 2048 3
    row_factor = dim[1] * dim[2]
    # Embedding the length of text in m = 0
    for i in range(text_length):
        m = i//row_factor
        n = i//3 - (dim[1]*m)
        o = i % 3
        if text[i//8][i%8] == '0' and im[m][n][o] % 2 != 0:
            if im[m][n][o] == 255:
                im[m][n][o] -= 1
            else:
                im[m][n][o] += 1
        elif text[i//8][i%8] == '1' and im[m][n][o] % 2 == 0:
            im[m][n][o] += 1
    return im

# Extraction 
def check_bit(bit):
    if bit % 2 == 0:
        return '0'
    return '1'

def get(im, keyword):
    dim = im.shape
    len_bits = ''
    for i in range(dim[1]):
        for j in im[0][i]:
            len_bits += check_bit(j)
    bit_len = []
    while('1' in len_bits):
        bit_len.insert(0,len_bits[-8:])
        len_bits = len_bits[:-8]
    plaintext_len = ''
    for i in bit_len:
        plaintext_len += chr(int(i,2))
    plaintext_len = int(plaintext_len)

    row_factor = dim[1] * dim [2]

    plaintext_bits = ''
    for i in range(plaintext_len*8):
        m = i // row_factor
        n = i // 3 - (dim[1] * m)
        o = i%3
        m += 1
        plaintext_bits += check_bit(im[m][n][o])
    bit_plaintext = []
    for i in range(plaintext_len):
        bit_plaintext.insert(0,plaintext_bits[-8:])
        plaintext_bits = plaintext_bits[:-8]

    plaintext = ''
    for i in bit_plaintext:
        plaintext += chr(int(i,2))
    plaintext = decrypt(plaintext,keyword)
    return plaintext