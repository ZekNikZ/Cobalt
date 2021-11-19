CODE_PAGE = {
    0x20: ' '
}

ENCODING = dict((v,k) for k,v in CODE_PAGE.items())
DECODING = CODE_PAGE

CCPX_EXT = '.ccp'
TEXT_EXT = '.cobalt'
TEXT_ENCODING = 'utf-8'

def encode(file : str, output : str=None):
    # TODO: check for existing file
    if output is None:
        output = file.rsplit('.', maxsplit=1)[0] + CCPX_EXT

    data = []
    with open(file, 'rt', encoding=TEXT_ENCODING) as input_file, open(output, 'wb') as output_file:
        for c in input_file.read():
            if c in ENCODING:
                data.append(ENCODING[c])
            else:
                # TODO: error
                print('error')
                pass

        print(data)

        output_file.write(bytes(data))

def decode(file, output=None):
    # TODO: check for existing file
    if output is None:
        output = file.rsplit('.', maxsplit=1)[0] + TEXT_EXT

    data = []
    with open(file, 'rb') as input_file, open(output, 'w+', encoding=TEXT_ENCODING) as output_file:
        for b in input_file.read():
            if b in DECODING:
                data.append(DECODING[b])
            else:
                # TODO: error
                print('error')
                pass

        output_file.write(''.join(data))