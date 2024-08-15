class CMat: 
    # dom: Integer 
    # codom: Integer 
    # body: Array [dom, codom]
    # 'inf' denotes the infinity
    def __init__(self, dom, codom, body): 
        self.dom    = dom
        self.codom  = codom
        self.body   = body

    def fromBodyToString(self):
        return str(self.body)
    

def id(dom): 
    return CMat(dom, dom, [ [ 0 if i == j else 'inf' for j in range(0,dom)] for i in range(0,dom)  ])

def seqc(cmat1, cmat2):
    dom1 = cmat1.dom
    codom2 = cmat2.codom
    intdom = cmat1.codom
    mb1 = cmat1.body
    mb2 = cmat2.body
    b   = []
    for i in range(0, dom1):
        tmp = []
        for j in range(0, codom2):
            v = 'inf'
            for k in range(0, intdom):
                v1 = cmat1.body[i][k]
                v2 = cmat2.body[k][j]
                if (v1 != 'inf' and  v2 != 'inf'):
                    if (v == 'inf'):
                        v = v1 + v2
                    else:
                        v = min(v, v1 + v2)
            tmp.append(v)
        b.append(tmp)
    return CMat(dom1, codom2, b)

def parc(cmat1, cmat2):
    dom1 = cmat1.dom
    dom2 = cmat2.dom
    codom1 = cmat1.codom
    codom2 = cmat2.codom
    mb1 = cmat1.body
    mb2 = cmat2.body
    b   = []
    for i in range(0, dom1+dom2):
        tmp = []
        for j in range(0, codom1+codom2):
            if (i < dom1 and j < codom1):
                v = mb1[i][j]
            elif (i >= dom1 and j >= codom1):
                v = mb2[i-dom1][j-codom1]
            else:
                v = 'inf'
            tmp.append(v)
        b.append(tmp)
    return CMat(dom1+dom2, codom1+codom2, b)


# compositon of A;(B_1+B_2+...+B_n)
def efficientComp(cmat, cmats):
    dom1 = cmat.dom 
    codom = 0
    indexdom = []
    tmpdom = 0
    # indexcod = []
    # tmpcod = 0
    for i in range(len(cmats)):
        codom += cmats[i].codom
        indexdom.append(tmpdom)
        tmpdom += cmats[i].dom
        # tmpcod += (cmats[i].cod-1)
        # indexcod.append(tmpcod)
    body = []
    for i in range(0, dom1):
        body2 = []
        indexc = 0
        indexj = 0
        for j in range(0, codom):
            if (indexj == cmats[indexc].codom):
                indexc += 1
                indexj = 0
            indexk = indexdom[indexc]
            ans = cmat.body[i][indexk] + cmats[indexc].body[0][indexj]
            for k in range(1, cmats[indexc].dom):
                ans = min(ans, cmat.body[i][indexk+k] + cmats[indexc].body[0+k][indexj])
            body2.append(ans)
            indexj += 1
        body.append(body2)
    return CMat(dom1, codom, body)

                    

def getIndex(array, index):
    for i in range(len(array)):
        if (array[i] < index) :
            return i-1
    return len(array) - 1 
