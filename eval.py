def c_eval(expression,line_number):

    line_number = line_number + 1  # Adjust line number for user-friendly reporting

    # expression is a string
    # this function returns True or False based on the evaluation of the expression


    # lexical analysis - tokenize the expression
    invalid_operators = ('++','{', '}' , '$' , '@' ,'--', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '>>=', '<<=')

    for op in invalid_operators:
        if op in expression:
            return "Error : Invalid operator in expression - " + op

    stringList = re.findall(r'(!defined)\((\w+)\)\s*|(defined)\((\w+)\)\s*|(!defined)\s+(\w+)\s*|(\w+)|(&&|\|\||==|!=|\(|\)|\
                            &|\||!|<<|>>|<|>|>=|<=|\+|-|/|%|\*|)\s*', expression)

    # convert list of tuples to list of strings
    tokens = []

    for tup in stringList:
        for item in tup:
            if item != '':
                tokens.append(item)

    # syntax checking & parsing
    for i in range(len(tokens)):
        # check defined and !defined syntax
        if tokens[i] in ('defined','!defined'):
            if tokens[i+1].isidentifier() == False and tokens[i+1].isnumeric() == False:
                print("Error : Invalid expression syntax after defined or !defined, at line " + str(line_number))
                sys.exit(1)
        # check counts of opening and closing parentheses
        open_parens = tokens.count('(')
        close_parens = tokens.count(')')
        if open_parens != close_parens:
            print("Error : Mismatched parentheses in expression, at line " + str(line_number))
            sys.exit(1)
        # There must be a identifier or number before and after binary operators
        if tokens[i] in ('==', '!=', '<', '>', '<=', '>=', '+' , '*', '&' , '&&' , '||' , '|', '/', '%', '<<', '>>'):
            if i == 0 or i == len(tokens) - 1:
                print("Error : Invalid expression syntax - operator at start or end, at line " + str(line_number))
                sys.exit(1)
            if not (tokens[i-1].isidentifier() or tokens[i-1].isnumeric() or tokens[i-1] in ('(', ')','-', 'defined', '!defined', '!')):
                print("Error : Invalid expression syntax - operator before, at line " + str(line_number))
                sys.exit(1)
            if not (tokens[i+1].isidentifier() or tokens[i+1].isnumeric() or tokens[i+1] in ('(', ')', 'defined', '!defined', '-','!')):
                print("Error : Invalid expression syntax - operator after, at line " + str(line_number))
                sys.exit(1)
        if tokens[i] == '!':
            if i == len(tokens) - 1:
                print("Error : Invalid expression syntax - ! operator at end, at line " + str(line_number))
                sys.exit(1)
            if not (tokens[i+1].isidentifier() or tokens[i+1].isnumeric() or tokens[i+1] in ('(', 'defined', '!defined')):
                print("Error : Invalid expression syntax - ! operator before, at line " + str(line_number))
                sys.exit(1)
        if tokens[i] == '-':
            if i < len(tokens) - 1:
                if not (tokens[i+1].isidentifier() or tokens[i+1].isnumeric() or tokens[i+1] in ('(', 'defined', '!defined')):
                    print("Error : Invalid expression syntax - - operator before, at line " + str(line_number))
                    sys.exit(1)

        if tokens[i] not in ('defined','!defined'):
            if (tokens[i].isidentifier() or tokens[i].isnumeric()) and i < len(tokens) - 1:
                if(tokens[i+1].isidentifier() or tokens[i+1].isnumeric()) :
                    print("Error : Invalid expression syntax - missing operator between identifiers or numbers, at line " + str(line_number))
                    sys.exit(1)

    #Precedence dictionary
    precedence = {
    '!': 4 , 'defined': 4 , '!defined': 4, '*': 3, '/': 3, '%': 3, '+': 2, '-': 2, '<<': 1, '>>': 1,
    '<': 0, '>': 0, '<=': 0, '>=': 0, '==': -1, '!=': -1, '&&': -2, '||': -3 , '&': -4 , '|': -5,
    '(': -6 , ')': -6

    }

    output = []
    stack = []

    #build postfix expression
    for token in tokens:
        if (token.isidentifier() or token.isnumeric()) and token not in ('defined','!defined'):
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Pop the '(' from the stack
        elif token in precedence:
            while (stack and stack[-1] != '(' and
                   precedence[stack[-1]] >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())

    # evaluate postfix expression
    eval_stack = []
    for token in output:
        #Add guard for defined identifiers as 0
        if token.isnumeric():
            # handle zero
            if token == '0':
                eval_stack.append(None)
            else:
                eval_stack.append(int(token))
        elif token.isidentifier() and token not in ('defined','!defined'):
            eval_stack.append(0)  # Undefined identifiers are treated as 0
        elif token == '+':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(a + b)
        elif token == '-':
            #push only negative of the number
            a = eval_stack.pop()
            if a is None:
                a = 0
            eval_stack.append(-a)
        elif token == '*':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(a * b)
        elif token == '/':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(a // b)
        elif token == '%':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(a % b)
        elif token == '<<':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(a << b)
        elif token == '>>':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(a >> b)
        elif token == '<':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(int(a < b))
        elif  token == '==':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(int(a == b))
        elif token == '!=':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(int(a != b))
        elif token == '!defined':
            a = eval_stack.pop()
            if a is None:
                eval_stack.append(0)
            else:
                eval_stack.append(int(a == 0))
        elif token == 'defined':
            a = eval_stack.pop()
            if a is None:
                eval_stack.append(1)
            else:
              eval_stack.append(int(a != 0))
        elif token == '>':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(int(a > b))
        elif token == '<=':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(int(a <= b))
        elif token == '>=':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(int(a >= b))
        elif token == '&&':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(int(a and b))
        elif token == '||':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(int(a or b))
        elif token == '&':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(a & b)
        elif token == '|':
            b = eval_stack.pop()
            a = eval_stack.pop()
            if a is None:
                a = 0
            if b is None:
                b = 0
            eval_stack.append(a | b)
        elif token == '!':
            a = eval_stack.pop()
            if a is None:
                a = 1
            eval_stack.append(int(not a))

    result = eval_stack.pop()
    output = True if result is None else result

    #handle 0 case, octal, binary, hexadecimal numbers
    return bool(output)
