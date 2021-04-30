import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

address = '/Users/alex_chiang/Documents/迴歸分析/期中_簡單迴歸/Data/'
df = pd.read_csv(address+'Regression_XY_data.csv', parse_dates=True, index_col='Date')

#1 ACF 檢驗樣本之間是否有時間相依性
kwargs = dict(alpha=0.05, color='orangered', markersize=2, linewidth=0.8)
sm.graphics.tsa.plot_acf(df['X_TSM'], lags=2368, **kwargs)


#2 Simple Regression Model
# https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html 

x = sm.add_constant(df['X_TSM']) # 新增常數項：Y=ax+b
Y = df['Y_2330']
reg_model = sm.OLS(Y, x)
result = reg_model.fit()
result.summary()

# Estimation
y_hat = result.fittedvalues # y hat
result.params # a, b hat


#3 OLS Picture
fig = plt.figure()
plt.xlabel("TW_2330")
plt.ylabel("TSM")
plt.title("Simple Linear Regression", fontsize=15)
plt.scatter(x['X_TSM'], Y, alpha=0.5)
plt.plot(x, y_hat, color = "red")
plt.xlim(-0.1, 0.1)
plt.ylim(-0.1, 0.1)
plt.show()


#4 Residuals
residuals = result.resid.to_frame("Residuals")
residuals.describe()

# Standardized Residuals
Standardized_residuals = residuals/residuals.std()
Standardized_residuals.rename(columns={"Residuals":"Standardized Residuals"}, inplace=True)
Standardized_residuals.describe()

sm.stats.stattools.durbin_watson(residuals)


#5 各種殘差圖
# 標準化殘差直方圖
Standardized_residuals.hist(bins = 80)

# 標準化殘差盒鬚圖
Standardized_residuals.boxplot(vert=False)

# 標準化殘差圖
plt.figure(figsize = (10,6))
plt.scatter(df['X_TSM'],Standardized_residuals, alpha=0.6)
plt.axhline(2, color="red")
plt.axhline(0, color="black", alpha=0.3)
plt.axhline(-2, color="red")
plt.xlabel('X_TSM', fontsize=15)
plt.ylabel('Standardized Residuals', fontsize=15)
plt.show()

# 標準化殘差的 q-q plot 解釋常態性
percentile_100 = []
for i in range(1,101,1):
    percentile_100.append(np.percentile(Standardized_residuals,i))
percentile_100 = pd.DataFrame(percentile_100)

sm.qqplot(percentile_100, dist="norm", line="r")
#%%
# 去除離群值後

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

address = '/Users/alex_chiang/Documents/迴歸分析/期中_簡單迴歸/Data/'
df = pd.read_csv(address+'RemoveOutliers_XY_data.csv', parse_dates=True, index_col='Date')

#1 ACF 檢驗樣本之間是否有時間相依性
kwargs = dict(alpha=0.05, color='orangered', markersize=2, linewidth=0.8)
sm.graphics.tsa.plot_acf(df['X_TSM'], lags=2254, **kwargs)


#2 Simple Regression Model
# https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html 

x = sm.add_constant(df['X_TSM']) # 新增常數項：Y=ax+b
Y = df['Y_2330']
reg_model = sm.OLS(Y, x)
result = reg_model.fit()
result.summary()

# Estimation
y_hat = result.fittedvalues # y hat
result.params # a, b hat


#3 OLS Picture
fig = plt.figure()
plt.xlabel("TW_2330")
plt.ylabel("TSM")
plt.title("Simple Linear Regression", fontsize=15)
plt.scatter(x['X_TSM'], Y, alpha=0.5)
plt.plot(x, y_hat, color = "red")
plt.xlim(-0.1, 0.1)
plt.ylim(-0.1, 0.1)
plt.show()


#4 Residuals
residuals = result.resid.to_frame("Residuals")
residuals.describe()

# Standardized Residuals
Standardized_residuals = residuals/residuals.std()
Standardized_residuals.rename(columns={"Residuals":"Standardized Residuals"}, inplace=True)
Standardized_residuals.describe()


#5 各種殘差圖
# 標準化殘差直方圖
Standardized_residuals.hist(bins = 80)

# 標準化殘差盒鬚圖
Standardized_residuals.boxplot(vert=False)

# 標準化殘差圖
plt.figure(figsize = (10,6))
plt.scatter(df['X_TSM'],Standardized_residuals, alpha=0.6)
plt.axhline(2, color="red")
plt.axhline(0, color="black", alpha=0.3)
plt.axhline(-2, color="red")
plt.xlabel('X_TSM', fontsize=15)
plt.ylabel('Standardized Residuals', fontsize=15)
plt.show()

# 標準化殘差的 q-q plot 解釋常態性
percentile_100 = []
for i in range(1,101,1):
    percentile_100.append(np.percentile(Standardized_residuals,i))
percentile_100 = pd.DataFrame(percentile_100)

sm.qqplot(percentile_100, dist="norm", line="r")
