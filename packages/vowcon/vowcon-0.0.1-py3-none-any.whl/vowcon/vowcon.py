def vowels(x):
    x.split()
    c=0
    l=['a','e','i','o','u']
    for i in x:
        if i in l:
            c=c+1
    return c
def consonants(x):
    x.split()
    c=0
    l=['a','e','i','o','u']
    for i  in x:
        if i not in l:
            c=c+1
    return c
