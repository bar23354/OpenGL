import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *

width = 960
height = 540

deltaTime = 0.0

def print_menu():
	print("\n" + "="*60)
	print("CONTROLES DE CAMARA")
	print("="*60)
	print("  MOUSE:")
	print("    Click Izq + Arrastrar : Orbitar alrededor del modelo")
	print("    Rueda del Mouse       : Zoom In/Out")
	print("")
	print("  TECLADO:")
	print("    Flechas ←→            : Rotar horizontalmente (Azimut)")
	print("    Flechas ↑↓            : Rotar verticalmente (Elevación)")
	print("    Z / X                 : Zoom Out / Zoom In")
	print("="*60)
	print("OTROS CONTROLES")
	print("="*60)
	print("  W/S             : Mover luz Z")
	print("  A/D             : Mover luz X")
	print("  Q/E             : Mover luz Y")
	print("  1               : Base Shader (Textura normal)")
	print("  2               : Chromatic Shader")
	print("  3               : Glitch Shader")
	print("  4               : Hologram Shader")
	print("  5               : Nuclear Shader")
	print("  6               : Pixelate Shader")
	print("  7               : Pulse Shader")
	print("  8               : Radiation Shader")
	print("  9               : Thermal Shader")
	print("  M               : Modelo Homero")
	print("  N               : Modelo Kirby")
	print("  B               : Modelo Jukebox")
	print("  F               : Toggle Filled Mode")
	print("="*60 + "\n")

print_menu()

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
rend.pointLight = glm.vec3(1,1,1)

currVertexShader = vertex_shader
currFragmentShader = fragment_shader

rend.SetShaders(currVertexShader, currFragmentShader)

skyboxTextures = ["skybox/right.png",
				  "skybox/left.png",
				  "skybox/top.png",
				  "skybox/bottom.png",
				  "skybox/front.png",
				  "skybox/back.png"]

rend.CreateSkybox(skyboxTextures)

homeroModel = Model("models/Homero.obj")
homeroModel.AddTexture("textures/homero_textures/Homer_simpsons_vyf2.png")
homeroModel.AddTexture("textures/radiation.jpg")
homeroModel.AddTexture("textures/uranium.jpg")
homeroModel.position.z = 0
homeroModel.AutoScale(4.0)

kirbyModel = Model("models/Kirbo.obj")
kirbyModel.AddTexture("textures/kirby_textures/kirbo.png")
kirbyModel.AddTexture("textures/radiation.jpg")
kirbyModel.AddTexture("textures/uranium.jpg")
kirbyModel.position.z = 0
kirbyModel.AutoScale(4.0)

jukeboxModel = Model("models/Jukebox.obj")
jukeboxModel.AddTexture("textures/jukebox_textures/jukebox_texture.png")
jukeboxModel.AddTexture("textures/jukebox_textures/Jukebox_N.png")
jukeboxModel.position.z = 0
jukeboxModel.AutoScale(4.0)

currentModel = homeroModel
rend.scene.append(currentModel)

cameraDistance = 15.0
cameraAzimuth = 45.0
cameraElevation = 20.0

MIN_DISTANCE = 5.0
MAX_DISTANCE = 100.0
MIN_ELEVATION = -89.0
MAX_ELEVATION = 89.0

mousePressed = False
lastMouseX = 0
lastMouseY = 0
mouseSensitivity = 0.2

keyboardRotationSpeed = 90.0
keyboardZoomSpeed = 20.0

targetPosition = glm.vec3(0, 0, 0)

def updateCameraPosition():
    azimuthRad = glm.radians(cameraAzimuth)
    elevationRad = glm.radians(cameraElevation)
    
    x = targetPosition.x + cameraDistance * glm.cos(elevationRad) * glm.sin(azimuthRad)
    y = targetPosition.y + cameraDistance * glm.sin(elevationRad)
    z = targetPosition.z + cameraDistance * glm.cos(elevationRad) * glm.cos(azimuthRad)
    
    rend.camera.position = glm.vec3(x, y, z)
    rend.camera.LookAt(targetPosition)

updateCameraPosition()

isRunning = True

while isRunning:

	deltaTime = clock.tick(60) / 1000

	rend.elapsedTime += deltaTime

	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_f:
				rend.ToggleFilledMode()

			if event.key == pygame.K_1:
				currVertexShader = vertex_shader
				currFragmentShader = fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_2:
				currVertexShader = vertex_shader
				currFragmentShader = chromatic_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_3:
				currVertexShader = glitch_shader
				currFragmentShader = fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_4:
				currVertexShader = vertex_shader
				currFragmentShader = hologram_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_5:
				currVertexShader = nuclear_decay_shader
				currFragmentShader = nuclear_fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_6:
				currVertexShader = vertex_shader
				currFragmentShader = pixelate_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_7:
				currVertexShader = pulse_shader
				currFragmentShader = fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_8:
				currVertexShader = radiation_pulse_shader
				currFragmentShader = radiation_fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_9:
				currVertexShader = vertex_shader
				currFragmentShader = thermal_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_m:
				rend.scene.clear()
				currentModel = homeroModel
				rend.scene.append(currentModel)
				rend.camera.LookAt(currentModel.position)

			if event.key == pygame.K_n:
				rend.scene.clear()
				currentModel = kirbyModel
				rend.scene.append(currentModel)
				rend.camera.LookAt(currentModel.position)

			if event.key == pygame.K_b:
				rend.scene.clear()
				currentModel = jukeboxModel
				rend.scene.append(currentModel)
				rend.camera.LookAt(currentModel.position)


		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				mousePressed = True
				lastMouseX, lastMouseY = event.pos
			elif event.button == 4:
				cameraDistance = max(MIN_DISTANCE, cameraDistance - 1.0)
				updateCameraPosition()
			elif event.button == 5:
				cameraDistance = min(MAX_DISTANCE, cameraDistance + 1.0)
				updateCameraPosition()

		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				mousePressed = False

		elif event.type == pygame.MOUSEMOTION:
			if mousePressed:
				mouseX, mouseY = event.pos
				deltaX = mouseX - lastMouseX
				deltaY = mouseY - lastMouseY
				
				cameraAzimuth += deltaX * mouseSensitivity
				cameraElevation -= deltaY * mouseSensitivity
				
				cameraElevation = max(MIN_ELEVATION, min(MAX_ELEVATION, cameraElevation))
				
				cameraAzimuth = cameraAzimuth % 360.0
				
				updateCameraPosition()
				
				lastMouseX = mouseX
				lastMouseY = mouseY



	if keys[K_UP]:
		cameraElevation += keyboardRotationSpeed * deltaTime
		cameraElevation = min(MAX_ELEVATION, cameraElevation)
		updateCameraPosition()

	if keys[K_DOWN]:
		cameraElevation -= keyboardRotationSpeed * deltaTime
		cameraElevation = max(MIN_ELEVATION, cameraElevation)
		updateCameraPosition()

	if keys[K_RIGHT]:
		cameraAzimuth += keyboardRotationSpeed * deltaTime
		cameraAzimuth = cameraAzimuth % 360.0
		updateCameraPosition()

	if keys[K_LEFT]:
		cameraAzimuth -= keyboardRotationSpeed * deltaTime
		cameraAzimuth = cameraAzimuth % 360.0
		updateCameraPosition()


	if keys[K_z]:
		cameraDistance += keyboardZoomSpeed * deltaTime
		cameraDistance = min(MAX_DISTANCE, cameraDistance)
		updateCameraPosition()

	if keys[K_x]:
		cameraDistance -= keyboardZoomSpeed * deltaTime
		cameraDistance = max(MIN_DISTANCE, cameraDistance)
		updateCameraPosition()



	if keys[K_w]:
		rend.pointLight.z -= 10 * deltaTime

	if keys[K_s]:
		rend.pointLight.z += 10 * deltaTime

	if keys[K_a]:
		rend.pointLight.x -= 10 * deltaTime

	if keys[K_d]:
		rend.pointLight.x += 10 * deltaTime

	if keys[K_q]:
		rend.pointLight.y -= 10 * deltaTime

	if keys[K_e]:
		rend.pointLight.y += 10 * deltaTime


	targetPosition = currentModel.position

	currentModel.rotation.y += 45 * deltaTime

	rend.Render()
	pygame.display.flip()

pygame.quit()