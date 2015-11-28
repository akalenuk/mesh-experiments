def _list_by_prefix(prefix, text, to_type = lambda x: float(x) ):
	ls = []
	for line in text.split('\n'):
		if line.startswith(prefix):
			line = line[len(prefix):].strip()
			ls += [[to_type(l.replace(',', '.')) for l in line.split(' ')]]
	return ls
	

def vertexes(text):
	#v 4,875346 21,185596 0,000000
	return _list_by_prefix('v ', text)

def triangles(text):
	#f 1/x/x 2/x/x 3/x/x
	return _list_by_prefix('f ', text, lambda s: int(s.split('/')[0]))

if __name__ == "__main__":
	f = open('ellipsoid.obj', 'r')		
	for vs in vertexes(f.read()):
		print 'v', vs
	f.close()
	f = open('ellipsoid.obj', 'r')		
	for tr in triangles(f.read()):
		print 'tr', tr
	f.close()

