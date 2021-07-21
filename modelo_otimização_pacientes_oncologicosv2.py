from ortools.sat.python import cp_model

def main():
    costs = [  #c[p][d][td]
                [[60, 45, 60], [15, 60, 60]],  # patient 1
                [[60, 15, 60], [60, 45, 15]] # patient 2
             ]
    D = [1,2] #days
    P = [1,2] #patients
    Dp = [[1,2], [1,2]] #days chosen by the patients
    Td = [[1,2,3], [1,2,3]]  #Shifts available each day

    # Model
    model = cp_model.CpModel()

    # Variables
    x = {}
    for p in P: # P = [1,2]
        for d in Dp[p-1]: # D = [1,2]
            for td in Td[d-1]:  #Td: [[1,2,3], [1,2,3]]
                x[(p,d,td)] = model.NewBoolVar('paciente_p%id%itd%i' % (p, d, td))

    # Constraints
    # Each shift is assigned to exactly one patient.
    for d in D:   # D = [1,2]
        for td in Td[d-1]:  #Td: [[1,2,3], [1,2,3]]
            model.Add(sum(x[(p,d,td)] for p in P) <= 1)  # P = [1,2]

    # Objective
    objective_terms = []
    for p in P:
        for d in Dp[p-1]:
            for td in Td[d-1]:
                objective_terms.append(costs[p-1][d-1][td-1] * x[(p,d,td)])
    model.Minimize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Total cost = {}'.format(solver.ObjectiveValue()))
        for p in P: #P = [1,2]
            for d in Dp[p-1]:  #   Dp = [[1,2], [1,2]]
                for td in Td[d-1]:  #  Td = [[1,2,3], [1,2,3]]
                    if solver.BooleanValue(x[(p, d, td)]):
                        print('Patient {} assigned to day {} and shift {} Cost = {}'.format(p, d, td, costs[p-1][d-1][td-1]))
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()
