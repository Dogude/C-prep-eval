# Program uses shunting yard algorithm to interpret C #if expressions
* It holds a Precedence Dictionary
  ```
   precedence = {
    '!': 4 , 'defined': 4 , '!defined': 4, '*': 3, '/': 3, '%': 3, '+': 2, '-': 2, '<<': 1, '>>': 1,
    '<': 0, '>': 0, '<=': 0, '>=': 0, '==': -1, '!=': -1, '&&': -2, '||': -3 , '&': -4 , '|': -5,
    '(': -6 , ')': -6

    }
  ```
# Examples
* Example assumes necessary define replacements has done.
* If still identifier in this expression, it means it has not defined and treated as 0 in eval loop
* so in that example B will be treated as 0
```
expr = "!defined(B) && 123 > 1257"
print(c_eval(expr,1)) ```

<img width="455" height="97" alt="image" src="https://github.com/user-attachments/assets/6c866087-1c7a-477a-a2c8-b69ed8186665" />


```  expr = "!defined(23) && 123678 > 1257 || F + 12"
    print(c_eval(expr,1))
```

<img width="452" height="114" alt="image" src="https://github.com/user-attachments/assets/e721b20b-4c58-4fe8-b8e6-9e1466dc1c39" />


