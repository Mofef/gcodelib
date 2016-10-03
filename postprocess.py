import sys
import numpy as np

from gcodelib import line_from_dict, dict_from_line

if len(sys.argv) != 3:
    print "please specify input and outputfile as commandline arguments. E.g.:\n python postprocess.py infile.gcode outfile.gcode"
    exit(1)

f = open(sys.argv[1])
my_text = f.readlines()
f.close()

center = np.asarray((129.0, 96.0))
radius = 16.5  # 17
well_height = 80

def inside_cylinder(state):
    position = np.asarray((state["X"], state["Y"]))
    return np.linalg.norm(position - center) < radius

def below_surface(state):
    return state["Z"] < well_height


current_state = {"X": 0., "Y": 0., "Z": 200.}
old_state = current_state.copy()
unfiltered_state = current_state.copy()
first_run = True
i = 0
while i < len(my_text):
    line = my_text[i]
    if line.startswith("G1 ") or line.startswith("G0 "):
        state_update = dict_from_line(line)
        unfiltered_state.update(state_update)
        new_state = current_state.copy()
        new_state.update(state_update)

        if not inside_cylinder(new_state) and (inside_cylinder(old_state) or first_run):  # entering critical area from the side
            if below_surface(old_state) or first_run:
                my_text.insert(i, "G1 Z" + str(well_height))
                try:
                    state_update.update({"Z": max(well_height, state_update["Z"])})
                except KeyError:
                    pass
                my_text[i + 1] = line_from_dict(state_update)
                i += 1
        if below_surface(new_state) and not below_surface(old_state):  # entering  critical area from above
            if not inside_cylinder(old_state):
                state_update.pop("Z")
                my_text[i] = line_from_dict(state_update)

        current_state.update(state_update)

        if inside_cylinder(current_state):
            current_state.update(unfiltered_state)
            my_text[i] = line_from_dict(unfiltered_state)
        old_state = current_state.copy()
        first_run = False
    i += 1

outfile = open(sys.argv[2], "w")
outfile.writelines(my_text)
outfile.close()