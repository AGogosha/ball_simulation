import numpy as np
import pandas as pd
import scipy.integrate as spi 
import matplotlib
import matplotlib.pyplot as plt
#Plot Function
def plot_paths(radius,paths,init_durations,init_velocities):
    plt.subplots(3,2, figsize = (12,9))
    q = np.linspace(0, 2*np.pi, 100)
    l = 'abcdef'
    j=0
    for i in range(len(paths)):
        plt.subplot(2, 3, j+1)
        plt.title('(' + l[j - 1] + ')', y = -0.01)
        plt.axis('off')
        plt.xlim(-radius, radius)
        plt.ylim(-radius, radius)
        plt.plot(np.cos(q), np.sin(q), color='black', linewidth = 1)
        plt.axis('equal')
        plt.scatter(-0.5*radius , 0, color='black')
        s = '$v_0 = ' + str(init_velocities[j]) + '\; m/s$' + '\n' + '$+$\n $T = $' + str(init_durations[j]) + ' $s$'
        plt.text(0, 0, s, horizontalalignment = 'center', verticalalignment = 'center')
        plt.plot(paths[i][0], paths[i][1], color = 'black', linewidth = 2)
        j+=1
    plt.show()
def data_read_3(file_names):
    path_out=[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]
    temp=[]
    for i in range(len(file_names)):
        if file_names[i].endswith(".csv"):
            temp.append(pd.read_csv(file_names[i],header=0))
    for j in range(len(temp)):
        columns_list = list(temp[j])
        print(j,columns_list)
        for k in range(len(temp[j][columns_list[0]])):
            temp_1=float(temp[j][columns_list[0]][k])
            temp_2=float(temp[j][columns_list[1]][k])           
            path_out[j][0].append(temp_1)
            path_out[j][1].append(temp_2)
    return path_out
if __name__ == "__main__":         
    delt_t=0.0001
    R=1
    pos_init=[-0.5*R,0,0]
    init_vel=[[0,1.5,0],[0,0.8,0],[0,0.45,0],[0,0.328,0],[0.33234,0.33234,0],[0.200111,0.200111,0]]
    init_velocities=[1.5,0.8,0.45,0.328,0.47,0.283]
    init_durations=[0.86,2.9,17.3,5,3.83,3.3]
    omega=[0,0,1]
    paths=data_read_3(["out 0.csv","out 1.csv","out 2.csv","out 3.csv","out 4.csv","out 5.csv"])
    plot_paths(R,paths,init_durations,init_velocities)