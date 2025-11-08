import glm

class Camera(object):
	def __init__(self, width, height):

		self.screenWidth = width
		self.screenHeight = height
		
		self.position = glm.vec3(0,0,0)

		self.rotation = glm.vec3(0,0,0)

		self.viewMatrix = None
		self.lookAtTarget = None

		self.CreateProjectionMatrix(60, 0.1, 1000)


	def Update(self):
		if self.lookAtTarget is not None:
			up = glm.vec3(0, 1, 0)
			self.viewMatrix = glm.lookAt(self.position, self.lookAtTarget, up)
		else:
			identity = glm.mat4(1)

			translateMat = glm.translate(identity, self.position)

			pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
			yawMat =   glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
			rollMat =  glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

			rotationMat = pitchMat * yawMat * rollMat

			camMat = translateMat * rotationMat

			self.viewMatrix = glm.inverse(camMat)

	def LookAt(self, target):
		self.lookAtTarget = glm.vec3(target)
		up = glm.vec3(0, 1, 0)
		self.viewMatrix = glm.lookAt(self.position, self.lookAtTarget, up)


	def CreateProjectionMatrix(self, fov, nearPlane, farPlane):
		self.projectionMatrix = glm.perspective( glm.radians(fov), self.screenWidth / self.screenHeight, nearPlane, farPlane)