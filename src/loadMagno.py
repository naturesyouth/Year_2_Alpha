'''This module loads csv type magnotomerter data and preps it for further use.'''

#import pandas as pd
import pickle 
import time
import os
from multiprocessing import Pool, Queue

thread_count = 10

def load_data_from_path(path):
	'''takes a list of filenames and opens them for processing in a thread pool, returning a list of pandas data frames.'''
	outq = Queue(maxsize=0)
	files = glob.glob(path, recursive=True)
	print(files)
	
	with Pool(processes=thread_count) as pool:
		pool.map(process_file, glob.iglob(path, recursive=True), 10)
		
	print(outq.qsize())
	return list(outq.get())
	
def process_file(file_name):
	'''takes a file name and trys to load it into a pandas dataframe, converting from mac time to a datetime object.'''
	print(file_name)
	with open(file_name) as fd:
		print(fd.readline())

if __name__ == "__main__":
	
    import glob
    
    #files = glob.glob("data/raw/**/*.csv", recursive=True)

    print (load_data_from_path( path = "data/raw/**/*.csv" ))
    
