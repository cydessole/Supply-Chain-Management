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
