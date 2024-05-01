# MICROL CHEN - TCHE284 
# THIS CODE WAS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING ANY SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR.  

# Question 7
# In class, we shifted from left to right, but I decided to implement LFSR from right to left to avoid having to reverse the state every iteration.
class lfsr():
    def generate(self, n, seed, tap):
        state = seed
        while True:
            yield (state >> (n-1)) & 1 
                    # leftmost bit  # isolate
            feedback = (state >> (n-1)) ^ (state >> tap) & 1 
                    # leftmost bit        # tap bit          #isolate
            state = (state << 1 | feedback) & ((1 << n) - 1)
                    # removeleft most - add feedback ++ create a mask to prevent overflow

# Test
'''
n = 5  # Number of bits
seed = 0b01111  # Initial seed
tap = 2  # Tap position

n = 5  # Number of bits
seed = 0b01111  # Initial seed
tap = 4  # Tap position

n = 4  # Number of bits
seed = 0b01001  # Initial seed
tap = 1  # Tap position

lfsr_instance = lfsr()
bits_generator = lfsr_instance.generate(n, seed, tap)
bits = [next(bits_generator) for _ in range(20)]
print(bits)
'''
