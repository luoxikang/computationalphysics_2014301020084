# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 22:11:35 2016

@author: Administrator
"""

import os
import time
import numpy as np
from matplotlib import pyplot as plt


a = """
  ### #                            #            #    
  #   #     ###     ###   ###   ## #            #      ##   ##
   #  #### #   #   #   # #   #  #  #### #  #    #     #### ####
    # #  # #   #   #   #  ####   # #  # #  #    #     #    #
  ### #  #  ###### #   #     #  ## #  # ####    #####  ###  ###
                             #
                          ###
"""

b = a.split('\n')
for j in range(10):
    for i in range(len(b)-1):
        b[i] = "   " + b[i]
        print b[i]
    time.sleep(0.1)
    c = os.system("clear")


