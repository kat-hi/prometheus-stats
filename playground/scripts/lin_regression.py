import numpy as np
import os
from json_converter import write_np_x_array

for file in os.listdir('../data/'):
    x = write_np_x_array(file)

write_np_y_array():
