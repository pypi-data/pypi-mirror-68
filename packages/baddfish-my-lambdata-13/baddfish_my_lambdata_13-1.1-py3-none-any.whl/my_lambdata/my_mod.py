

# my_lambdata/my_mod.py

def enlarge(n):
    """
    Param n is a number
    Function will enlarge the number
    """
    return n * 100
    

if __name__ == "__main__":
    # only run the code below IF this script is envoked in the command line
    # not if it is imported from another
    print("Hello there")
    y = int(input("Please choose a number"))
    print(y, enlarge(y))

## Helper and main helper functions

def helper(x, n):
    if (x > n):
        return x - n
    else:
        return x

def main():
    x = 10

    # do something that changes x
    x = helper(x, 2)
    # now x has changed 