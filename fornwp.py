import re
reg = "cat|dog"
s = "the cat ate the mouse"
s2 = "the dog ate the cat"
print(re.search(reg,s).group())
print(re.search(reg,s2).group())


def mymap(f,L):
    R = []
    for elem in L:
        R.append(f(elem))
    return R

def myfilter(f,L):
    R = []
    for elem in L:
        if f(elem):
            R.append(elem)
    return R

def reduce(f,L):
    if L == []:
        assert(False)
    if len(L) == 1:
        return L[0]
    r = f(L[0],L[1])
    for i in L[2:]:
        r = f(r,i)
    return r

def reducer(f,L):
    if L == []:
        assert(False)
    if len(L) == 1:
        return L[0]
    b = f(L[0],L[1])
    return reducer(f, [b] + L[2:])


A = [2, 4, 5, 6,7, 9]
B = ["i", "abe", "mnt"]

print(list(filter(lambda x: x%2 == 0 or x%5 == 0, A)))
vowels = myfilter(lambda x: x not in "aeiou", B)
print(list(vowels))
length = reducer(lambda x,y: x+1, [0]+ A)
average = reducer(lambda x, y: x+y, A)
mean = average / length
print(mean)
