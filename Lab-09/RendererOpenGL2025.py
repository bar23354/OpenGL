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
    print("CONTROLES")
    print("="*60)
    print("  Flechas (↑↓←→)  : Mover camara")
    print("  W/S             : Mover luz Z")
    print("  A/D             : Mover luz X")
    print("  Q/E             : Mover luz Y")
    print("  1               : Normal Shader")
    print("  2               : Toon Shader")
    print("  3               : Negative Shader")
    print("  4               : Magma Shader")
    print("  7               : Vertex Normal")
    print("  8               : Fat Shader")
    print("  9               : Water Shader")
    print("  0               : Radiation Pulse (Ondas radioactivas)")
    print("  -               : Nuclear Decay (Desintegracion nuclear)")
    print("  Z/X             : Disminuir/Aumentar intensidad")
    print("  F               : Toggle Filled Mode")
    print("="*60 + "\n")

print_menu()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
rend.pointLight = glm.vec3(1,1,1)

currVertexShader = vertex_shader
currFragmentShader = fragment_shader

rend.SetShaders(currVertexShader, currFragmentShader)

skyboxTextures = ["skybox/right.jpg",
				  "skybox/left.jpg",
				  "skybox/top.jpg",
				  "skybox/bottom.jpg",
				  "skybox/front.jpg",
				  "skybox/back.jpg"]

rend.CreateSkybox(skyboxTextures)


faceModel = Model("models/model.obj")
faceModel.AddTexture("textures/model.bmp")
faceModel.AddTexture("textures/lava_cracks.jpg")
faceModel.position.z = -10
faceModel.scale = glm.vec3(2, 2, 2)

rend.scene.append(faceModel)

rend.camera.position.z = -5

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
				currFragmentShader = fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_2:
				currFragmentShader = toon_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_3:
				currFragmentShader = negative_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_4:
				currFragmentShader = magma_shader
				rend.SetShaders(currVertexShader, currFragmentShader)


			if event.key == pygame.K_7:
				currVertexShader = vertex_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_8:
				currVertexShader = fat_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_9:
				currVertexShader = water_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_0:
				currVertexShader = radiation_pulse_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_MINUS:
				currVertexShader = nuclear_decay_shader
				rend.SetShaders(currVertexShader, currFragmentShader)


	if keys[K_UP]:
		rend.camera.position.z += 1 * deltaTime

	if keys[K_DOWN]:
		rend.camera.position.z -= 1 * deltaTime

	if keys[K_RIGHT]:
		rend.camera.position.x += 1 * deltaTime

	if keys[K_LEFT]:
		rend.camera.position.x -= 1 * deltaTime



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


	if keys[K_z]:
		if rend.value > 0.0:
			rend.value -= 1 * deltaTime

	if keys[K_x]:
		if rend.value < 1.0:
			rend.value += 1 * deltaTime



	faceModel.rotation.y += 45 * deltaTime


	rend.Render()
	pygame.display.flip()

pygame.quit()