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

#print(dnk("aaabbdDcccz"))

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

#print(unpackDnk("a12b12"))

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

#print(find_popular_word(string_to_words("ab cd ed ab")))
#print(find_popular_word_in_file("tasks.py"))
#print(find_popular_word_in_file("input"))

from collections import OrderedDict

# @input string file name
# @return dict of name:[marks]
def school_results_from_file(file_name):
    result = OrderedDict()
    with open(file_name) as fin:
        lines = fin.read().split("\n")
    for line in lines:
        if line == '':
            continue
        fields = line.split(";")
        name = fields[0]
        math_mark = int(fields[1])
        phys_mark = int(fields[2])
        rusl_mark = int(fields[3])
        result[name] = [math_mark, phys_mark, rusl_mark]
    return result

def school_results_from_file_lc(file_name):
    with open(file_name) as fin:
        return [marks.split(";")[1:] for marks in fin.read().split("\n") if marks != '']

def calc_avg_makrs_every_lc(students_marks):
    return [avg/len(students_makrs[0]) for avg in students_marks]

def calc_avg_makrs_every(students_makrs):
    result = OrderedDict()
    for name, marks in students_makrs.items():
        result[name] = sum(marks) / float(len(marks))
    return result

def calc_avg_marks_total(students_makrs):
    if len(students_makrs) < 1:
        return []
    result = list()
    first = True
    for marks in students_makrs.values():
        if first:
            first = False
            result = marks[::]
        else:
            result = (a + b for a, b in zip(marks, result))
    result = list(result)
    length = len(students_makrs)
    return list(map(lambda x: x / length, result))

def students_print():
    inp = school_results_from_file('input_test')
    avg = calc_avg_makrs_every(inp)
    for avg_mark in avg.values():
        print(avg_mark)
    mid = calc_avg_marks_total(inp)
    for mid_mark in mid:
        print(mid_mark, end=' ')

    print(school_results_from_file_lc('input_test'))

#students_print()

def list_neigh_sum(lst):
    if len(lst) == 1:
        return lst
    ln = len(lst)
    result = list()
    for i in range(ln):
        if i == 0:
            result.append(lst[-1] + lst[i+1])
        elif i == ln - 1:
            pass
            result.append(lst[0] + lst[i-1])
        else:
            result.append(lst[i-1] + lst[i+1])
    return result

def string_to_intlist(string):
    return [int(x) for x in string.split(" ")]

from functools import reduce

def intlist_to_string(lst):
    return reduce(lambda x, y: x + str(y) + " ", lst, "")

def test_list_nei():
    print(list_neigh_sum([1]))
    print(list_neigh_sum([1, 2]))
    print(list_neigh_sum([1, 8, 2]))
    print(list_neigh_sum([1, 3, 5, 6, 10]))
    print(list_neigh_sum(string_to_intlist("1 2 3")))
    print(intlist_to_string(list_neigh_sum(string_to_intlist("1 2 3"))))



test_list_nei()


