import re

pattern = r'^[a-zA-Z0-9]+$'
pattern = re.compile(pattern)
string = 'fef'
# if pattern.match(string):
#     print('match')
# else:
#     print('no match')

if re.compile(r'^[a-zA-Z0-9]+$').match(string):
    print('match')
else:
    print('no match')
