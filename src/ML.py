import numpy as np 
import pandas as pd 
#pip install mlxtend
from mlxtend.frequent_patterns import apriori, association_rules 
from mlxtend.preprocessing import TransactionEncoder
import database_connector as DB
import random

pd.set_option('display.max_rows', None)

transactions = DB.return_transactions()
# print(transactions)

#DATASET = BOOKS ISBNs OF EACH TRANSACTION
dataset = transactions

#ENCODING DATA WITH TRUE/FALSE IF THEY ARE FOUND IN DATASET

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns= te.columns_)

ap = apriori(df,min_support= 0.01,use_colnames=True) #run apriori with 10% minimum support


def top3():
    #Applying apriori with max_len 1 so we get 1 antecedent length
    #Returns a list of the top 3 books (str)
    ap2 = apriori(df,min_support = 0.1,use_colnames=True,max_len=1)
    ap2 = ap2.sort_values('support',ascending = False).head(3)  #Top 3 books
    books = [next(iter(x)) for x in ap2.itemsets]   #Un-frozenset-ing
    return books

def recommendations(cart):
    #Cart needs to be cast as set to work with the association rules
    cart = set(cart)
    recommendation = {}
    rules = association_rules(ap,metric='lift')
    rules = rules[["antecedents","consequents","lift","confidence"]]
    rules['consequents_len'] = rules['consequents'].apply(lambda x: len(x))
    #Getting the required fields

    if rules[(rules['antecedents'] == cart)].empty:
        #If we cannot find any itemset that is in cart, check for each item in the cart
        #Then store the lift and the item in a dictionary
        #If the dictionary is empty at the end it means we don't have any good data
        #About the currect item so return a random book instead
        for i in cart:
            rules2 = rules[
                (rules['antecedents'] == {i}) &
                (rules['lift'] > 1) & 
                (rules['consequents_len'] == 1)]
            rules2 = rules2.sort_values(by = 'lift' , ascending = False).head(1)
            if not rules2['lift'].empty:
                recommendation[i] = rules2['lift'].item()
        if recommendation:
            recommendation = sorted(recommendation.items(),reverse= True)
            rules = rules[(rules['antecedents'] == {recommendation[0][0]}) &
                          (rules['lift'] > 1) &
                          (rules['consequents_len'] == 1)]
            rules = rules.sort_values(by = 'lift',ascending = False)
            rules = rules['consequents'].head(1)
            a = rules.item()
            return next(iter(a))
        else:
            return random.randint(1,13)
        
    else:
        #If there is a valid association rules about all items in cart return the consequent
        rules = rules[rules['antecedents'] == cart]
        rules = rules.sort_values(by = ['lift'], ascending = False)
        rules = rules[(rules['consequents_len'] == 1)].head(1)
        result = rules['consequents'].item()
        return next(iter(result))

def top20():
    #Applying apriori with max_len 1 so we get 1 antecedent length
    #Returns a list of the top 3 books (str)
    ap2 = apriori(df,min_support = 0.01,use_colnames=True)
    ap2 = ap2.sort_values('support',ascending = False).head(20)
    result = []
    for item in ap2.itemsets:
        result.append(list(item))
    return result

def bottom20():
    #Applying apriori with max_len 1 so we get 1 antecedent length
    #Returns a list of the top 3 books (str)
    ap2 = apriori(df,min_support = 0.01,use_colnames=True)
    ap2 = ap2.sort_values('support',ascending = False).tail(20)
    result = []
    for item in ap2.itemsets:
        result.append(list(item))
    return result





