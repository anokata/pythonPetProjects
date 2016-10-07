#0.0  Написать процедуру тестирующую все следующие функции, и выводящую отчёт.
#1.0  написать функцию sumArray принимающую массив целых чисел и вычисляющих сумму.
def sumArray(l):
  i = 0
  rez = 0
  while i < len(l):
    rez = rez + l[i]
    i = i + 1
  return rez
#1.1  написать функцию avgArray принимающую массив целых чисел и вычисляющих среднее арифметическое.
def avgArray(l):
  from functools import reduce
  return reduce(int.__add__, l) / len(l)
#1.2  написать функцию lenString вычисляющую длинну переданной строки.
def lenString(l):
  return 0 if [] == l else 1 + lenString(l[1:])
#2.0  Написать функцию max2 возвращающую большее из двух чисел.
def max2(a, b):
  return a if a > b else b
  #return (a+b) - abs(a-b) # как без условий?
#2.1  Написать функцию max3 принимающую 3 числа и возвращающую максимальное.
#2.2  Написать функцию sortArray принимающую массив чисел и сортирующую его с помощью функции max2
def sortArray(l):
  i = 0
  j = 0
  for i in range(len(l)):
    for j in range(i,len(l)):
      l[i], l[j] = min(l[i],l[j]), max2(l[i],l[j])
  return l
#2.3  Написать функцию maxArray принимающую массив целых чисел и находящую максимальное значение.
def maxArray(a):
  r = a[0]
  for x in a:
    r = max(x, r)
  return r
#2.4  Написать функцию is_member проверяющая встречается ли строка в массиве строк.
#2.5  Написать функцию overlapping принимающую два массива и возвращую True если у массивов есть хотя бы один общий элемент. можно использовать is_member.
#3.0  написать функцию принимающую два массива целых чисел и возвращающую массив разности элементов. Result = X - Y
#3.1  написать функцию принимающую массив целых чисел и целое число, и вычисляющих сумму элементов меньших переданного числа.
#4.0  написать функцию isInRectangle принимающую 4 целых числа - декартовы координаты углов прямоугольника и два числа - координаты точки. функция должна определять находится ли точка внутри прямоугольника.
#4.1  написать функцию greaterThan принимающую массив целых чисел и число, возвращающую массив чисел превыщающих переданное. (смотри про динамические массивы)
#5.0  написать функцию isVowel проверяющая символ на гласный(True)\согласный(False)
#5.1  написать функцию is_palindrome проверяющая строку на палиндром, вида "радар"
#5.2  написать функцию reverseString переворачивающую строку. 'abcd' -> 'dcba'
#5.3  написать функцию stringToNumber для преобразования строки содержащую десятичное число в число integer. строка состоит из символов, подобна массиву из char. каждый char это код символа в кодировке. коды цифр - 48 = '0'  можно использовать функции ORD CHR, смотрим справку, ищем примеры. CHR(50) == '2', ORD('3')==51
#5.4  написать функцию numberToString преобразования числа в строку.
#5.5  Написать функцию strCmpGT принимающую две строки и возвращающую True если первая больше второй.(сравнивая в лексикографическом порядке) Например:  ab > aa    aba < ca    aba < z    abc < abca
#5.6  Напсать функцию sortStringArray сортирующую массив строк в лексикографическом порядке, пользуясь функцией strCmpGT.
#6.0  написать функцию fileStringChange для замены в файле заданной строку на другую заданную.
#6.1  написать функцию fileStringReverse для переворачивания файла построчно, с конца в начало и обращающую и каждую строку функцией reverseString.
#7.0  написать функцию вычисляющую факториал числа не используя циклы.
#7.1  написать функцию суммирующую массив чисел не используя циклы.
#7.2  написать функцию перемножающую массив чисел не используя циклы.
#8.0  написать функцию принимающую матрицу(двумерный массив) символов и два символа и заполняющую первыми символами диагонали, а вторыми символами элементы с обоими чётными индексами.
#8.1  написать процедуру печатающую матрицу символов, поэлементно, без пробелов, каждую строку с новой строки.
#8.2 Напиши функцию которая преобразует массив слов в массив чисел представляющих длинну каждого слова.
#8.3 Напиши функцию find_longest_word которая принимает массив слов и возвращает длинну самого длинного.
#8.4 Напиши функцию filter_long_words которая принимает массив слов и целое число N, и возвращает массив слов длинны больше N.
def alltest():
  print('Begining of Tests.')
  l1 = [2,8,4,9,23,3, 1]
  print(sumArray(l1))
  print(avgArray(l1))
  print(lenString(l1))
  print(max2(23,13),max2(13,22))
  print(sortArray(l1))
  print(maxArray(l1))
  #сделать задачи из книги

def myexperiments():
  class A():
    n = []
    k = []
    def __init__(self, x):
      self.n = list()
      self.k = list()
      self.n += [x]
    def a(self, x):
      print(self)
      self.k += [x]

  a = A(1)
  b = A(2)
  a.a(3)
  b.a(4)
  print(a.n, a.k, b.n, b.k, a.k == b.k)

  a = [A(1),A(2),A(3)]
  print(a)
  for i in a:
    if i.n[0] == 2:
      print('del')
  print(a)
  a[:]=filter(lambda i: i.n[0] != 2, a)
  print(a)


myexperiments()
alltest()
