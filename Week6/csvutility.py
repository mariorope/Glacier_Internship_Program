import logging
import os
import subprocess
import yaml
import pandas as pd
import datetime 
import gc
import re


################
# File Reading #
################

def read_config_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)


def replacer(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, char, string) 
    return string

def col_header_val(df, table_config):
    '''
    replace whitespaces in the column
    and standardized column names
    '''
    df.columns = df.columns.str.upper()
    df.columns = df.columns.str.replace('[^\w]','_',regex=True)
    df.columns = list(map(lambda x: x.strip('_'), list(df.columns)))
    df.columns = list(map(lambda x: replacer(x,'_'), list(df.columns)))
    expected_col = list(map(lambda x: x.upper(),  table_config['columns']))
    expected_col.sort()
    df.columns =list(map(lambda x: x.upper(), list(df.columns)))
    columns_index = list(df.columns)
    df = df.reindex(sorted(df.columns), axis=1)
    if len(df.columns) == len(expected_col) and list(expected_col) == list(df.columns):
        print("column name and column length validation passed")
        df = df.reindex(columns=columns_index)
        return 1
    
    else:
        print("column name and column length validation failed")
        mismatched_columns_file = list(set(df.columns).difference(expected_col))
        print("Following File columns are not in the YAML file",mismatched_columns_file)
        missing_YAML_file = list(set(expected_col).difference(df.columns))
        print("Following YAML columns are not in the file uploaded",missing_YAML_file)
        logging.info(f'df columns: {df.columns}')
        logging.info(f'expected columns: {expected_col}')
        return 0
    
def file_summary(df):
    '''
    create a summary of the loaded dataframe, including the number of rows,
    number of columns and the size of the file
    '''
    nc = len(df.columns)
    nr = len(df.index)
    mem = sum(df.memory_usage()) 
    print("\nThis dataset presents {} columns (variables) and {} rows (registers).".format(nc, nr))
    
    if mem < 1000:
        print("\nThe file size is: {} bytes".format(mem))
    elif mem < 1000000:
        print("\nThe file size is: {} KB".format(round(mem/1000, 1)))
    elif mem < 1000000000:
        print("\nThe file size is: {} MB".format(round(mem/1000000, 1)))
    elif mem < 1000000000000:
        print("\nThe file size is: {} GB".format(round(mem/1000000000, 1)))
    return 1

def save_pipe_txtgz_file(df, table_config):
    
    output = "data/" + table_config["output_file"] + "." + table_config["output_file_format"] + "." + table_config["compress_type"]
    df.to_csv(output, index=False, sep="|", header=True, chunksize=5000, compression="gzip")
