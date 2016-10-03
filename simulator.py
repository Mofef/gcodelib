import sys
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

from gcodelib import line_reader

if len(sys.argv) != 2:
    print "please specify gcode file you want to plot as commandline argument. E.g.:\n python postprocess.py model.gcode"
    exit(1)

f = open(sys.argv[1])
gcode = f.readlines()
f.close()


## 3D

def update_line(state):
    xdata.append(state["X"])
    ydata.append(state["Y"])
    zdata.append(state["Z"])
    #line.set_data(np.asarray([xdata, ydata, zdata]))
    line.set_data(xdata, ydata)
    line.set_3d_properties(zdata)

fig = plt.figure()
ax = p3.Axes3D(fig)
xdata, ydata, zdata = [0,0], [0,0], [0,0]
line = ax.plot(xdata, ydata, zdata,"-")[0]
ax.set_xlim3d([90.0, 130.0])
ax.set_xlabel('X')
ax.set_ylim3d([90.0, 130.0])
ax.set_ylabel('Y')
ax.set_zlim3d([0.0, 4.0])
ax.set_zlabel('Z')
ani = animation.FuncAnimation(fig, update_line, line_reader(gcode), blit=False, interval=1, repeat=True)

plt.show()


## 2D

fig, ax = plt.subplots()
xdata, ydata = [], []
line, = ax.plot(xdata, ydata)
ax.set_ylim(0, 200)
ax.set_xlim(0, 200)
ani = animation.FuncAnimation(fig, update_line, line_reader(gcode), blit=False, interval=10, repeat=True)

plt.show()

