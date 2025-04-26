from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import pandas as pd

def prediction(df,userinput,n_clusters=3):
    # reg = LinearRegression()
    # reg.fit(df[['Age', 'Income']],df['SpendingScore'])
    # return reg.predict(userinput)
    X = df[['Age', 'Income', 'SpendingScore']]
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X)
    return kmeans.predict(userinput)


