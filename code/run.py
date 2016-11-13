from matplotlib import pyplot as plt
from CNLpendulum import NLpendulum
import numpy as np

a = NLpendulum()
the=[]
Fd=[]
for fd in np.arange(1.2, 1.6, 0.001):
    a.reset(FD=fd)
    a.calculate()
    the = the + a.b_the
    Fd = Fd + [fd]*len(a.b_the)

plt.plot(Fd, the, '.')
plt.ylim(1, 3)
plt.xlabel("$F_D$")
plt.ylabel(r"$\theta/rads$")