def dnk(string):
    result = '';
    lastSame = string[0]
    sameCount = 1
    for i in range(1, len(string)):
        if lastSame == string[i]:
            sameCount += 1
        else:
            result += lastSame + str(sameCount)
            sameCount = 1
            lastSame = string[i]
    result += lastSame + str(sameCount)


    return result

print(dnk("aaabbdDcccz"))

def unpackDnk(string):
    result = '';
    count = '';
    lastChar = '';
    for char in string:
        if char.isalpha():
            if count != '':
                result += lastChar * int(count)
            lastChar = char
            count = ''
        else:
            count += char
    result += lastChar * int(count)

    return result

print(unpackDnk("a12b12"))

def unpackDnkFile(fileName):
    with open(fileName) as fin:
        result = unpackDnk(fin.readline())
    return result

#print(unpackDnkFile("input"))
from collections import defaultdict

def string_to_words(string):
    return [w for w in string.split() if w.strip() != '']

def file_to_words(file_name):
    with open(file_name) as fin:
        content = fin.read()
    return string_to_words(content)

def find_popular_word(words: [str]):
    word_popularity = defaultdict(int)
    most_popular_word = ''
    most_popular_count = 0
    for word in words:
        word_popularity[word] += 1
        if word_popularity[word] > most_popular_count:
            most_popular_word = word
            most_popular_count = word_popularity[word]
    return (most_popular_word, most_popular_count)

def find_popular_word_in_file(file_name):
    word, count = find_popular_word(file_to_words(file_name))
    print(word, count)

print(find_popular_word(string_to_words("ab cd ed ab")))
print(find_popular_word_in_file("tasks.py"))
print(find_popular_word_in_file("input"))

