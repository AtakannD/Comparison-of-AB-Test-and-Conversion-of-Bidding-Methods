import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, \
    spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.multicomp import MultiComparison

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Task 1

df_control = pd.read_excel(
    r"C:\Users\atakan.dalkiran\PycharmProjects\Comparison of Conversion of Bidding Methods with AB Testing\ab_testing.xlsx",
    sheet_name="Control Group")
df_test = pd.read_excel(
    r"C:\Users\atakan.dalkiran\PycharmProjects\Comparison of Conversion of Bidding Methods with AB Testing\ab_testing.xlsx",
    sheet_name="Test Group")
df_control["group"] = "control"
df_test["group"] = "test"


def check_df(dataframe, head=5):
    """
    This function gives us a first look when we import our dataset.

    Parameters
    ----------
    dataframe: pandas.dataframe
    It is the dataframe from which variable names are to be drawn.
    head: int
    The variable that determines how many values we want to look at first when browsing the data set we have.

    Returns
    -------
    shape: tuple
    it gives us how many rows and how many columns our dataset consists of.
    type: pandas.series
    gives us the datatypes of our variables in our dataset.
    head: pandas.Dataframe
    It gives us the variables and values of our dataset, starting from the 0th index to the number we entered,
    as a dataframe.
    tail: pandas.Dataframe
    Contrary to head, this method counts us down starting from the index at the end.
    isnull().sum(): pandas.series
    It visits the variables in our data set and checks if there are any null values and, gives us the statistics
    of how many of them are in each variable.
    quantile: pandas.dataframe
    It gives the range values of the variables in our data set as a percentage according to the values we entered.

    Examples
    --------
    The output of shape return is given to us as a tuple (5000, 5).
    """
    print("######################### Shape #########################")
    print(dataframe.shape)
    print("\n######################### Type #########################")
    print(dataframe.dtypes)
    print("\n######################## Columns ########################")
    print(dataframe.columns)
    print("\n######################### Head #########################")
    print(dataframe.head(head))
    print("\n######################### Tail #########################")
    print(dataframe.tail(head))
    print("\n######################### NA #########################")
    print(dataframe.isnull().sum())
    print("\n######################### Quantiles #########################")
    print(dataframe.quantile([0, 0.25, 0.5, 0.75, 0.95, 1]).T)


check_df(df_test)
check_df(df_control)

df = pd.concat([df_test, df_control], ignore_index=True, sort=False)

# Task 2

# HO: M1 = M2 (There is no statistically significant difference in terms of purchasing averages in the control
#               and test groups.)
# H1: M1 !=M2

df.groupby("group").agg({"Purchase": "mean"})

# Task 3

# Normality Assumptions

test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
# p-value > 0.05, H0 can not reject.

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
# p-value > 0.05, H0 can not reject.

# Variance Homogeneity

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
# p-value > 0.05, H0 can not reject.

# T-testing

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
# H0 can not reject.
# There is no statistically significant difference in terms of purchasing averages in the control and test groups.
