import time 
import csv
import string_diagrams_of_cost_matrices as cm
import solveOT as sot
import solveLP as slp


            
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

