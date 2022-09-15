# Author: YUHongfei
# CreatTime: 2022/9/15
# FileName: objective
# Description:目标函数

"""
租赁成本
 LS = sum(i=1~N)(LS_i)

运营成本：
 LB = sum(t=1~T)(LB_t)
 LB_t = 0.036 * (E_t + 12 * I_t)^0.82
 E_t = sum(m=1~M) (sum(j=0~N)(N_L_tjim * N_LA_tjim * LP_m)
                 + sum(j=1~N)(N_L_tijm * N_LA_tijm * LP_m)
                 + sum(d=1~D)(D_L_tidm * D_LA_tidm * LP_m) )

 I_t =  sum(t=1~t) (sum(m=1~M) (sum(j=0~N)(N_L_tjim * N_LA_tjim * LP_m)
                              - sum(j=1~N)(N_L_tijm * N_LA_tijm * LP_m)
                              - sum(d=1~D)(D_L_tidm * D_LA_tidm * LP_m) ) )

配送成本：
 LD_ij = sum(t=1~T) ( sum(m=1~M) ( (N_LA_tijm * N_L_tijm * DS_N_ij
                                 + D_LA_tijm * D_L_tijm * DS_D_ij) * LW_m * 2 ) )
 LD = sum(i=1~N) ( sum(j=1~N) (LD_ij) )

货物持有成本：
 LI =sum(t=1~T)( I_t )

需求满足率：
 SR_dm = sum(t=D_TX_dm~D_TY_dm)( sum(i=1~N) ( D_L_tidm * D_LA_tidm )) / D_A_dm
"""