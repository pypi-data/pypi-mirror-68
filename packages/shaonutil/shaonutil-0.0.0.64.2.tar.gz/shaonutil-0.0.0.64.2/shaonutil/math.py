"""Math"""
def calculate_distance(p1,p2):
	"""Calculate Distance between two points p1=[x1,y1],p2=[x2,y2]"""
	x1,y1 = p1
	x2,y2 = p2
	distance  = ( (y1 - y2)**2 + (x1 - x2)**2 ) ** (1/2)
	return distance