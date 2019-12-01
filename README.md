# Supply Chain Management
A compilation of programs for Supply Chain Analytics

## Getting started in 5 minutes

- Clone this repo
- Install requirements
- Run the script
- Done! :tada:


<p align="center">
  <img src="SCM.jpeg" width="600px" alt="SCM Image">
</p>


## Informations
MPS.py is a compilation of algorithms for Master Production Schedule:
1. One Time run
2. Chase (Lot for Lot)
3. Fixed Order Quantity
4. Periodic Order Quantity
5. Silver-Meal Heuristic
6. Wagner-Within Optimization

## Local Installation

### Clone the repo
```shell
$ git clone https://github.com/cydessole/Supply-Chain-Management.git
```

### Requirement
* Python 3
* NumPy
* Pandas

### Install requirements

```shell
$ pip install -r requirements.txt
```

## Run the script
You can either run the script as a standalone program or as a module

### Standalone
```
Master Production Schedule

positional arguments:
  fcost          The fixed cost
  hcost          The holding cost
  demands        Demands during each period

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Print information during process
  -e, --excel    Write Final DataFrame to excel
```
#### Usage
#### Example #1
##### Input
```shell
python MPS.py 500 1.5 150 50 150 200 50 250 50 200 50 100 50 300
```
##### Result
```shell
Master Production Schedule :
1: One time Run
2: Chase
3: Fixed Order Quantity
4: Periodic Order Quantity
5: Silver-Meal
6: Wagner-Within
Choose the method number you want to run : 3
Quantity to order: 300
========================Input========================
setup cost: 500.0
holding cost: 1.5
demands: [150, 50, 150, 200, 50, 250, 50, 200, 50, 100, 50, 300]
Quantity: 300.0
========================Final Cost========================
total_holding_cost: 2100.0
total_setup: 3000.0
total_cost: 5100.0
```

#### Example #2
##### Input
```shell
python MPS.py 500 1.5 150 50 150 200 50 250 50 200 50 100 50 300 -v -e
```

##### Result
```shell
Master Production Schedule :
1: One time Run
2: Chase
3: Fixed Order Quantity
4: Periodic Order Quantity
5: Silver-Meal
6: Wagner-Within
Choose the method number you want to run : 5
========================Input========================
setup cost: 500.0
holding cost: 1.5
demands: [150, 50, 150, 200, 50, 250, 50, 200, 50, 100, 50, 300]
========================Step 1========================
period 1
Number of period to produce : 2
cost [500.0, 287.5]
Number of period to produce : 3
cost : [500.0, 287.5, 341.67]

production [200, 0]
inventory [50, 0]
Best number of period to produce : 2
Minimum cost: 287.5
========================Step 2========================
period 3
Number of period to produce : 2
cost [500.0, 400.0]
Number of period to produce : 3
cost : [500.0, 400.0, 316.67]
Number of period to produce : 4
cost : [500.0, 400.0, 316.67, 518.75]

production [200, 0, 400, 0, 0]
inventory [50, 0, 250, 50, 0]
Best number of period to produce : 3
Minimum cost: 316.6666666666667
========================Step 3========================
period 6
Number of period to produce : 2
cost [500.0, 287.5]
Number of period to produce : 3
cost : [500.0, 287.5, 391.67]

production [200, 0, 400, 0, 0, 300, 0]
inventory [50, 0, 250, 50, 0, 50, 0]
Best number of period to produce : 2
Minimum cost: 287.5
========================Step 4========================
period 8
Number of period to produce : 2
cost [500.0, 287.5]
Number of period to produce : 3
cost : [500.0, 287.5, 291.67]

production [200, 0, 400, 0, 0, 300, 0, 250, 0]
inventory [50, 0, 250, 50, 0, 50, 0, 50, 0]
Best number of period to produce : 2
Minimum cost: 287.5
========================Step 5========================
period 10
Number of period to produce : 2
cost [500.0, 287.5]
Number of period to produce : 3
cost : [500.0, 287.5, 491.67]

production [200, 0, 400, 0, 0, 300, 0, 250, 0, 150, 0]
inventory [50, 0, 250, 50, 0, 50, 0, 50, 0, 50, 0]
Best number of period to produce : 2
Minimum cost: 287.5
========================Step 6========================
cost [500.0]
period 12
production [200, 0, 400, 0, 0, 300, 0, 250, 0, 150, 0, 300]
inventory [50, 0, 250, 50, 0, 50, 0, 50, 0, 50, 0, 0]
========================Final Cost========================
total_holding_cost: 750.0
total_setup: 3000.0
total_cost: 3750.0
        demand  production  IOH  Setup_cost  Holding_cost  total_cost
period                                                               
1          150         200   50       500.0          75.0       575.0
2           50           0    0         0.0           0.0         0.0
3          150         400  250       500.0         375.0       875.0
4          200           0   50         0.0          75.0        75.0
5           50           0    0         0.0           0.0         0.0
6          250         300   50       500.0          75.0       575.0
7           50           0    0         0.0           0.0         0.0
8          200         250   50       500.0          75.0       575.0
9           50           0    0         0.0           0.0         0.0
10         100         150   50       500.0          75.0       575.0
11          50           0    0         0.0           0.0         0.0
12         300         300    0       500.0           0.0       500.0

Excel saved
```

### Module
#### Usage
##### Input
```python
from MPS import *
import numpy as np
import pandas as pd
setup_cost=500.0
holding_cost= 1.5
demands= [150, 50, 150, 200, 50, 250, 50, 200, 50, 100, 50, 300]

inventory,production,total_cost=wagnerWithin(setup_cost,holding_cost,demands,verbose=False,excel=False)

print()
strategy=pd.DataFrame(data={'period':range(1,len(demands)+1),
                            'demand':demands,
                            'production':production,
                            'IOH':inventory})
strategy=strategy.set_index('period')
strategy['Setup_cost']=np.where(strategy['production']>0,setup_cost,0)
strategy['Holding_cost']=strategy['IOH']*holding_cost
strategy['total_cost']=strategy['Setup_cost']+strategy['Holding_cost']
print(strategy)
print('The total cost: ',total_cost)
```
##### Result
```shell
========================Input========================
setup cost: 500.0
holding cost: 1.5
demands: [150, 50, 150, 200, 50, 250, 50, 200, 50, 100, 50, 300]
========================Final Cost========================
total_holding_cost: 1200.0
total_setup: 2500.0
total_cost: 3700.0
        demand  production  IOH  Setup_cost  Holding_cost  total_cost
period                                                               
1          150         200   50       500.0          75.0       575.0
2           50           0    0         0.0           0.0         0.0
3          150         400  250       500.0         375.0       875.0
4          200           0   50         0.0          75.0        75.0
5           50           0    0         0.0           0.0         0.0
6          250         300   50       500.0          75.0       575.0
7           50           0    0         0.0           0.0         0.0
8          200         400  200       500.0         300.0       800.0
9           50           0  150         0.0         225.0       225.0
10         100           0   50         0.0          75.0        75.0
11          50           0    0         0.0           0.0         0.0
12         300         300    0       500.0           0.0       500.0
The total cost:  3700.0
```

## Notes
Other algorithms will be added to this repository for SCM.

For example, Dijkstra, Clarke-Wright for Supply Chain Design.
