# FAMA 三因子
# 作者 科大财经 

import pandas as pd
import numpy as np
import tqdm

# 计算 HML SMB
SMB_total = pd.DataFrame()
HML_total = pd.DataFrame()
for i in tqdm(range(len(month_date)-1)):
    start = pd.to_datetime(str(month_date[i]))
    end = pd.to_datetime(str(month_date[i+1]))
    all_price_change_rate_single_priod = all_price_change_rate.loc[start:end]
    #price_change_rate_singal_priod = price_change_rate.loc[start:end]
    single_priod = hml_base[hml_base.date == month_date[i]].set_index(['order_book_id','date']).dropna()
    single_priod = single_priod.sort_values('mc') #市值升序排布
    S = single_priod.index[:int(len(single_priod.index)/2)].get_level_values(0)
    B = single_priod.index[int(len(single_priod.index)/2):].get_level_values(0)
    single_priod = single_priod.sort_values('pb') #净市率升序排列
    L = single_priod.index[:int(len(single_priod.index)*0.3)].get_level_values(0)
    M = single_priod.index[int(len(single_priod.index)*0.3):int(len(single_priod.index)*0.7)].get_level_values(0)
    H = single_priod.index[int(len(single_priod.index)*0.7):].get_level_values(0)

    portfolio = {}
    portfolio['SL'] = list(set(S).intersection(set(L)))
    portfolio['SM'] = list(set(S).intersection(set(M)))
    portfolio['SH'] = list(set(S).intersection(set(H)))
    portfolio['BL'] = list(set(B).intersection(set(L)))
    portfolio['BM'] = list(set(B).intersection(set(M)))
    portfolio['BH'] = list(set(B).intersection(set(H)))

    # 市值加权求出每个类别的日收益率时间序列
    portfolio_return = {}
    for por in portfolio:
        portfolio_return[por] = 0
        for stock in portfolio[por]:
            portfolio_return[por] += single_priod['mc'][stock].values*all_price_change_rate_single_priod[stock].fillna(0)
        portfolio_return[por] = portfolio_return[por]/np.sum(single_priod['mc'][portfolio[por]])

    SMB = ((portfolio_return['SL']+portfolio_return['SM']+portfolio_return['SH'])/3-(portfolio_return['BL']+portfolio_return['BM']+portfolio_return['BH'])/3).iloc[:-1]
    HML = ((portfolio_return['SH']+portfolio_return['BH'])/2-(portfolio_return['SL']+portfolio_return['BL'])/2).iloc[:-1]
    #Rb = price_change_rate_singal_priod['000001.XSHG']-price_change_rate_singal_priod['risk_free_rate']
    SMB_total = pd.concat([SMB_total,SMB],axis = 0)
    HML_total = pd.concat([HML_total,HML],axis = 0)