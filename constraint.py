# Author: YUHongfei
# CreatTime: 2022/9/15
# FileName: constraint
# Description: 约束条件

"""
仓库类型：
仓库i在t时刻不能既不是区域库也不是周转库(i>=1)
 r_ti + f_ti >= 1

辐射关系：
周转库j只能跟一个区域库存在联系，区域库可以链接多个周转库，供应商可以链接所有库
 RS_N_t0i * RS_N_ti0 == 1
 - MAX * r_tj <= sum(i=1~N)(RS_N_tij * f_ti) <= MAX * r_tj
 1 - r_tj <= sum(i=1~N)(RS_N_tij * r_ti) <= 1 - r_tj
一个需求单位d只能与一个周转库存在联系
 sum(i=1~N)(RS_D_tid * f_ti) == 1 #TODO 注意0.9
 sum(i=1~N)(RS_D_tid * r_ti) == 0

距离关系：
两点间距离有上限(i、j>=1)
 RS_N_tij * DS_N_ij <= R1
 RS_D_tid * DS_D_id <= R2

仓库数量：
暂时考虑只有一个区域库(i、j>=1)
 sum(i=1~N)(r_ti) == 1
 sum(i=1~N)(f_ti) >= 1

货运关系：
限制供应商送区域库，区域库送周转库，周转库送需求单位
 N_L_t0jm == r_tj * RS_N_t0j
 N_L_tijm == r_ti * f_tj
 N_L_tijm == RS_N_tij
 D_L_tidm == f_ti * RS_D_tid

抽检两周：
到货后需库存2周才能发货
 sum(j=1~N)(N_L_tijm * N_LA_tijm) + sum(d=1~D)(D_L_tidm * D_LA_tidm) <=
   sum(t=1~t-2)( sum(j=0~N)(N_L_tjim * N_LA_tjim) - sum(j=1~N)(N_L_tijm * N_LA_tijm)
    - sum(d=1~D)( D_L_tidm * D_LA_tidm ) )

需求满足率：
至少要大于90%
0.9 <= SR_dm

"""
