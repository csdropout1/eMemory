# MICROL CHEN - TCHE284 
# THIS CODE WAS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING ANY SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR.  

'''
Consider all possible curves of the form y2 = x3 + ax + b over the field GF(103) where a
and b ∈ GF(103). Write a program that will find the order of all elliptic curves with different values of a; b ∈ {0, 1,
2, ...., 102}. All arithmetic is performed mod 103. List 10 pairs of a and b parameters for which the curve order is
prime and the largest.
'''

def curve_x(x, a, b, p):
    r = pow(x,3) + a*x + b
    r = r % p
    return r

def curve_y(y, p):
    r = pow(y, 2)
    r = r % p
    return r

def find_order(): # Main Function in the assignment, finds the order of all a and b pairs
    orders = {}
    for a in range(103):
        for b in range(103):
            num_orders = 0
            book_x = {}
            book_y = {}
            for x in range(103):
                t = curve_x(x, a, b, 103)
                if t in book_x:
                    book_x[t].append(x)
                else:
                    book_x[t] = []
                    book_x[t].append(x)
            for y in range(103):
                u = curve_y(y, 103)
                if u in book_y:
                    book_y[u].append(y)
                else:
                    book_y[u] = []
                    book_y[u].append(y)
            
            points = set(book_x.keys())&set(book_y.keys())
            for item in points:
                num_orders += len(book_x[item]) * len(book_y[item])
            orders[(a,b)] = num_orders+1 # neutral element
    # print(orders)
    return orders

o = find_order()
inv_map = {v: k for k, v in o.items()}
s = [x for x in inv_map.keys()]
s.sort(reverse = True)
large_primes = []

def is_prime(n):
    for i in range(n):
        if i == 0 or i == 1:
            pass
        else:
            if n%i == 0:
                return False
    return True

for i in s:
    if is_prime(i):
        large_primes.append(i)
        if len(large_primes) == 10:
            break

def find_pairs(): # finds 10 pairs of a and b that has the largest prime number of orders
    res = []
    while 1:
        if len(large_primes) != 0:
            tar = large_primes.pop(0)
        else:
            return res

        for i in o.keys():
            if o[i] == tar:
                res.append(i)
                if len(res) == 10:
                    return res

pairs = find_pairs()
print(pairs)