# String　Diagram　Of　Optimal　Transports
## Requirements
Version: Python 3.12.3
```sh
pip install -r requirements.txt
```
## How to Solve Benchmarks


```sh
python3 src [DirectoryName] 1
```

Example 
```sh
python3 src BRooms-199-100-30-40 1
```

The result is stored in the ans0.csv file in the specified directory. These values are also printed as the output. 

## How to Run Experiments
### Table 
```sh
python3 src solveForTable
```
Each output is stored in the corresponding benchmark directory. 

### Figure 
For the sequential compositions, 
```sh
python3 src solveExpSeqcomp
```
For the parallel compositions, 
```sh
python3 src solveExpParcomp
```
Each output is stored in the corresponding benchmark directory. 

We can produce the plots by 
```sh
python3 src picturingSeqc
```
and 
```sh
python3 src picturingParc
```

## Benchmarks
### Table
BRoom1 => BRooms-199-100-30-40

BRoom2 => BRoomsP-209-100-100

URoom1 => URooms-399-10-500-4-240-270-3

URoom2 => URooms-599-10-500-4-240-270-3

BChain1 => BChains-210-100

BChain2 => BChains-400-100

UChain1 => UChains-399-10-200

UChain2 => UChains-799-10-200

### Figures 
For the sequential compositions: BChains-k-100, for k = 30, 60, 90, 120, 150, 180, 210.

For the parallel compositions: BRoomsP-k-100-100, for k = 29, 59, 89, 119, 149, 179, 209. 

