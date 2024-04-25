import argparse

parser = argparse.ArgumentParser(description="Lorem ipsum")
parser.add_argument('-w', '--word')
parser.add_argument('-o', '--offset', type=int)
args = parser.parse_args()

def decode_Caesar_cipher(s, n):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',.?!"
    s = s.strip()
    text = ''
    for c in s:
        text += alpha[(alpha.index(c) - n) % len(alpha)]
    print(text)

# Write your parser here
decode_Caesar_cipher(args.word, args.offset)