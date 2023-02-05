#Import Statements
import numpy as np
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
    
#Fist timestep Position
def first_pos(zero_pos,zero_vel,zero_acel,timestep):
    return zero_pos+zero_vel*timestep+zero_acel*np.square(timestep)/2

#Position Function
def next_pos(pos_cur,pos_prev,a_cur,timestep):
    return 2*pos_cur-pos_prev+a_cur*np.square(timestep)

#Velocity Function
def cal_vel(cur_pos,prev_pos,timestep):
    vel_out=[]
    for i in range(len(prev_pos)):
        vel_out.append((cur_pos[i]-prev_pos[i])/timestep)
    return vel_out 

#Acceleration Function
def cal_accel(omega,pos,rad_vel):
    return-np.cross(omega,np.cross(omega,pos))-2*np.cross(omega,rad_vel)

#Calculate the path
def cal_path(init_pos,init_vel,omega,timestep,duration):
    a0=cal_accel(omega,init_pos,init_vel) #calculate initial acceleration
    path=[[init_pos[0]],[init_pos[1]],[0]] #the path the particle takes
    path[0].append(first_pos(init_pos[0],init_vel[0],a0[0],timestep)) #update path with the second position
    path[1].append(first_pos(init_pos[1],init_vel[1],a0[1],timestep))
    loop_length=int((duration+timestep)/timestep) #calculates how long the simulation will run for
    
    for i in range(0,loop_length):
        cur_pos=[path[0][-1],path[1][-1]]
        prev_pos=[path[0][-2],path[1][-2]]
        
        if i==0: #fist loop to use inital values given in function call
            cur_vel=cal_vel(cur_pos,prev_pos,timestep) #calculates the current velocity based on the previous acceleration and velocity
            cur_accel=cal_accel(omega,cur_pos,cur_vel) #calculates the current acceleration based on the previous position and velocity
            path[0].append(next_pos(cur_pos[0],prev_pos[0],cur_accel[0],timestep)) #update path
            path[1].append(next_pos(cur_pos[1],prev_pos[1],cur_accel[1],timestep))
            
        else:
            #print("prev vel {}".format(prev_vel))
            cur_vel=cal_vel(cur_pos,prev_pos,timestep)# same steps as above but based on previously calculated values
            cur_accel=cal_accel(omega,cur_pos,cur_vel)
            path[0].append(next_pos(cur_pos[0],prev_pos[0],cur_accel[0],timestep))
            path[1].append(next_pos(cur_pos[1],prev_pos[1],cur_accel[1],timestep))
            
    return path #returns the calculated path

def run_sim(rad,omega,timestep,init_position,init_velocities,duration):
    path_out=[] 
    for i in range(len(init_velocities)):
        path_out.append(cal_path(init_position,init_velocities[i],omega,timestep,duration[i]))
    return path_out

if __name__=="__main__":
    #set constants
    delt_t=0.0001
    R=1
    pos_init=[-0.5*R,0,0]
    init_vel=[[0,1.5,0],[0,0.8,0],[0,0.45,0],[0,0.328,0],[0.33234,0.33234,0],[0.200111,0.200111,0]]
    init_velocities=[1.5,0.8,0.45,0.328,0.47,0.283]
    init_durations=[0.86,2.9,17.3,5,3.83,3.3]
    omega=[0,0,1]
    paths=run_sim(R,omega,delt_t,pos_init,init_vel,init_durations)
    plot_paths(R,paths,init_durations,init_velocities)