# State abbreviation -> Full Name and visa versa. FL -> Florida, etc. (Handle Washington DC and territories like Puerto Rico etc.)
from pandas import DataFrame 

def add_state_names(my_df):

    # Plan: 
    # add a column of corresponding state names
    # dict with abbreviation/name mapping 
    # create a new column that is a copy of the first, but mapped with names 
    # concat with axis=1 
    new_df = my_df.copy()

    names_map = {"CA": "California", "CT":"Connecticut", "CO": "Colorado", 
                "DC": "District of Columbia", "TX": "Texas", "FL": "Florida",
                "NY": "New York"}

    new_df['name'] = new_df['abbrev'].map(names_map) #  type(my_df['abbrev'])
    #we created a new column 'name' which was added to the existing dataframe
    # that had one column abbrev

    #breakpoint(): helps to stop and investigate in terminal up to the breakpoint()function

    return new_df


if __name__ == "__main__":

    df = DataFrame({"abbrev":["CA", "CT", "CO", "DC", "TX", "FL", "NY"]})
    print(df.head())

    df2 = add_state_names(df)
    print(df2)