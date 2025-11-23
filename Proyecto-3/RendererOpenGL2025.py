import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *
from diorama_config import DIORAMA_MODELS, CAMERA_CONFIG, LIGHT_CONFIG

width = 960
height = 540

deltaTime = 0.0

def print_menu():
	print("\n" + "="*60)
	print("DIORAMA DE FALLOUT - CONTROLES")
	print("="*60)
	print("  CAMARA:")
	print("    Click Izq + Arrastrar : Orbitar alrededor del diorama")
	print("    Rueda del Mouse       : Zoom In/Out")
	print("    Flechas ←→            : Rotar horizontalmente")
	print("    Flechas ↑↓            : Rotar verticalmente")
	print("    Z / X                 : Zoom Out / Zoom In")
	print("")
	print("  LUZ:")
	print("    W/S                   : Mover luz Z")
	print("    A/D                   : Mover luz X")
	print("    R/T                   : Mover luz Y")
	print("")
	print("  SHADERS:")
	print("    1                     : Base Shader")
	print("    2                     : Chromatic Shader")
	print("    3                     : Glitch Shader")
	print("    4                     : Hologram Shader")
	print("    5                     : Nuclear Shader")
	print("    6                     : Pixelate Shader")
	print("    7                     : Pulse Shader")
	print("    8                     : Radiation Shader")
	print("    9                     : Thermal Shader")
	print("")
	print("  OTROS:")
	print("    F                     : Toggle Filled Mode")
	print("="*60)
	print("  MODELOS: Ver diorama_config.py para configurar")
	print("="*60 + "\n")

print_menu()

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
rend.pointLight = glm.vec3(LIGHT_CONFIG["position"][0], 
                           LIGHT_CONFIG["position"][1], 
                           LIGHT_CONFIG["position"][2])
rend.ambientLight = LIGHT_CONFIG["ambient"]

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

# Cargar todos los modelos habilitados desde la configuración
print("Cargando modelos del diorama...")
models = []
for config in DIORAMA_MODELS:
	if not config["enabled"]:
		print(f"  ⊗ {config['name']:20} - DESACTIVADO")
		continue
	
	try:
		print(f"  ⊙ {config['name']:20} - Cargando...", end="")
		model = Model(config["file"])
		
		# Cargar textura
		if config["texture"]:
			model.AddTexture(config["texture"])
		
		# Cargar normal map si existe
		if config["normal_map"]:
			model.AddNormalMap(config["normal_map"])
		
		# Aplicar transformaciones
		model.position = glm.vec3(config["position"][0], 
		                          config["position"][1], 
		                          config["position"][2])
		model.rotation = glm.vec3(config["rotation"][0], 
		                          config["rotation"][1], 
		                          config["rotation"][2])
		model.scale = glm.vec3(config["scale"], config["scale"], config["scale"])
		
		models.append(model)
		rend.scene.append(model)
		print(" ✓")
	except Exception as e:
		print(f" ✗ Error: {e}")

print(f"\nModelos cargados: {len(models)}/{len([m for m in DIORAMA_MODELS if m['enabled']])}")
print("="*60 + "\n")

cameraDistance = CAMERA_CONFIG["distance"]
cameraAzimuth = CAMERA_CONFIG["azimuth"]
cameraElevation = CAMERA_CONFIG["elevation"]

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

targetPosition = glm.vec3(CAMERA_CONFIG["target"][0], 
                          CAMERA_CONFIG["target"][1], 
                          CAMERA_CONFIG["target"][2])

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

	if keys[K_r]:
		rend.pointLight.y -= 10 * deltaTime

	if keys[K_t]:
		rend.pointLight.y += 10 * deltaTime

	rend.Render()
	pygame.display.flip()

pygame.quit()