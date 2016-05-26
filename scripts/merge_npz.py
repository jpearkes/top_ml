import numpy as np
import glob

files = glob.glob("../outputs/*zprime*/*npz")
print(files)

i = 0
for file_name in files:
    info = np.load(file_name)
    if i == 0:
        array = info['data']
    else:
        array = np.vstack((array, info['data']))
    i +=1 
    print(i)
np.savez("master_zprime_array", array)
print("done saving")