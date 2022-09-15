# Author: YUHongfei
# CreatTime: 2022/9/15
# FileName: main
# Description:

# 代码中出现的字符含义
"""
下标

 i（0-N）、j（0-N）：仓库编号 （其中0代表供应商）
 t（1-T）：时间编号
 m（1-M）：物料类型编号
 d（1-D）：需求单位编号
"""

"""
决策量

 仓库类型
 r_ti：t时刻仓库i是否为区域库（1/0）
 f_ti：t时刻仓库i是否为周转库（1/0）

 辐射关系 RelationShip
 RS_N_tij：t时刻仓库i与仓库j之间是否有联系（1/0）
 RS_D_tid：t时刻仓库i与需求单位d之间是否有联系（1/0）
 
 仓库间货运关系
 N_L_tijm：t时刻仓库i是否能给仓库j送物料m（1/0）
 N_LA_tijm：t时刻仓库i给仓库j送物料m的数量（整数）
 
 仓库-需求单位货运关系
 D_L_tidm：t时刻仓库i是否能给需求单位d送物料m（1/0）
 D_LA_tidm：t时刻仓库i给需求单位d送物料m的数量（整数）
"""


"""
目标函数

 成本
 LS：租赁成本
 LB：运营成本
 LD：配送成本
 LI：存货持有成本
 
 利用率 Usage Ratio
 UR_ti：t时刻仓库i利用率
 U_ti：t时刻仓库i利用面积
"""

"""
常量

 距离 DiStance 
 DS_N_ij：库-库距离
 DS_D_id：库-需求距离
 R1：库-库间最大距离
 R2：库-需求单位间最大距离
 
 需求 Demand
 D_A_dm：需求单位d对物料m的需求总数量
 D_TX_dm：需求单位d对物料m的需求提出时间
 D_TY_dm：需求单位d对物料m的需求截止时间
 
 物料 Load
 LS_m：单位物料m的面积
 LP_m：单位物料m的金额
 LW_m：单位物料m的重量
 
 仓库
 NS_i：仓库i容量的面积
 
 MAX：一个大常量
 MIN：一个小常量
"""