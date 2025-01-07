import time 
import csv
import string_diagrams_of_cost_matrices as cm
import solveOT as sot
import solveLP as slp



#args[1]: 'synthesizeFile'
#args[2]: name of the directory
#args[3]: number of benchmark

def synthesizeFile(args):
    path = f"benchmarks/{args[2]}"
    numBench = int(args[3]) - 1
    filename = f"main{numBench}.csv"
    with open(f"{path}/{filename}") as f:
        reader = csv.reader(f)
        cmats = []
        hierarchicalMap = []
        for row in reader: 
            tmp = []
            hierarchicalDom = 0
            hierarchicalCodom = 0
            for cma in row: 
                cma = cma.replace(' ', '')
                with open(f"benchmarks/{args[2]}/cmat{cma}.csv") as g:
                    reader = csv.reader(g)
                    c = [list(map(int, row)) for row in reader]
                    dom = len(c)
                    codom = len(c[0])
                    hierarchicalDom += dom
                    hierarchicalCodom += codom
                    cmat = cm.CMat(dom, codom, c)
                    tmp.append(cmat)
            cmats.append(tmp)
            hierarchicalMap.append([ [ 0 for j in range(hierarchicalCodom)] for i in range(hierarchicalDom) ])
    
    start_time1 = time.perf_counter()
    cmat = cmats[0][0]
    shortestPathes = [ [ [] for j in range(cmat.codom) ] for i in range(cmat.dom) ]
    for i in range(len(cmats)-1):
        (cmat, shortestPathes) = cm.compWithCache(cmat, cmats[i+1], shortestPathes)

    end_time1 = time.perf_counter()
    
    start_time2 = time.perf_counter()
    (opMap, ansSH) = sot.synthesizeOT(cmat)
    end_time2 = time.perf_counter()
    start_time3 = time.perf_counter()
    dom = cmat.dom
    codom = cmat.codom
    for i in range(dom):
        for j in range(codom):
            shortestRoots = shortestPathes[i][j]
            currentdom = i
            for k in range(len(shortestRoots)):
                hierarchicalMap[k][currentdom][shortestRoots[k]] += opMap[i][j]
                currentdom = shortestRoots[k]
            hierarchicalMap[len(shortestRoots)][currentdom][j] += opMap[i][j]
    end_time3 = time.perf_counter()
    anscheck = cm.multiplication(hierarchicalMap, cmats)
    print(ansSH)
    print(anscheck)
    time1 = end_time1 - start_time1
    time2 = end_time2 - start_time2
    time3 = end_time3 - start_time3
    # print(time1 + time2 + time3)


    # lp = slp.LP([[cmat]])
    # exact_ans = slp.solveLP(lp, exact=True)[0]

    start_time4 = time.perf_counter()
    lp = slp.LP(cmats)
    end_time4 = time.perf_counter()
    ans = slp.solveLP(lp)
    ansCompLP = ans[0]
    time4 = (end_time4 - start_time4) + ans[1]
    # print(time4)

    lp = slp.LP(cmats)
    exact_ans = slp.solveLP(lp, exact=True)[0]
    error1 = abs(ansSH-exact_ans)/exact_ans
    error2 = abs(ansCompLP-exact_ans)/exact_ans
    result = [[time1, time2, time3, time1+time2+time3, error1],
              [time4, error2]
    ]
    print(result)
    path = f"{path}/ans{numBench}.csv"
    with open(path, mode='w') as f:
        writer = csv.writer(f)
        writer.writerows(result)
    



            
#args[1]: 'solveFile'
#args[2]: name of the directory
#args[3]: number of benchmark
def solveFile(args):
    path = f"benchmarks/{args[2]}"
    numBench = int(args[3]) - 1
    filename = f"main{numBench}.csv"
    with open(f"{path}/{filename}") as f:
        reader = csv.reader(f)
        cmats = []
        for row in reader: 
            tmp = []
            for cma in row: 
                cma = cma.replace(' ', '')
                with open(f"benchmarks/{args[2]}/cmat{cma}.csv") as g:
                    reader = csv.reader(g)
                    c = [list(map(int, row)) for row in reader]
                    dom = len(c)
                    codom = len(c[0])
                    cmat = cm.CMat(dom, codom, c)
                    tmp.append(cmat)
            cmats.append(tmp)
    
    start_time1 = time.perf_counter()
    cmat = cmats[0][0]
    # for i in range(len(cmats)-1):
    #     tmp = cmats[i+1][0]
    #     for j in range(len(cmats[i+1])-1):
    #         tmp = cm.parc(tmp, cmats[i+1][j+1])
    #     cmat = cm.seqc(cmat, tmp)
    for i in range(len(cmats)-1):
        cmat = cm.efficientComp(cmat, cmats[i+1])
    end_time1 = time.perf_counter()

    start_time2 = time.perf_counter()
    ansSH = sot.solveOT(cmat)
    end_time2 = time.perf_counter()

    lp = slp.LP([[cmat]])
    exact_ans = slp.solveLP(lp, exact=True)[0]

    start_time3 = time.perf_counter()
    lp = slp.LP([[cmat]])
    end_time3 = time.perf_counter()
    ansMonLP = slp.solveLP(lp)[0]
    time3 = (end_time3 - start_time3) + slp.solveLP(lp)[1]

    # cmats = [ [cmats[i]] for i in range(len(cmats))]
    start_time4 = time.perf_counter()
    lp = slp.LP(cmats)
    end_time4 = time.perf_counter()
    ans = slp.solveLP(lp)
    ansCompLP = ans[0]
    # print(f"test: {ans[1]}")
    time4 = (end_time4 - start_time4) + ans[1]

    result= [[end_time1-start_time1, time3, end_time1-start_time1 + time3, abs(ansMonLP-exact_ans)/exact_ans],
                       [end_time1-start_time1, end_time2-start_time2, end_time1-start_time1 + end_time2-start_time2, abs(ansSH-exact_ans)/exact_ans],
                       [time4, abs(ansCompLP-exact_ans)/exact_ans]
                       ]
    print(f"===Result for {path}===")
    print(f"Computing cost matrices requires: {end_time1 - start_time1}s,\n")
    print(f"Running LP algorithm requires: {time3}s,\n")
    print(f"Total MonLP requires: {end_time1-start_time1 + time3}s,\n")
    print(f"Error of MonLP: {abs(ansMonLP-exact_ans)/exact_ans},\n")
    print(f"Computing cost matrices requires: {end_time1 - start_time1}s,\n")
    print(f"Running Sinkhorn algorithm requires: {end_time2 - start_time2},\n")
    print(f"Total SH requires: {end_time1 - start_time1 + end_time2 - start_time2}s,\n")
    print(f"Error of SH: {abs(ansSH-exact_ans)/exact_ans},\n")
    print(f"Total CompLP requires: {time4},\n")
    print(f"Error of CompLP: {abs(ansCompLP-exact_ans)/exact_ans},\n")
    path = f"{path}/ans{numBench}.csv"
    with open(path, mode='w') as f:
        writer = csv.writer(f)
        writer.writerows(result)

