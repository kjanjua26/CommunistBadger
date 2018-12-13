import pickle
import multiprocessing
from math import cos
import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def loads_of_pickling(names_dict):
	filename = 'names_'						# No Extension
	for i in xrange(1,10):
		pickleDict(names_dict, filename + i)
		print("Pickling ...\nFile Name : ", filename + i, "\nTask Number: ", i)

	# tempDict = unpickleDict(filename)
	# print ("\nUnpickling ", filename)
	# print (tempDict)

def main():
	names_dict = {'Shahzaib': 3, 'Kamran': 8, 'Shafay': 5, 'Hasnain': 10}
	visualize_runtimes(multithreading(loads_of_pickling, names_dict, 1), "Single Thread")

def pickleDict(dictionary, filename):
	pickleFile = open(filename, 'wb')		# Writing
	pickle.dump(dictionary, pickleFile)
	pickleFile.close()

def unpickleDict(filename):
	pickleFile = open(filename, 'rb')		# Reading
	dictionary = pickle.load(pickleFile)
	pickleFile.close()
	return dictionary

def multithreading(multiThreadedFunction, args, threads):
    begin_time = time.time()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(multiThreadedFunction, args, [begin_time for i in range(len(args))])
    return list(results)

def multiprocessing(multiProcessFunction, args, processes):
    begin_time = time.time()
    with ProcessPoolExecutor(max_workers=processes) as executor:
        results = executor.map(multiProcessFunction, args, [begin_time for i in range(len(args))])
    return list(results)

def visualize_runtimes(results, title):
	start,stop = np.array(results).T
	plt.barh(range(len(start)),stop-start,left=start)
	plt.grid(axis='x')
	plt.ylabel("Tasks")
	plt.xlabel("Seconds")
	plt.title(title)
	return stop[-1]-start[0]

if __name__ == '__main__':
	main()