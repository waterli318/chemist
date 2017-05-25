import re
import sys

""" Entries like 'ml' are copied here to help remove the ending 'x's
    ATTN: 4Baby is a brand name
"""
UNIT = {
    'cm'   : 'cm',
    'cap'  : 'capsule',
    'caps' : 'capsules',
    'ea'   : 'each',
    'g'    : 'gram',
    'hr'   : 'hour',
    'hrs'  : 'hours',
    'in'   : 'inch',
    'l'    : 'litre',
    'liter': 'litre',
    'm'    : 'metre',
    'ml'   : 'ml',
    'mm'   : 'mm',
    'mth'  : 'month',
    'mths' : 'months', 
    'meter': 'metre',
    'pc'   : 'piece',
    'pcs'  : 'pieces',
    'pk'   : 'pack',
    'pks'  : 'packs',
    'yr'   : 'year',
    'yrs'  : 'years'
}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class Tokeniser:
    def __init__(self, title):
        title = title.lower().strip()
        
        # 14,250mg => 14250 mg
        title = re.sub(r'\b(\d+),(\d{3}),(\d{3})', r'\1\2', title)
        title = re.sub(r'\b(\d+),(\d{3})', r'\1\2', title)

        self.str = title
        self.pos = 0

    def read_char(self):
        if self.pos < len(self.str):
            ch = self.str[self.pos]
            self.pos += 1
            return ch
        return None

    def eof(self):
        return self.pos >= len(self.str)

    def read_number(self):
        i = self.pos
        
    def read_word(self):
        i = self.pos
        while not self.eof():
            ch = self.read_char()
            i = i + 1
        
def tokenise(S, reserved={}):
    S = S.lower().strip()

    if len(S) == 0: return []

    # 1,234,567 => 1234567
    S = re.sub(r'\b(\d+),(\d{3}),(\d{3})', r'\1\2\3', S)
    S = re.sub(r'\b(\d+),(\d{3})', r'\1\2', S)

    
    T = []
    def split_alpha_number(w):
        if w in reserved:
            T.append(w)
            return

        i = 0
        while i < len(w):
            #while i < len(w) and w[i].isspace(): i += 1
            j = i
            if w[i].isalpha() or w[i] == '_':
                while i < len(w) and (w[i].isalpha() or w[i] == '_'):
                    i = i + 1
            elif w[i].isdigit():
                while i < len(w) and (w[i].isdigit() or w[i] == '.'):
                    i = i + 1
            else:
                if i > j: T.append(w[j:i])
                i = i + 1
                j = i
            if i > j: T.append(w[j:i])

    for w in re.split(r'\s+', S):
        split_alpha_number(w)

    i = 0
    while i < len(T) - 1:
        w1 = T[i]
        w2 = T[i + 1] 
        if is_number(w1) and w2 in UNIT:
            # l => litre
            T[i + 1] = UNIT[w2]
            i += 2
        else:
            n = len(w1)
            # 5cmx6cm => 5 cm 6 cm
            if is_number(w2) and n > 1 and n < 5 and w1.endswith('x'):
                w = w1[:-1]
                if w in UNIT:
                    T[i] = UNIT[w]
                    i += 1
            i += 1

    return T
    
if __name__ == '__main__':
    print tokenise(sys.argv[1])
