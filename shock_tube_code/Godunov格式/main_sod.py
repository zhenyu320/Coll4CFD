import numpy as np
import matplotlib.pyplot as plt
import function as fc
# np.savetxt('e.csv', uu, delimiter=',')
N = 100          # 划分数
cfl = 0.1  # 科朗数
xmax = 1
xmin = -1
x = np.linspace(xmin, xmax, N+1)  # 划分x
xx = np.linspace(xmin, xmax, 100)
dx = (xmax-xmin)/N
n_dis = int(0.5*N)  # 不连续点下标
t_max = 0.2  # 时间
gamma = 1.4
param0 = [1, 0, 2.5, 0.125, 0, 0.25]  # 前三个为左侧气体的密度速度压强，后三个为右侧气体对应项
#param0 = [0.445, 0.698, 3.528, 0.5, 0.0, 0.571]
flag = 1
steps = 0
maxsteps = 1000
current_time = 0
# initial

u_0 = utt = fc.euler_generate(N, n_dis, *param0)  # 初始化原始量
u_vector = fc.physics_to_conservation(utt)  # 把原始量转化为守恒量
u_t = np.zeros((3, N+1))  # 不同时间的守恒量
# dF = np.zeros((3, N-1))  # flux的差分
c = np.sqrt(gamma*u_vector[2, :]/u_vector[0, :])  # 声速
dt = cfl*dx/max(abs(u_vector[1, :])+c)
dF = np.zeros((3, N+1))


while flag:
    # 初始化dt以及判断
    steps = steps+1
    u_0 = fc.consevation_to_physics(u_vector)
    c = np.sqrt(gamma*u_0[2, :]/u_0[0, :])  # 声速
    dt = cfl*dx/max(abs(u_0[1, :])+c)  # 时间步长
    if steps > maxsteps:
        print('warning: maxsteps reach')
        break
    if current_time+dt >= t_max:
        dt = t_max-current_time
        flag = 0
    current_time = current_time+dt

    u_vector = np.column_stack(
        (u_vector[:, 0], u_vector[:, 0], u_vector, u_vector[:, -1], u_vector[:, -1]))
    dF = fc.fluxDiscre(dx, dt, u_vector)  # 计算dF

    u_1 = u_vector[:, 2:-2]-dt*dF
    u_1 = np.column_stack((u_1[:, 0], u_1[:, 0], u_1, u_1[:, -1], u_1[:, -1]))
    dF = fc.fluxDiscre(dx, dt, u_1)  # 计算dF

    u_2 = 0.75*u_vector[:, 2:-2]+0.25 * u_1[:, 2:-2]-0.25*dt*dF
    u_2 = np.column_stack((u_2[:, 0], u_2[:, 0], u_2, u_2[:, -1], u_2[:, -1]))
    dF = fc.fluxDiscre(dx, dt, u_2)  # 计算dF
    u_t = 1/3*u_vector[:, 2:-2]+2/3*u_2[:, 2:-2]-2/3*dt*dF
    u_vector = u_t.copy()  # 更新
    # 先随时间推进，再计算边界，再计算dF,更新u_vector

uuu = np.loadtxt(open("/Users/jixingzhou/Desktop/python3.6/e.csv",
                      "rb"), delimiter=",", skiprows=0)

uu = fc.consevation_to_physics(u_t)

plt.figure(1)
plt.style.use("ggplot")
plt.plot(x, uu[0, :], color='b', marker='o')
plt.plot(xx, uuu[:, 0], '-r')
plt.xlabel('x')
plt.ylabel('density')
plt.savefig('g1', dpi=600, format='eps')

plt.figure(2)
plt.style.use("ggplot")
plt.plot(x, uu[1, :], color='b', marker='o')
plt.plot(xx, uuu[:, 1], '-r')
plt.xlabel('x')
plt.ylabel('velocity')
plt.savefig('g2', dpi=600, format='eps')

plt.figure(3)
plt.style.use("ggplot")
plt.plot(x, uu[2, :], color='b', marker='o')
plt.plot(xx, uuu[:, 2], '-r')
plt.xlabel('x')
plt.ylabel('pressure')
plt.savefig('g3', dpi=600, format='eps')

plt.show()
