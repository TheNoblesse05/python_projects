import numpy as np 
import sys
import random

n = 9

#Solves the matrix uisng backtracking
def solve(arr,seq):	
	if(0 not in arr):
		print(arr)
		print('THANK YOU FOR PLAYING!')
		sys.exit()
	for i in range(n): # to iterate over the rows
		test = np.setdiff1d(seq,arr[i]) #gives the numbers that are not present in the row
		space = np.where(arr[i]==0) #type of space is (array(...))
		space = list(space[0]) #converts the array to list
		for x in space: # empty cells in the row
			for y in test: # missing numbers that can go in the row
				if (y not in arr[:,x] and y not in arr[i]): 
					x1,i1=x%3,i%3 #used to calculate the 3x3 box of the sudoku
					if(x1==0):
						xa,xb=0,2
					elif(x1==1):
						xa,xb=-1,1
					else:
						xa,xb=-2,0
					if(i1==0):
						ia,ib=0,2
					elif(i1==1):
						ia,ib=-1,1
					else:
						ia,ib=-2,0
					subarr = arr[i+ia:i+ib+1][:,x+xa:x+xb+1] #the 3x3 bos of the sudoku
					if(y not in subarr):
						arr[i][x] = y
						solve(arr,seq)
						arr[i][x] = 0 #if backtracks, the filled number should be 0/empty
					
			return


def main():
	print('''WELCOME!
	THIS PROGRAM WILL CREATE A SUDOKU PUZZLE & SOLVE IT!''')
	arr = np.zeros((9,9))
	seq = np.array([1,2,3,4,5,6,7,8,9])
	random.shuffle(seq) #the elements in a row
	arr[0] = seq

	#SUDOKU CREATION - shifts the previous row by 6 units
	for i in range(1,n):
		x=6
		if i%3==0:
			x=x+1
		arr[i] = np.append(arr[i-1][x:],arr[i-1][:x])
	print(arr)

	# Adding blanks/zeros to the matrix
	for i in range(20):
		x = random.randrange(0,n)
		y = random.randrange(0,n)
		arr[x][y] = arr[n-x-1][n-y-1] = 0

	print('THE SUDOKU PUZZLE IS\n',arr,'\nBEST OF LUCK!')
	print('\nTHE SOLUTION OF THE SUDOKU PUZZLE IS\n')

	solve(arr,seq)
	
main()