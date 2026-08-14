* Program uses shunting yard algorithm to interpret C prep expressions
* It holds a Precedence Dictionary
  
   precedence = {
    '!': 4 , 'defined': 4 , '!defined': 4, '*': 3, '/': 3, '%': 3, '+': 2, '-': 2, '<<': 1, '>>': 1,
    '<': 0, '>': 0, '<=': 0, '>=': 0, '==': -1, '!=': -1, '&&': -2, '||': -3 , '&': -4 , '|': -5,
    '(': -6 , ')': -6

    }
  
* !defined(A) && defined(B) && C == D
* A && B
