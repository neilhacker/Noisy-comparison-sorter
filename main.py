import choix
import numpy as np
import pandas as pd
import random
import math
import itertools

def pick_next_comparison(data, n_items):
    params = choix.ilsr_pairwise(n_items, data, alpha=0.01)

    count = 10
    while count > 0:
        x = random.randint(0,n_items-1)
        y = random.randint(0,n_items-1)
        while y == x:
            y = random.randint(0,n_items-1)
        prob_x_wins, prob_y_wins = choix.probabilities([x, y], params)
        if abs(0.5-prob_x_wins) <0.1: #if comparison has below 60% chance of being guessed correctly atm
            return x,y
        count -=1

    #if search 10 times for good comparison and fail pick random one
    x = random.randint(0,n_items-1)
    y = random.randint(0,n_items-1)
    while y == x:
        y = random.randint(0,n_items-1)
    return x,y


#---------------------------- read in data and initialise values -------------------------------------
df=pd.read_csv('books1.csv')
n_items = df.shape[0]
data = []
comparing = True
abort = False

#--------------------- add in comparisons for data that has already been ranked  -----------------------

# if some things have been ranked before input rankings into data
if pd.isnull(df.iloc[0][1]) == False:
    rows = 0 
    while rows < n_items and pd.isnull(df.iloc[rows][1]) == False:
        rows+=1
    for i in range(rows-1):
        data.append((i+1, i))

#-------------------------------- give person pairwise comparisons  ----------------------------------
while comparing:
    x,y = pick_next_comparison(data, n_items)

    trying = True
    while trying:
        try:
            option = int(input(f"which do you prefer \n> {df.iloc[x][0]} \n> {df.iloc[y][0]} "))
            trying = False
        except:
            continue
        
    if option == 1:
        data.append((x,y))
    elif option == 2:
        data.append((y,x))
    elif option == 8:
        comparing = False
    elif option == 0:
        abort = True
        comparing = False
    else:
        pass

if abort == False:
    #-------------------- convert values that have been compared into min range to order  ----------------------------------
    unique_vals_ranked = list(set(itertools.chain.from_iterable(data)))
    values = {}
    for i in range(len(unique_vals_ranked)):
        values[i] = unique_vals_ranked[i]

    new_data = []
    # this will convert something like [(7, 23)] into [(0, 1)] so that we can use choix
    for comparison in data:
        for key,value in values.items():
            if value == comparison[0]:
                new_x = key
            elif value == comparison[1]:
                new_y = key
        new_data.append((new_x, new_y))

    #---------------------------------- find order  ------------------------------------------
    params = choix.ilsr_pairwise(len(unique_vals_ranked), new_data, alpha=0.01)
    order = np.argsort(params)

    # if order is [3,12,7,9] we want to add all the other rows 
    # that have values in at the end so we can sort the list
    for i in range(len(order)):
        order[i] = values[order[i]]
    for i in range(n_items):
        if i not in order:
            order = np.append(order,[i], axis=0)
            

    #---------------------------------- rearrange list  ------------------------------------------
    x = df.reindex(order).reset_index(drop=True)

    #--------------------------------------- allocate scores  -------------------------------------
    #buckets gives distribution that is downward sloping straight line (see excel file pairWiseComparisonDist)
    # note you need >=50 options to ever get something ranking 10
    buckets =[18,34,49,61,72,81,89,94,98,100] 

    # allocate scores  
    # using len(unique_vals_ranked) so we only calc scores for the values that have been ranked
    for row in range(len(unique_vals_ranked)): 
        score = (row/len(unique_vals_ranked))*100
        for bucket in range(len(buckets)):
            if score < buckets[bucket]:
                x.loc[row,"Ranking"] = bucket+1
                break


    print(x)

    #--------------------------------------- write to csv-------------------------------------
    x.to_csv("books1.csv", index=False)
