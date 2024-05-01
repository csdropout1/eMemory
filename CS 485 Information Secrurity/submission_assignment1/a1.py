# MICROL CHEN - TCHE284 
# THIS CODE WAS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING ANY SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR.  

# Qestion 1
## PART A Code
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ct = "wsgeaeiqof ol q rtetfzkqsomtr qfr rolzkowxztr rouozqs strutk zteifgsgun ziqz tfqwstl ltexkt, zkqflhqktfz, qfr zqdhtk ktlolzqfz ktegkr atthofu gy zkqflqezogfl qekgll q ftzvgka gy egdhxztkl Oz ltkctl ql zit xfrtksnofu zteifgsgun ygk cqkogxl eknhzgexkktfeotl vozi Wozegof wtofu zit yoklz qfr dglz vtss- afgvf qhhsoeqzogf Igvtctk, zit hgztfzoqs qhhsoeqzogfl gy wsgeaeiqof tbztfr yqk wtngfr eknhzgexkktfeotl odhqezofu cqkogxl ofrxlzkotl" 

b = [0]* len(a)
abc = dict.fromkeys(a, 0)
ct = ct.lower()
extra = [' ', ',','.','!', '-', '?']

def part_a():
    
    total = 0
    for i in range(len(ct)):
        if ct[i] in extra:
            continue
        else:
            abc[ct[i]] += 1
            total += 1


    freq = dict.fromkeys(abc)
    for key in abc.keys():
        freq[key] = float(abc[key]/total)

    ## PART A
    sorted_freq = sorted(freq.items(), key=lambda x:x[1])
    for x in sorted_freq:
        print(x)

''' Frequency for Ciphered Messege
('j', 0.0)
('p', 0.0)
('b', 0.0026954177897574125)
('m', 0.0026954177897574125)
('c', 0.01078167115902965)
('d', 0.01078167115902965)
('a', 0.013477088948787063)
('v', 0.013477088948787063)
('n', 0.016172506738544475)
('y', 0.016172506738544475)
('w', 0.018867924528301886)
('u', 0.0215633423180593)
('x', 0.02425876010781671)
('i', 0.026954177897574125)
('h', 0.03234501347708895)
('r', 0.03773584905660377)
('s', 0.03773584905660377)
('e', 0.05929919137466307)
('l', 0.0646900269541779)
('g', 0.07277628032345014)
('q', 0.07547169811320754)
('k', 0.07816711590296496)
('f', 0.08355795148247978)
('o', 0.08355795148247978)
('z', 0.09164420485175202)
('t', 0.10512129380053908)
'''

## PART B
def part_b():
    let_freq = [0.0817, 0.0150, 0.0278, 0.0425, 0.1270, 0.0223, 0.0202, 0.0609, 0.0697, 0.0015, 0.0077, 0.0403, 0.0241, 0.0675, 0.0751, 0.0193, 0.0010, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007]
    e_freq = dict(zip(a, let_freq)) 
    sorted_efreq = sorted(e_freq.items(), key=lambda x:x[1])
    # for x in sorted_efreq:
    #     print(x)

    translation_attempt = {}
    for i in range(26):
        translation_attempt[sorted_efreq[i][0]] = sorted_efreq[i][0]
        # print(sorted_efreq[i][0], sorted_freq[i][0])
    
    translation_attempt["l"] = "s"
    translation_attempt["q"] = "a"
    translation_attempt["f"] = "n"
    translation_attempt["r"] = "d"
    translation_attempt["s"] = "l"
    translation_attempt["i"] = "h"
    translation_attempt["u"] = "g"
    translation_attempt["y"] = "w"
    translation_attempt["e"] = "c"
    translation_attempt["g"] = "o"
    translation_attempt["k"] = "r"
    translation_attempt["o"] = "i"
    translation_attempt["a"] = "k"
    translation_attempt["w"] = "b"
    translation_attempt["x"] = "u"
    translation_attempt["h"] = "p"
    translation_attempt["d"] = "m"
    translation_attempt["y"] = "f"
    translation_attempt["c"] = "v"
    translation_attempt["v"] = "w"
    translation_attempt["b"] = "x"
    translation_attempt["t"] = "e"
    translation_attempt["z"] = "t"

    deciphered = ''
    for i in range(len(ct)):
        if ct[i] in extra:
            deciphered += ct[i]
        else:
            deciphered += translation_attempt[ct[i]]
    print(deciphered)


''' THE DECIPHERED MESSEGE
blockchain is a decentralized and distributed digital ledger technology that enables secure, transparent, and tamper 
resistant record keeping of transactions across a network of computers it serves as the underlying technology for various 
cryptocurrencies with bitcoin being the first and most well- known application however, the potential applications of blockchain 
extend far beyond cryptocurrencies impacting various industries
'''

# Question 2
class caesar():
    
    def __init__(self):
        self.a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.abc = {}
        for i in range(26):
            self.abc[a[i]] = i
    
    def encrypt(self, string, key):
        string = string.lower()
        l = len(string)
        cipher = ''
        for i in range(l):
            if string[i] in self.a:
                t = (self.abc[string[i]]+key) %26
                if t > -1:
                    cipher += self.a[t]
                else: ## edge cases if key integers are negative numbers
                    while t <0:
                        t += 26
                    cipher += self.a[t]
            else:
                cipher += string[i]
        return cipher
    
    def decrypt(self, string, key):
        string = string.lower()
        l = len(string)
        decipher = ''
        for i in range(l):
            if string[i] in self.a:
                t = (self.abc[string[i]]-key)
                if t > -1 and t < 26:
                    decipher += self.a[t]
                elif t > 25: ### edge cases if key are too large or negative numbers
                    while t > 25:
                        t -= 26
                    decipher += self.a[t]
                else:
                    while t <0:        
                        t += 26
                    decipher += self.a[t]
            else:
                decipher += string[i]
        return decipher

class affine():
    def __init__(self):
        self.a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.abc = {}
        for i in range(26):
            self.abc[self.a[i]] = i

    def encrypt(self, string, key):
        l = len(string)
        string = string.lower()
        cipher = ''
        if key[0] not in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
            raise ValueError("KEY IS NOT COPRIME!!! INVALID KEY")
        else:
            for i in range(l):
                if string[i] in self.a:
                    t = ((self.abc[string[i]]) * key[0]) + key[1] %26
                    if t > -1 and t < 26:
                        cipher += self.a[t]
                    elif t < -1:
                        while t < -1:
                            t += 26
                        cipher += self.a[t]
                    else:
                        while t > 25:
                            t -= 26
                        cipher += self.a[t]
                else:
                    cipher += string[i]
            return cipher
        
    def decrypt(self, string, key):
        l = len(string)
        string = string.lower()
        decipher = ''
        
        q = 26 + 1 ### Finding inverse ~ 1 mod 26
        r = 0
        while q != 0:
            if q < 1:
                q += 26
            else:
                q -= (key[0])
                r += 1


        for i in range(l):
            if string[i] in self.a:    
                t = ((self.abc[string[i]]) - key[1]) *r
                if t > -1 and t < 26:
                    decipher += self.a[t]
                elif t > 25: 
                    while t > 25:
                        t -= 26
                    decipher += self.a[t]
                else:
                    while t <0:        
                        t += 26
                    decipher += self.a[t]        
            else:
                decipher += string[i]
        return decipher

def test():
    # part_a()
    # part_b()

    c = caesar()
    a = c.encrypt('Would you be my valentine 2024', 36)
    print(f'Ciphered Text: {a}')
    print(c.decrypt(a, 36))
            
    af = affine()
    m = af.encrypt('No I will not be your valentine 2024', (5, 7))
    print(f'Ciphered Text: {m}')
    print(af.decrypt(m, (5, 7)))

test()