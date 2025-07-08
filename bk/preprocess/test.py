import numpy as np

s = np.array([1, 6, 16, 31, 61, 101, 201])
layer = [0, 5, 15, 30, 60, 100, 200, float('inf')]
for i in range(7):
    print('the layer is')
    print(i)
    s1 = np.where((s>=layer[i]) & (s<layer[i+1]), (s-layer[i])*10, 0)
    print(s1)
    print(s1.min(),s1.max())

    s1 = np.where((s>=layer[i]) & (s<layer[i+1]), 1, 0)
    print(s1)
    print(s1.min(),s1.max())
    print(f'DTB_{layer[i]}_{layer[i+1]}.nc')