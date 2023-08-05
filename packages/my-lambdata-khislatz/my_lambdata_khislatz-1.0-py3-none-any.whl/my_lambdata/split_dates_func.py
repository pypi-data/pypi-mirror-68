import pandas as pd
import numpy as np

# Function to split dates ("MM/DD/YYYY", etc.) into multiple columns

def split_dates(my_df):

    new_df = my_df.copy()
    #Convert dob to datetime
    new_df['dob'] = pd.to_datetime(new_df['dob'], infer_datetime_format=True)
    #Extract components from DOB
    new_df['year'] = new_df['dob'].dt.year                  
    new_df['month'] = new_df['dob'].dt.month
    new_df['day'] = new_df['dob'].dt.day

    return new_df

if __name__ == "__main__":
    
    #Creating a dictionary
    dict = {'Name': ['John', 'Peter', 'Sam', np.nan],
            'Age': [30, np.nan, np.nan, 45],
            'Income': [100000, 75000, np.nan, 50000],
            'dob': ['01/01/1990', '04/25/1970', '12/19/2000', '05/02/1975']}

    #Creating a DataFrame from list
    df = pd.DataFrame(dict)
    print(df.head())

    df2 = split_dates(df)
    print(df2.head())