from parsy import digit, generate, match_item, regex, string, success, test_item
from .string_diagrams_of_cost_matrices import id, seqc, parc

lparen = match_item("(") 
rparen = match_item(")")

def parse(path):
    with open('{0}'.format(path)) as f:
        lines = f.readlines()
        return eval_tokens(lexer(lines[0]))

def lexer(code):
    whitespace = regex(r"\s*")
    termVar  = regex(r"C[0-9]+")
    tseqc = string(";")
    tparc = string("+")
    termId   = regex(r"id")
    parser = whitespace >> ((termVar | tseqc | tparc | termId | lparen | rparen) << whitespace).many()
    return parser.parse(code)

def eval_tokens(tokens):
    @generate 
    def termParc():
        res = yield termSeqc
        op  = match_item('+')
        while True: 
            operation = yield op | success("")
            if not operation:
                break
            operand = yield termSeqc
            res = parc(res, operand)
        return res
    
    @generate
    def termSeqc():
        res = yield simple
        op = match_item(';')
        while True:
            operation = yield op | success("")
            if not operation:
                break
            operand = yield simple
            res = seqc(res, operand)
        return res
    
    @generate 
    def termId():
        d = yield match_item('id')
        return id(1) 
    
    @generate 
    def termVar():
        d = yield test_item(lambda x: x[0] == 'C', "variable")
        return openOT(int(d[1:]))


    expr = termParc
    simple = termId | termVar | (lparen >> expr << rparen)
    return expr.parse(tokens)