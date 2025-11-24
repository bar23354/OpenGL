from OpenGL.GL import *
from obj import Obj
from buffer import Buffer

import glm

import pygame
import os

class Model(object):
	def __init__(self, filename):
		self.objFile = Obj(filename)

		self.position = glm.vec3(0,0,0)
		self.rotation = glm.vec3(0,0,0)
		self.scale = glm.vec3(1,1,1)

		self.textures = []
		self.textureNames = []
		self.matIdBuffer = None
		self.rawMatIds = []
		self.useMaterialTexturing = False
		self.hasNormalMap = False
		self.hasFaceTexture = False

		self.BuildBuffers()

	def ComputeBounds(self):
		if len(self.objFile.vertices) == 0:
			return glm.vec3(0,0,0), glm.vec3(0,0,0)
		minV = glm.vec3(float('inf'), float('inf'), float('inf'))
		maxV = glm.vec3(float('-inf'), float('-inf'), float('-inf'))
		for v in self.objFile.vertices:
			if v[0] < minV.x: minV.x = v[0]
			if v[1] < minV.y: minV.y = v[1]
			if v[2] < minV.z: minV.z = v[2]
			if v[0] > maxV.x: maxV.x = v[0]
			if v[1] > maxV.y: maxV.y = v[1]
			if v[2] > maxV.z: maxV.z = v[2]
		return minV, maxV

	def AutoScale(self, targetSize=2.0):
		minV, maxV = self.ComputeBounds()
		sizeVec = maxV - minV
		maxDim = max(sizeVec.x, sizeVec.y, sizeVec.z)
		if maxDim <= 1e-6:
			factor = 1.0
		else:
			factor = float(targetSize) / float(maxDim)
		self.scale = glm.vec3(factor, factor, factor)

	def GetModelMatrix(self):
		identity = glm.mat4(1)
		translateMat = glm.translate(identity, self.position)
		pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
		yawMat =   glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
		rollMat =  glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))
		rotationMat = pitchMat * yawMat * rollMat
		scaleMat = glm.scale(identity, self.scale)
		return translateMat * rotationMat * scaleMat

	def BuildBuffers(self):
		positions = []
		texCoords = []
		normals = []
		matIds = []
		self.vertexCount = 0
		for faceIndex, face in enumerate(self.objFile.faces):
			matIdRaw = 0
			if hasattr(self.objFile, 'faceMaterials') and faceIndex < len(self.objFile.faceMaterials):
				m = self.objFile.faceMaterials[faceIndex]
				if m is not None and m >= 0:
					matIdRaw = int(m)
			facePositions = []
			faceTexCoords = []
			faceNormals = []
			for i in range(len(face)):
				facePositions.append(self.objFile.vertices[face[i][0] - 1])
				
				if face[i][1] > 0 and face[i][1] <= len(self.objFile.texCoords):
					faceTexCoords.append(self.objFile.texCoords[face[i][1] - 1])
				else:
					faceTexCoords.append([0.0, 0.0])
				
				if face[i][2] > 0 and face[i][2] <= len(self.objFile.normals):
					faceNormals.append(self.objFile.normals[face[i][2] - 1])
				else:
					faceNormals.append([0.0, 0.0, 1.0])
					
			for value in facePositions[0]: positions.append(value)
			for value in facePositions[1]: positions.append(value)
			for value in facePositions[2]: positions.append(value)
			matIds.extend([float(matIdRaw), float(matIdRaw), float(matIdRaw)])
			for value in faceTexCoords[0]: texCoords.append(value)
			for value in faceTexCoords[1]: texCoords.append(value)
			for value in faceTexCoords[2]: texCoords.append(value)
			for value in faceNormals[0]: normals.append(value)
			for value in faceNormals[1]: normals.append(value)
			for value in faceNormals[2]: normals.append(value)
			self.vertexCount += 3
			if len(face) == 4:
				for value in facePositions[0]: positions.append(value)
				for value in facePositions[2]: positions.append(value)
				for value in facePositions[3]: positions.append(value)
				for value in faceTexCoords[0]: texCoords.append(value)
				for value in faceTexCoords[2]: texCoords.append(value)
				for value in faceTexCoords[3]: texCoords.append(value)
				for value in faceNormals[0]: normals.append(value)
				for value in faceNormals[2]: normals.append(value)
				for value in faceNormals[3]: normals.append(value)
				matIds.extend([float(matIdRaw), float(matIdRaw), float(matIdRaw)])
				self.vertexCount += 3
		self.posBuffer = Buffer(positions)
		self.texCoordsBuffer = Buffer(texCoords)
		self.normalsBuffer = Buffer(normals)
		self.rawMatIds = matIds[:] if len(matIds) > 0 else [0.0]*self.vertexCount
		self.matIdBuffer = Buffer(self.rawMatIds)

	def AddTexture(self, filename):
		try:
			textureSurface = pygame.image.load(filename)
			textureData = pygame.image.tostring(textureSurface, "RGBA", True)
			width = textureSurface.get_width()
			height = textureSurface.get_height()
		except:
			try:
				import imageio.v3 as iio
				import numpy as np
				img = iio.imread(filename)
				
				if img.shape[2] == 3:
					alpha = np.ones((img.shape[0], img.shape[1], 1), dtype=img.dtype) * 255
					img = np.concatenate([img, alpha], axis=2)
				
				img = np.flipud(img)
				
				textureData = img.tobytes()
				height, width = img.shape[:2]
			except:
				try:
					from PIL import Image
					img = Image.open(filename)
					img = img.convert("RGBA")
					img = img.transpose(Image.FLIP_TOP_BOTTOM)
					textureData = img.tobytes()
					width, height = img.size
				except ImportError:
					raise Exception(f"Cannot load {filename}. Install imageio: pip install imageio")
		
		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		glTexImage2D(GL_TEXTURE_2D,
					 0,
					 GL_RGBA,
					 width,
					 height,
					 0,
					 GL_RGBA,
					 GL_UNSIGNED_BYTE,
					 textureData)
		glGenerateMipmap(GL_TEXTURE_2D)
		self.textures.append(texture)
		self.textureNames.append(os.path.basename(filename))
		self._remap_mat_ids_to_textureslots()
	
	def AddFaceTexture(self, filename):
		"""Add a face decal texture specifically for Securitrons. This goes in tex2."""
		try:
			textureSurface = pygame.image.load(filename)
			textureData = pygame.image.tostring(textureSurface, "RGBA", True)
			width = textureSurface.get_width()
			height = textureSurface.get_height()
		except:
			try:
				import imageio.v3 as iio
				import numpy as np
				img = iio.imread(filename)
				if img.shape[2] == 3:
					alpha = np.ones((img.shape[0], img.shape[1], 1), dtype=img.dtype) * 255
					img = np.concatenate([img, alpha], axis=2)
				img = np.flipud(img)
				textureData = img.tobytes()
				height, width = img.shape[:2]
			except:
				try:
					from PIL import Image
					img = Image.open(filename)
					img = img.convert("RGBA")
					img = img.transpose(Image.FLIP_TOP_BOTTOM)
					textureData = img.tobytes()
					width, height = img.size
				except ImportError:
					raise Exception(f"Cannot load {filename}. Install imageio: pip install imageio")
		
		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		glTexImage2D(GL_TEXTURE_2D,
					 0,
					 GL_RGBA,
					 width,
					 height,
					 0,
					 GL_RGBA,
					 GL_UNSIGNED_BYTE,
					 textureData)
		glGenerateMipmap(GL_TEXTURE_2D)
		
		if self.useMaterialTexturing and len(self.textures) > 3:
			print(f"    Replacing Screen material texture with face: {os.path.basename(filename)}")
			self.textures[3] = texture
			self.textureNames[3] = os.path.basename(filename)
		else:
			self.textures.append(texture)
			self.textureNames.append(os.path.basename(filename))
		
		self.hasFaceTexture = True

	def AddNormalMap(self, filename):
		"""Add a normal map texture. Should be added after the diffuse texture."""
		try:
			textureSurface = pygame.image.load(filename)
		except:
			try:
				from PIL import Image
				img = Image.open(filename)
				img = img.convert("RGBA")
				textureData = img.tobytes()
				width, height = img.size
				
				texture = glGenTextures(1)
				glBindTexture(GL_TEXTURE_2D, texture)
				glTexImage2D(GL_TEXTURE_2D,
							 0,
							 GL_RGBA,
							 width,
							 height,
							 0,
							 GL_RGBA,
							 GL_UNSIGNED_BYTE,
							 textureData)
				glGenerateMipmap(GL_TEXTURE_2D)
				self.textures.append(texture)
				self.textureNames.append(os.path.basename(filename))
				self.hasNormalMap = True
				return
			except ImportError:
				raise Exception(f"Cannot load {filename}. Install Pillow: pip install Pillow")
		
		textureData = pygame.image.tostring(textureSurface, "RGBA", True)
		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		glTexImage2D(GL_TEXTURE_2D,
					 0,
					 GL_RGBA,
					 textureSurface.get_width(),
					 textureSurface.get_height(),
					 0,
					 GL_RGBA,
					 GL_UNSIGNED_BYTE,
					 textureData)
		glGenerateMipmap(GL_TEXTURE_2D)
		self.textures.append(texture)
		self.textureNames.append(os.path.basename(filename))
		self.hasNormalMap = True

	def LoadMaterialTextures(self):
		"""Load all textures from the OBJ's MTL file for material-based texturing"""
		if not hasattr(self.objFile, 'materials') or not hasattr(self.objFile, 'materialTextures'):
			print("  Warning: No materials found in OBJ")
			return
		
		try:
			from texture_mapping import map_texture_path
		except ImportError:
			map_texture_path = lambda x: x
		
		print(f"  Loading material textures for {len(self.objFile.materials)} materials...")
		
		sorted_materials = sorted(self.objFile.materials.items(), key=lambda x: x[1])
		
		obj_dir = os.path.dirname(getattr(self.objFile, 'filename', ''))
		
		for mat_name, mat_id in sorted_materials:
			if mat_name in self.objFile.materialTextures:
				tex_path = self.objFile.materialTextures[mat_name]
				tex_path_mapped = map_texture_path(tex_path)
				
				if tex_path_mapped.startswith("textures/"):
					full_path = tex_path_mapped
				elif obj_dir and not os.path.isabs(tex_path_mapped):
					full_path = os.path.join(obj_dir, tex_path_mapped)
				else:
					full_path = tex_path_mapped
				
				print(f"    Material '{mat_name}' (ID {mat_id}): {tex_path_mapped}")
				
				try:
					self.AddTexture(full_path)
				except Exception as e:
					print(f"      Failed to load: {e}")
					self.textures.append(0)
					self.textureNames.append(f"missing_{mat_name}")
			else:
				print(f"    Material '{mat_name}' (ID {mat_id}): No texture")
				self.textures.append(0)
				self.textureNames.append(f"missing_{mat_name}")
		
		self.useMaterialTexturing = True
		self._remap_mat_ids_to_textureslots()

	def _remap_mat_ids_to_textureslots(self):
		if self.rawMatIds is None or len(self.rawMatIds) == 0:
			return
		
		if self.useMaterialTexturing:
			self.matIdBuffer = Buffer(self.rawMatIds)
			return
		
		mapped = []
		texCount = len(self.textureNames)
		for raw in self.rawMatIds:
			mat_index = int(raw + 0.5)
			slot = 0
			name = None
			if hasattr(self.objFile, 'materialIndexToName') and mat_index >= 0 and mat_index < len(self.objFile.materialIndexToName):
				name = self.objFile.materialIndexToName[mat_index]
			if name and hasattr(self.objFile, 'materialTextures') and name in self.objFile.materialTextures:
				texFile = os.path.basename(self.objFile.materialTextures[name])
				if texFile in self.textureNames:
					slot = self.textureNames.index(texFile)
				elif texCount > 0:
					slot = mat_index % texCount
			else:
				if texCount > 0:
					slot = mat_index % texCount
				else:
					slot = 0
			mapped.append(float(slot))
		self.matIdBuffer = Buffer(mapped)

	def Render(self):
		for i in range(len(self.textures)):
			glActiveTexture(GL_TEXTURE0 + i)
			glBindTexture(GL_TEXTURE_2D, self.textures[i])
		self.posBuffer.Use(0, 3)
		self.texCoordsBuffer.Use(1, 2)
		self.normalsBuffer.Use(2, 3)
		if self.matIdBuffer is not None:
			self.matIdBuffer.Use(3, 1)
		glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glDisableVertexAttribArray(2)
		glDisableVertexAttribArray(3)