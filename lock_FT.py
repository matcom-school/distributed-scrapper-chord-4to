import sys
from deamon import Deamon

d = Deamon(1, port_base=int(sys.argv[1]))

list_ = []
for i in range(2, len(sys.argv)):
    list_.append(int(sys.argv[i]))

list_.sort()
print(list_)
for i in list_:
    d.sendTo(i, (1, 1, 1, ('finger_table', ())))
