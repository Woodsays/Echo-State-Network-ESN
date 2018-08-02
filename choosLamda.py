import numpy as np  
from ESN import *
import matplotlib.pyplot as plt
from function import *
import math

"""
Investigation of Regularization Parameter
"""



def choose(object,timeshift,x):
    
    print('**---------------timeshift==%d----------------**'
    %timeshift)
    error=[]
    para=0
    object.update(u_train,1)
    temp1=object.allstate
    temp1=discard(temp1)

    object.update(u_valid,0) 
    temp2=object.allstate
    print(temp2)
    print(np.shape(temp2))
    temp2=discard(temp2)
    # esn=ESN(n_inputs=1,n_outputs=1,sparsity=0.1)
    # esn.initweights()
    for lamda in x:
        y=10**lamda
        object.allstate=temp1
        object.fit(u_train,u_target,y,0)
        object.allstate=temp2
        object.predict(1)
        err=object.err(object.outputs,u_true,1)
        print('lamda==',lamda,'err==',err)
        error.append(err)
    
    minE=np.min(error)

    para=x[np.argmin(error)]
    print('timeshift==',timeshift,
        'choose parameter==',para,
        'minError===',minE)



    plt.plot(x,error,label='timeshift=%d'%timeshift)
    #esn.mydel()
    return minE,para


u1=Lorenz((1,1,1),len=100000)  # already discarded the transient
u1.downsample()
u1.normalize()
u1=u1.get()


u2 = Lorenz((5,-3,3),len=100000)
u2.downsample(10)
u2.normalize()
u2=u2.get()


esn=ESN(n_inputs=1,n_outputs=1,sparsity=0.1)
esn.initweights()
err=[]
para=[]
timerange=np.arange(-10,11)
x=np.linspace(-8, 8, num=200)   
plt.subplot(211)
plt.title('ESN')
plt.xlabel('lamda')
plt.ylabel('NMSE')

for timeshift in timerange:
    u_train=u1[0][12:-12-timeshift]
    u_target=u1[0][12+timeshift:-12]
    u_valid=u2[0][12:-12-timeshift]
    u_true=u2[0][12+timeshift:-12]
    u_true=discard(u_true)
    error,lamda=(choose(esn,timeshift,x))
    err.append(error)
    para.append(lamda)

lesn=LESN(n_inputs=1,n_outputs=1,sparsity=0.1)
lesn.initweights()
err_lesn=[]
plt.subplot(212)
plt.title('Linear Reservoir')
plt.xlabel('lamda')
plt.ylabel('NMSE')
for timeshift in timerange:
    u_train=u1[0][12:-12-timeshift]
    u_target=u1[0][12+timeshift:-12]
    u_valid=u2[0][12:-12-timeshift]
    u_true=u2[0][12+timeshift:-12]
    u_true=discard(u_true)
    temp,lamda=(choose(lesn,timeshift,x))
    err_lesn.append(temp)





plt.figure()
plt.plot(timerange,err,label='error of ESN')
plt.plot(timerange,err_lesn,label='error of Linear Reservoir')
plt.title('NMSE of ESN and Linear Reservoir regarding lambda')
plt.xlabel('lambda')
plt.ylabel('NMSE')




"""

Result:

parameter================== 

[-8.0, -8.0, -5.0875562639840055, -7.6242008082560009, -8.0, -7.9060502020639998, -5.6512550516000051, -6.0270542433440042, -7.
9060502020639998, -6.2149538392160038, -5.8391546474720046, -3.8662088908160088, -8.0, -2.3630121238400115, -5.3694056577920053, -4.9936064660480062, -5.27
5455859856006, -4.9936064660480062, -0.2021667713120161, -3.0206607093920104]


error===================== 
[1.8114845499291468, 0.41751749456385878, 0.17290615016411601, 0.15066139938276638, 0.065537416857594732, 0.022472596397571366,
0.0069058321931869211, 0.0038446718884230491, 0.02064286507786833, 0.01444615382904439, 0.0050213075260660996, 0.0099552650896471626, 0.13679334334598675,
0.4113828509941847, 2.1905427932752244, 3.4343613861461666, 5.1325539857315832, 35.492762217880781, 83.72624606909288, 72.780154407157326]


"""
print('parameter==================',para)
print('error=====================',err)

plt.show()