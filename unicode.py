from unicodedata import *

NFC = 'NFC'
NFKC = 'NFKC'
NFD = 'NFD'
NFKD = 'NFKD'

a = normalize(NFC, '\u0995\u09BF') 
print(a)

print(name('\u0995'), name('\u09BF'))

print("done")