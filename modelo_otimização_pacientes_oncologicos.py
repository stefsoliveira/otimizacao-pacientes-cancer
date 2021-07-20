from ortools.sat.python import cp_model

def main():
    costs = [  #c[p][d][td]
                [[60, 45, 1000], [15, 60, 1000]],  # patient 1
                [[60, 15, 60], [1000, 45, 15]] # patient 2
             ]
    D = [1,2] #days
    P = [1,2] #patients
    Dp = [[1,2], [1,2]] #days chosen by the patients
    Td = [[1,2,3], [1,2,3]]  #Shifts available each day

    # Model
    model = cp_model.CpModel()

    # Variables
    x = []
    for i in range(len(P)):
        p = P[i]
        x.append([])
        for j in range(len(Dp[i])):
            d = Dp[i][j]
            temp = []
            for k in range(len(Td[Dp[i][j] - 1])):
                td = Td[Dp[i][j]-1][k]
                temp.append(model.NewBoolVar('paciente_p%id%itd%i' % (p, d, td)))
            x[i].append(temp)

    # Constraints
    # Each shift is assigned to exactly one patient.
    for j in range(len(D)):   # D = [1,2,3]
        for k in range(len(Td[j])):  #Td: [[1,2,3], [1,2,3]
            model.Add(sum(x[p-1][j][k] for p in P) <= 1)

    # Objective
    objective_terms = []
    for i in range(len(P)):
        for j in range(len(Dp[i])):
            for k in range(len(Td[Dp[i][j] - 1])):
                objective_terms.append(costs[i][j][k] * x[i][j][k])
    model.Minimize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Total cost = {}'.format(solver.ObjectiveValue()))
        for i in range(len(P)): #P = [1,2]
            for j in range(len(Dp[i])):  #   Dp = [[1,2], [1,2]]
                for k in range(len(Td[Dp[i][j] - 1])):  #  Td = [[1,2,3], [1,2,3]]
                    if solver.BooleanValue(x[i][j][k]):
                        print('Patient {} assigned to shift {} Cost = {}'.format(P[i], Dp[i][j], Td[Dp[i][j]-1][k], costs[i][j][k]))
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()
