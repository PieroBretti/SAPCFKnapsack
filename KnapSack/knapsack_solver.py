#Hasan Rafiq -> Knapsack solver using ranks
import os
import json
from bottle import route, run, post, request
from ortools.algorithms import pywrapknapsack_solver

port = int(os.getenv("PORT"))

@route('/')
def input():
   return("Ok.. ")

@route('/call_knapsack', method='POST')
def input():
  # Create the solver.
  solver = pywrapknapsack_solver.KnapsackSolver(
      pywrapknapsack_solver.KnapsackSolver.
      KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
      'test')
  #values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]                              #All ranks
  #weights = [[5000, 3700, 3210, 837, 1500, 3122, 1900, 820, 100, 800]] #All AR amounts
  #capacities = [10000]                                                  #Cheque amount
  #print(request.json['RANKS'])
  values = request.json['RANKS']                              #All ranks
  weights = [request.json['WEIGHTS']]                         #All AR amounts
  capacities = [request.json['AMOUNT']]                       #Cheque 
  
  rank = max(values)                                          #Get max of ranks
  digits = len(str(rank))                                                               #Number of digits in max rank
  #values = [((rank + 1) - i) for i in values]                                          #Reverse all ranks
  values = [ ( 10 ** digits ) * rank * ( 2 ** (1 + (-1 * i ))) for i in values]         #Rank decay logic
  #values = [ ( 10 ** digits ) * ( rank / i ) for i in values]                          #Divide max rank by current rank -> * 10^digits
  #print ("AR Risks: ", values)

  solver.Init(values,
              weights,
              capacities)
  computed_value = solver.Solve()

  packed_items = [x for x in range(0, len(weights[0]))
                  if solver.BestSolutionContains(x)]
  packed_weights = [weights[0][i] for i in packed_items]
  total_weight= sum(packed_weights)
  #print ("Selected ARs", [(i + 1) for i in packed_items])
  #print ("Selected AR amounts: ", packed_weights)
  #print ("Total risk cleared: ", computed_value)
  #print ("Total AR amount cleared: ", total_weight, "out of", capacities[0])
  return {"AR_SELECTED":[(i + 1) for i in packed_items], 'AR_SELECTED_AMOUNTS':packed_weights, 'RISK_CLEARED':computed_value, "AMOUNT_CLEARED":total_weight}
  #return {'Ok':'123'}
  
if __name__ == '__main__':
   run(host='0.0.0.0', port=port)
