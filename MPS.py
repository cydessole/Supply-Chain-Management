import sys
import argparse
import numpy as np
import pandas as pd
def onetimerun(setup_cost,holding_cost,demands,verbose=False,excel=False):
    '''
    Signature:
    onetimerun(setup_cost,holding_cost,demands,verbose,excel)

    Docstring:
    One time run strategy. Produce everything in one go

    Parameters
    ----------
    setup_cost : fixed Cost
    holding_cost : variable cost of the stock
    demands: List of all period forecast
    verbose: Add layer of information during process (flag)
    excel: Output to excel file (flag)

    Returns
    -------
    inventory : List of inevntory on hand for each period
    Produce : List of production schedule for each periods
    Total cost : Sum of holding and setup cost for all period
    '''
    #Initialization of inventory and production schedule per period
    period=0 #First period 1 at position 0
    inventory=[]
    production=[]

    Ibegin=-1
    #Initialization of the start inventory
    while Ibegin<0 :
        try:
            Ibegin=int(input('Start Inventory : '))
            if Ibegin<0:
                print("Inventory must be positive ")
        except ValueError:
            print("This isn't a integer")

    if Ibegin>0:
        temp_inv=Ibegin
        while demands[period]<=temp_inv:
            production.append(0)
            inventory.append(temp_inv-demands[period])
            temp_inv=temp_inv-demands[period]
            print(temp_inv)
            period+=1
            if period>=len(demands):
                break
    #Input Data
    print('========================Input========================')
    print('setup cost:',setup_cost)
    print('holding cost:',holding_cost)
    print('Start Inventory:',Ibegin)
    print('demands:',demands)

    #Find the total production for all period
    if len(inventory)==0:
        if Ibegin==0:
            total_prod=sum(demands)
            #Produce everything at the first period
            production.append(total_prod)
            #Compute the first inventory
            inventory.append(total_prod-demands[period])
        else:
            total_prod=sum(demands)-Ibegin
            #Produce everything at the t period
            production.append(total_prod)
            #Compute the first inventory
            inventory.append(total_prod-demands[period]+Ibegin)
    else:
        total_prod=sum(demands)-inventory[period-1]
        #Produce everything at the t period
        production.append(total_prod)
        #Compute the first inventory
        inventory.append(total_prod-demands[period]+inventory[period-1])

    for i in range(period+1,len(demands)):
        inventory.append(inventory[i-1]-demands[i])
        production.append(0)

    if verbose:
            print('========================Schedule========================')
            print('production',production)
            print('inventory',inventory)
    #Cost Calculation
    total_holding_cost=sum(inventory)*holding_cost
    total_setup=sum(1 for each in production if each>0)*setup_cost
    total_cost=total_setup+total_holding_cost

    print('========================Final Cost========================')
    print('total_holding_cost:',total_holding_cost)
    print('total_setup:',total_setup)
    print('total_cost:', total_cost)

    #Format to DataFrame
    if verbose:
        strategy=pd.DataFrame(data={'period':range(1,len(demands)+1),
                                    'demand':demands,
                                    'production':production,
                                    'IOH':inventory})
        strategy=strategy.set_index('period')
        strategy['Setup_cost']=np.where(strategy['production']>0,setup_cost,0)
        strategy['Holding_cost']=strategy['IOH']*holding_cost
        strategy['total_cost']=strategy['Setup_cost']+strategy['Holding_cost']

        print(strategy)
        print()
    if excel:
        strategy.to_excel("output_onetimerun.xlsx")
        print('Excel saved')

    return inventory,production,total_cost

def chase(setup_cost,holding_cost,demands,verbose=False,excel=False):
    '''
    Signature:
    chase(setup_cost,holding_cost,demands,verbose,excel)

    Docstring:
    Chase strategy. Produce the exact amount for the period

    Parameters
    ----------
    setup_cost : fixed Cost
    holding_cost : variable cost of the stock
    demands: List of all period forecast
    verbose: Add layer of information during process (bool)
    excel: Output to excel file (bool)

    Returns
    -------
    inventory : List of inevntory on hand for each period
    Produce : List of production schedule for each periods
    Total cost : Sum of holding and setup cost for all period
    '''
    #Initialization of inventory and production schedule per period
    period=0 #First period 1 at position 0
    inventory=[]
    production=[]

    Ibegin=-1
    #Initialization of the start inventory
    while Ibegin<0 :
        try:
            Ibegin=int(input('Start Inventory : '))
            if Ibegin<0:
                print("Inventory must be positive ")
        except ValueError:
            print("This isn't a integer")

    if Ibegin>0:
        temp_inv=Ibegin
        while demands[period]<=temp_inv:
            production.append(0)
            inventory.append(temp_inv-demands[period])
            temp_inv=temp_inv-demands[period]
            print(temp_inv)
            period+=1
            if period>=len(demands):
                break
    #Input Data
    print('========================Input========================')
    print('setup cost:',setup_cost)
    print('holding cost:',holding_cost)
    print('Start Inventory:',Ibegin)
    print('demands:',demands)

    print(inventory)
    if len(inventory)>0:
        for i in range(period,len(demands)):
            #print(inventory[i-1])
            production.append(demands[i]-inventory[i-1])
            inventory.append(inventory[i-1]-demands[i]+production[i])
    else:
        if Ibegin==0:
            #Produce every time when needed
            production=demands.copy()
            #Compute the first inventory
            inventory.extend([0]*len(demands))
        else:
            production.append(demands[period]-Ibegin)
            inventory.append(Ibegin-demands[period]+production[period])
            for i in range(period+1,len(demands)):
                #print(inventory[i-1])
                production.append(demands[i]-inventory[i-1])
                inventory.append(inventory[i-1]-demands[i]+production[i])

    if verbose:
            print('========================Schedule========================')
            print('production',production)
            print('inventory',inventory)
    #Cost Calculation
    total_holding_cost=sum(inventory)*holding_cost
    total_setup=sum(1 for each in production if each>0)*setup_cost
    total_cost=total_setup+total_holding_cost

    print('========================Final Cost========================')
    print('total_holding_cost',total_holding_cost)
    print('total_setup',total_setup)
    print('total_cost:', total_cost)

    #Format to DataFrame
    if verbose:
        strategy=pd.DataFrame(data={'period':range(1,len(demands)+1),
                                    'demand':demands,
                                    'production':production,
                                    'IOH':inventory})
        strategy=strategy.set_index('period')
        strategy['Setup_cost']=np.where(strategy['production']>0,setup_cost,0)
        strategy['Holding_cost']=strategy['IOH']*holding_cost
        strategy['total_cost']=strategy['Setup_cost']+strategy['Holding_cost']

        print(strategy)
        print()
    if excel:
        strategy.to_excel("output_chase.xlsx")
        print('Excel saved')

    return inventory,production,total_cost

def fixedOrderQuantity(setup_cost,holding_cost,demands,Q,verbose=False,excel=False):
    '''
    Signature:
    FixedOrderQuantity(setup_cost,holding_cost,Q,demands,verbose,excel)

    Docstring:
    Fixed Order Quantity strategy. Produce a fixed order quantity when needed

    Parameters
    ----------
    setup_cost : fixed Cost
    holding_cost : variable cost of the stock
    demands: List of all period forecast
    Q: Quantity produced
    verbose: Add layer of information during process (bool)
    excel: Output to excel file (bool)

    Returns
    -------
    inventory : List of inevntory on hand for each period
    Produce : List of production schedule for each periods
    Total cost : Sum of holding and setup cost for all period
    '''
    #Initialization of inventory and production schedule per period
    period=0 #First period 1 at position 0
    step=0
    inventory=[]
    production=[]
    Ibegin=-1
    #Initialization of the start inventory
    while Ibegin<0 :
        try:
            Ibegin=int(input('Start Inventory : '))
            if Ibegin<0:
                print("Inventory must be positive ")
        except ValueError:
            print("This isn't a integer")

    if Ibegin>0:
        temp_inv=Ibegin
        while demands[period]<=temp_inv:
            production.append(0)
            inventory.append(temp_inv-demands[period])
            temp_inv=temp_inv-demands[period]
            period+=1
            if period>=len(demands):
                break

    #Input Data
    print('========================Input========================')
    print('setup cost:',setup_cost)
    print('holding cost:',holding_cost)
    print('demands:',demands)
    print('Start Inventory:',Ibegin)
    print('Quantity:',Q)

    step+=1
    if verbose:
        print('========================Step {}========================'.format(step))
        print('period',period+1)

    #First step Initialization for production and inventory
    if len(inventory)==0:
        if Ibegin==0:
            production.append(Q)
            inventory.append(production[period]-demands[period])
        else:
            production.append(Q)
            inventory.append(production[period]-demands[period]+Ibegin)

        if verbose:
                print('production',production)
                print('inventory',inventory)

        period+=1

    while  period<len(demands) :
        step+=1
        if verbose:
            print('========================Step {}========================'.format(step))
            print('period',period+1)
        if (inventory[period-1]-demands[period])>=0:
            produce_now=0
        else:
            if sum(demands[period:len(demands)])-inventory[period-1]>=Q:
                produce_now=Q
            else:
                produce_now=sum(demands[period:len(demands)])-inventory[period-1]
        production.append(produce_now)
        inventory.append(production[period]-demands[period]+inventory[period-1])

        if verbose:
                print('production',production)
                print('inventory',inventory)

        period+=1


    if verbose:
            print('========================Final Schedule========================')
            print('production',production)
            print('inventory',inventory)
    #Cost Calculation
    total_holding_cost=sum(inventory)*holding_cost
    total_setup=sum(1 for each in production if each>0)*setup_cost
    total_cost=total_setup+total_holding_cost

    print('========================Final Cost========================')
    print('total_holding_cost:',total_holding_cost)
    print('total_setup:',total_setup)
    print('total_cost:', total_cost)

    #Format to DataFrame
    if verbose:
        strategy=pd.DataFrame(data={'period':range(1,len(demands)+1),
                                    'demand':demands,
                                    'production':production,
                                    'IOH':inventory})
        strategy=strategy.set_index('period')
        strategy['Setup_cost']=np.where(strategy['production']>0,setup_cost,0)
        strategy['Holding_cost']=strategy['IOH']*holding_cost
        strategy['total_cost']=strategy['Setup_cost']+strategy['Holding_cost']

        print(strategy)
        print()
    if excel:
        strategy.to_excel("output_FixedOrderQuantity.xlsx")
        print('Excel saved')

    return inventory,production,total_cost

def periodicOrderQuantity(setup_cost,holding_cost,demands,T,verbose=False,excel=False):
    '''
    Signature:
    PeriodicOrderQuantity(setup_cost,holding_cost,demands,T,verbose,excel)

    Docstring:
    Periodic Order Quantity strategy. Produce at constant time the quantity needed for t period

    Parameters
    ----------
    setup_cost : fixed Cost
    holding_cost : variable cost of the stock
    demands: List of all period forecast
    T: Cycle time
    verbose: Add layer of information during process (bool)
    excel: Output to excel file (bool)

    Returns
    -------
    inventory : List of inevntory on hand for each period
    Produce : List of production schedule for each periods
    Total cost : Sum of holding and setup cost for all period
    '''
    #Initialization of inventory and production schedule per period
    period=0 #First period 1 at position 0
    step=0
    inventory=[]
    production=[]

    Ibegin=-1
    #Initialization of the start inventory
    while Ibegin<0 :
        try:
            Ibegin=int(input('Start Inventory : '))
            if Ibegin<0:
                print("Inventory must be positive ")
        except ValueError:
            print("This isn't a integer")

    if Ibegin>0:
        temp_inv=Ibegin
        while demands[period]<=temp_inv:
            production.append(0)
            inventory.append(temp_inv-demands[period])
            temp_inv=temp_inv-demands[period]
            period+=1
            if period>=len(demands):
                break
    #Input Data
    print('========================Input========================')
    print('setup cost:',setup_cost)
    print('holding cost:',holding_cost)
    print('demands:',demands)
    print('Start Inventory:',Ibegin)
    print('Period:',T)


    while period<len(demands):
        step+=1
        if verbose:
            print('========================Step {}========================'.format(step))
            print('period',period+1)
        close_to_end=(len(demands)-(period+1))+1 # Exemple if T=3 for period 9 : 9 10 11 so if len(d)=11 --> 11-9=2+1=3
        if close_to_end>=T:
            n=T
        else:
            n=close_to_end
        n=int(n)
        if len(inventory)==0:
            if Ibegin==0:
                total_prod=sum(demands[period:period+n])
                production.append(total_prod)
                inventory.append(total_prod-demands[period])
            else:
                total_prod=sum(demands[period:period+n])-Ibegin
                production.append(total_prod)
                inventory.append(total_prod-demands[period]+Ibegin)
        else:
            total_prod=sum(demands[period:period+n])-inventory[period-1]
            production.append(total_prod)
            inventory.append(total_prod-demands[period]+inventory[period-1])

        for i in range(period+1,period+n):
            inventory.append(inventory[i-1]-demands[i])
            production.append(0)
        period+=n

        if verbose:
            print('production',production)
            print('inventory',inventory)

    if verbose:
        print('========================Schedule========================')
        print('production',production)
        print('inventory',inventory)
    #Cost Calculation
    total_holding_cost=sum(inventory)*holding_cost
    total_setup=sum(1 for each in production if each>0)*setup_cost
    total_cost=total_setup+total_holding_cost

    print('========================Final Cost========================')
    print('total_holding_cost:',total_holding_cost)
    print('total_setup:',total_setup)
    print('total_cost:', total_cost)

    #Format to DataFrame
    if verbose:
        strategy=pd.DataFrame(data={'period':range(1,len(demands)+1),
                                    'demand':demands,
                                    'production':production,
                                    'IOH':inventory})
        strategy=strategy.set_index('period')
        strategy['Setup_cost']=np.where(strategy['production']>0,setup_cost,0)
        strategy['Holding_cost']=strategy['IOH']*holding_cost
        strategy['total_cost']=strategy['Setup_cost']+strategy['Holding_cost']

        print(strategy)
        print()
    if excel:
        strategy.to_excel("output_PeriodicOrderQuantity.xlsx")
        print('Excel saved')

    return inventory,production,total_cost


def silvermeal(setup_cost,holding_cost,demands,verbose=False,excel=False):
    '''
    Signature:
    silvermeal(setup_cost,holding_cost,demands)

    Docstring:
    Silver-Meal Heuristic to find a low cost to produce based on fixed and variable cost

    Parameters
    ----------
    setup_cost : fixed Cost
    holding_cost : variable cost of the stock
    demands: List of all period forecast
    verbose: Add layer of information during process (bool)
    excel: Output to excel file (bool)

    Returns
    -------
    inventory : List of inevntory on hand for each period
    Produce : List of production schedule for each periods
    Total cost : Sum of holding and setup cost for all period
    '''
    #Initialization of inventory and production schedule per period
    period=0 #First period 1 at position 0
    step=0
    inventory=[]
    production=[]
    Ibegin=-1
    #Initialization of the start inventory
    while Ibegin<0 :
        try:
            Ibegin=int(input('Start Inventory : '))
            if Ibegin<0:
                print("Inventory must be positive ")
        except ValueError:
            print("This isn't a integer")

    if Ibegin>0:
        temp_inv=Ibegin
        while demands[period]<=temp_inv:
            production.append(0)
            inventory.append(temp_inv-demands[period])
            temp_inv=temp_inv-demands[period]
            period+=1
            if period>=len(demands):
                break
    #Input Data
    print('========================Input========================')
    print('setup cost:',setup_cost)
    print('holding cost:',holding_cost)
    print('Start Inventory:',Ibegin)
    print('demands:',demands)


    #First Loop : from period 1 to last period-1
    while  (period+1)<len(demands) :
        step+=1
        if verbose:
            print('========================Step {}========================'.format(step))
            print('period',period+1)

        temp_inv_n_minus_1=[0] #if the choice is only one period to handle --> 0 stock
        n=1  #Number of period added to the period t to produce
        if verbose:
            print('Number of period to produce :',n+1)
        #Sum of Demand to produce
        if len(inventory)==0:
            if Ibegin==0:
                total_prod=sum(demands[period:(period+n+1)])
                #Initialization of the stock of the first period of production
                temp_inv_n=[total_prod-demands[period]]
            else:
                total_prod=sum(demands[period:(period+n+1)])-Ibegin
                #Initialization of the stock of the first period of production
                temp_inv_n=[total_prod-demands[period]+Ibegin]
        else:
            total_prod=sum(demands[period:(period+n+1)])-inventory[period-1]
            #Initialization of the stock of the first period of production
            temp_inv_n=[total_prod-demands[period]+inventory[period-1]]

        #Loop to find the inventory for all the period handled by the production at period t : inventory(t-1)-demand(t)
        for i,t in enumerate(range(period+1,period+1+n),1):
            temp_inv_n.append(temp_inv_n[i-1]-demands[t])

        #Cost first cost: Produce for one period (0 stock + setup cost) and two periods (stock*holding + setup cost)
        cost=[setup_cost,(setup_cost+holding_cost*sum(temp_inv_n))/(n+1)]
        if verbose:
            print('cost',[round(each,2) for each in cost])

        #Second Loop : Compare cost with n period added versus n-1 period added
        while cost[n]<cost[n-1] and period+1+n+1<=len(demands):
            n+=1 # Add another period to handle
            if verbose:
                print('Number of period to produce :',n+1)

            #n periods become n-1 and initialization of n period
            temp_inv_n_minus_1=temp_inv_n.copy()
            if len(inventory)==0:
                total_prod=sum(demands[period:(period+n+1)])
                temp_inv_n=[total_prod-demands[period]]
            else:
                total_prod=sum(demands[period:(period+n+1)])-inventory[period-1]
                temp_inv_n=[total_prod-demands[period]+inventory[period-1]]

            #Loop to find the inventory for all period handled t period inventory i (0 start of period t specific to silver-meal because inventory begins for period t)
            for i,t in enumerate(range(period+1,period+1+n),1):
                temp_inv_n.append(temp_inv_n[i-1]-demands[t])

            #Add the new cost to the list of costs for all case scenario for period t
            cost.append((setup_cost+holding_cost*sum(temp_inv_n))/(n+1))
            if verbose:
                print('cost :',[round(each,2) for each in cost])

        if (cost[n]<cost[n-1]) and not (period+1+n+1<=len(demands)): #Case where the new cost is lower but you are at the limit of your array
            temp_inv=temp_inv_n.copy() #The best result is the n of the last comparison because you can't move forward
        else:
            temp_inv=temp_inv_n_minus_1.copy() #The best result is the n-1 of the last comparison
            n-=1 #Best result

        #Retrieves the best schedule of production
        if len(inventory)==0:
            if Ibegin==0:
                production.append(sum(demands[period:(period+n+1)]))
            else:
                production.append(sum(demands[period:(period+n+1)])-Ibegin)
        else:
            production.append(sum(demands[period:(period+n+1)])-inventory[period-1])
        production.extend([0]*n) #Number of periods when we don't produce

        #Retrieves the best choice of inventory
        inventory.extend(temp_inv)

        if verbose:
            print()
            print('production',production)
            print('inventory',inventory)
            print('Best number of period to produce :',n+1)
            print('Minimum cost:',cost[n])
        period+=(n+1) #Jump to the next production

    #Case where we are at the last period : can't add another period to handle
    if (period+1)==len(demands):
        step+=1
        production.append(demands[period])
        inventory.append(0)

        if verbose :
            print('========================Step {}========================'.format(step))
            print('cost',[setup_cost])
            print('period',period+1)
            print('production',production)
            print('inventory',inventory)

    #Cost Calculation
    total_holding_cost=sum(inventory)*holding_cost
    total_setup=sum(1 for each in production if each>0)*setup_cost
    total_cost=total_setup+total_holding_cost

    print('========================Final Cost========================')
    print('total_holding_cost:',total_holding_cost)
    print('total_setup:',total_setup)
    print('total_cost:', total_cost)

    #Format to DataFrame
    if verbose:
        strategy=pd.DataFrame(data={'period':range(1,len(demands)+1),
                                    'demand':demands,
                                    'production':production,
                                    'IOH':inventory})
        strategy=strategy.set_index('period')
        strategy['Setup_cost']=np.where(strategy['production']>0,setup_cost,0)
        strategy['Holding_cost']=strategy['IOH']*holding_cost
        strategy['total_cost']=strategy['Setup_cost']+strategy['Holding_cost']

        print(strategy)
        print()
    if excel:
        strategy.to_excel("output_silvermeal.xlsx")
        print('Excel saved')
    return inventory,production,total_cost

def wagnerWhitin(setup_cost,holding_cost,demands,verbose=False,excel=False):
    '''
    Signature:
    wagnerWhitin(setup_cost,holding_cost,demands)

    Docstring:
    Wagner-Whitin optimization to find the lowest cost to produce based on fixed and variable cost

    Parameters
    ----------
    setup_cost : fixed Cost
    holding_cost : variable cost of the stock
    demands: List of all period forecast
    verbose: Add layer of information during process (bool)
    excel: Output to excel file (bool)

    Returns
    -------
    inventory : List of inevntory on hand for each period
    Produce : List of production schedule for each periods
    Total cost : Sum of holding and setup cost for all period
    '''
    #Initialization of inventory and production schedule per period
    step=0
    inventory=[]
    production=[]
    min_cost=[]
    #Input Data
    print('========================Input========================')
    print('setup cost:',setup_cost)
    print('holding cost:',holding_cost)
    print('demands:',demands)
    #Initialization of the cost matrix
    matrix=np.zeros((len(demands),len(demands)))
    #First method to handle half of matrix
    #matrix=np.where(matrix==0,99999999999,0)

    if verbose:
        print('========================Forward========================')
    #Frist Loop to go through each period
    for period in range(0,len(demands)):
        #Second Loop to handle each Order possibilities
        for order in range(0,period+1):
            #The #Order gives the next position of the demand to handle
            total_prod=sum(demands[order:period+1])
            #Start inventory at the start of #Order
            temp_inv=[total_prod-demands[order]]
            #Loop to find the inventory for all period handled from the #Order
            for i,t in enumerate(range(order+1,period+1),1):
                temp_inv.append(temp_inv[i-1]-demands[t])
            #Min cost of the previous order + compute cost
            if order==0:
                cost=setup_cost+holding_cost*sum(temp_inv)
            else:
                cost=min_cost[order-1]+setup_cost+holding_cost*sum(temp_inv)
            matrix[period,order]=cost
        #Second method, set max of the row for the other half, better memory optimization, loss of speed
        matrix[period,:]=np.where(matrix[period,:]==0,matrix[period,:].max(),matrix[period,:])
        min_cost.append(matrix[period,:].min())

    if verbose:
        print("Minimun cost for each row",min_cost)
        print(pd.DataFrame(matrix))

    if verbose:
        print('========================Backward========================')

    step=0
    backward_schedule=[]
    while period>=0 and step<=len(demands):
        row=matrix[period,:]
        row_inv=row[::-1]
        backward_schedule.append(len(row_inv)-row_inv.argmin()-1) #To find the last occurence min for the row
        #backward_schedule.append(matrix[period,:].argmin()) #First the first occurence min
        period=backward_schedule[step]-1
        if verbose:
            print('========================Step {}========================'.format(step+1))
            print('Backward Schedule:',backward_schedule)
            print('Next period:', period)
        step+=1
    schedule=backward_schedule[::-1]
    if verbose:
        print('Schedule:',schedule)

    if verbose:
        print('========================Create Schedule========================')
    final_move=len(schedule)
    move=1
    period=0
    #Loop the schedule and produce for next-1 period
    while move<=final_move:
        if verbose:
            print('move:',move)
            print('period:',period)
        if move<final_move:
            next=schedule[move]
        #When we are the end of the Schedule list the final step is to produce until the last period
        else:
            next=len(demands)
        if verbose:
            print('next',next)
            print()
        total_prod=sum(demands[period:next])
        production.append(total_prod)
        inventory.append(total_prod-demands[period])
        for i in range(period+1,next):
            inventory.append(inventory[i-1]-demands[i])
            production.append(0)
        period+=(next-period)
        move+=1

    if verbose:
        print('========================Final Schedule========================')
        print('production',production)
        print('inventory',inventory)

    #Cost Calculation
    total_holding_cost=sum(inventory)*holding_cost
    total_setup=sum(1 for each in production if each>0)*setup_cost
    total_cost=total_setup+total_holding_cost

    print('========================Final Cost========================')
    print('total_holding_cost:',total_holding_cost)
    print('total_setup:',total_setup)
    print('total_cost:', total_cost)

    #Format to DataFrame
    if verbose:
        strategy=pd.DataFrame(data={'period':range(1,len(demands)+1),
                                    'demand':demands,
                                    'production':production,
                                    'IOH':inventory})
        strategy=strategy.set_index('period')
        strategy['Setup_cost']=np.where(strategy['production']>0,setup_cost,0)
        strategy['Holding_cost']=strategy['IOH']*holding_cost
        strategy['total_cost']=strategy['Setup_cost']+strategy['Holding_cost']

        print(strategy)
        print()
    if excel:
        strategy.to_excel("output_WagnerWhitin.xlsx")
        print('Excel saved')

    return inventory,production,total_cost


def create_parser():
    """
    Creates a command line interface parser.
    """

    parser = argparse.ArgumentParser(description='Master Production Schedule')

    parser.add_argument('fcost', type=float,
        help="The fixed cost")
    parser.add_argument('hcost', type=float,
        help="The holding cost")
    parser.add_argument('demands', nargs='+', type=int,
        help="Demands during each period")
    parser.add_argument('-v','--verbose', action='store_true',
        help='Print information during process')
    parser.add_argument('-e','--excel', action='store_true',
        help='Write Final DataFrame to excel')

    return parser

def main(argv):
    # Create the command line parser.
    parser = create_parser()
    # Get the options and arguments.
    args = parser.parse_args(argv)
    f_cost = args.fcost
    h_cost = args.hcost
    demands = args.demands
    verbose= args.verbose
    excel=args.excel

    print('Master Production Schedule :')
    print('1: One time Run')
    print('2: Chase')
    print('3: Fixed Order Quantity')
    print('4: Periodic Order Quantity')
    print('5: Silver-Meal')
    print('6: Wagner-Whitin')


    i=0
    while i<1 or i>6 :
        try:
            i=int(input('Choose the method number you want to run : '))
            if i<1 or i>6:
                print("There is no method with this number ")
        except ValueError:
            print("This isn't a integer")
    if i==1:
        onetimerun(f_cost,h_cost,demands,verbose,excel)
    elif i==2:
        chase(f_cost,h_cost,demands,verbose,excel)
    elif i==3:
        while True:
            try:
                Q=float(input('Quantity to order: '))
                break
            except ValueError:
                print("This isn't a number")
        fixedOrderQuantity(f_cost,h_cost,demands,Q,verbose,excel)
    elif i==4:
        while True:
            try:
                T=int(input('Order cycle: '))
                break
            except ValueError:
                print("This isn't a number")
        periodicOrderQuantity(f_cost,h_cost,demands,T,verbose,excel)
    elif i==5:
        silvermeal(f_cost,h_cost,demands,verbose,excel)
    elif i==6:
        wagnerWhitin(f_cost,h_cost,demands,verbose,excel)

if __name__ == "__main__":
    main(sys.argv[1:])
