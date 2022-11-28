from exp_mod import exp_mod

class RSA:

    def __init__(self, p, q, e):
        self.p = p
        self.q = q
        self.e = e
        self.n = p * q
        self.d = modInverso(self.e, (self.p-1)*(self.q-1))

        # if (_ehPrimo(p)):
        #     self.p = p
        # if (_ehPrimo(q)):
        #     self.q = q
        # if(_ehPrimo(p) and _ehPrimo(q)):
        #     self.n = p * q
        # if (self.p and self.q and _eh_coprimo(e, (self.p-1)*(self.q-1))):
        #     self.e = e
            
        #     self.d = modInverso(self.e, (self.p-1)*(self.q-1))

    def getChavePublica(self):
        return (self.n, self.e)
    
    def getChavePrivada(self):
        return self.d

def modInverso(a, m):
    m0 = m
    y = 0
    x = 1
 
    if (m == 1):
        return 0
 
    while (a > 1):
 
        q = a // m
 
        t = m
 
        m = exp_mod(a, 1, m)
        a = t
        t = y
 
        y = x - q * y
        x = t
    if (x < 0):
        x = x + m0
 
    return x

def _ehPrimo(num):
    i=2
    while i < num:
        if exp_mod(num, 1, i)== 0:
            return False
        i+=1
    if num<=1:
        return False
    return True

def _mdc(num1, num2):
    if(num2==0):
        return num1
    else:
        return _mdc(num2, exp_mod(num1, 1, num2))

def _eh_coprimo(num1, num2):
    if num1 < num2:
        if _mdc(num2, num1)==1:
            return True
        else:
            return False
    else:
        if _mdc(num1, num2)==1:
            return True
        else:
            return False