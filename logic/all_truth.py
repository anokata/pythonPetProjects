def test_formula(formula):
    var = sorted(extract_formula_vars(formula))
    var_len = len(var)
    for v in var:
        print("| {} ".format(v.center(7)), end='')
    print("|")
    print(' ', end='')
    print("-" * (10 * var_len))

    for x in range(2 ** var_len):
        z = bin(x)[2:].zfill(var_len)
        table_row = list(map(lambda x: True if x == '1' else False, z))
        print("|", end='')
        for val in table_row:
            print(str(val).center(9), end='|')
        # result
        print()


def calc_implication(a, b):
    return (not a) or b

def extract_formula_vars(formula):
    return list(set(filter(str.isalpha, tokenize_formula(formula))))

def is_correct_formula_parentetheses(formula):
    balance = 0
    for t in tokenize_formula(formula):
        if t == '(':
            balance += 1
        elif t == ')':
            balance -= 1
        if balance < 0:
            return False

    return balance == 0

TOKENS = ["a", "b", "c", "(", "->", ")"]
MAX_TOKEN_LEN = max(map(len, TOKENS))

def tokenize_formula(formula):
    formula = formula.strip().replace(' ', '')
    tokens = list()
    while formula != '':
        token, formula = take_token(formula)
        tokens.append(token)
    return tokens

def take_token(formula):
    token = ''
    i = 0
    while token not in TOKENS and i < MAX_TOKEN_LEN:
        token += formula[i]
        i += 1
    return token, formula[i:]

formula_1 = "a"
formula_11 = "(a->a)"
formula_2 = "(a -> a)"
formula_3 = "(a -> (b -> a))"
formula_4 = "(()"

print(take_token(formula_11))
assert(take_token(formula_1) == (formula_1[0], formula_1[1:]))
print(tokenize_formula(formula_1))
assert(tokenize_formula(formula_1) == [formula_1])
print(tokenize_formula(formula_11))
assert(tokenize_formula(formula_11) == ['(', 'a', '->', 'a', ')'])
assert(tokenize_formula(formula_2) == ['(', 'a', '->', 'a', ')'])
print(tokenize_formula(formula_2))
print(tokenize_formula(formula_3))
assert(is_correct_formula_parentetheses(formula_3))
assert(is_correct_formula_parentetheses(formula_2))
assert(is_correct_formula_parentetheses(formula_1))
assert(is_correct_formula_parentetheses(formula_11))
assert(not is_correct_formula_parentetheses(formula_4))
print(extract_formula_vars(formula_3))
print(extract_formula_vars(formula_4))
#test_formula(formula_2)
test_formula(formula_3)
