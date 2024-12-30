import sys
import csv
import matplotlib.pyplot as plt
import createBenchmarks as cb 
import solveBenchmarks as sb

def picturingExSeq():
    x = []
    ymonlp = []
    ysh    = []
    ycomplp = []
    for i in range(7):
        path = f'benchmarks/BChains-{(i+1)*30}-100/ans0.csv'
        with open(path) as f:
            reader = csv.reader(f)
            reader = [list(map(float, row)) for row in reader]
            x.append((i+1)*30)
            ymonlp.append(reader[0][2])
            ysh.append(reader[1][2])
            ycomplp.append(reader[2][0])
    psh = plt.plot(x, ysh, color='blue', marker="o", linestyle="dashed")
    pmonlp = plt.plot(x, ymonlp, color='red', marker="o", linestyle="dashdot")
    pcomplp = plt.plot(x, ycomplp, color='green', marker="o")

    plt.xlabel('# of sequential compositions')
    plt.ylabel('execution time [s]')
    # plt.show()  
    plt.legend((pmonlp[0], psh[0], pcomplp[0]), ("MonLP (proposed)", "SH (proposed)", "CompLP"), loc=2)
    plt.savefig('exseq.png')

def picturingExPar():
    x = []
    ymonlp = []
    ysh    = []
    ycomplp = []
    for i in range(7):
        path = f'benchmarks/BRoomsP-{(i+1)*30-1}-100-100/ans0.csv'
        with open(path) as f:
            reader = csv.reader(f)
            reader = [list(map(float, row)) for row in reader]
            x.append((i+1)*30-2)
            ymonlp.append(reader[0][2])
            ysh.append(reader[1][2])
            ycomplp.append(reader[2][0])
    psh = plt.plot(x, ysh, color='blue', marker="o", linestyle="dashed")
    pmonlp = plt.plot(x, ymonlp, color='red', marker="o", linestyle="dashdot")
    pcomplp = plt.plot(x, ycomplp, color='green', marker="o")

    plt.xlabel('# of parallel compositions')
    plt.ylabel('execution time [s]')
    # plt.show()  
    plt.legend((pmonlp[0], psh[0], pcomplp[0]), ("MonLP (proposed)", "SH (proposed)", "CompLP"), loc=2)
    plt.savefig('expar.png')
    



def run(args):
    if (args[1] == 'picturingSeqc'):
        picturingExSeq()
    if (args[1] == 'picturingParc'):
        picturingExPar()
    if (args[1] == 'createBChains'):
        cb.createBChains(args)
    if (args[1] == 'fileBChains'):
        cb.fileBChains(args)
    if (args[1] == 'createUChains'):
        cb.createUChains(args)
    if (args[1] == 'fileUChains'):
        cb.fileUChains(args)
    if (args[1] == 'createBRooms'):
        cb.createBRooms(args)
    if (args[1] == 'fileBRooms'):
        cb.fileBRooms(args)
    if (args[1] == 'createBRoomsP'):
        cb.createBRoomsP(args)
    if (args[1] == 'fileBRoomsP'):
        cb.fileBRoomsP(args)
    if (args[1] == 'createURooms'):
        cb.createURooms(args)
    if (args[1] == 'fileURooms'):
        cb.fileURooms(args)
    if (args[1] == 'synthesizeFile'):
        sb.synthesizeFile(args)
    if (args[1] == 'solveFile'):
        sb.solveFile(args)
    if (args[1] == 'solveExpSeqcomp'):
        for i in range(7):
            numOfSeqcomp = (i+1)*30
            s = f'BChains-{numOfSeqcomp}-100'
            sb.solveFile([0, 'solveFile', s, 1])
    if (args[1] == 'solveExpParcomp'):
        for i in range(7):
            numOfParcomp = (i+1)*30-1
            s = f'BRoomsP-{numOfParcomp}-100-100'
            sb.solveFile([0, 'solveFile', s, 1])
    if (args[1] == 'solveForTable'):
        i = 1
        while(i <= 1):
        # BRoom1 == BRooms-199-100-30-40
            s = 'BRooms-199-100-30-40'
            sb.solveFile([0, 'solveFile', s, i])
        # BRoom2 == BRoomsP-209-100-100
            s = 'BRoomsP-209-100-100'
            sb.solveFile([0, 'solveFile', s, i])
        # URoom1 == URooms-399-10-500-4-240-270-3
            s = 'URooms-399-10-500-4-240-270-3'
            sb.solveFile([0, 'solveFile', s, i])
        # URoom2 == URooms-599-10-500-4-240-270-3
            s = 'URooms-599-10-500-4-240-270-3'
            sb.solveFile([0, 'solveFile', s, i])
        # BChain1 == BChains-210-100
            s = 'BChains-210-100'
            sb.solveFile([0, 'solveFile', s, i])
        # BChain2 == BChains-400-100
            s = 'BChains-400-100'
            sb.solveFile([0, 'solveFile', s, i])
        # UChain1 == UChains-399-10-200
            s = 'UChains-399-10-200'
            sb.solveFile([0, 'solveFile', s, i])
        # UChain2 == UChains-799-10-200
            s = 'UChains-799-10-200'
            sb.solveFile([0, 'solveFile', s, i])
            i += 1
    

    
    
if __name__ == '__main__':
    args = sys.argv
    run(args)
    print('finish')