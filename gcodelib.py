def line_from_dict(d):
    line = "G1 "
    for k in d:
        v = d[k]
        line += k
        line += str(v)
        line += " "
    line = line[:-1] + "\n"
    return line

def dict_from_line(line):
    state = dict()
    tokens = line[3:].split(" ")
    for token in tokens:
        state[token[0]] = float(token[1:])
    return state

def line_reader(lines):
    current_state = {"X": 0., "Y": 0., "Z": 200.}
    unfiltered_state = current_state.copy()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("G1 ") or line.startswith("G0 "):
            state_update = dict_from_line(line)
            unfiltered_state.update(state_update)
            new_state = current_state.copy()
            new_state.update(state_update)

            current_state.update(state_update)
            yield current_state
        i += 1
