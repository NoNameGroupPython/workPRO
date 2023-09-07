import pandas as pd
import numpy as np
import os

def read_from_file(filename, print_out, index_plus_one):
    """Read csv and return DataFrame"""
    with open(filename, 'r') as f:
       df = pd.read_csv(filename)
       if index_plus_one:
            df.index = np.arange(1, len(df) + 1)
    if print_out == True:
        print(df.to_string())
    return df


def create_files(file1, file2, file3, file4):
    with open(file1, 'a+') as f:
            if os.stat(file1).st_size == 0:
                f.write('Name,Capacity,Adress\n')
    with open(file2, 'a+') as f:
            if os.stat(file2).st_size == 0:
                f.write('User,Location,Date\n')
    with open(file3, 'a+') as f:
            if os.stat(file3).st_size == 0:
                f.write('Username,Password,First Name,Last Name,Is Admin\n')
    with open(file4, 'a+') as f:        
            if os.stat(file4).st_size == 0:
                f.write('Location,Event,Date\n')