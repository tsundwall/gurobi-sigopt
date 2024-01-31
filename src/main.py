import gurobipy as gp
from gurobipy import GRB
import numpy as np

def solve(a_array,b_array,c_array,l_bounds,u_bounds,A=[],b=[],C=[],d=[]):

    all_param_lists = [a_array,b_array,c_array]
    it = iter(all_param_lists)
    n = len(next(it))
    if not all(len(l) == n for l in it):
         raise ValueError('Param Lists Have Mismatched Lengths')

    if (len(A) > 0 and len(A[0]) != n):
        raise ValueError(f'number of rows in A matrix ({len(A[0])}) does not match problem size {n}')

    if (len(C) > 0 and len(C[0]) != n):
        raise ValueError(f'number of rows in C matrix ({len(C[0])}) does not match problem size {n}')

    if len(A) != len(b):
        raise ValueError(f'number of variables in A matrix does not match size of vector b')

    if len(C) != len(d):
        raise ValueError(f'number of variables in C matrix does not match size of vector d')

    if  len(l_bounds) != n:
        raise ValueError(f'Array of lower bounds has size {len(l_bounds)}, mismatching variable length {n}')

    if  len(u_bounds) != n:
        raise ValueError(f'Array of lower bounds has size {len(u_bounds)}, mismatching variable length {n}')


    try:

        x_neg_lb = [-ub for ub in u_bounds]
        x_neg_ub = [-lb for lb in l_bounds]
        print(x_neg_lb)
        m = gp.Model("NewModel")

        t = m.addMVar((n,),vtype="C", name="t (epigraph variables)")
        x_e = m.addMVar((n,),vtype="C", name="x evaluate exp",lb=[1e-6]*n,ub=[1e6]*n)
        z = m.addMVar((n,),vtype="C", name="x division",lb=[1e-6],ub=[1e6])
        x = m.addMVar((n,),vtype="C", name="x",lb=l_bounds,ub=u_bounds)
        x_neg = m.addMVar((n,),vtype="C", name="x neg",lb=x_neg_lb)

        m.setObjective(gp.quicksum(t[i] for i in range(n)), GRB.MAXIMIZE)

        for row_idx, A_row in enumerate(A):
            m.addConstr(gp.quicksum(A_col*x[col_idx] for col_idx,A_col in enumerate(A_row)) == b[row_idx])

        for row_idx, C_row in enumerate(C):
            m.addConstr(gp.quicksum(C_col*x[col_idx] for col_idx,C_col in enumerate(C_row)) <= d[row_idx])


        m.addConstrs((t[i] <= a_array[i]*z[i] for i in range(n)), "epigraph constraints")
        m.addConstrs((z[i]*(1+x_e[i])==1 for i in range(n)), "divisor constraints")
        m.addConstrs((x_neg[i]+b_array[i]*x[i]-c_array[i] == 0 for i in range(n)), "exp term constraints")

        for i in range(n): #need to add iteratively; forms PLB of exp()
            m.addGenConstrExp(x_neg[i],x_e[i]) #f"exp approximation constraint #{i}"

        m.setParam('NonConvex', 2)
        m.optimize()

        for v in m.getVars():

            if 'x[' in v.VarName:
                print(f"{v.VarName} {v.X:g}")

        print(f"Obj: {m.ObjVal:g}")

    except gp.GurobiError as e:
        print(f"Error code {e.errno}: {e}")

    except AttributeError:
        print("Encountered an attribute error")

    return m

a_array = [1,1,1,1]
b_array = [1,2,3,4]
c_array = [1,1,1,1]

l_bounds = [0]*4
u_bounds = [10]*4

A = np.array([[1,1,1,1]])
b = np.array([7.5])

sol = solve(a_array,b_array,c_array,l_bounds,u_bounds,A,b)