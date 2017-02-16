from random import *


def rand_dist():
    answer = []
    a = randint(1, 10)
    print a
    answer.append(a)
    if a == 10:
        answer.append(0)
        answer.append(0)
    else:
        b = randint(1, 10-a)
        print b
        answer.append(b)
        if b+a == 10:
            answer.append(0)
        else:
            c = 10 - (a + b)
            print c
            answer.append(c)
    shuffle(answer)
    return answer
