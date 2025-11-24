import pygame
import pygame.display
from pygame.locals import *

import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *
from diorama_config import DIORAMA_MODELS, CAMERA_CONFIG, LIGHT_CONFIG

width = 960
height = 540

deltaTime = 0.0

musicMenuExpanded = False
musicMenuRect = pygame.Rect(10, 10, 200, 40)
pauseButtonRect = pygame.Rect(20, 60, 180, 30)
volumeUpRect = pygame.Rect(20, 100, 85, 30)
volumeDownRect = pygame.Rect(115, 100, 85, 30)
musicPaused = False
musicVolume = 0.3

def print_menu():
	print("\n" + "="*60)
	print("DIORAMA DE FALLOUT - CONTROLES")
	print("="*60)
	print("  CAMARA:")
	print("    Click Izq + Arrastrar : Orbitar alrededor del punto")
	print("    Rueda del Mouse       : Zoom In/Out")
	print("    Flechas <- ->         : Rotar horizontalmente")
	print("    Flechas ^ v           : Rotar verticalmente")
	print("    Z / X                 : Zoom Out / Zoom In")
	print("    PageUp / PageDown     : Desplazar verticalmente")
	print("    TAB                   : Cambiar a siguiente modelo")
	print("    SHIFT+TAB             : Cambiar a modelo anterior")
	print("    HOME                  : Volver a vista global")
	print("")
	print("  LUZ:")
	print("    W/S                   : Mover luz Z")
	print("    A/D                   : Mover luz X")
	print("    R/T                   : Mover luz Y")
	print("")
	print("  SHADERS (Modelo Seleccionado):")
	print("    1                     : Base Shader")
	print("    2                     : Chromatic Shader")
	print("    3                     : Glitch Shader")
	print("    4                     : Hologram Shader")
	print("    5                     : Nuclear Shader")
	print("    6                     : Pixelate Shader")
	print("    7                     : Pulse Shader")
	print("    8                     : Radiation Shader")
	print("    9                     : Thermal Shader")
	print("    0                     : Remover shader personalizado")
	print("")
	print("  MODOS:")
	print("    M                     : Modo aleatorio (cada modelo diferente)")
	print("    F                     : Toggle Filled Mode")
	print("")
	print("  MUSICA:")
	print("    P                     : Pausar/Reanudar musica")
	print("    + / -                 : Subir/Bajar volumen")
	print("="*60)
	print("  MODELOS: Ver diorama_config.py para configurar")
	print("="*60 + "\n")

print_menu()

pygame.init()
pygame.mixer.init()

try:
	pygame.mixer.music.load("music/Marty Robbins - Big Iron.mp3")
	pygame.mixer.music.set_volume(0.3)
	pygame.mixer.music.play(-1)
	print("Musica cargada: Marty Robbins - Big Iron")
except Exception as e:
	print(f"No se pudo cargar la musica: {e}")

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

print("Cargando modelos del diorama...")
models = []
model_cache = {}

for config in DIORAMA_MODELS:
	if not config["enabled"]:
		print(f"  x {config['name']:20} - DESACTIVADO")
		continue
	
	try:
		print(f"  * {config['name']:20} - Cargando...", end="")
		
		cache_key = config["file"]
		
		needs_unique_textures = config.get("face_texture") is not None
		
		if cache_key in model_cache and not needs_unique_textures:
			base_model = model_cache[cache_key]
			model = Model.__new__(Model)
			model.objFile = base_model.objFile
			model.posBuffer = base_model.posBuffer
			model.texCoordsBuffer = base_model.texCoordsBuffer
			model.normalsBuffer = base_model.normalsBuffer
			model.matIdBuffer = base_model.matIdBuffer
			model.rawMatIds = base_model.rawMatIds
			model.vertexCount = base_model.vertexCount
			model.textures = base_model.textures
			model.textureNames = base_model.textureNames
			model.useMaterialTexturing = base_model.useMaterialTexturing
			model.hasNormalMap = base_model.hasNormalMap
			model.position = glm.vec3(0, 0, 0)
			model.rotation = glm.vec3(0, 0, 0)
			model.scale = glm.vec3(1, 1, 1)
			print(" OK (instancia)")
		else:
			if cache_key in model_cache:
				base_model = model_cache[cache_key]
				model = Model.__new__(Model)
				model.objFile = base_model.objFile
				model.posBuffer = base_model.posBuffer
				model.texCoordsBuffer = base_model.texCoordsBuffer
				model.normalsBuffer = base_model.normalsBuffer
				model.matIdBuffer = base_model.matIdBuffer
				model.rawMatIds = base_model.rawMatIds
				model.vertexCount = base_model.vertexCount
				model.textures = []
				model.textureNames = []
				model.useMaterialTexturing = False
				model.hasNormalMap = False
				model.position = glm.vec3(0, 0, 0)
				model.rotation = glm.vec3(0, 0, 0)
				model.scale = glm.vec3(1, 1, 1)
			else:
				model = Model(config["file"])
				model_cache[cache_key] = model
			
			if config.get("use_material_textures"):
				model.LoadMaterialTextures()
			elif config["texture"]:
				model.AddTexture(config["texture"])
			
			if config.get("normal_map") and not config.get("use_material_textures"):
				model.AddNormalMap(config["normal_map"])

			if config.get("face_texture"):
				model.AddFaceTexture(config["face_texture"])
			
			print(" OK" if not needs_unique_textures else " OK (cara única)")

		model.position = glm.vec3(config["position"][0], 
		                          config["position"][1], 
		                          config["position"][2])
		model.rotation = glm.vec3(config["rotation"][0], 
		                          config["rotation"][1], 
		                          config["rotation"][2])
		model.scale = glm.vec3(config["scale"], config["scale"], config["scale"])
		
		models.append(model)
		rend.scene.append(model)
		
	except Exception as e:
		print(f" ERROR: {e}")

print(f"\nModelos cargados: {len(models)}/{len([m for m in DIORAMA_MODELS if m['enabled']])}")
print("="*60 + "\n")

currentModelIndex = -1
modelShaders = {}
randomShaderMode = False

shaderSourceList = [
	(vertex_shader, fragment_shader, "Base"),
	(vertex_shader, chromatic_shader, "Chromatic"),
	(glitch_shader, fragment_shader, "Glitch"),
	(vertex_shader, hologram_shader, "Hologram"),
	(nuclear_decay_shader, nuclear_fragment_shader, "Nuclear"),
	(vertex_shader, pixelate_shader, "Pixelate"),
	(pulse_shader, fragment_shader, "Pulse"),
	(radiation_pulse_shader, radiation_fragment_shader, "Radiation"),
	(vertex_shader, thermal_shader, "Thermal")
]

print("Compilando shaders...")
compiledShaders = []
for i, (vShader, fShader, name) in enumerate(shaderSourceList):
	try:
		shader = compileProgram(
			compileShader(vShader, GL_VERTEX_SHADER),
			compileShader(fShader, GL_FRAGMENT_SHADER)
		)
		compiledShaders.append(shader)
		print(f"  ✓ {i+1}. {name}")
	except Exception as e:
		print(f"  ✗ {i+1}. {name} - Error: {e}")
		compiledShaders.append(None)
print("="*60 + "\n")

cameraDistance = CAMERA_CONFIG["distance"]
cameraAzimuth = CAMERA_CONFIG["azimuth"]
cameraElevation = CAMERA_CONFIG["elevation"]
verticalOffset = 0.0

MIN_DISTANCE = 5.0
MAX_DISTANCE = 100.0
MIN_ELEVATION = -89.0
MAX_ELEVATION = 89.0
MIN_VERTICAL = -50.0
MAX_VERTICAL = 50.0

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
    
    adjustedTarget = glm.vec3(targetPosition.x, targetPosition.y + verticalOffset, targetPosition.z)
    
    x = adjustedTarget.x + cameraDistance * glm.cos(elevationRad) * glm.sin(azimuthRad)
    y = adjustedTarget.y + cameraDistance * glm.sin(elevationRad)
    z = adjustedTarget.z + cameraDistance * glm.cos(elevationRad) * glm.cos(azimuthRad)
    
    rend.camera.position = glm.vec3(x, y, z)
    rend.camera.LookAt(adjustedTarget)

def focusOnModel(modelIndex):
    global targetPosition, cameraDistance, currentModelIndex
    if modelIndex >= 0 and modelIndex < len(models):
        currentModelIndex = modelIndex
        targetPosition = models[modelIndex].position
        cameraDistance = 15.0
        model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][modelIndex]]['name']
        print(f"\nEnfocando: {model_name}")
    else:
        currentModelIndex = -1
        targetPosition = glm.vec3(CAMERA_CONFIG["target"][0], 
                                  CAMERA_CONFIG["target"][1], 
                                  CAMERA_CONFIG["target"][2])
        cameraDistance = CAMERA_CONFIG["distance"]
        print("\nVista global del diorama")
    updateCameraPosition()

def draw_music_menu():
    global musicMenuExpanded, musicPaused, musicVolume
    
    # Switch to 2D rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    
    # Main menu button
    glColor4f(0.2, 0.2, 0.2, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(musicMenuRect.x, musicMenuRect.y)
    glVertex2f(musicMenuRect.x + musicMenuRect.width, musicMenuRect.y)
    glVertex2f(musicMenuRect.x + musicMenuRect.width, musicMenuRect.y + musicMenuRect.height)
    glVertex2f(musicMenuRect.x, musicMenuRect.y + musicMenuRect.height)
    glEnd()
    
    # Border
    glColor4f(0.0, 1.0, 0.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(musicMenuRect.x, musicMenuRect.y)
    glVertex2f(musicMenuRect.x + musicMenuRect.width, musicMenuRect.y)
    glVertex2f(musicMenuRect.x + musicMenuRect.width, musicMenuRect.y + musicMenuRect.height)
    glVertex2f(musicMenuRect.x, musicMenuRect.y + musicMenuRect.height)
    glEnd()
    
    # Expanded menu
    if musicMenuExpanded:
        # Pause button
        glColor4f(0.3, 0.3, 0.3, 0.8)
        glBegin(GL_QUADS)
        glVertex2f(pauseButtonRect.x, pauseButtonRect.y)
        glVertex2f(pauseButtonRect.x + pauseButtonRect.width, pauseButtonRect.y)
        glVertex2f(pauseButtonRect.x + pauseButtonRect.width, pauseButtonRect.y + pauseButtonRect.height)
        glVertex2f(pauseButtonRect.x, pauseButtonRect.y + pauseButtonRect.height)
        glEnd()
        
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(pauseButtonRect.x, pauseButtonRect.y)
        glVertex2f(pauseButtonRect.x + pauseButtonRect.width, pauseButtonRect.y)
        glVertex2f(pauseButtonRect.x + pauseButtonRect.width, pauseButtonRect.y + pauseButtonRect.height)
        glVertex2f(pauseButtonRect.x, pauseButtonRect.y + pauseButtonRect.height)
        glEnd()
        
        # Volume Up button
        glColor4f(0.3, 0.3, 0.3, 0.8)
        glBegin(GL_QUADS)
        glVertex2f(volumeUpRect.x, volumeUpRect.y)
        glVertex2f(volumeUpRect.x + volumeUpRect.width, volumeUpRect.y)
        glVertex2f(volumeUpRect.x + volumeUpRect.width, volumeUpRect.y + volumeUpRect.height)
        glVertex2f(volumeUpRect.x, volumeUpRect.y + volumeUpRect.height)
        glEnd()
        
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(volumeUpRect.x, volumeUpRect.y)
        glVertex2f(volumeUpRect.x + volumeUpRect.width, volumeUpRect.y)
        glVertex2f(volumeUpRect.x + volumeUpRect.width, volumeUpRect.y + volumeUpRect.height)
        glVertex2f(volumeUpRect.x, volumeUpRect.y + volumeUpRect.height)
        glEnd()
        
        # Volume Down button
        glColor4f(0.3, 0.3, 0.3, 0.8)
        glBegin(GL_QUADS)
        glVertex2f(volumeDownRect.x, volumeDownRect.y)
        glVertex2f(volumeDownRect.x + volumeDownRect.width, volumeDownRect.y)
        glVertex2f(volumeDownRect.x + volumeDownRect.width, volumeDownRect.y + volumeDownRect.height)
        glVertex2f(volumeDownRect.x, volumeDownRect.y + volumeDownRect.height)
        glEnd()
        
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(volumeDownRect.x, volumeDownRect.y)
        glVertex2f(volumeDownRect.x + volumeDownRect.width, volumeDownRect.y)
        glVertex2f(volumeDownRect.x + volumeDownRect.width, volumeDownRect.y + volumeDownRect.height)
        glVertex2f(volumeDownRect.x, volumeDownRect.y + volumeDownRect.height)
        glEnd()
    
    # Restore 3D rendering
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    # Draw text using pygame
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    
    # Main button text
    text = font.render("MUSICA", True, (0, 255, 0))
    text_data = pygame.image.tostring(text, "RGBA", True)
    glWindowPos2d(int(musicMenuRect.x + 60), int(height - musicMenuRect.y - 27))
    glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    if musicMenuExpanded:
        # Pause button text
        pause_text = "REANUDAR" if musicPaused else "PAUSAR"
        text = font.render(pause_text, True, (0, 255, 0))
        text_data = pygame.image.tostring(text, "RGBA", True)
        glWindowPos2d(int(pauseButtonRect.x + 45), int(height - pauseButtonRect.y - 22))
        glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
        # Volume buttons text
        text = font.render("VOL +", True, (0, 255, 0))
        text_data = pygame.image.tostring(text, "RGBA", True)
        glWindowPos2d(int(volumeUpRect.x + 15), int(height - volumeUpRect.y - 22))
        glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
        text = font.render("VOL -", True, (0, 255, 0))
        text_data = pygame.image.tostring(text, "RGBA", True)
        glWindowPos2d(int(volumeDownRect.x + 15), int(height - volumeDownRect.y - 22))
        glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
        # Volume percentage
        vol_text = f"{int(musicVolume * 100)}%"
        text = font.render(vol_text, True, (0, 255, 0))
        text_data = pygame.image.tostring(text, "RGBA", True)
        glWindowPos2d(int(musicMenuRect.x + 80), int(height - volumeDownRect.y - 55))
        glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

updateCameraPosition()

isRunning = True

while isRunning:

	deltaTime = clock.tick(60) / 1000

	rend.elapsedTime += deltaTime

	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			# Check music menu clicks
			if event.button == 1:  # Left click
				mouse_pos = pygame.mouse.get_pos()
				
				if musicMenuRect.collidepoint(mouse_pos):
					musicMenuExpanded = not musicMenuExpanded
				elif musicMenuExpanded:
					if pauseButtonRect.collidepoint(mouse_pos):
						if musicPaused:
							pygame.mixer.music.unpause()
							musicPaused = False
							print("Musica reanudada")
						else:
							pygame.mixer.music.pause()
							musicPaused = True
							print("Musica pausada")
					elif volumeUpRect.collidepoint(mouse_pos):
						musicVolume = min(1.0, musicVolume + 0.1)
						pygame.mixer.music.set_volume(musicVolume)
						print(f"Volumen: {int(musicVolume * 100)}%")
					elif volumeDownRect.collidepoint(mouse_pos):
						musicVolume = max(0.0, musicVolume - 0.1)
						pygame.mixer.music.set_volume(musicVolume)
						print(f"Volumen: {int(musicVolume * 100)}%")

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_f:
				rend.ToggleFilledMode()
			
			elif event.key == pygame.K_TAB:
				if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
					newIndex = currentModelIndex - 1
					if newIndex < -1:
						newIndex = len(models) - 1
				else:
					newIndex = (currentModelIndex + 1) % len(models)
				focusOnModel(newIndex)
			
			elif event.key == pygame.K_HOME:
				focusOnModel(-1)
			
			elif event.key == pygame.K_m:
				randomShaderMode = not randomShaderMode
				if randomShaderMode:
					import random
					for i, model in enumerate(models):
						modelShaders[i] = random.randint(0, len(compiledShaders) - 1)
					print("\nRandom Shader Mode")
				else:
					modelShaders.clear()
					print("\nDefault Shader Mode")
			
			elif event.key == pygame.K_1:
				if currentModelIndex >= 0:
					modelShaders[currentModelIndex] = 0
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"Shader Base → {model_name}")
				else:
					currVertexShader = vertex_shader
					currFragmentShader = fragment_shader
					rend.SetShaders(currVertexShader, currFragmentShader)

			elif event.key == pygame.K_2:
				if currentModelIndex >= 0:
					modelShaders[currentModelIndex] = 1
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"Shader Chromatic → {model_name}")
				else:
					currVertexShader = vertex_shader
					currFragmentShader = chromatic_shader
					rend.SetShaders(currVertexShader, currFragmentShader)

			elif event.key == pygame.K_3:
				if currentModelIndex >= 0:
					modelShaders[currentModelIndex] = 2
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"Shader Glitch → {model_name}")
				else:
					currVertexShader = glitch_shader
					currFragmentShader = fragment_shader
					rend.SetShaders(currVertexShader, currFragmentShader)

			elif event.key == pygame.K_4:
				if currentModelIndex >= 0:
					modelShaders[currentModelIndex] = 3
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"Shader Hologram → {model_name}")
				else:
					currVertexShader = vertex_shader
					currFragmentShader = hologram_shader
					rend.SetShaders(currVertexShader, currFragmentShader)

			elif event.key == pygame.K_5:
				if currentModelIndex >= 0:
					modelShaders[currentModelIndex] = 4
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"Shader Nuclear → {model_name}")
				else:
					currVertexShader = nuclear_decay_shader
					currFragmentShader = nuclear_fragment_shader
					rend.SetShaders(currVertexShader, currFragmentShader)

			elif event.key == pygame.K_6:
				if currentModelIndex >= 0:
					modelShaders[currentModelIndex] = 5
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"Shader Pixelate → {model_name}")
				else:
					currVertexShader = vertex_shader
					currFragmentShader = pixelate_shader
					rend.SetShaders(currVertexShader, currFragmentShader)

			elif event.key == pygame.K_7:
				if currentModelIndex >= 0:
					modelShaders[currentModelIndex] = 6
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"Shader Pulse → {model_name}")
				else:
					currVertexShader = pulse_shader
					currFragmentShader = fragment_shader
					rend.SetShaders(currVertexShader, currFragmentShader)

			elif event.key == pygame.K_8:
				if currentModelIndex >= 0:
					modelShaders[currentModelIndex] = 7
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"Shader Radiation → {model_name}")
				else:
					currVertexShader = radiation_pulse_shader
					currFragmentShader = radiation_fragment_shader
					rend.SetShaders(currVertexShader, currFragmentShader)

			elif event.key == pygame.K_9:
				if currentModelIndex >= 0:
					modelShaders[currentModelIndex] = 8
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"Shader Thermal → {model_name}")
				else:
					currVertexShader = vertex_shader
					currFragmentShader = thermal_shader
					rend.SetShaders(currVertexShader, currFragmentShader)
			
			elif event.key == pygame.K_0:
				if currentModelIndex >= 0 and currentModelIndex in modelShaders:
					del modelShaders[currentModelIndex]
					model_name = DIORAMA_MODELS[[i for i, m in enumerate(DIORAMA_MODELS) if m["enabled"]][currentModelIndex]]['name']
					print(f"X Shader removido de {model_name}")
			
			elif event.key == pygame.K_p:
				# Pausar/Reanudar música
				if pygame.mixer.music.get_busy():
					pygame.mixer.music.pause()
					print("\nMusica pausada")
				else:
					pygame.mixer.music.unpause()
					print("\nMusica reanudada")
			
			elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
				# Subir volumen
				current_volume = pygame.mixer.music.get_volume()
				new_volume = min(1.0, current_volume + 0.1)
				pygame.mixer.music.set_volume(new_volume)
				print(f"\nVolumen: {int(new_volume * 100)}%")
			
			elif event.key == pygame.K_MINUS:
				# Bajar volumen
				current_volume = pygame.mixer.music.get_volume()
				new_volume = max(0.0, current_volume - 0.1)
				pygame.mixer.music.set_volume(new_volume)
				print(f"\nVolumen: {int(new_volume * 100)}%")


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
	
	if keys[K_PAGEUP]:
		verticalOffset += 10 * deltaTime
		verticalOffset = min(MAX_VERTICAL, verticalOffset)
		updateCameraPosition()
	
	if keys[K_PAGEDOWN]:
		verticalOffset -= 10 * deltaTime
		verticalOffset = max(MIN_VERTICAL, verticalOffset)
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

	if randomShaderMode or len(modelShaders) > 0:
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		rend.camera.Update()
		if rend.skybox is not None:
			rend.skybox.Render()
		
		for i, obj in enumerate(models):
			if i in modelShaders:
				shaderIndex = modelShaders[i]
				modelShader = compiledShaders[shaderIndex]
			else:
				modelShader = rend.activeShader
			
			if modelShader is None:
				continue
			
			glUseProgram(modelShader)
			glUniformMatrix4fv(glGetUniformLocation(modelShader, "viewMatrix"),
							1, GL_FALSE, glm.value_ptr(rend.camera.viewMatrix))
			glUniformMatrix4fv(glGetUniformLocation(modelShader, "projectionMatrix"),
							1, GL_FALSE, glm.value_ptr(rend.camera.projectionMatrix))
			glUniform3fv(glGetUniformLocation(modelShader, "pointLight"), 1, glm.value_ptr(rend.pointLight))
			glUniform1f(glGetUniformLocation(modelShader, "ambientLight"), rend.ambientLight)
			glUniform1f(glGetUniformLocation(modelShader, "value"), rend.value)
			glUniform1f(glGetUniformLocation(modelShader, "time"), rend.elapsedTime)
			
			for j in range(7):
				glUniform1i(glGetUniformLocation(modelShader, f"tex{j}"), j)
			
			glUniformMatrix4fv(glGetUniformLocation(modelShader, "modelMatrix"),
							1, GL_FALSE, glm.value_ptr(obj.GetModelMatrix()))
			
			useMat = 1 if hasattr(obj, 'useMaterialTexturing') and obj.useMaterialTexturing else 0
			locUseMat = glGetUniformLocation(modelShader, "useMatId")
			if locUseMat != -1:
				glUniform1i(locUseMat, useMat)
			
			hasNormalMap = 1 if hasattr(obj, 'hasNormalMap') and obj.hasNormalMap else 0
			locHasNormalMap = glGetUniformLocation(modelShader, "hasNormalMap")
			if locHasNormalMap != -1:
				glUniform1i(locHasNormalMap, hasNormalMap)
			
			hasFaceTexture = 1 if hasattr(obj, 'hasFaceTexture') and obj.hasFaceTexture else 0
			locHasFaceTexture = glGetUniformLocation(modelShader, "hasFaceTexture")
			if locHasFaceTexture != -1:
				glUniform1i(locHasFaceTexture, hasFaceTexture)
			
			obj.Render()
	else:
		rend.Render()
	
	# Draw 2D music menu on top
	draw_music_menu()
	
	pygame.display.flip()

pygame.quit()