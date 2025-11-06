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

		self.BuildBuffers()

		self.textures = []
		self.textureNames = []
		self.matIdBuffer = None
		self.rawMatIds = []
		self.useMaterialTexturing = False

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
				faceTexCoords.append(self.objFile.texCoords[face[i][1] - 1])
				faceNormals.append(self.objFile.normals[face[i][2] - 1])
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
		textureSurface = pygame.image.load(filename)
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
		self._remap_mat_ids_to_textureslots()

	def _remap_mat_ids_to_textureslots(self):
		if self.rawMatIds is None or len(self.rawMatIds) == 0:
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