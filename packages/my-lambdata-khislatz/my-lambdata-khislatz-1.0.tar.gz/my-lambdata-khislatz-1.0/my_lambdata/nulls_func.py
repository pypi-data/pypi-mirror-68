
import numpy as np 
import pandas as pd

#Check a dataframe for nulls, print/report them in a nice "pretty" format

def check_nulls(my_df):
    
    new_df = my_df.copy()

    # using isnull() function   
    new_df = new_df.isna()

    return new_df


if __name__ == "__main__":
    #Creating a dictionary
    dict = {'Name': ['John', 'Peter', 'Sam', np.nan],
            'Age': [30, np.nan, np.nan, 45],
            'Income': [100000, 75000, np.nan, 50000]}

    #Creating a DataFrame from list
    df = pd.DataFrame(dict)
    print(df.head())

    df2 = check_nulls(df)
    print(df2.head())
  
