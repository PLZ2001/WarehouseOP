# -*- coding: utf-8 -*-
# @Time : 2022/9/15 22:02
# @Author : PLZ
# @File : template.py
# @Software : PyCharm

import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB
from Helper import *

# 下标总量
N = 3
T = 10
M = 3
D = 3

# 常量设置
MAX = 100000000

# 仓库一年租赁成本
LS = np.zeros(N+1)
LS[1] = 100
LS[2] = 200
LS[3] = 300

# 仓库容量
NS = np.zeros(N+1)
NS[1] = 10
NS[2] = 20
NS[3] = 30

# 单位物料的金额
LP = np.zeros(M+1)
LP[1] = 1
LP[2] = 2
LP[3] = 3

# 单位物料的重量
LW = np.zeros(M+1)
LW[1] = 1
LW[2] = 2
LW[3] = 3

# 单位物料的面积
LS2 = np.zeros(M+1)
LS2[1] = 1
LS2[2] = 2
LS2[3] = 3

# 库-库距离
DS_N = np.zeros((N+1,N+1))
DS_N[1,1] = 0
DS_N[1,2] = 130
DS_N[1,3] = 120
DS_N[2,1] = 130
DS_N[2,2] = 0
DS_N[2,3] = 90
DS_N[3,1] = 120
DS_N[3,2] = 90
DS_N[3,3] = 0

# 库-需求距离
DS_D = np.zeros((N+1,D+1))
DS_D[1,1] = 20
DS_D[1,2] = 18
DS_D[1,3] = 16
DS_D[2,1] = 14
DS_D[2,2] = 12
DS_D[2,3] = 10
DS_D[3,1] = 11
DS_D[3,2] = 12
DS_D[3,3] = 13

# 需求提出和截止时间
D_TX = np.zeros((D+1,M+1),dtype=int)
D_TY = np.zeros((D+1,M+1),dtype=int)
D_TX[1,1] = 1
D_TY[1,1] = 3
D_TX[1,2] = 3
D_TY[1,2] = 7
D_TX[1,3] = 4
D_TY[1,3] = 5
D_TX[2,1] = 2
D_TY[2,1] = 3
D_TX[2,2] = 8
D_TY[2,2] = 9
D_TX[2,3] = 6
D_TY[2,3] = 10
D_TX[3,1] = 4
D_TY[3,1] = 7
D_TX[3,2] = 7
D_TY[3,2] = 8
D_TX[3,3] = 5
D_TY[3,3] = 6

# 需求量
D_A = np.zeros((D+1,M+1))
D_A[1,1] = 15
D_A[1,2] = 17
D_A[1,3] = 12
D_A[2,1] = 1
D_A[2,2] = 5
D_A[2,3] = 8
D_A[3,1] = 3
D_A[3,2] = 9
D_A[3,3] = 4

# 需求量的倒数
D_A_ = np.zeros((D+1,M+1))
D_A_[1,1] = 1/D_A[1,1]
D_A_[1,2] = 1/D_A[1,2]
D_A_[1,3] = 1/D_A[1,3]
D_A_[2,1] = 1/D_A[2,1]
D_A_[2,2] = 1/D_A[2,2]
D_A_[2,3] = 1/D_A[2,3]
D_A_[3,1] = 1/D_A[3,1]
D_A_[3,2] = 1/D_A[3,2]
D_A_[3,3] = 1/D_A[3,3]

# 库-库之间最大距离
R1 = 150
# 库-需求单位之间最大距离
R2 = 30


try:
    # Create a new model
    model = gp.Model("warehouseOP")

    r = model.addMVar((T+1, N+1), vtype=GRB.BINARY, name="r")
    f = model.addMVar((T+1, N+1), vtype=GRB.BINARY, name="f")
    RS_N = model.addMVar((T+1, N+1, N+1), vtype=GRB.BINARY, name="RS_N")
    RS_D = model.addMVar((T+1, N+1, D+1), vtype=GRB.BINARY, name="RS_D")
    N_L = model.addMVar((T+1, N+1, N+1, M+1), vtype=GRB.BINARY, name="N_L")
    N_LA = model.addMVar((T+1, N+1, N+1, M+1), vtype=GRB.INTEGER, lb=0, name="N_LA")
    D_L = model.addMVar((T+1, N+1, D+1, M+1), vtype=GRB.BINARY, name="D_L")
    D_LA = model.addMVar((T+1, N+1, D+1, M+1), vtype=GRB.INTEGER, lb=0, name="D_LA")

    LS_total = LS.sum()

    LB = zeros((T+1,N+1))
    E = zeros((T+1,N+1))
    I = zeros((T+1,N+1))
    for t in range(1,T+1):
        for i in range(1, N+1):
            E[t][i] = 0
            for m in range(1,M+1):
                for j in range(0,N+1):
                    E[t][i] = E[t][i] + N_L[t,j,i,m]*N_LA[t,j,i,m]*LP[m]
                for j in range(1,N+1):
                    E[t][i] = E[t][i] + N_L[t,i,j,m]*N_LA[t,i,j,m]*LP[m]
                for d in range(1,D+1):
                    E[t][i] = E[t][i] + D_L[t,i,d,m]*D_LA[t,i,d,m]*LP[m]
            I[t][i] = 0
            for t_ in range(1,t+1):
                for m in range(1, M+1):
                    for j in range(0, N+1):
                        I[t][i] = I[t][i] + N_L[t_, j, i, m] * N_LA[t_, j, i, m] * LP[m]
                    for j in range(1, N+1):
                        I[t][i] = I[t][i] - N_L[t_, i, j, m] * N_LA[t_, i, j, m] * LP[m]
                    for d in range(1, D+1):
                        I[t][i] = I[t][i] - D_L[t_, i, d, m] * D_LA[t_, i, d, m] * LP[m]
            LB[t][i] = E[t][i] + 12 * I[t][i]
    LB_total = 0
    for t in range(1,T+1):
        for i in range(1,N+1):
            LB_total = LB_total + LB[t][i]

    LD_N = zeros((N+1,N+1))
    LD_D = zeros((N+1,D+1))
    for i in range(1,N+1):
        for j in range(1,N+1):
            LD_N[i][j] = 0
            for t in range(1,T+1):
                for m in range(1,M+1):
                    LD_N[i][j] = LD_N[i][j] + N_LA[t,i,j,m] * N_L[t,i,j,m] * DS_N[i,j]
    for i in range(1,N+1):
        for d in range(1,D+1):
            LD_D[i][d] = 0
            for t in range(1,T+1):
                for m in range(1,M+1):
                    LD_D[i][d] = LD_D[i][d] + D_LA[t,i,d,m] * D_L[t,i,d,m] * DS_D[i,d]
    LD_total = 0
    for i in range(1,N+1):
        for j in range(1,N+1):
            LD_total = LD_total + LD_N[i][j]
    for i in range(1,N+1):
        for d in range(1,D+1):
            LD_total = LD_total + LD_D[i][d]

    LI_total = 0
    for t in range(1,T+1):
        for i in range(1,N+1):
            LI_total = LI_total + I[t][i]

    SR = zeros((D+1,M+1))
    for d in range(1,D+1):
        for m in range(1,M+1):
            for t in range(D_TX[d,m],D_TY[d,m]+1):
                for i in range(1,N+1):
                    SR[d][m] = SR[d][m] + D_L[t,i,d,m]*D_LA[t,i,d,m]
            SR[d][m] = SR[d][m] * D_A_[d,m]
    SR_total = 0
    for d in range(1,D+1):
        for m in range(1,M+1):
            SR_total = SR_total + SR[d][m]/(D*M)

    UR = zeros((T + 1, N + 1))
    for t in range(1, T + 1):
        for i in range(1, N + 1):
            for m in range(1,M+1):
                sum = 0
                for t_ in range(1, t + 1):
                    for j in range(0,N+1):
                        sum = sum + N_L[t_,j,i,m]*N_LA[t_,j,i,m]
                    for j in range(1, N + 1):
                        sum = sum - N_L[t_,i,j,m]*N_LA[t_,i,j,m]
                    for d in range(1, D + 1):
                        sum = sum - D_L[t_,i,d,m]*D_LA[t_,i,d,m]
                sum = sum * LS2[m]
                UR[t][i] = UR[t][i] + sum
            UR[t][i] = UR[t][i] / NS[i]
    UR_total = 0
    for t in range(1, T + 1):
        for i in range(1, N + 1):
            UR_total = UR_total + UR[t][i] / (T * N)


    total = LS_total+LB_total+LD_total+LI_total
    # Set objective - maximize number of queens
    model.setObjective(total, GRB.MINIMIZE)

    # Add constraints
    for t in range(1,T+1):
        for i in range(1,N+1):
            model.addConstr(r[t,i] + f[t,i] >= 1)

    for t in range(1,T+1):
        for i in range(1,N+1):
            model.addConstr(RS_N[t,0,i] * RS_N[t,i,0] == 1)

    for t in range(1,T+1):
        for j in range(1,N+1):
            sum = 0
            for i in range(1,N+1):
                sum = sum + RS_N[t,i,j]*f[t,i]
            model.addConstr(-MAX * r[t,j] <= sum)
            model.addConstr(sum <= MAX * r[t, j])

    for t in range(1, T + 1):
        for j in range(1, N + 1):
            sum = 0
            for i in range(1, N + 1):
                sum = sum + RS_N[t, i, j] * r[t, i]
            model.addConstr(1 - r[t, j] <= sum)
            model.addConstr(sum <= 1 - r[t, j])

    for t in range(1,T+1):
        for d in range(1,D+1):
            sum = 0
            for i in range(1,N+1):
                sum = sum + RS_D[t,i,d]*f[t,i]
            model.addConstr(0<=sum)
            model.addConstr(sum<=1)

    for t in range(1,T+1):
        for i in range(1,N+1):
            for j in range(1, N + 1):
                model.addConstr(RS_N[t,i,j] * DS_N[i,j] <= R1)

    for t in range(1,T+1):
        for i in range(1,N+1):
            for d in range(1, D + 1):
                model.addConstr(RS_D[t,i,d] * DS_D[i,d] <= R2)

    for t in range(1,T+1):
        sum = 0
        for i in range(1, N + 1):
            sum = sum + r[t,i]
        model.addConstr(sum == 1)

    for t in range(1,T+1):
        sum = 0
        for i in range(1, N + 1):
            sum = sum + f[t,i]
        model.addConstr(sum >= 1)

    for t in range(1,T+1):
        for j in range(1, N + 1):
            for m in range(1, M + 1):
                model.addConstr(N_L[t,0,j,m] == r[t,j] * RS_N[t,0,j])

    for t in range(1, T + 1):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                for m in range(1, M + 1):
                    model.addConstr(N_L[t, i, j, m] == RS_N[t, i, j])
                    model.addConstr(N_L[t, i, j, m] == r[t, i] * f[t, j])

    for t in range(1, T + 1):
        for i in range(1, N + 1):
            for d in range(1, D + 1):
                for m in range(1, M + 1):
                    model.addConstr(D_L[t, i, d, m] == f[t,i] * RS_D[t, i, d])

    for t in range(1, T + 1):
        for i in range(1, N + 1):
            for m in range(1, M + 1):
                sum1 = 0
                for j in range(1, N+1):
                    sum1 = sum1 + N_L[t,i,j,m]*N_LA[t,i,j,m]
                sum2 = 0
                for d in range(1, D + 1):
                    sum2 = sum2 + D_L[t,i,d,m]*D_LA[t,i,d,m]
                sum3 = 0
                if (t>=3):
                    for t_ in range(1,t-2+1):
                        sum31 = 0
                        for j in range(0, N+1):
                            sum31 = sum31 + N_L[t_,j,i,m]*N_LA[t_,j,i,m]
                        sum32 = 0
                        for j in range(1, N+1):
                            sum32 = sum32 + N_L[t_,i,j,m]*N_LA[t_,i,j,m]
                        sum33 = 0
                        for d in range(1, D+1):
                            sum33 = sum33 + D_L[t_,i,d,m]*D_LA[t_,i,d,m]
                        sum3 = sum3 + sum31 - sum32 - sum33
                model.addConstr(sum1+sum2<=sum3)

    for d in range(1, D + 1):
        for m in range(1, M + 1):
            model.addConstr(SR[d][m] >= 0.9)

    for t in range(1, T + 1):
        for i in range(1, N + 1):
            model.addConstr(UR[t][i] >= 0)
            model.addConstr(UR[t][i] <= 1.5)




    # Optimize model
    model.optimize()


    print_r_f(T,N,r.X, f.X)
    print("——————————————————————")
    # print_RS_N(T,N,RS_N.X)
    # print("——————————————————————")
    # print_RS_D(T, N, D, RS_D.X)
    # print("——————————————————————")
    print_N_LA(T, N, M, N_L.X, N_LA.X)
    print("——————————————————————")
    print_D_LA(T, N, D, M, D_L.X, D_LA.X)
    print("——————————————————————")
    print_LS_total(LS)
    print("——————————————————————")
    print_LB_total(T, N, M, D, N_L.X, N_LA.X, D_L.X, D_LA.X, LP)
    print("——————————————————————")
    print_LD_total(T,N,M,D,N_LA.X,N_L.X,D_LA.X,D_L.X,DS_N,DS_D)
    print("——————————————————————")
    print_LI_total(T, N, M, D, N_L.X, N_LA.X, D_L.X, D_LA.X, LP)
    print("——————————————————————")
    print_SR_total(T,N,M,D,D_TX,D_TY,D_L.X,D_LA.X,D_A_)
    print("——————————————————————")
    print_UR_total(T,N,M,D,N_L.X,N_LA.X,D_L.X,D_LA.X,LS2,NS)




except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))


