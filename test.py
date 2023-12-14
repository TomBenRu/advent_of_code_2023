import re

def check_string(s, num1, num2, num3):
    pattern = f'\\.*[#?]{{{num1}}}\\.+[#?]{{{num2}}}\\.+[#?]{{{num3}}}'
    return bool(re.match(pattern, s))

num1 = 4
num2 = 2
num3 = 3
s = '..####..##...###.....'
print(check_string(s, num1, num2, num3))  # Ausgabe: True