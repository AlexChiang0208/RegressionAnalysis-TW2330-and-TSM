from pandas_datareader import DataReader as dr
import pandas as pd

# 抓取十年股價資料
start = '2011-01-01'
end = '2020-12-31'
TW_2330 = dr('2330.TW','yahoo',start,end)['Adj Close']
TSM = dr('TSM','yahoo',start,end)['Adj Close']

# 取出共同的交易日
TSM = TSM[list(TW_2330.index)].dropna(how='all')
TW_2330 = TW_2330[list(TSM.index)].dropna(how='all')
list(TW_2330.index) == list(TSM.index)

# 把 TSM 往前移一天～「讓同一天 TSM 比 TW_2330 早開盤」
TSM = TSM.shift(1)
TW_2330 = TW_2330[1:]

# 計算每日報酬率
TSM_ret = ((TSM - TSM.shift(1)) / TSM.shift(1)).dropna(how='all')
TW_2330_ret = ((TW_2330 - TW_2330.shift(1)) / TW_2330.shift(1)).dropna(how='all')

# 製作 DataFrame
TSM_ret = TSM_ret.rename('X_TSM')
TW_2330_ret = TW_2330_ret.rename('Y_2330')
df_XY = pd.concat([TW_2330_ret, TSM_ret], axis=1)

TSM = TSM[1:].rename('TSM')
TW_2330 = TW_2330.rename('TW_2330')
df_price = pd.concat([TW_2330, TSM], axis=1)

# 儲存成 csv
address = '/Users/alex_chiang/Documents/迴歸分析/期中_簡單迴歸/Data/'
df_XY.to_csv(address+'Regression_XY_data.csv')
df_price.to_csv(address+'StockPrice.csv')
#%%

# 去除離群值

import matplotlib.pyplot as plt
import statsmodels.api as sm

# Simple Regression Model
# https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html 

x = sm.add_constant(df_XY['X_TSM']) # 新增常數項：Y=ax+b
Y = df_XY['Y_2330']
reg_model = sm.OLS(Y, x)
result = reg_model.fit()
result.summary()

# Create instance of influence
influence = result.get_influence()

# Obtain Cook's distance for each observation
cooks = influence.cooks_distance
cooks_df = pd.DataFrame(cooks[0], index=df_XY.index)

def plot_cooks_distance(c):
    _, ax = plt.subplots(figsize=(9,6))
    ax.stem(c, markerfmt=",")
    ax.set_xlabel("instance index")
    ax.set_ylabel("influence")
    ax.set_title("Cook's Distance Outlier Detection")    
    return ax

plot_cooks_distance(cooks_df[0])

large_influence_date = cooks_df[cooks_df.iloc[:,0] > 4/len(cooks_df)].index
df_remove_inf = df_XY.drop(index=large_influence_date)

address = '/Users/alex_chiang/Documents/迴歸分析/期中_簡單迴歸/Data/'
df_remove_inf.to_csv(address+'RemoveOutliers_XY_data.csv')
