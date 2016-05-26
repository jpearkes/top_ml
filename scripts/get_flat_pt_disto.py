import numpy as np 
from pprint import pprint
import matplotlib as mpl
import matplotlib.pyplot as plt

#x = np.load("master_numpy_array.npz")
x = np.load("../outputs/zprime400_000001jet_inv_mass.npz")
y = x['data']
#y = y[0:5,:]

print(y.shape)
rows,cols = y.shape
max_count = 100

# pt bins 
class bin:
    """Bin checker """
    count = 0 
    start = 0
    stop = 0
    full = False

    def __init__(self, start, stop):
        self.count = 0 
        self.start = start
        self.stop = stop
    def in_bin(self, number):
        if(number>=self.start and number< self.stop):
            self.count += 1
            if self.count > max_count:
                self.full = True
            return True
        else:
            return False
    def is_full(self):
        if self.count < max_count:
            return False 
        if self.count >= max_count:
            self.full = True
            return True 
    def print_object(self):
        print("["+str(self.start)+","+str(self.stop)+")")
        print("Count:"+str(self.count))
        print("Full? "+str(self.full))
n_bins = 10
lst = [bin(i*100,i*100+100) for i in range(n_bins)]
new_array = np.zeros((1,2))
#print(new_array)

for row in xrange(rows):
    print(y[row][0][0])
    if row == 0:
        #print(y[row])
        new_array = y[row]
        #print("----------------------------------")
        #print(new_array)
        [lst[i].in_bin(y[0][0][0]) for i in range(n_bins)]
    else:
        for i in range(n_bins):
            if(lst[i].in_bin(y[row][0][0]) and not lst[i].full):
                #print(y[row])
                new_array = np.vstack((new_array,y[row]))
                #print("----------------------------------")

rows,cols = new_array.shape
print("new array:")
#print(new_array)
print(new_array.shape)
for row in xrange(rows):
    print(new_array[row][0][0])

[lst[i].print_object() for i in range(n_bins)]

# Make font size small
#mpl.rcParams.update({'font.size': 8})

# for col in range(0,30):
#     [value, wrong_value] = split (data, data[:,col]!=-999.0)
#     print "Number of -999s = "+str(wrong_value.size)
#     [real_signal, real_background] = split(value, value[:,-1] == 1.0)
#     print "real_background weights"
#     print real_background[:,-2]
#     print "real_signal weights"
#     print real_signal[:,-2]
#     if (int(col%6) == 0):
#         plt.cla()
#         plt.figure(figure_num)
#         figure_num += 1 

#print([new_array[i][0][0] for i in range(rows)])
min_x_calc = 0
max_x_calc = 1000
binwidth = (max_x_calc - min_x_calc) / n_bins
print "min_x_calc: " + str(min_x_calc)
print "max_x_calc: " + str(max_x_calc)
print "binwidth: "+ str(binwidth)
plt.plot()
p1 = plt.hist([new_array[i][0][0] for i in range(rows)],
              #range=[min_x_calc,max_x_calc],
              bins = np.arange(min_x_calc, max_x_calc + binwidth, binwidth),
              #weights = [real_background[:,-2],real_signal[:,-2]],
              label = ['signal'],
              linewidth = 0.0, 
              edgecolor = None,
              #histtype = 'barstacked',
              color = 'blue',
              alpha = 0.5 )
              
plt.legend(loc=1,prop={'size':6})
#plt.title(header[col+1])
plt.xlabel("Value")
plt.ylabel("Counts/Bin")

x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2,y1,y2+10))
#plt.text(0.0, 500, 'Number of invalid points:'+str(m-count[col]), fontsize=6)

# eta
plt.savefig("../plots/test"+".png")
plt.cla()
plt.figure(1)
#print([new_array[i][0][0] for i in range(rows)])
min_x_calc = -3
max_x_calc = 3
binwidth = 0.1
n_bins = (max_x_calc - min_x_calc) / binwidth

print "min_x_calc: " + str(min_x_calc)
print "max_x_calc: " + str(max_x_calc)
print "binwidth: "+ str(binwidth)
plt.plot()
p1 = plt.hist([new_array[i][0][1] for i in range(rows)],
              #range=[min_x_calc,max_x_calc],
              bins = np.arange(min_x_calc, max_x_calc + binwidth, binwidth),
              #weights = [real_background[:,-2],real_signal[:,-2]],
              label = ['signal'],
              linewidth = 0.0, 
              edgecolor = None,
              #histtype = 'barstacked',
              color = 'blue',
              alpha = 0.5 )
              
plt.legend(loc=1,prop={'size':12})
#plt.title(header[col+1])
plt.xlabel("Value")
plt.ylabel("Events")

x1,x2,y1,y2 = plt.axis()
plt.axis((min_x_calc,max_x_calc,y1,y2+5))
#plt.text(0.0, 500, 'Number of invalid points:'+str(m-count[col]), fontsize=6)

plt.savefig("../plots/test2"+".png")

plt.show()





