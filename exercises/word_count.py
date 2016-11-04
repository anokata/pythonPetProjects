import unittest

# procedural
def word_count(s):
    if s == '':
        return 0
    words = 0
    in_word = False

    for c in s:
        if c != ' ':
            if in_word:
                pass
            else:
                in_word = True
        else:
            if in_word:
                words += 1
                in_word = False
            else:
                pass
    if in_word:
        words += 1
    #test
    print(s, words)
    return words

def word_count_func(s):
    def wd(s, char, in_word, words):
        if s == '' and in_word:
            return words + 1
        if s == '':
            return words
        if (in_word and char != ' ') or (!in_word and char == ' '):
            wd(s[1:], s[0], 

class Test_word_count(unittest.TestCase):
    def test(self):
        self.assertEqual(word_count(''), 0)
        self.assertEqual(word_count('   '), 0)
        self.assertEqual(word_count('one'), 1)
        self.assertEqual(word_count('one, two three'), 3)
        self.assertEqual(word_count(' one, two three# ehu&, '), 4)

if __name__=="__main__":
    unittest.main()
    
