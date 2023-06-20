import pickle
import numpy as np

def Extract(lst,idx1,idx2):
    return [item[idx1][idx2] for item in lst]

data = pickle.load(open('orbit_data_3.p', 'rb'))
print(np.average(Extract(data,1,13)))
