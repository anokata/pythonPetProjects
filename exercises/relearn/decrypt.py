from simplecrypt import decrypt

with open("passwords.txt") as fin:
    passwords = fin.read().splitlines()

with open("encrypted.bin", "rb") as inp:
    encrypted = inp.read()

print('readed' + str(passwords))
for pwd in passwords:
    print('decrypt with ' + pwd)
    try:
        text = decrypt(pwd, encrypted)
        print('decrypted ok:')
        print(text)
    except:
        print('can\'t ')
