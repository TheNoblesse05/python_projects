'''
ALGORITHM -

OPEN - the set of nodes to be evaluated
CLOSED - the set of nodes already evaluated
add the start node to open
f_cost - heuristic cost

loop:
	current = node in OPEN with lowest f_cost
	remove current from OPEN
	add current to CLOSED

	if current is the target node: //path has been found
		return

	for each neighbour of the current node:
		if neighbour is not traversable or neighbour is in CLOSED:
			skip to the next neighbout
		if new path to neighbour is shorter OR neigbour is not in OPEN:
			set f_cost of neighbour
			set parent of neighbour to current
			if neighbour is not in OPEN:
				add neighbour to OPEN

Author - Vedant Tilwani
'''

import pygame
import pdb
import math
pygame.init()

#a node of a linked list
class node:
	def __init__(self,x=1,y=1):
		self.x = x
		self.y = y
		self.fcost = math.sqrt((18-x)**2+(18-y)**2) 	#heuristic cost estimate
		self. next = None

#linked list
class linked_list():
	def __init__(self):
		self.head = node()
	def insert(self,x,y):
		new_node = node(x,y)
		cur = self.head
		while cur.next!=None:
			cur = cur.next
		cur.next = new_node
	def delete(self,x,y):
		cur = self.head
		while cur.next!=None:
			temp = cur
			cur = cur.next
			if cur.x==x and cur.y==y:
				temp.next = cur.next
	def display(self):
		cur = self.head
		while cur.next!=None:
			cur = cur.next
			print('(x,y) is ',cur.x,',',cur.y)
			print('fcost is',cur.fcost)
		print()
	def remove(self):	 #removes the node with the lowest fcost
		cur = self.head
		x,y = -1,-1
		min = 9999999
		while cur.next!=None:
			cur = cur.next
			if(cur.fcost < min):
				min = cur.fcost
				x = cur.x
				y = cur.y
		cur = self.head
		while cur.next!=None:
			temp = cur
			cur = cur.next
			if(cur.x==x and cur.y==y):
				temp.next = cur.next
				return cur
	def check(self,x,y):	 #checks if the given(x,y) is present in the linked list
			cur = self.head
			while cur.next!=None:
				cur = cur.next
				if cur.x==x and cur.y==y:
					return True

#method to draw grids on the screen
def drawGrid(surface):
	sizebtw = width//rows
	x, y = 0, 0
	for l in range(rows):
		x += sizebtw
		y += sizebtw
		pygame.draw.line(surface, (255,255,255),(x,0),(x,width))
		pygame.draw.line(surface, (255,255,255),(0,y),(height,y))
	pygame.draw.rect(surface,(255,0,0),(1*sizebtw+1,1*sizebtw+1,1*sizebtw-1,1*sizebtw-1))
	pygame.draw.rect(surface,(0,255,0),(18*sizebtw+1,18*sizebtw+1,1*sizebtw-1,1*sizebtw-1))
	pygame.display.update()

#medthod which lets the user to mark the blocked tiles/squares
def setBlocks(surface,rows):
	sizebtw = width//rows
	for e in pygame.event.get():
		if e.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			mx = pos[0]//sizebtw
			my = pos[1]//sizebtw
			pygame.draw.rect(surface,(150,150,150),((mx)*sizebtw+1,(my)*sizebtw+1,1*sizebtw-1,1*sizebtw-1))
			lst = [mx,my]
			if lst not in blx:
				blx.append(lst)
			else:
				pass
			pygame.display.update()
			return True

#method that colours yellow the tiles/squares that are in the open list
def make_yellow(surface,check_n):
	sizebtw = width//rows
	mx = check_n[0]
	my = check_n[1]
	pygame.draw.rect(surface,(255,255,0),((mx)*sizebtw+1,(my)*sizebtw+1,1*sizebtw-1,1*sizebtw-1))

#method that colours blue the tiles/squares that are in the closed list
def make_blue(surface,put_n):
	sizebtw = width//rows
	mx = put_n[0]
	my = put_n[1]
	pygame.draw.rect(surface,(0,0,128),((mx)*sizebtw+1,(my)*sizebtw+1,1*sizebtw-1,1*sizebtw-1))
	pygame.display.update()


global width, height, rows, blx
width, height = 500, 500
rows = 20
blx = []
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Reach Green from Red')
screen.fill((0,0,0))
pygame.display.flip()
drawGrid(screen)
open = linked_list()
closed = linked_list()
open.insert(1,1) 	#adding the starting point in the open list
running = True
blo = True

while running:	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False	
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			blo = False 		#a variable which sets to false when the user wants to stop entering the blocked tiles 
	if(blo):
		setBlocks(screen,rows)
		continue

	current = open.remove() #node in OPEN with lowest f_cost
	closed.insert(current.x,current.y)
	put_n = [current.x,current.y]
	make_blue(screen,put_n)
	
	if(current.x==18 and current.y==18): #path has been found
		running = False

	neigh = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]] #for calculation of the neighbours of the current node
	for i in range(len(neigh)):
		check_n = [current.x+neigh[i][0],current.y+neigh[i][1]] 
		if(check_n[0] <0 or check_n[1] < 0 or check_n[0] > rows-1 or check_n[1] >rows-1): #the square shouldn't be out of the grid
			continue
		if check_n in blx or closed.check(check_n[0],check_n[1]): #if neighbour is is not traversable or neighbour is in CLOSED
			continue
		if(open.check(check_n[0],check_n[1])): #neighbour is not already in the open list
			continue
		open.insert(check_n[0],check_n[1])
		make_yellow(screen,check_n) #makes the tile yellow
	pygame.display.update()
pygame.time.delay(5000)