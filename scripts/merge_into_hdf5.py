import h5py
import glob
import numpy as np
from pprint import pprint
files = ["test_dijet_array2.npz"] #glob.glob("../zprime3000_000001jet_inv_mass.npz")
#files = ["test_dijet_array3.npz"]#,"test_dijet_array3.npz"]
files = glob.glob("test_dijet_array[2-9].npz")
print(files)
f = h5py.File("mytestfile2.hdf5", "w")
#dset = f.create_dataset("my_data_set", (100,2), dtype='f')
#dset = f.create_dataset("autochunk", (100000, 150), chunks=True, dtype='f')
#dset = f.create_dataset("resizable", (1000,60), maxshape=(5000, 20))

offsets = [0]
for i in range(len(files)):
    file_name = files[i]
    print("loading" +file_name)
    x = np.load(file_name)
    print("done loading, getting size")
    rows, cols= x['arr_0'].shape
    offsets.append(rows)
print(offsets)
total = sum(offsets)
print(total)
dt = h5py.special_dtype(vlen=np.dtype('f'))
dset = f.create_dataset('vlen_float', (total,), dtype=dt)


#dset = f.create_dataset('vlen_float', (1000,), dtype=dt)

for i in range(len(files)):
    file_name = files[i]
    print("loading file"+file_name)
    x = np.load(file_name)
    print("done loading, setting data")
    data = x['arr_0']
    print("done setting data")
    rows, cols = data.shape
    print(len(data))
    print(data.shape)
    
    print("dataset")
    for row in range(rows):
        #dset[row,0:3] = data[row][0][:]#.append(data[row][1])m#this works
        #dset[row,3:9] = data[row][1][:][:] #thsi doesn't
        #print("data")
        #print(data[row][0])#.extend(data[row][1]))
        #print(data[row][1])
        #pprint(np.append(data[row][0],data[row][1]))
        dset[row+offsets[i]] = np.append(data[row][0],data[row][1]) 
        if (row%10000==0):
            print(row)
            #print(len(data[row][1]))
        '''
        for j in range(len(data[row][1])):
            dset[row,3+3*j:6+3*j] = data[row][1][j][:]
            #print("ho")
        '''
        #dset[row] = data[row]
        #dset[row,3:] = data[row][1][:]
        #dset[row,0,:] = data[row][0][:] #data[row][0][:]
        #dset[row,1,:] = data[row][1][:]
        #pprint(dset[row])


'''

for i in range(len(files)):
    file_name = files[i]
    print("loading file")
    x = np.load(file_name)
    print("done loading, setting data")
    data = x['arr_0']
    print("done setting data")
    rows, cols = data.shape
    print(len(data))
    print(data.shape)
    dset = f.create_dataset('vlen_float', (rows,), dtype=dt)
    print("dataset")
    for row in range(rows):
        #dset[row,0:3] = data[row][0][:]#.append(data[row][1])m#this works
        #dset[row,3:9] = data[row][1][:][:] #thsi doesn't
        #print("data")
        #print(data[row][0])#.extend(data[row][1]))
        #print(data[row][1])
        #pprint(np.append(data[row][0],data[row][1]))
        dset[row] = np.append(data[row][0],data[row][1])


        
        if (row%1000==0):
            print(row)
            #print(len(data[row][1]))
        
        for j in range(len(data[row][1])):
            dset[row,3+3*j:6+3*j] = data[row][1][j][:]
            #print("ho")
        
        #dset[row] = data[row]
        #dset[row,3:] = data[row][1][:]
        #dset[row,0,:] = data[row][0][:] #data[row][0][:]
        #dset[row,1,:] = data[row][1][:]
        #pprint(dset[row])
'''        
