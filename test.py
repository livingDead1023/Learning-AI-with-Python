def XOR(a, b):
    return (not a or not b) and (a or b)

def XNOR(a, b):
    return not((not a or not b) and (a or b))

def test_batch(a,b):
    print(f"XOR({a},{b}): {XOR(a,b)}")
    print(f"XNOR({a},{b}): {XNOR(a,b)}")

a = [0,1]
b = [0,1]

for i in enumerate(a):
    for j in enumerate(b):
        test_batch(i[1],j[1])
