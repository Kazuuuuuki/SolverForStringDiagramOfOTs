from pulp import *
import time 

# LP for n-sequentially composed OT
# cmats: Array [CMat], representing the sequentially composed structure. 
class SeqLP:
    def __init__(self, cmats):
        # create the LP problem
        prob = LpProblem("The OT Problem", LpMinimize)
        
        # create variables
        variables = []
        for i in range(len(cmats)):
            variables.append(self.create_variables(i, cmats[i].dom, cmats[i].codom))

        # create objective
        prob += self.objective(cmats, variables)

        # create constraint for \vect{a}
        val = 1.0/cmats[0].dom
        for i in range(cmats[0].dom):
            prob += self.leftmost_const(cmats[0].codom, variables[0], i, val)
        
        # create constraint for \vect{b}
        val = 1.0/cmats[len(cmats)-1].codom
        for i in range(cmats[len(cmats)-1].codom):
            prob += self.rightmost_const(cmats[len(cmats)-1].dom, variables[len(cmats)-1], i, val)

        # create constraint for connections
        for i in range(len(cmats)-1):
            for j in range(cmats[i].codom):
                prob+= self.connection_const(i, j, cmats[i].dom, variables[i], cmats[i+1].codom, variables[i+1])

        prob.writeLP("SeqCompOT.lp")

        # The problem is solved using PuLP's choice of Solver
        self.prob = prob




        
    def create_variables(self, k, dom, codom):
        return [
            [
                LpVariable(f"Pvar{k}|{i}|{j}", 0, None, LpContinuous)
                for j in range(codom)
            ]
            for i in range(dom)
        ]

    def objective(self, cmats, variables):
        length = len(cmats)
        return (
            lpSum([ cmats[i].body[j][k] * variables[i][j][k] for i in range(length) for j in range(cmats[i].dom) for k in range(cmats[i].codom)]),
            "the objective")

    # def non_negative_const(self, variable, i, j, k):
    #     return (
    #         lpSum([variable[i][j][k]]) >= 0,
    #         f"Non-negativeConst{i}{j}{k}")

    def leftmost_const(self, codom, variable, index, val):
        return (
            lpSum([ variable[index][i] for i in range(codom) ]) == val,
            f"a-Const{index}")
    
    def rightmost_const(self, dom, variable, index, val):
        return (
            lpSum([ variable[i][index] for i in range(dom) ]) == val,
            f"b-Const{index}")
    
    def connection_const(self, i, j, dom, variable1, codom, variable2):
        return (
            lpSum([ variable1[k][j] for k in range(dom) ]) == lpSum([ variable2[j][k] for k in range(codom) ]),
            f"c-Const{i}|{j}"
        )


# LP for canonical string diagrams of OTs
# cmats: Array [ Array [CMat] ], representing the canonical structure. The outer list represents the sequential composition, and the inner list represents the parallel composition. 
class LP:
    def __init__(self, cmats):
        # create the LP problem
        prob = LpProblem("The OT Problem", LpMinimize)
        
        # create variables
        variables = []
        for i in range(len(cmats)):
            level = []
            for j in range(len(cmats[i])):
                level.append(self.create_variables(i, j, cmats[i][j].dom, cmats[i][j].codom))
            variables.append(level)

        # create objective
        prob += self.objective(cmats, variables)

        # create constraint for \vect{a}
        val = 1.0/cmats[0][0].dom
        for i in range(cmats[0][0].dom):
            prob += self.leftmost_const(cmats[0][0].codom, variables[0][0], i, val)
        
        # create constraint for \vect{b}
        size = 0
        for i in range(len(cmats[len(cmats)-1])):
            size += cmats[len(cmats)-1][i].codom
        val = 1.0/size
        for i in range(size):
            prob += self.rightmost_const(cmats[len(cmats)-1], variables[len(cmats)-1], i, val)

        # create constraint for connections
        for i in range(len(cmats)-1):
            size = 0
            for j in range(len(cmats[i])):
                size += cmats[i][j].codom
            for k in range(size):
                prob+= self.connection_const(i, k, cmats[i], variables[i], cmats[i+1], variables[i+1])

        prob.writeLP("CanonicalSD-OT.lp")

        # The problem is solved using PuLP's choice of Solver
        self.prob = prob
        #only works for monolithic LP
        self.variables = [ [ variables[0][0][i][j] for j in range(cmats[0][0].codom)] for i in range(cmats[0][0].dom)]




        
    def create_variables(self, i, j, dom, codom):
        return [
            [
                LpVariable(f"Pvar{i}|{j}|{k}|{l}", 0, None, LpContinuous)
                for l in range(codom)
            ]
            for k in range(dom)
        ]

    def objective(self, cmats, variables):
        length = len(cmats)
        return (
            lpSum([ cmats[i][j].body[k][l] * variables[i][j][k][l] for i in range(length) for j in range(len(cmats[i])) for k in range(cmats[i][j].dom) for l in range(cmats[i][j].codom)]),
            "the objective")

    def leftmost_const(self, codom, variable, index, val):
        return (
            lpSum([ variable[index][i] for i in range(codom) ]) == val,
            f"a-Const{index}")
    
    def rightmost_const(self, cmats, variable, index, val):
        o_index = index
        for i in range(len(cmats)):
            if cmats[i].codom <= index: 
                index -= cmats[i].codom
            else: 
                return (
                    lpSum([ variable[i][j][index] for j in range(cmats[i].dom) ]) == val,
                    f"b-Const{o_index}"
                    )

    
    def connection_const(self, i, index, cmats1, variable1, cmats2, variable2):
        tmp = 0 
        index1 = index
        for j in range(len(cmats1)):
            if  cmats1[j].codom <= index1:
                index1 -= cmats1[j].codom
            else: 
                num1 = j
                break
        index2 = index
        for j in range(len(cmats2)):
            if cmats2[j].dom <= index2:
                index2 -= cmats2[j].dom
            else: 
                num2 = j
                break
        # print(f"num1:{num1}, num2:{num2}, index1: {index1}, index2: {index2}")
        return (
            lpSum([ variable1[num1][k][index1] for k in range(cmats1[num1].dom) ]) == lpSum([ variable2[num2][index2][k] for k in range(cmats2[num2].codom) ]),
            f"c-Const{i}|{index}"
        )
    

# solving LP 
# output = [value, solutionTime]
def solveLP(lp, exact=False):
    # solver_list = listSolvers()
    # print(solver_list)
    # ['GLPK_CMD', 'PYGLPK', 'CPLEX_CMD', 'CPLEX_PY', 'GUROBI', 'GUROBI_CMD', 'MOSEK', 'XPRESS', 'XPRESS', 'XPRESS_PY', 'PULP_CBC_CMD', 'COIN_CMD', 'COINMP_DLL', 'CHOCO_CMD', 'MIPCL_CMD', 'SCIP_CMD', 'FSCIP_CMD', 'SCIP_PY', 'HiGHS', 'HiGHS_CMD', 'COPT', 'COPT_DLL', 'COPT_CMD']
    # lp.prob.solve(PULP_CBC_CMD(timeLimit=20))
    # lp.prob.solve(PULP_CBC_CMD())
    # time_start = time.perf_counter()
    exTime = 0
    if (exact):
        time_start = time.perf_counter()
        lp.prob.solve(GLPK(options=['--exact'],msg=False))
        time_stop = time.perf_counter()
        exTime = time_stop - time_start
    else: 
        lp.prob.solve(PULP_CBC_CMD(msg=False, logPath="stats.log"))
    # time_stop = time.perf_counter()
        path = "stats.log"
        with open(path) as f:
            data = f.read().splitlines()
            data = data[-2].split()
            exTime = data[4]
    # The status of the solution is printed to the screen
    # print("Status:", LpStatus[lp.prob.status])

    # # Each of the variables is printed with it's resolved optimum value
    # for v in lp.prob.variables():
    #     print(v.name, "=", v.varValue)

    # # The optimised objective function value is printed to the screen
    # print("Total Cost:", value(lp.prob.objective))
    return [value(lp.prob.objective), float(exTime)]

# synthesizing LP 
# output = [value, solutionTime, opMat]
def synthesizeLP(lp, dom, codom):
    lp.prob.solve(PULP_CBC_CMD(msg=False, logPath="stats.log"))
    # time_stop = time.perf_counter()
    path = "stats.log"
    with open(path) as f:
        data = f.read().splitlines()
        data = data[-2].split()
        exTime = data[4]
    opMap = [[value(lp.variables[i][j]) for j in range(codom)] for i in range(dom)]
    return [value(lp.prob.objective), float(exTime), opMap]
