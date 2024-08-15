import random
import csv


# args[1]: 'createBChains'
# args[2]: number of benchmarks
# args[3]: number of sequential compositions
# args[4]: domain and codomain size
def createBChains(args):
    for i in range(int(args[2])):
            for j in range(int(args[3])):
                filename =  f"cmat{i}|{j}"
                path = f"benchmarks/BChains-{args[3]}-{args[4]}/{filename}.csv"
                with open(path, mode='w') as f:
                    dom = int(args[4])
                    codom = int(args[4])
                    l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    writer = csv.writer(f)
                    writer.writerows(l)


# args[1]: 'createBChains'
# args[2]: number of benchmarks
# args[3]: number of sequential compositions
# args[4]: domain and codomain size
def fileBChains(args):
     for i in range(int(args[2])):
            with open(f"benchmarks/BChains-{args[3]}-{args[4]}/main{i}.csv", mode='w') as f:
                output = []
                for j in range(int(args[3])):
                    filename =  f"{i}|{j}"
                    output.append([filename])
                writer = csv.writer(f)
                writer.writerows(output)
                    
     

# args[1]: 'createUChains'
# args[2]: number of benchmarks
# args[3]: number of sequential compositions
# args[4]: even domain size
# args[5]: odd domain size
def createUChains(args):
    for i in range(int(args[2])):
        for j in range(int(args[3])):
            filename =  f"cmat{i}|{j}"
            path = f"benchmarks/UChains-{args[3]}-{args[4]}-{args[5]}/{filename}.csv"
            with open(path, mode='w') as f:
                if j % 2 == 0:
                    dom = int(args[4])
                    codom = int(args[5])
                    l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                else:
                    dom = int(args[5])
                    codom = int(args[4])
                    l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                writer = csv.writer(f)
                writer.writerows(l)

# args[1]: 'fileUChains'
# args[2]: number of benchmarks
# args[3]: number of sequential compositions
# args[4]: even domain size
# args[5]: odd domain size
def fileUChains(args):
     for i in range(int(args[2])):
            with open(f"benchmarks/UChains-{args[3]}-{args[4]}-{args[5]}/main{i}.csv", mode='w') as f:
                output = []
                for j in range(int(args[3])):
                    filename =  f"{i}|{j}"
                    output.append([filename])
                writer = csv.writer(f)
                writer.writerows(output)


# args[1]: 'createBRooms'
# args[2]: number of benchmarks
# args[3]: (number of cost matrices) - 1: the first one is leftmost, and later we have two component for each layer. 
# args[4]: the size of entire domain and codomain for internal components
# args[5]: the size of domain and codomain for the upper components in even layers. 
# args[6]: the size of domain and codomain for the upper components in odd layers. 
def createBRooms(args):
    for i in range(int(args[2])):
            for j in range(int(args[3])):
                filename =  f"cmat{i}|{j}"
                path = f"benchmarks/BRooms-{args[3]}-{args[4]}-{args[5]}-{args[6]}/{filename}.csv"
                with open(path, mode='w') as f:
                    if j == 0:
                        dom = int(args[4])
                        codom = int(args[4])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    elif j % 4 == 1: 
                        dom =  int(args[6])
                        codom = int(args[6])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    elif j % 4 == 2: 
                        dom = int(args[4]) - int(args[6])
                        codom = int(args[4]) - int(args[6])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    elif j % 4 == 3: 
                        dom =  int(args[5])
                        codom = int(args[5])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    else: 
                        dom = int(args[4]) - int(args[5])
                        codom = int(args[4]) - int(args[5])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    writer = csv.writer(f)
                    writer.writerows(l)
            filename =  f"cmat{i}|{int(args[3])}"
            path = f"benchmarks/BRooms-{args[3]}-{args[4]}-{args[5]}-{args[6]}/{filename}.csv"
            with open(path, mode='w') as f:
                    dom = int(args[4])
                    codom = int(args[4])
                    l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    writer = csv.writer(f)
                    writer.writerows(l)


# args[1]: 'fileBRooms'
# args[2]: number of benchmarks
# args[3]: (number of cost matrices) - 1: the first one is leftmost, and later we have two component for each layer. 
# args[4]: the size of entire domain and codomain for internal components
# args[5]: the size of domain and codomain for the upper components in even layers. 
# args[6]: the size of domain and codomain for the upper components in odd layers. 
def fileBRooms(args):
     for i in range(int(args[2])):
            with open(f"benchmarks/BRooms-{args[3]}-{args[4]}-{args[5]}-{args[6]}/main{i}.csv", mode='w') as f:
                output = []
                j = 0 
                while (j < int(args[3])): 
                    if j == 0: 
                        filename =  f"{i}|{j}"
                        output.append([filename])
                        j += 1
                    else: 
                        filename1 = f"{i}|{j}"
                        filename2 = f"{i}|{j+1}"
                        output.append([filename1, filename2])
                        j += 2
                    
                filename = f"{i}|{int(args[3])}"
                output.append([filename])
                writer = csv.writer(f)
                writer.writerows(output)

# args[1]: 'createURooms'
# args[2]: number of benchmarks
# args[3]: (number of cost matrices)-1: the first one is leftmost, and later we have two component for each layer
# args[4]: the size of entire domain for components in even layers
# args[5]: the size of entire domain for components in odd layers
# args[6]: the size of domain for the upper components in even layers. 
# args[7]: the size of codomain for the upper components in even layers. 
# args[8]: the size of domain for the upper components in odd layers. 
# args[9]: the size of codomain for the upper components in odd layers. 
def createURooms(args):
    for i in range(int(args[2])):
            for j in range(int(args[3])):
                filename =  f"cmat{i}|{j}"
                path = f"benchmarks/URooms-{args[3]}-{args[4]}-{args[5]}-{args[6]}-{args[7]}-{args[8]}-{args[9]}/{filename}.csv"
                with open(path, mode='w') as f:
                    if j == 0:
                        dom = int(args[4])
                        codom = int(args[5])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    elif j % 4 == 1: 
                        dom =  int(args[8])
                        codom = int(args[9])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    elif j % 4 == 2: 
                        dom = int(args[5]) - int(args[8])
                        codom = int(args[4]) - int(args[9])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    elif j % 4 == 3: 
                        dom =  int(args[6])
                        codom = int(args[7])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    else: 
                        dom = int(args[4]) - int(args[6])
                        codom = int(args[5]) - int(args[7])
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    writer = csv.writer(f)
                    writer.writerows(l)
            filename =  f"cmat{i}|{int(args[3])}"
            path = f"benchmarks/URooms-{args[3]}-{args[4]}-{args[5]}-{args[6]}-{args[7]}-{args[8]}-{args[9]}/{filename}.csv"
            with open(path, mode='w') as f:
                    if (int(args[3]) % 4 == 1):
                        dom = int(args[5])
                        codom = int(args[5])
                    if (int(args[3]) % 4 == 3):
                        dom = int(args[4])
                        codom = int(args[4])
                    l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    writer = csv.writer(f)
                    writer.writerows(l)

# args[1]: 'fileURooms'
# args[2]: number of benchmarks
# args[3]: (number of cost matrices)-1: the first one is leftmost, and later we have two component for each layer
# args[4]: the size of entire domain for components in even layers
# args[5]: the size of entire domain for components in odd layers
# args[6]: the size of domain for the upper components in even layers. 
# args[7]: the size of codomain for the upper components in even layers. 
# args[8]: the size of domain for the upper components in odd layers. 
# args[9]: the size of codomain for the upper components in odd layers.
def fileURooms(args):
     for i in range(int(args[2])):
            with open(f"benchmarks/URooms-{args[3]}-{args[4]}-{args[5]}-{args[6]}-{args[7]}-{args[8]}-{args[9]}/main{i}.csv", mode='w') as f:
                output = []
                j = 0 
                while (j < int(args[3])): 
                    if j == 0: 
                        filename =  f"{i}|{j}"
                        output.append([filename])
                        j += 1
                    else: 
                        filename1 = f"{i}|{j}"
                        filename2 = f"{i}|{j+1}"
                        output.append([filename1, filename2])
                        j += 2
                filename = f"{i}|{int(args[3])}"
                output.append([filename])
                writer = csv.writer(f)
                writer.writerows(output)



# args[1]: 'createBRoomsP'
# args[2]: number of benchmarks
# args[3]: (number of cost matrices)-1: the first one is leftmost, and later we have two component for each layer
# args[4]: the size of domain for internal components
# args[5]: the size of codomain for internal components
def createBRoomsP(args):
    for i in range(int(args[2])):
            for j in range(int(args[3])):
                filename =  f"cmat{i}|{j}"
                path = f"benchmarks/BRoomsP-{args[3]}-{args[4]}-{args[5]}/{filename}.csv"
                with open(path, mode='w') as f:
                    if j == 0:
                        dom = int(args[4])
                        codom = int(args[4])*(int(args[3])-1)
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    else: 
                        dom = int(args[4])
                        codom = int(args[5]) 
                        l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    writer = csv.writer(f)
                    writer.writerows(l)
            filename =  f"cmat{i}|{int(args[3])}"
            path = f"benchmarks/BRoomsP-{args[3]}-{args[4]}-{args[5]}/{filename}.csv"
            with open(path, mode='w') as f:
                    dom = int(args[5]) * (int(args[3])-1)
                    codom = int(args[5])
                    l = [ [ random.randint(0,1000000) for j in range(codom)]  for i in range(dom) ]
                    writer = csv.writer(f)
                    writer.writerows(l)

# args[1]: 'fileBRoomsP'
# args[2]: number of benchmarks
# args[3]: (number of cost matrices)-1: the first one is leftmost, and later we have two component for each layer
# args[4]: the size of domain for internal components
# args[5]: the size of codomain for internal components
def fileBRoomsP(args):
     for i in range(int(args[2])):
            with open(f"benchmarks/BRoomsP-{args[3]}-{args[4]}-{args[5]}/main{i}.csv", mode='w') as f:
                output = []
                output2 = []
                for j in range(int(args[3])):
                    if j == 0: 
                        filename =  f"{i}|{j}"
                        output.append([filename])
                    else: 
                        output2.append(f"{i}|{j}")
                output.append(output2)
                filename = f"{i}|{int(args[3])}"
                output.append([filename])
                writer = csv.writer(f)
                writer.writerows(output)






