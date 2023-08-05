def enlarge(n):
    return n * 100
    

if __name__ == "__main__": #if we use it the rest of the file my_mode will not be executed
    #only run the code below if executing this script 
    # from the command line
    #otherwise don't run it (for example if we are trying 
    # to import something)

    x = 5 
    print(enlarge(x))

    y = int(input('Please choose a number(e.g. 5): '))
    print(enlarge(y))