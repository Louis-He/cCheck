braket = {'if', 'for', 'while', 'do'}
bothBlank1 = {'==', '!=', '+=', '-=', '*=', '/=', '<=', '>='}
bothBlank = {'+', '-', '*', '/', '%', '=', '<', '>'}
noBlank = {'%c', '%s', '%d', '%lf', '%llf', '//', '++', '--', '**', '<s', 'h>', '<m', 'char*', 'int*', 'double*', 'bool*', 'char**', 'int**', 'double**', 'bool**', 'char *', 'int *', 'double *', 'bool *'}
afterBlank = {';', ','}
warningPhrase = {"%c'"}