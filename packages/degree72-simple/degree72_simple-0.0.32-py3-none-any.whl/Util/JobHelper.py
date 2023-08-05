import os


def debug():
    return not (os.getenv('PRODUCTION') == 'TRUE')


def get_stack_frame(stack, frame_trace_num=0):  # the order of frame you want to trace
    frames = []
    switch = True
    temp = ''
    for each in stack:
        path = each[1]
        folder = os.path.basename(os.path.dirname(path)) # folder name of **.py
        if folder in ['Core', 'Util']:
            continue
        elif switch:
            temp = folder
            switch = False
        if temp == folder:
            frames.append(each)

    return frames[frame_trace_num]
