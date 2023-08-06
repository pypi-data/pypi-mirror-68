import math

# includes endpoints! [d0,d1]
def wall_follower(length, d0, d1, mapping, imapping):
	#print('wall_follower(',length,',',d0,',',d1,',...)')

	width = int(math.sqrt(length))
	def ok(x, y):
		if x<0 or y<0 or x>=width or y>=width: return False
		d = imapping(x, y, length)
		#print('is %d within %d,%d' % (d, d0, d1))
		return d>=0 and d>=d0 and d<=d1

	# move left until stop (so we can face down with right hand on wall)
	(x,y) = mapping(d0, length)
	while 1:
		if x == 0: break
		if not ok(x-1,y): break
		x = x-1

	direction = 'down'
	start = (x, y, direction)
	trace = [(x,y)]

	tendencies = ['right', 'down', 'left', 'up']

	while 1:
		#print('at (%d,%d) heading %s' % (x,y,direction))

		tendency = tendencies[(tendencies.index(direction)+1) % 4]

		xmod = {'right':1, 'down':0, 'left':-1, 'up':0}
		ymod = {'right':0, 'down':-1, 'left':0, 'up':1}

		moved = False

		# case A: we can turn right
		x_try = x+xmod[tendency]
		y_try = y+ymod[tendency]
		if ok(x_try, y_try):
			direction = tendency
			(x,y) = (x_try, y_try)
			moved = True
		else:
			# case B: we can continue in current direction
			x_try = x+xmod[direction]
			y_try = y+ymod[direction]
			if ok(x_try, y_try):
				(x,y) = (x_try, y_try)
				moved = True
			else:
				# case C: we can't continue! turn
				direction = tendencies[(tendencies.index(direction)-1)%4]

		if (x, y, direction) == start:
			break

		# don't apply duplicates
		if moved:
			trace.append((x,y))

	return trace

