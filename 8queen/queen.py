def conflict(state, nextX):
	nextY = len(state)
	for i in range(nextY):
		print(abs(state[i] - nextX))
		print((0,nextY - i))
		if abs(state[i] - nextX) in (0,nextY - i):
			return True
	return False
def queens(num=8, state=()):
	for pos in range(num):
		if not conflict(state, pos):
			if len(state) == num-1:
				print((pos,))
				yield (pos,)
			else:
				for result in queens(num, state+(pos,)):
					print((pos,)+result)
					yield (pos,) + result 

if __name__ == "__main__":
	print (list(queens(2)))