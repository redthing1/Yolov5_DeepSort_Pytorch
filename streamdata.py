import os
import sys
import time

INF = sys.argv[1]

with open(INF, 'rb') as f:
    # seek to end
    f.seek(-1, 2)

    # stream data line_data by line_data from the file
    done = False
    while not done:
        line_data = f.readline()
        if not line_data:
            time.sleep(0.016) # sleep for 16ms
        else:
            line_str = line_data.decode('utf-8').strip()
            print(f"DATA: {line_str}")
