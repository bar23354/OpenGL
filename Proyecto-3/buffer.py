import glm
from OpenGL.GL import *
from numpy import array, float32


class Buffer(object):
	def __init__(self, data):
		self.data = data

		self.vertexBuffer = array(self.data, dtype = float32)

		self.VBO = glGenBuffers(1)


	def Use(self, attribNumber, size):

		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

		glBufferData(GL_ARRAY_BUFFER,
					 self.vertexBuffer.nbytes,
					 self.vertexBuffer,
					 GL_STATIC_DRAW)

		glVertexAttribPointer(attribNumber,
							  size,
							  GL_FLOAT,
							  GL_FALSE,
							  0,
							  ctypes.c_void_p(0))

		glEnableVertexAttribArray(attribNumber)
		