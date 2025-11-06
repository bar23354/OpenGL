
class Obj(object):
	def __init__(self, filename):
		with open(filename, "r") as file:
			lines = file.read().splitlines()
			
		self.vertices = []
		self.texCoords = []
		self.normals = []
		self.faces = []
		
		for line in lines:

			line = line.rstrip()

			try:
				prefix, value = line.split(" ", 1)
			except:
				continue
			
			if prefix == "v":
				vert = list(map(float,value.split(" ")))
				self.vertices.append(vert)
				
			elif prefix == "vt":
				vts = list(map(float,value.split(" ")))
				self.texCoords.append([vts[0],vts[1]])
				
			elif prefix == "vn":
				norm = list(map(float,value.split(" ")))
				self.normals.append(norm)
				
			elif prefix == "f":
				face = []
				verts = value.split(" ")
				for vert in verts:
					vert = list(map(int, vert.split("/")))
					face.append(vert)
				self.faces.append(face)                                                                                                                                                                                                                                                                                                                                                                                           