
from pandas import DataFrame 
from my_lambdata.my_mod import enlarge #this works



print ('Hello')

df = DataFrame({'a':[1,2,3], 'b':[4,5,6]})

print(df.head())

x = 11 
print(enlarge(x)) #importing only enlarge function
#if we use from my_mod import enlarge without "if __name__ == "__main__":"
# then the entire file my_mod will be executed 

