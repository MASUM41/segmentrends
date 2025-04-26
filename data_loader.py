import pandas as pd
def load_customer_data(filepath='Synthetic_Customers_with_Age__Income__SpendingScore__Email.csv'):
    return pd.read_csv(filepath)
