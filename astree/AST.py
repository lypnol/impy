#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from astree.StatementSequence import StatementSequence


# AST represents a program's abstract syntax tree
class AST(StatementSequence):

    @staticmethod
    def preprocess(source):
        # Add endline after ';'
        source = source.replace(';', ';\n')
        # Replace tabs with spaces
        source = source.replace('\t', ' ')
        # Replace 'if(' by 'if ('
        source = source.replace('if(', 'if (')
        # Replace 'while(' by 'while '
        source = source.replace('while(', 'while (')
        # Add endline before and after '{' '}'
        source = source.replace('{', ' { ')
        source = source.replace('}', ' } ')
        source = re.sub(r'\s+\{\s+', '\n{\n', source)
        source = re.sub(r'\s+\}\s+', '\n}\n', source)
        # Remove extra endlines
        source = re.sub(r'\n+', '\n', source)
        # Remove extra whitespace
        source = re.sub(r' +', ' ', source)
        # Remove all whitespace at begining of line
        source = re.sub(r'\n\s+', '\n', source)
        # Remove all whitespace before endline
        source = re.sub(r'\s+\n', '\n', source)
        # Look for if and while to group their conditions in one line
        lines = source.split('\n')
        result = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
            elif line.startswith('if ') or line.startswith('while '):
                j = i+1
                while lines[j] != '{':
                    j += 1
                result.append(' '.join([line.strip() for line in lines[i:j]]))
                result.append('{')
                i = j+1
            else:
                result.append(line)
                i += 1
        
        return '\n'.join(result)

if __name__ == "__main__":
    source = """
0 : X := 2;
1 : if (X <= 0) {
    2 : X := -X;
} else {
    3 : X := 1 - X;
}
4 : if (X == 1) {
    5 : X := 1;
    6 : X := X + 1;
}
7 : Y := 5;
8 : while Y + X >= X    
{
    9 : Y := X - Y;
    10 : X := Y + X;
    11 : if ((X < 2) && (1 >= 0)) || true {
        12 : var := 4*3;
    }
}
"""
    print(AST.parse(AST.preprocess(source)))
