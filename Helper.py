# -*- coding: utf-8 -*-
# @Time : 2022/9/16 19:19
# @Author : PLZ
# @File : Helper.py
# @Software : PyCharm

def zeros(rowcol):
    result = [None] * rowcol[0]
    for i in range(len(result)):
        result[i] = [0] * rowcol[1]
    return result


def print_r_f(T,N, r, f):
    for t in range(1,T+1):
        for i in range(1,N+1):
            if r[t,i]==1 and f[t,i]==1:
                print(f'第{t}周：{i}号库类型是"区域库且周转库"')
            elif r[t,i]==0 and f[t,i]==1:
                print(f'第{t}周：{i}号库类型是"周转库"')
            elif r[t,i]==1 and f[t,i]==0:
                print(f'第{t}周：{i}号库类型是"区域库"')

def print_RS_N(T,N,RS_N):
    for t in range(1,T+1):
        for i in range(1,N+1):
            for j in range(1, N + 1):
                if RS_N[t,i,j]==1:
                    print(f'第{t}周：{i}号库与{j}号库相联系')

def print_RS_D(T,N,D,RS_D):
    for t in range(1,T+1):
        for i in range(1,N+1):
            for d in range(1, D + 1):
                if RS_D[t,i,d]==1:
                    print(f'第{t}周：{i}号库与{d}号需求单位相联系')

def print_N_LA(T, N, M, N_L, N_LA):
    for t in range(1,T+1):
        for i in range(0,N+1):
            for j in range(0, N + 1):
                for m in range(1, M + 1):
                    if N_L[t,i,j,m]==1 and N_LA[t,i,j,m]>0:
                        if i==0 and j==0:
                            print(f'第{t}周：供应商向供应商送了{N_LA[t, i, j, m]}个{m}号物料')
                        elif i==0 and j!=0:
                            print(f'第{t}周：供应商向{j}号库送了{N_LA[t, i, j, m]}个{m}号物料')
                        elif i!=0 and j==0:
                            print(f'第{t}周：{i}号库向供应商送了{N_LA[t, i, j, m]}个{m}号物料')
                        else:
                            print(f'第{t}周：{i}号库向{j}号库送了{N_LA[t,i,j,m]}个{m}号物料')

def print_D_LA(T, N, D, M, D_L, D_LA):
    for t in range(1,T+1):
        for i in range(0,N+1):
            for d in range(1, D + 1):
                for m in range(1, M + 1):
                    if D_L[t,i,d,m]==1 and D_LA[t,i,d,m] >0:
                        if i==0:
                            print(f'第{t}周：供应商向{d}号需求单位送了{D_LA[t, i, d, m]}个{m}号物料')
                        else:
                            print(f'第{t}周：{i}号库向{d}号需求单位送了{D_LA[t,i,d,m]}个{m}号物料')



def print_LS_total(LS):
    LS_total = LS.sum()
    print(f"租赁总成本：{LS_total}")

def print_LB_total(T,N,M,D,N_L,N_LA,D_L,D_LA,LP):
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
    print(f'运营总成本：{LB_total}')

def print_LD_total(T,N,M,D,N_LA,N_L,D_LA,D_L,DS_N,DS_D):
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
    print(f"配送总成本：{LD_total}")

def print_LI_total(T,N,M,D,N_L,N_LA,D_L,D_LA,LP):
    I = zeros((T + 1, N + 1))
    for t in range(1, T + 1):
        for i in range(1, N + 1):
            I[t][i] = 0
            for t_ in range(1, t + 1):
                for m in range(1, M + 1):
                    for j in range(0, N + 1):
                        I[t][i] = I[t][i] + N_L[t_, j, i, m] * N_LA[t_, j, i, m] * LP[m]
                    for j in range(1, N + 1):
                        I[t][i] = I[t][i] - N_L[t_, i, j, m] * N_LA[t_, i, j, m] * LP[m]
                    for d in range(1, D + 1):
                        I[t][i] = I[t][i] - D_L[t_, i, d, m] * D_LA[t_, i, d, m] * LP[m]
    LI_total = 0
    for t in range(1,T+1):
        for i in range(1,N+1):
            LI_total = LI_total + I[t][i]
    print(f"货物持有总成本：{LI_total}")

def print_SR_total(T,N,M,D,D_TX,D_TY,D_L,D_LA,D_A_):
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
    for d in range(1,D+1):
        for m in range(1,M+1):
            print(f"{d}号需求单位对{m}号物料的需求满足率：{SR[d][m]*100}%")
    print(f"总平均需求满足率：{SR_total*100}%")

def print_UR_total(T,N,M,D,N_L,N_LA,D_L,D_LA,LS2,NS):
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
    for t in range(1, T + 1):
        for i in range(1, N + 1):
            print(f"第{t}周：{i}号库的利用率为{UR[t][i]*100}%")
    print(f"平均仓库利用率：{UR_total*100}%")


