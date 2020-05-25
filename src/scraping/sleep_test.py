import time
from random import randint

for i in range (1, 25):
    t = randint(1,3)
    print(f'Sleep for {t} sec')
    time.sleep(t)