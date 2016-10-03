from pprint import pprint as print
#46 Simple Python Exercises
#Define a function max() that takes two numbers as arguments and returns the largest of them. Use the if-then-else construct available in Python. (It is true that Python has the max() function built in, but writing it yourself is nevertheless a good exercise.)
def max(a, b):
  if a > b:
    return a
  else:
    return b
print(max(1,2),max(2,1), max(3,8))
#Define a function max_of_three() that takes three numbers as arguments and returns the largest of them.
def max_of_three(a,b,c):
  return max(a,(max(b,c)))
print(max_of_three(1,2,3),max_of_three(8,7,6),max_of_three(8,10,3))
#
#Define a function that computes the length of a given list or string. (It is true that Python has the len() function built in, but writing it yourself is nevertheless a good exercise.)
def leng(x):
  l = 0
  for i in x:
    l += 1
  return l
print(leng("abladfalsfd;"),leng([2,3,"",7]))
#Write a function that takes a character (i.e. a string of length 1) and returns True if it is a vowel, False otherwise.
def vow(c):
  vowels = "aeiouy"
  return c in vowels
print(vow('a'),vow('b'))
#Write a function translate() that will translate a text into "rövarspråket" (Swedish for "robber's language"). That is, double every consonant and place an occurrence of "o" in between. For example, translate("this is fun") should return the string "tothohisos isos fofunon".
def translate(s):
  r = ""
  for x in s:
    if not vow(x) and not x == ' ':
      r += x + "o" + x
    else:
      r += x
  return r
print(translate("this is fun"))
#Define a function sum() and a function multiply() that sums and multiplies (respectively) all the numbers in a list of numbers. For example, sum([1, 2, 3, 4]) should return 10, and multiply([1, 2, 3, 4]) should return 24.
def sum(a):
  s = 0
  for x in a:
    s += x
  return s
def mul(a):
  m = 1
  for x in a:
    m *= x
  return m
print(sum([1,2,3,4]), mul([1,2,3,4]))
#Define a function reverse() that computes the reversal of a string. For example, reverse("I am testing") should return the string "gnitset ma I".
def reverse(s):
  r=""
  for x in range(leng(s)-1, -1, -1):
    r += s[x]
  return r
print(reverse("I am testing"))
#Define a function is_palindrome() that recognizes palindromes (i.e. words that look the same written backwards). For example, is_palindrome("radar") should return True.
def is_palindrome(s):
  for x in range(len(s) // 2):
    #print(x, s[x], s[len(s) -x - 1], len(s) - x - 1)
    if s[x] != s[len(s) - x - 1]:
      return False
  return True
print(is_palindrome("radar"), is_palindrome("zoxaxoz"))
#Write a function is_member() that takes a value (i.e. a number, string, etc) x and a list of values a, and returns True if x is a member of a, False otherwise. (Note that this is exactly what the in operator does, but for the sake of the exercise you should pretend Python did not have this operator.)
def is_member(l, v):
  for x in l:
    if x == v:
      return True
  return False
print(is_member(list("123456678"),"6"),is_member(list("123456678"),"1"),is_member(list("123456678"),'8'), is_member("lj;lj","a"),is_member([1,5,6],6))
#Define a function overlapping() that takes two lists and returns True if they have at least one member in common, False otherwise. You may use your is_member() function, or the in operator, but for the sake of the exercise, you should (also) write it using two nested for-loops.
def overlapping(x, y):
  for a in x:
    for b in y:
      if a == b:
        return True
  return False
print(overlapping("23456789","rtyuio"), overlapping("56789","2345"))
#Define a function generate_n_chars() that takes an integer n and a character c and returns a string, n characters long, consisting only of c:s. For example, generate_n_chars(5,"x") should return the string "xxxxx". (Python is unusual in that you can actually write an expression 5 * "x" that will evaluate to "xxxxx". For the sake of the exercise you should ignore that the problem can be solved in this manner.)
def generate_n_chars(n, c):
  s = ''
  x = 0
  while x < n:
    s += c
    x += 1
  return s
print(generate_n_chars(10,"a"),generate_n_chars(5,"5"))
#Define a procedure histogram() that takes a list of integers and prints a histogram to the screen. For example, histogram([4, 9, 7]) should print the following:
#****
#*********
#*******
def histogram(l):
  for x in l:
    print(generate_n_chars(x,"*"))
histogram([4,9,7,1,2,3,8,8,1,0,1,5,1,1])
#The function max() from exercise 1) and the function max_of_three() from exercise 2) will only work for two and three numbers, respectively. But suppose we have a much larger number of numbers, or suppose we cannot tell in advance how many they are? Write a function max_in_list() that takes a list of numbers and returns the largest one.
def max_in_list(l):
  m = l[0]
  for x in l:
    if x > m:
      m = x
  return m
print(max_in_list([-20,2,-30,8,10,8,1]))
#Write a program that maps a list of words into a list of integers representing the lengths of the correponding words.
def wordsLens1(l):
  r = []
  for x in l:
    r += [len(x)]
  return r
def wordsLens2(l):
  return [len(x) for x in l]
def wordsLens3(l):
  return list(map(len, l))
print(wordsLens1(["x","run","asdf",'']))
print(wordsLens2(["x","run","asdf",'']))
print(wordsLens3(["x","run","asdf",'']))
#Write a function find_longest_word() that takes a list of words and returns the length of the longest one.
def find_longest_word(l):
  return max_in_list(wordsLens3(l))
print(find_longest_word(["x","run","asdf",'']))
#Write a function filter_long_words() that takes a list of words and an integer n and returns the list of words that are longer than n.
def filter_long_words(l,n):
  r = []
  for x in l:
    if len(x) > n:
      r += [x]
  return r
print(filter_long_words(["x","run","asdf",'kkkkkk'],3))
#Write a version of a palindrome recognizer that also accepts phrase palindromes such as "Go hang a salami I'm a lasagna hog.", "Was it a rat I saw?", "Step on no pets", "Sit on a potato pan, Otis", "Lisa Bonet ate no basil", "Satan, oscillate my metallic sonatas", "I roamed under it as a tired nude Maori", "Rise to vote sir", or the exclamation "Dammit, I'm mad!". Note that punctuation, capitalization, and spacing are usually ignored.
def is_palindrome2(s):
  z = ''
  for x in s.lower():
    if x.isalpha():
      z += x
  #print(z)
  return is_palindrome(z)
print(is_palindrome2("Was it a rat I saw?"), is_palindrome2("Was it a rat I saz?"))
#A pangram is a sentence that contains all the letters of the English alphabet at least once, for example: The quick brown fox jumps over the lazy dog. Your task here is to write a function to check a sentence to see if it is a pangram or not.
def is_pangram(s):
  alphabet = set(map(chr, range(ord('a'), ord('z') + 1)))
  x = set(s)
  return (alphabet - x) == set()
print(is_pangram("The quick brown fox jumps over the lazy dogggg"))
print(is_pangram("The quick brown fox jumps over the lazy do"))
#"99 Bottles of Beer" is a traditional song in the United States and Canada:
#99 bottles of beer on the wall, 99 bottles of beer.
#Take one down, pass it around, 98 bottles of beer on the wall.
#The same verse is repeated, each time with one fewer bottle. The song is completed when the singer or singers reach zero.
#
#Your task here is write a Python program capable of generating all the verses of the song.
def a99bofb():
  for x in range(99,0,-1):
    print(str(x) + ' bottles of beer on the wall, ' + str(x) + ' bottles of beer.')
    print('Take one down, pass it around, ' + str(x-1) + ' bottles of beer on the wall.')
a99bofb()
#Represent a small bilingual lexicon as a Python dictionary in the following fashion {"merry":"god", "christmas":"jul", "and":"och", "happy":gott", "new":"nytt", "year":"år"} and use it to translate your Christmas cards from English into Swedish. That is, write a function translate() that takes a list of English words and returns a list of Swedish words.
def strToWordList(s):
  return s.split(' ')
def translate(l):
  a = {"merry":"god", "christmas":"jul", "and":"och", "happy":"gott", "new":"nytt", "year":"år"}
  return list(map(lambda x: a.get(x,x), strToWordList(l)))
print(translate("We wish you a merry christmas and xmas. happy new year!"))
#Write a function char_freq() that takes a string and builds a frequency listing of the characters contained in it. Represent the frequency listing as a Python dictionary. Try it with something like char_freq("abbabcbdbabdbdbabababcbcbab").
def char_freq(s):
  r = {}
  for x in s:
    if not x in r:
      r[x] = 1
    else:
      r[x] += 1
  return r
print(char_freq("abbabcbdbabdbdbabababcbcbab"))
#In cryptography, a Caesar cipher is a very simple encryption techniques in which each letter in the plain text is replaced by a letter some fixed number of positions down the alphabet. For example, with a shift of 3, A would be replaced by D, B would become E, and so on. The method is named after Julius Caesar, who used it to communicate with his generals. ROT-13 ("rotate by 13 places") is a widely used example of a Caesar cipher where the shift is 13. In Python, the key for ROT-13 may be represented by means of the following dictionary:
#
#key = {'a':'n', 'b':'o', 'c':'p', 'd':'q', 'e':'r', 'f':'s', 'g':'t', 'h':'u', 
#       'i':'v', 'j':'w', 'k':'x', 'l':'y', 'm':'z', 'n':'a', 'o':'b', 'p':'c', 
#       'q':'d', 'r':'e', 's':'f', 't':'g', 'u':'h', 'v':'i', 'w':'j', 'x':'k',
#       'y':'l', 'z':'m', 'A':'N', 'B':'O', 'C':'P', 'D':'Q', 'E':'R', 'F':'S', 
#       'G':'T', 'H':'U', 'I':'V', 'J':'W', 'K':'X', 'L':'Y', 'M':'Z', 'N':'A', 
#       'O':'B', 'P':'C', 'Q':'D', 'R':'E', 'S':'F', 'T':'G', 'U':'H', 'V':'I', 
#       'W':'J', 'X':'K', 'Y':'L', 'Z':'M'}
#Your task in this exercise is to implement an encoder/decoder of ROT-13. Once you're done, you will be able to read the following secret message:
#   Pnrfne pvcure? V zhpu cersre Pnrfne fnynq!
#Note that since English has 26 characters, your ROT-13 program will be able to both encode and decode texts written in English.
key = {'a':'n', 'b':'o', 'c':'p', 'd':'q', 'e':'r', 'f':'s', 'g':'t', 'h':'u', 
       'i':'v', 'j':'w', 'k':'x', 'l':'y', 'm':'z', 'n':'a', 'o':'b', 'p':'c', 
       'q':'d', 'r':'e', 's':'f', 't':'g', 'u':'h', 'v':'i', 'w':'j', 'x':'k',
       'y':'l', 'z':'m', 'A':'N', 'B':'O', 'C':'P', 'D':'Q', 'E':'R', 'F':'S', 
       'G':'T', 'H':'U', 'I':'V', 'J':'W', 'K':'X', 'L':'Y', 'M':'Z', 'N':'A', 
       'O':'B', 'P':'C', 'Q':'D', 'R':'E', 'S':'F', 'T':'G', 'U':'H', 'V':'I', 
       'W':'J', 'X':'K', 'Y':'L', 'Z':'M'}
def rot13decode(msg):
  m = ''
  for x in msg:
    if x in key:
      m += key[x]
    else:
      m += x
  return m
def rot13encode2(msg):
  return ''.join((list(map(lambda x: key[x], msg))))
print(rot13decode("Pnrfne pvcure? V zhpu cersre Pnrfne fnynq!"))
#Define a simple "spelling correction" function correct() that takes a string and sees to it that 1) two or more occurrences of the space character is compressed into one, and 2) inserts an extra space after a period if the period is directly followed by a letter. E.g. correct("This   is  very funny  and    cool.Indeed!") should return "This is very funny and cool. Indeed!" Tip: Use regular expressions!
def correct(s): #N:23
  import re
  nomorespace = re.sub('\s\s+',' ',s)
  return re.sub('\.(\w)','. \g<1>',nomorespace)
print(correct("This   is  very funny  and    cool.Indeed!"))
#The third person singular verb form in English is distinguished by the suffix -s, which is added to the stem of the infinitive form: run -> runs. A simple set of rules can be given as follows:
#If the verb ends in y, remove it and add ies
#If the verb ends in o, ch, s, sh, x or z, add es
#By default just add s
#Your task in this exercise is to define a function make_3sg_form() which given a verb in infinitive form returns its third person singular form. Test your function with words like try, brush, run and fix. Note however that the rules must be regarded as heuristic, in the sense that you must not expect them to work for all cases. Tip: Check out the string method endswith().
def make_3sg_form(s):
  import re
  if s.endswith('y'):
    return s[:-1] + 'ies'
  else:
    return re.sub('(o$|ch$|s$|sh$|x$|z$)','\g<1>e',s) + 's'
print(make_3sg_form('try'), make_3sg_form('brush'), make_3sg_form('run'), make_3sg_form('fix'))
#In English, the present participle is formed by adding the suffix -ing to the infinite form: go -> going. A simple set of heuristic rules can be given as follows:
#If the verb ends in e, drop the e and add ing (if not exception: be, see, flee, knee, etc.)
#If the verb ends in ie, change ie to y and add ing
#For words consisting of consonant-vowel-consonant, double the final letter before adding ing
#By default just add ing
#Your task in this exercise is to define a function make_ing_form() which given a verb in infinitive form returns its present participle form. Test your function with words such as lie, see, move and hug. However, you must not expect such simple rules to work for all cases.

#Higher order functions and list comprehensions

#Using the higher order function reduce(), write a function max_in_list() that takes a list of numbers and returns the largest one. Then ask yourself: why define and call a new function, when I can just as well call the reduce() function directly?
def max_in_list2(l):
  import functools
  return functools.reduce(max, l)
print(max_in_list2([1,2,3,4,66,5,43,4,4]))
#Write a program that maps a list of words into a list of integers representing the lengths of the correponding words. Write it in three different ways: 1) using a for-loop, 2) using the higher order function map(), and 3) using list comprehensions.

#Write a function find_longest_word() that takes a list of words and returns the length of the longest one. Use only higher order functions.
def find_longest_word2(l):
  import functools
  return functools.reduce(lambda x, y: max(x, len(y)),l,0)
print(find_longest_word2(["x","run","asdf",'']))
#Using the higher order function filter(), define a function filter_long_words() that takes a list of words and an integer n and returns the list of words that are longer than n.
def filter_long_words2(l, n):
  return list(filter(lambda x: x if len(x) > n else False, l))
print(filter_long_words2(["x","run","asdf",'kkkkkk'],3))
#Represent a small bilingual lexicon as a Python dictionary in the following fashion {"merry":"god", "christmas":"jul", "and":"och", "happy":gott", "new":"nytt", "year":"år"} and use it to translate your Christmas cards from English into Swedish. Use the higher order function map() to write a function translate() that takes a list of English words and returns a list of Swedish words.
def translate2(s):
  d = {"merry":"god", "christmas":"jul", "and":"och", "happy":"gott", "new":"nytt", "year":"år"} 
  return list(map(lambda x: d.get(x, x), s))
print(translate2("We wish you a merry christmas and xmas. happy new year!".split()))
#Implement the higher order functions map(), filter() and reduce(). (They are built-in but writing them yourself may be a good exercise.)
def map2(f,l):
  r = []
  for x in l:
    r += [f(x)]
  return r
print(map2(lambda x: x*x, list(range(10))))
def odd(x):
  return x % 2 == 1
def filter2(f, l):
  r = []
  for x in l:
    if f(x):
      r += [x]
  return r
print(filter2(odd, list(range(10))))
def reduce2(f,l,i = False):
  if not i:
    i = l[0]
  r = i
  for x in l:
    r = f(r, x)
  return r
print(reduce2(lambda x, y: x * y,list(range(1,10))))
#Simple exercises including I/O

#Write a version of a palindrome recogniser that accepts a file name from the user, reads each line, and prints the line to the screen if it is a palindrome.
def palindromF(fn):
  fileobj = open(fn, 'r')
  while True:
    line = fileobj.readline()
    #print(is_palindrome2(line))
    if not line:
      break
    if is_palindrome2(line):
      print(line)
  fileobj.close()
palindromF('pali.txt')
#According to Wikipedia, a semordnilap is a word or phrase that spells a different word or phrase backwards. ("Semordnilap" is itself "palindromes" spelled backwards.) Write a semordnilap recogniser that accepts a file name (pointing to a list of words) from the user and finds and prints all pairs of words that are semordnilaps to the screen. For example, if "stressed" and "desserts" is part of the word list, the the output should include the pair "stressed desserts". Note, by the way, that each pair by itself forms a palindrome!
def semordnilap(fn):
  with open(fn, 'rt') as f:
  #  for line in f:
    a = f.read().split()
    printed = []
    for x in a:
      if x[::-1] in a and not x in printed:
        print(x, x[::-1])
        printed += [x[::-1]]
semordnilap('semo.txt')
#Write a procedure char_freq_table() that, when run in a terminal, accepts a file name from the user, builds a frequency listing of the characters contained in the file, and prints a sorted and nicely formatted character frequency table to the screen.
def char_freq_table(fn):
  with open(fn, 'rt') as f:
    cf = char_freq(f.read())
    import math
    col = int(math.ceil(math.sqrt(len(cf))))
    i = 0
    for x,y in sorted(cf.items(), key=lambda x: x[1]):
      print( (str(ord(x)) + ' : ' + str(y)).center(10) , end='|\n' if col == i else '    ')
      i+=1
      if i > col:
        i = 0
char_freq_table('semo.txt')
#The International Civil Aviation Organization (ICAO) alphabet assigns code words to the letters of the English alphabet acrophonically (Alfa for A, Bravo for B, etc.) so that critical combinations of letters (and numbers) can be pronounced and understood by those who transmit and receive voice messages by radio or telephone regardless of their native language, especially when the safety of navigation or persons is essential. Here is a Python dictionary covering one version of the ICAO alphabet:
#
#d = {'a':'alfa', 'b':'bravo', 'c':'charlie', 'd':'delta', 'e':'echo', 'f':'foxtrot',
#     'g':'golf', 'h':'hotel', 'i':'india', 'j':'juliett', 'k':'kilo', 'l':'lima',
#     'm':'mike', 'n':'november', 'o':'oscar', 'p':'papa', 'q':'quebec', 'r':'romeo',
#     's':'sierra', 't':'tango', 'u':'uniform', 'v':'victor', 'w':'whiskey', 
#     'x':'x-ray', 'y':'yankee', 'z':'zulu'}
#Your task in this exercise is to write a procedure speak_ICAO() able to translate any text (i.e. any string) into spoken ICAO words. You need to import at least two libraries: os and time. On a mac, you have access to the system TTS (Text-To-Speech) as follows: os.system('say ' + msg), where msg is the string to be spoken. (Under UNIX/Linux and Windows, something similar might exist.) Apart from the text to be spoken, your procedure also needs to accept two additional parameters: a float indicating the length of the pause between each spoken ICAO word, and a float indicating the length of the pause between each word spoken.
def speak_ICAO(s, charPause, wordPause):
  d = {'a':'alfa', 'b':'bravo', 'c':'charlie', 'd':'delta', 'e':'echo', 'f':'foxtrot',
     'g':'golf', 'h':'hotel', 'i':'india', 'j':'juliett', 'k':'kilo', 'l':'lima',
     'm':'mike', 'n':'november', 'o':'oscar', 'p':'papa', 'q':'quebec', 'r':'romeo',
     's':'sierra', 't':'tango', 'u':'uniform', 'v':'victor', 'w':'whiskey', 
     'x':'x-ray', 'y':'yankee', 'z':'zulu'}
  import os
  import time
  for x in s:
    print(d.get(x,''))
    if ' ' == x:
      time.sleep(wordPause)
    else:
      time.sleep(charPause)
  
def icaotest():
  speak_ICAO("some birds can fly", 0.1, 0.5)
#python -i 46Sim...
#A hapax legomenon (often abbreviated to hapax) is a word which occurs only once in either the written record of a language, the works of an author, or in a single text. Define a function that given the file name of a text will return all its hapaxes. Make sure your program ignores capitalization.
def hapax(fn): # Гапакс
  with open(fn, 'rt') as f:
    contents = f.read().lower()
    wordFreq = dict()
    for x in contents.split():
      if x in wordFreq:
        wordFreq[x] += 1
      else:
        wordFreq[x] = 1
    #hapaxes = list(filter(lambda x: x == 1, wordFreq.values()))
    hapaxes = []
    for s,n in wordFreq.items():
      if n == n:
        hapaxes += [s]
    return hapaxes
print(hapax('semo.txt'))
#Write a program that given a text file will create a new text file in which all the lines from the original file are numbered from 1 to n (where n is the number of lines in the file).
def numFileLines(fn):
  with open(fn, 'rt') as fin:
    with open(fn+'.out', 'wt') as fout:
      n = 1
      for x in fin:
        fout.write(str(n) + ' ' + x)
        n += 1
#numFileLines('46SimplePythonExercises.py')
 #Write a program that will calculate the average word length of a text stored in a file (i.e the sum of all the lengths of the word tokens in the text, divided by the number of word tokens).
def avgWordLen(fn):
  with open(fn, 'rt') as f:
    words = f.read().split()
    return sum(wordsLens3(words)) / len(words)
print(avgWordLen('semo.txt'))
#39. Write a program able to play the "Guess the number"-game, where the number to be guessed is randomly chosen between 1 and 20. (Source: http://inventwithpython.com) This is how it should work when run in a terminal:
#>>> import guess_number
#Hello! What is your name?
#Torbjörn
#Well, Torbjörn, I am thinking of a number between 1 and 20.
#Take a guess.
#10
#Your guess is too low.
#Take a guess.
#15
#Your guess is too low.
#Take a guess.
#18
#Good job, Torbjörn! You guessed my number in 3 guesses!
def guess_number():
  import random
  print('Hello! What is your name?')
  name = input()
  print('Well, ' + name + ', I am thinking of a number between 1 and 20.')
  number = random.randint(1,20)
  turns = 0
  while True:
    print('Take a guess.')
    g = int(input())
    turns += 1
    if g > number:
      print('Your guess is too high.')
    elif g < number:
      print('Your guess is too low.')
    else:
      print('Good job, ' + name + '! You guessed my number in ' + str(turns) + ' guesses!')
      break
#guess_number()

#40. An anagram is a type of word play, the result of rearranging the letters of a word or phrase to produce a new word or phrase, using all the original letters exactly once; e.g., orchestra = carthorse, A decimal point = I'm a dot in place. Write a Python program that, when started 1) randomly picks a word w from given list of words, 2) randomly permutes w (thus creating an anagram of w), 3) presents the anagram to the user, and 4) enters an interactive loop in which the user is invited to guess the original word. It may be a good idea to work with (say) colour words only. The interaction with the program may look like so:
#>>> import anagram
#Colour word anagram: onwbr
#Guess the colour word!
#black
#Guess the colour word!
#brown
#Correct!
def anagram(l):
  import random as r
  r.seed()
  word = l[r.randint(0, len(l)-1)]
  lword = list(word)
  #print(l, lword, word)
  for x in range(r.randint(5,20)):
    a = r.randint(0, len(word)-1)
    b = r.randint(0, len(word)-1)
    lword[a], lword[b] = lword[b], lword[a]
  print('Colour word anagram:', ''.join(lword))
  while True:
    print('Guess the colour word!')
    g = input()
    if g == word:
      print('Correct!')
      break
def anagramRun():
  anagram('there hidden word five characters long'.split())

#41. In a game of Lingo, there is a hidden word, five characters long. The object of the game is to find this word by guessing, and in return receive two kinds of clues: 1) the characters that are fully correct, with respect to identity as well as to position, and 2) the characters that are indeed present in the word, but which are placed in the wrong position. Write a program with which one can play Lingo. Use square brackets to mark characters correct in the sense of 1), and ordinary parentheses to mark characters correct in the sense of 2). Assuming, for example, that the program conceals the word "tiger", you should be able to interact with it in the following way:
#>>> import lingo
#snake
#Clue: snak(e)
#fiest
#Clue: f[i](e)s(t)
#times
#Clue: [t][i]m[e]s
#tiger
#Clue: [t][i][g][e][r]
def lingo():
  def printLingo(s, w):
    i = 0
    r = ''
    while i < len(s):
      if s[i] == w[i]:
        r += '[' + s[i] + ']'
      elif s[i] in w:
        r += '(' + s[i] + ')'
      else:
        r += s[i]
      i += 1
    print(r)
  
  import random as r
  r.seed()
  words='tiger snake holod burge cotto'.split()
  word = words[r.randint(0, len(words)-1)]
  while True:
    g = input('Clue: ')
    printLingo(g[:5], word)
    if g == word:
      break
  
#Somewhat harder exercises
#42. A sentence splitter is a program capable of splitting a text into sentences. The standard set of heuristics for sentence splitting includes (but isn't limited to) the following rules:
#Sentence boundaries occur at one of "." (periods), "?" or "!", except that

#Periods followed by whitespace followed by a lower case letter are not sentence boundaries.
#Periods followed by a digit with no intervening whitespace are not sentence boundaries.
#Periods followed by whitespace and then an upper case letter, but preceded by any of a short list of titles are not sentence boundaries. Sample titles include Mr., Mrs., Dr., and so on.
#Periods internal to a sequence of letters with no adjacent whitespace are not sentence boundaries (for example, www.aptex.com, or e.g).
#Periods followed by certain kinds of punctuation (notably comma and more periods) are probably not sentence boundaries.
# (\.\s[a-z]) (\.\d) ((Mr|Mrs|Dr|Jr)\.\s[A-Z]) (\w\.\w) (\.(\,|\.))
# (\.\s[a-z])|(\.\d)|((Mr|Mrs|Dr|Jr)\.\s[A-Z])|(\w\.\w)|(\.(\,|\.))
# ((Mr|Mrs|Dr|Jr)\.\s[A-Z]) (\w\.\w)   (\.\s[a-z]) (\.\d) (\.(\,|\.))
#Your task here is to write a program that given the name of a text file is able to write its content with each sentence on a separate line. Test your program with the following short text: Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it. Did he mind? Adam Jones Jr. thinks he didn't. In any case, this isn't true... Well, with a probability of .9 it isn't. The result should be:
#Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it.
#Did he mind?
#Adam Jones Jr. thinks he didn't.
#In any case, this isn't true...
#Well, with a probability of .9 it isn't.
def sentenceSplitter(fn):
  content = ''
  with open(fn, 'rt') as fin:
    content = fin.read();
  with open(fn, 'wt') as fout:
    import re
    s = re.sub('\.','.\n', content)
    s = re.sub('((Mr|Mrs|Dr|Jr)\.\n(\s[A-Z]))','\g<2>.\g<3>', s)
    s = re.sub('(\w)\.\n(\w)','\g<1>.\g<2>', s)
    s = re.sub('\.\n(\s[a-z])','.\g<1>', s)
    s = re.sub('\.\n(\d)','.\g<1>', s)
    s = re.sub('\.\n(\.+)','.\g<1>', s)
    s = re.sub('\.\n(\,|\.)','.\g<1>', s)
    s = re.sub('(\?|\!)\s', '\g<1>\n', s)
    print(s)
    fout.write(content)
#sentenceSplitter('test.txt')
#43. An anagram is a type of word play, the result of rearranging the letters of a word or phrase to produce a new word or phrase, using all the original letters exactly once; e.g., orchestra = carthorse. Using the word list at http://www.puzzlers.org/pub/wordlists/unixdict.txt, write a program that finds the sets of words that share the same characters that contain the most words in them.
def is_anagram(a,b):
  a = list(a)
  b = list(b)
  for x in a:
    if x in b:
      del b[b.index(x)]
      
  return [] == b
def anagrams(l):
  x = y = 0
  r = []
  while x < len(l)-1:
    y = x + 1
    z = []
    while y < len(l)-1:
      if is_anagram(l[x], l[y]):
        if len(z) == 0:
          z += [l[x]]
        z += [l[y]]
      y += 1
    if z:
      r += [z]
    x +=1
  return r
#print(is_anagram('bda', 'dab'))
#print(anagrams('bda dab bad ddd ada daa dda cad aaa dac'.split()))
def anagramFile():

  fn = 'unixdict.txt'
  content = ''
  with open(fn, 'rt') as f:
    content = f.read().split()
  # сначала создадим словарь вида {длинна : список слов данной длинны}
  words = dict()
  for x in content:
    if words.get(len(x),False):
      words[len(x)] += [x]
    else:
      words[len(x)] = [x]
    
  anag = []
  for l,v in words.items():
    words[l] = anagrams(v)
  
  with open(fn+'.out', 'wt') as f:
    for l,v in words.items():
      for x in v:
        f.write(x)
      f.write('\n')
#anagramFile()
#44. Your task in this exercise is as follows:
#
#Generate a string with N opening brackets ("[") and N closing brackets ("]"), in some arbitrary order.
#Determine whether the generated string is balanced; that is, whether it consists entirely of pairs of opening/closing brackets (in that order), none of which mis-nest.
#Examples:
#
#   []        OK   ][        NOT OK
#   [][]      OK   ][][      NOT OK
#   [[][]]    OK   []][[]    NOT OK
def bracketsBalance(s):
  balance = 0
  if ']' == s[0] or '[' == s[-1]:
    return False
  for x in s:
    if balance < 0:
      return False
    if '[' == x:
      balance += 1
    else:
      balance -= 1
  return 0 == balance
def bracketsTest():
  import random as r
  r.seed()
  n = r.randint(2,3) * 2
  while True:
    s = ''
    for x in range(n):
      s += r.choice(['[',']'])
    print(s, bracketsBalance(s))
    if bracketsBalance(s):
      return
  #генерировать пока не будет True
bracketsTest()
for x in ' [] ][ [[ ]] [[[ ]]] [[] []] [][] [[][]] ][ ][][ []][[]'.split():
  print(x, bracketsBalance(x))
bracketsTest()
#45. A certain childrens game involves starting with a word in a particular category. Each participant in turn says a word, but that word must begin with the final letter of the previous word. Once a word has been given, it cannot be repeated. If an opponent cannot give a word in the category, they fall out of the game. For example, with "animals" as the category,
#Child 1: dog 
#Child 2: goldfish
#Child 1: hippopotamus
#Child 2: snake
#Your task in this exercise is as follows: Take the following selection of 70 English Pokemon names (extracted from Wikipedia's list of Pokemon) and generate the/a sequence with the highest possible number of Pokemon names where the subsequent name starts with the final letter of the preceding name. No Pokemon name is to be repeated.
pokes = 'audino bagon baltoy banette bidoof braviary bronzor carracosta charmeleon cresselia croagunk darmanitan deino emboar emolga exeggcute gabite girafarig gulpin haxorus heatmor heatran ivysaur jellicent jumpluff kangaskhan kricketune landorus ledyba loudred lumineon lunatone machamp magnezone mamoswine nosepass petilil pidgeotto pikachu pinsir poliwrath poochyena porygon2 porygonz registeel relicanth remoraid rufflet sableye scolipede scrafty seaking sealeo silcoon simisear snivy snorlax spoink starly tirtouga trapinch treecko tyrogue vigoroth vulpix wailord wartortle whismur wingull yamask'
def seqpo(lst, n, al):
  item = lst[n]
  del lst[n]
  nxt = list(filter(lambda x: x.startswith(item[-1]), lst))
  print(item, lst, nxt)
  r = [item]
  if nxt:
    for x in nxt:
      r += seqpo(lst.copy(), lst.index(x), al + [item])
  return r
def highestSeq(l):
  return
print(seqpo('abc can nok nak ona'.split(),4, []))
# 45 Пред СЛОЖН

#46. An alternade is a word in which its letters, taken alternatively in a strict sequence, and used in the same order as the original word, make up at least two other words. All letters must be used, but the smaller words are not necessarily of the same length. For example, a word with seven letters where every second letter is used will produce a four-letter word and a three-letter word. Here are two examples:
#
#  "board": makes "bad" and "or".
#  "waists": makes "wit" and "ass".
#Using the word list at http://www.puzzlers.org/pub/wordlists/unixdict.txt, write a program that goes through each word in the list and tries to make two smaller words using every second letter. The smaller words must also be members of the list. Print the words to the screen in the above fashion.

