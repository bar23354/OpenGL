
import os

class Obj(object):
	def __init__(self, filename):
		self.filename = filename
		with open(filename, "r") as file:
			lines = file.read().splitlines()
			
		self.vertices = []
		self.texCoords = []
		self.normals = []
		self.faces = []
		self.materials = {}
		self.faceMaterials = []
		self.materialIndexToName = []
		self.mtlFileName = None
		self.materialTextures = {}
		currentMaterial = None
		objDir = os.path.dirname(filename)
		
		for line in lines:
			line = line.rstrip()

			try:
				prefix, value = line.split(" ", 1)
			except:
				continue
			
			if prefix == "v":
				vert = list(map(float, value.split()))
				self.vertices.append(vert)
				
			elif prefix == "vt":
				vts = list(map(float, value.split()))
				self.texCoords.append([vts[0], vts[1]])
				
			elif prefix == "vn":
				norm = list(map(float, value.split()))
				self.normals.append(norm)

			elif prefix == "mtllib":
				self.mtlFileName = value.strip()
				mtlPath = os.path.join(objDir, self.mtlFileName)
				try:
					self._load_mtl(mtlPath)
				except Exception as e:
					print(f"Warning: Failed to load MTL file '{mtlPath}': {e}")

			elif prefix == "usemtl":
				matName = value.strip()
				if matName not in self.materials:
					self.materials[matName] = len(self.materials)
					self.materialIndexToName.append(matName)
				currentMaterial = self.materials[matName]
				
			elif prefix == "f":
				face = []
				verts = value.split()
				for vert in verts:
					parts = vert.split("/")
					vertex_index = [0, 0, 0]
					
					if len(parts) >= 1 and parts[0]:
						vertex_index[0] = int(parts[0])
					if len(parts) >= 2 and parts[1]:
						vertex_index[1] = int(parts[1])
					if len(parts) >= 3 and parts[2]:
						vertex_index[2] = int(parts[2])
					
					face.append(vertex_index)
				self.faces.append(face)
				if currentMaterial is None:
					self.faceMaterials.append(-1)
				else:
					self.faceMaterials.append(currentMaterial)

	def _load_mtl(self, mtlPath):
		current = None
		with open(mtlPath, 'r') as f:
			for raw in f.read().splitlines():
				raw = raw.strip()
				if not raw or raw.startswith('#'):
					continue
				parts = raw.split(None, 1)
				if len(parts) < 2:
					continue
				key, val = parts[0], parts[1].strip()
				if key == 'newmtl':
					current = val
				elif key == 'map_Kd' and current is not None:
					self.materialTextures[current] = val