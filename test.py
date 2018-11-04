import pandas as pd
import skinematics as skin
from skinematics.sensors.manual import MyOwnSensor
from skinematics.sensors.xsens import XSens
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skinematics import imus
import numpy as np

def show_result(imu_data):
  "Dummy function, to simplify the visualization"

  fig, axs = plt.subplots(3, 1)
  axs[0].plot(imu_data.omega)
  axs[0].set_ylabel('Omega')
  axs[0].set_title(imu_data.q_type)
  axs[1].plot(imu_data.acc)
  axs[1].set_ylabel('Acc')
  axs[2].plot(imu_data.quat[:, 1:])
  axs[2].set_ylabel('Quat')
  plt.show()


in_file = r"/Users/sid/Downloads/happy2.csv"

data = pd.read_csv(in_file)

acc = data.iloc[:, 5:8].values
omega = data.iloc[:, 9:12].values
rate = 100
mag = data.iloc[:, 12:15].values

def draw_histogram(i):
  hist, bin_edges = np.histogram(acc[..., i])
  n, bins, patches = plt.hist(x=acc[..., i], bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
  plt.grid(axis='y', alpha=0.75)
  plt.xlabel('Value')
  plt.ylabel('Frequency')
  plt.title('My Very Own Histogram')
  plt.text(23, 45, r'$\mu=15, b=3$')
  maxfreq = n.max()
  # Set a clean upper y-axis limit.
  plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
  plt.show()


for i in {0,1,2}:
  # draw_histogram(i)
  for j in range(len(acc[..., i])):
    if acc[j, i] > -0.25 and acc[j,i] < 0.25:
      acc[j, i] = acc[j, i] * 0.001
    elif -0.5 < acc[j, i] < -0.25 and 0.25 < acc[j,i] < 0.5:
      acc[j, i] = acc[j, i] * 0.7
    else:
      acc[j, i] = acc[j, i] * 0.9

  # draw_histogram(i)

in_data = {'rate': rate, 'acc': acc, 'omega': omega, 'mag': mag}

def show():
  fig = plt.figure()
  # plt.plot(my_sensor.pos[:,0],-my_sensor.pos[:,1])
  ax = fig.add_subplot(111, projection='3d')
  ax.plot(my_sensor.pos[:, 0], my_sensor.pos[:, 1], my_sensor.pos[:, 2])
  plt.show()



my_sensor = MyOwnSensor(in_data=in_data, q_type='madgwick')
show()
# my_sensor.quat = data.iloc[:, 3:7].values
# my_sensor.calc_position()
# show()

