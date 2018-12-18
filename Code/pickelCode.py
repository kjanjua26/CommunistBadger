from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import pickle
import time
import glob
import csv
import re

NUMBER_OF_PROCESSES = 4		# Number of Processes running together
filename = ''

# UNPICKLING ALL THE PICKLE FILES AND SAVING THE DATA IN DICTIONARIES
def getAllDictionaries():
	path = '../Data'
	print("UNPICKLING DATA")

	print("NEWS")
	for fname in glob.glob(path + '/News/Pickle/' + '*'):
		tempDict = unpickleDict(pickleFile)
		print(tempDict)

	print("STOCKS")
	for fname in glob.glob(path + '/Stocks/Pickle/' + '*'):
		tempDict = unpickleDict(pickleFile)
		print(tempDict)

	print("TWEETS")
	for fname in glob.glob(path + '/Tweets/Pickle/' + '*'):
		tempDict = unpickleDict(pickleFile)
		print(tempDict)

# PICKLING ALL THE .csv FILES INTO /Pickle/ DIRECTORY
def pickleAllFiles(dictionary, baseTime):
	start = time.time() - baseTime

	pickleFilePath = filename.split('/')
	pickleFileName = pickleFilePath[0] + '/' + pickleFilePath[1] + '/' + pickleFilePath[2] + '/Pickle/' + pickleFilePath[3]

	for i in range(10):
		pickleDict(dictionary, pickleFileName)
		print("Task Number: ", i)

	# tempDict = unpickleDict(filename)
	# print ("\nUnpickling ", filename)
	# print (tempDict)
	stop = time.time() - baseTime
	return start, stop

def main():
	path = '../Data'
	# NEWS DIRECTORY
	print('NEWS')
	for fname in glob.glob(path + '/News/' + '*.csv'):
		global filename
		filename = fname[:-4]
		print ("Pickling ...\nFile Name : ", filename)
		with open(fname , mode='r') as csvRead:
			reader = csv.reader(csvRead)
			dictionary = {rows[0]:rows[1] for rows in reader}
		visualize_runtimes(multithreading(pickleAllFiles, dictionary, NUMBER_OF_PROCESSES), "NEWS\n" + filename.split('/')[3] + "\nNumber of Processes : " + str(NUMBER_OF_PROCESSES))

	print('\nSTOCKS')
	# STOCKS DIRECTORY
	for fname in glob.glob(path + '/Stocks/' + '*.csv'):
		filename = fname[:-4]
		print ("Pickling ...\nFile Name : ", filename)
		with open(fname , mode='r') as csvRead:
			reader = csv.reader(csvRead)
			dictionary = {rows[0]:rows[1] for rows in reader}
		visualize_runtimes(multithreading(pickleAllFiles, dictionary, NUMBER_OF_PROCESSES), "STOCKS\n" + filename.split('/')[3] + "\nNumber of Processes : " + str(NUMBER_OF_PROCESSES))

	print('\nTWEETS')
	# TWEETS DIRECTORY
	for fname in glob.glob(path + '/Tweets/' + '*.csv'):
		filename = fname[:-4]
		print ("Pickling ...\nFile Name : ", filename)
		with open(fname , mode='r') as csvRead:
			reader = csv.reader(csvRead)
			dictionary = {rows[0]:rows[1] for rows in reader}
		visualize_runtimes(multithreading(pickleAllFiles, dictionary, NUMBER_OF_PROCESSES), "TWEETS\n" + filename.split('/')[3] + "\nNumber of Processes : " + str(NUMBER_OF_PROCESSES))

def pickleDict(dictionary, filename):
	pickleFile = open(filename, 'wb')		# Writing
	pickle.dump(dictionary, pickleFile)
	pickleFile.close()

def unpickleDict(filename):
	pickleFile = open(filename, 'rb')		# Reading
	dictionary = pickle.load(pickleFile)
	pickleFile.close()
	return dictionary

def multithreading(multiThreadedFunction, arg1, threads):
    begin_time = time.time()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(multiThreadedFunction, arg1, [begin_time for i in range(len(arg1))])
    return list(results)

def multiprocessing(multiProcessFunction, arg1, processes):
    begin_time = time.time()
    with ProcessPoolExecutor(max_workers=processes) as executor:
        results = executor.map(multiProcessFunction, arg1, [begin_time for i in range(len(arg1))])
    return list(results)

def visualize_runtimes(results, title):
	start,stop = np.array(results).T
	plt.barh(range(len(start)),stop-start,left=start)
	plt.ion()
	plt.grid(axis='x')
	plt.ylabel("Tasks")
	plt.xlabel("Seconds")
	plt.title(title)
	plt.pause(0.0001)
	plt.style.use(['dark_background', 'seaborn-dark'])
	plt.show()
	return stop[-1]-start[0]

if __name__ == '__main__':
	main()