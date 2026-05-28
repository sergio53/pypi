"""
&midpoint $1 $2 $3
//$1-result midpoint
//$2-first point 
//$3-second point
= ab $2 $3
@ Ca $2 $3
@ Cb $3 $2
+ p1,p2 Ca Cb
= p1p2 p1 p2
+ $1 ab p1p2
"""

body = E.macros['midpoint'][1:][0].split('\n')[3:]
display(body)
p_codes = {'$2' : ['.', 365.1000061035156, 244.875],
           '$3' : ['.', 515.1000061035156, 236.875]}
p_codes['ab'] = ['=', '$2', '$3']
p_codes['Ca'] = ['@', '$2', '$3']
p_codes['Cb'] = ['@', '$3', '$2']
p_codes['p1,p2'] = ['+', '$2', '$3']
p_codes['p1p2'] = ['=', 'p1', 'p2']
p_codes['mp'] = ['+', 'ab', 'p1p2']
display(p_codes)


macros = {}
macros['midpoint'] = {
  'ab': ['=', '$2', '$3'],
  'Ca': ['@', '$2', '$3'],
  'Cb': ['@', '$3', '$2'],
  'p1,p2': ['+', '$2', '$3'],
  'p1p2': ['=', 'p1', 'p2'],
  'mp': ['+', 'ab', 'p1p2']
}
macros
######################################################
body = E.macros['midpoint'][1:][0]
print(body)
print()
#display(body.split('\n'))

macros = {}
macros['midpoint'] = {}
for line in body.split('\n'):
  if line.startswith('//'):
    continue
  code = line.split()
  print(code)
  macros['midpoint'][code[1]] = [code[0], *code[2:]]

display(macros)
######################################################

self.macros - текстовый код
Исполнение:
self.macros[name] --> convert to pcode
execute pcode