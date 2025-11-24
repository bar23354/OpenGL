"""
CONFIGURACIÓN DEL DIORAMA
========================
Cada modelo tiene las siguientes propiedades:
- enabled: True/False - Activar o desactivar el modelo
- file: Ruta al archivo .obj
- texture: Ruta a la textura diffuse
- normal_map: Ruta al normal map (None si no tiene)
- position: [x, y, z] - Posición en el mundo
- rotation: [x, y, z] - Rotación en grados
- scale: factor de escala (1.0 = tamaño original, 2.0 = doble, 0.5 = mitad)

TIPS:
- Activa solo 1-2 modelos mientras posicionas para mejor rendimiento
- Ajusta position para mover el modelo
- Ajusta rotation para rotar (0-360 grados)
- Ajusta scale para cambiar tamaño
"""

DIORAMA_MODELS = [
    {
        "name": "Barrel",
        "enabled": True,
        "file": "models/Barrel.obj",
        "texture": "textures/Barrel_d.png",
        "normal_map": "textures/Barrel_n.png",
        "position": [3, -4.9, 26],
        "rotation": [0, 0, 0],
        "scale": 3.5
    },
    {
        "name": "Bloatfly",
        "enabled": True,
        "file": "models/Bloatfly.obj",
        "texture": "textures/Bloatfly_d.png",
        "normal_map": "textures/Bloatfly_n.png",
        "position": [-10, 1, 15],
        "rotation": [0, -45, 0],
        "scale": 0.07
    },
    {
        "name": "Cars",
        "enabled": True,
        "file": "models/Cars.obj",
        "texture": "textures/Cars_d.png",
        "normal_map": None,
        "position": [22, -6, 4.1],
        "rotation": [0, 36, 0],
        "scale": 0.09
    },
    {
        "name": "Concrete",
        "enabled": True,
        "file": "models/Concrete.obj",
        "texture": "textures/Concrete_d.jpg",
        "normal_map": "textures/Concrete_n.jpg",
        "position": [-3, -7.4, 13],
        "rotation": [0, 30, 0],
        "scale": 9.0
    },
    {
        "name": "Desert",
        "enabled": True,
        "file": "models/Desert.obj",
        "texture": "textures/Desert_d.png",
        "normal_map": None,
        "position": [5, -15, 5],
        "rotation": [90, 180, 90],
        "scale": 60.0
    },
    {
        "name": "Eyebot",
        "enabled": True,
        "file": "models/Eyebot.obj",
        "texture": "textures/Eyebot_d.png",
        "normal_map": "textures/Eyebot_n.png",
        "position": [-3, 1, 2],
        "rotation": [-10, -35, -10],
        "scale": 0.06
    },
    {
        "name": "MrHandy",
        "enabled": False,
        "file": "models/MrHandy.obj",
        "texture": "textures/MrHandy_d.png",
        "normal_map": None,
        "position": [10, 1, 10],
        "rotation": [0, 180, 0],
        "scale": 1.5
    },
    {
        "name": "Radroach",
        "enabled": True,
        "file": "models/Radroach.obj",
        "texture": "textures/Radroach_d.png",
        "normal_map": None,
        "position": [31, -5, -16],
        "rotation": [0, 135, 0],
        "scale": 1.1
    },
    {
        "name": "Securitron",
        "enabled": True,
        "file": "models/Securitron.obj",
        "use_material_textures": True,
        "texture": None,
        "normal_map": None,
        "face_texture": "textures/faces/infantry_neutral.png",
        "position": [4, -1.8, 8],
        "rotation": [0, 80, 0],
        "scale": 0.05
    },
    {
        "name": "Tent2",
        "enabled": True,
        "file": "models/Tent2.obj",
        "texture": "textures/Tent2_d.png",
        "normal_map": None,
        "position": [20, -5, 20],
        "rotation": [0, 225, 0],
        "scale": 15.0
    },
    {
        "name": "Tent3",
        "enabled": True,
        "file": "models/Tent3.obj",
        "texture": "textures/Tent3_d.png",
        "normal_map": None,
        "position": [12, 0, -15],
        "rotation": [0, 0, 0],
        "scale": 35.0
    },
    {
        "name": "Box",
        "enabled": True,
        "file": "models/Box.obj",
        "texture": "textures/Box_d.png",
        "normal_map": "textures/Box_n.png",
        "position": [5, -4, 48],
        "rotation": [0, -40, 0],
        "scale": 1.5
    },
    {
        "name": "Flag",
        "enabled": True,
        "file": "models/Flag.obj",
        "texture": "textures/Flag_d.png",
        "normal_map": None,
        "position": [-1, 1.5, -15],
        "rotation": [0, 180, 0],
        "scale": 2.0
    },
    {
        "name": "Gurney",
        "enabled": True,
        "file": "models/Gurney.obj",
        "texture": "textures/Gurney_d.png",
        "normal_map": "textures/Gurney_n.png",
        "position": [15, -4.8, 18],
        "rotation": [0, 180, 0],
        "scale": 0.6
    },
    {
        "name": "Ranger",
        "enabled": True,
        "file": "models/Ranger.obj",
        "texture": "textures/Ranger_d.png",
        "normal_map": "textures/Ranger_n.png",
        "position": [25, -0.3, 24],
        "rotation": [0, 220, 0],
        "scale": 0.09
    },
    {
        "name": "Rubble",
        "enabled": False,
        "file": "models/Rubble.obj",
        "texture": "textures/Rubble_d.png",
        "normal_map": "textures/Rubble_n.png",
        "position": [-15, 0, 13],
        "rotation": [0, 0, 0],
        "scale": 0.001
    },
    {
        "name": "Securitron2", #JANE
        "enabled": True,
        "file": "models/Securitron.obj",
        "use_material_textures": True,
        "texture": None,
        "normal_map": None,
        "face_texture": "textures/faces/jane_neutral.png",
        "position": [-7, -1.7, -12],
        "rotation": [0, 220, 0],
        "scale": 0.05
    },
    {
        "name": "Securitron3", #HOUSE
        "enabled": True,
        "file": "models/Securitron.obj",
        "use_material_textures": True,
        "texture": None,
        "normal_map": None,
        "face_texture": "textures/faces/mrhouse_neutral.png",
        "position": [-8, -1.7, -9],
        "rotation": [0, 70, 0],
        "scale": 0.05
    },
    {
        "name": "Concrete2",
        "enabled": True,
        "file": "models/Concrete.obj",
        "texture": "textures/Concrete_d.jpg",
        "normal_map": "textures/Concrete_n.jpg",
        "position": [-6, -6.2, -12],
        "rotation": [0, -45, 0],
        "scale": 9.0
    }
]

CAMERA_CONFIG = {
    "distance": 20.0,
    "azimuth": 45.0,
    "elevation": 30.0,
    "target": [0, 0, 0]
}

LIGHT_CONFIG = {
    "position": [5, 15, 5],  # Luz más alta para mayor cobertura
    "ambient": 0.5  # Mayor luz ambiente para mejor visibilidad
}
