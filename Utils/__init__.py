"""
Utility function for plotting analysis results
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import statsmodels.api as sm

def plot_scatter(
        df: pd.DataFrame = None,
        change_date: str = '2023-01-29',
        plot_x: str = 'temperature',
        plot_y: str = 'consumption'
        ):
    pre_X = np.array(df.loc[:change_date][plot_x]).reshape(-1, 1)
    pre_y = df.loc[:change_date][plot_y]
    post_X = np.array(df.loc[change_date:][plot_x]).reshape(-1, 1)
    post_y = df.loc[change_date:][plot_y]
    pre_curtain_consumption = LinearRegression().fit(pre_X, pre_y)
    print(f"Pre R2 score: {pre_curtain_consumption.score(pre_X, pre_y):.3f}")
    
    print(f"Model post with pre model R2 score: {pre_curtain_consumption.score(post_X, post_y):.3f}")
    pre_m, pre_b = (pre_curtain_consumption.coef_, pre_curtain_consumption.intercept_)
    
    print(f"Pre-curtain coefficient: {pre_m[0]:.3f}")
    print(f"Pre-curtain intercept: {pre_b:.3f}")
    pre_mod = sm.OLS(pre_y, pre_X)
    pre_fii = pre_mod.fit()
    pre_p_values = pre_fii.summary2().tables[1]['P>|t|']

    post_curtain_consumption = LinearRegression().fit(post_X, post_y)
    print(f"Post R2 score: {post_curtain_consumption.score(post_X, post_y):.3f}")
    post_m, post_b = (post_curtain_consumption.coef_, post_curtain_consumption.intercept_)

    print(f"Post-curtain coefficient: {post_m[0]:.3f}")
    print(f"Post-curtain coefficient: {post_b:.3f}")

    post_mod = sm.OLS(post_y, post_X)
    post_fii = post_mod.fit()
    post_p_values = post_fii.summary2().tables[1]['P>|t|']

    plt.scatter(
        df.loc[:change_date][plot_x], 
        df.loc[:change_date][plot_y], 
        s=4)
    plt.scatter(
        df.loc[change_date:][plot_x], 
        df.loc[change_date:][plot_y], 
        s=4)
    plt.plot(pre_X, pre_m*pre_X+pre_b, c='blue', lw=1)
    plt.plot(post_X, post_m*post_X+post_b, c='orange', lw=1)
    plt.grid()
    plt.show()

    print(pre_p_values)
    print( post_p_values)
