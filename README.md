# OpenGL

**UVG - GRÁFICAS POR COMPUTADORA - SECCIÓN 20 - 2025**

**Nombre:** Roberto José Barreda Siekavizza  
**Carné:** #23354

---

## Actividades:

### Lab 9: Shaders II

### Lab 10: Model Viewer

---

## Proyecto-3: OpenGL - Diorama de Fallout New Vegas

---

#### **CÁMARA:**
- `Click Izquierdo + Arrastrar`: Orbitar alrededor del punto actual
- `Rueda del Mouse`: Zoom In/Out
- `Flechas ←→`: Rotar horizontalmente
- `Flechas ↑↓`: Rotar verticalmente  
- `Z / X`: Zoom Out / Zoom In (teclado)
- `PageUp / PageDown`: Desplazar verticalmente
- `TAB`: Cambiar a siguiente modelo (enfoque individual)
- `SHIFT+TAB`: Cambiar a modelo anterior
- `HOME`: Volver a vista global del diorama

#### **LUZ:**
- `W/S`: Mover luz en eje Z
- `A/D`: Mover luz en eje X
- `R/T`: Mover luz en eje Y

#### **SHADERS (Aplicar al modelo seleccionado):**
- `1`: Base Shader (iluminación estándar + normal mapping)
- `2`: Chromatic Aberration Shader (separación de canales RGB)
- `3`: Glitch Shader (distorsión digital)
- `4`: Hologram Shader (efecto holográfico con scanlines)
- `5`: Nuclear Decay Shader (derretimiento radioactivo)
- `6`: Pixelate Shader (pixelación dinámica)
- `7`: Pulse Shader (pulsación rítmica)
- `8`: Radiation Pulse Shader (ondas radioactivas verdes)
- `9`: Thermal Vision Shader (visión térmica)
- `0`: Remover shader personalizado del modelo

#### **MODOS:**
- `M`: Modo aleatorio - asigna shader diferente a cada modelo automáticamente
- `F`: Toggle Filled/Wireframe Mode

---

### Flujo

1. **Vista Global**: Al iniciar, la cámara muestra todo el diorama en una vista panorámica
2. **Selección de Modelo**: Presiona `TAB` para navegar entre modelos individuales
   - La cámara se enfoca automáticamente en cada modelo
   - El nombre del modelo se muestra en consola
3. **Aplicar Shaders**: Con un modelo seleccionado, presiona `1-9` para asignarle un shader específico
4. **Persistencia**: Cada modelo mantiene su shader asignado al cambiar a otro
5. **Modo Aleatorio**: Presiona `M` para que cada modelo obtenga un shader diferente automáticamente
6. **Control de Luz**: Usa `W/A/S/D/R/T` para mover la luz y ver diferentes efectos de iluminación
7. **Vista Global**: Presiona `HOME` en cualquier momento para volver a la vista completa del diorama

---

### Configuración del Diorama

Edita `Proyecto-3/diorama_config.py` para personalizar:
- **Modelos**: Activar/desactivar modelos individuales
- **Posiciones**: Ajustar coordenadas `[x, y, z]`
- **Rotaciones**: Cambiar orientación en grados `[pitch, yaw, roll]`
- **Escalas**: Modificar tamaño de modelos
- **Texturas**: Cambiar texturas diffuse y normal maps
- **Caras de Securitrons**: Asignar diferentes expresiones faciales (infantry, jane, mrhouse)
- **Cámara**: Configurar posición inicial, distancia, y ángulos
- **Luz**: Ajustar posición y luz ambiente

Ejemplo de configuración de modelo:
```python
{
    "name": "Securitron",
    "enabled": True,
    "file": "models/Securitron.obj",
    "use_material_textures": True,
    "texture": None,
    "normal_map": None,
    "face_texture": "textures/faces/infantry_neutral.png",
    "position": [-10, -1.5, -9],
    "rotation": [0, 200, 0],
    "scale": 0.05
}
```

---

### Requisitos e Instalación

#### Requisitos:
```bash
pip install pygame PyOpenGL PyGLM imageio
```


#### Ejecución:
```bash
cd Proyecto-3
python RendererOpenGL2025.py
```

---

### Modelos Incluidos en el Diorama

1. **Desert Terrain** - Base desértica del diorama (escala: 60x)
2. **Securitron** (×3) - Robots de seguridad con caras diferentes
   - Infantry (neutral)
   - Jane (femenina)
   - Mr. House (líder)
3. **Barrel** - Barril metálico post-apocalíptico
4. **Bloatfly** - Criatura mutante voladora
5. **Cars** - Vehículos destruidos
6. **Concrete Barriers** (×2) - Barreras de concreto
7. **Eyebot** - Robot explorador flotante
8. **Radroach** - Cucaracha radioactiva gigante
9. **Tent2, Tent3** - Tiendas de campaña militares
10. **Box** - Caja de suministros
11. **Flag** - Bandera del NCR
12. **Gurney** - Camilla médica
13. **Ranger** - NCR Ranger armado

### Proyecto para

**Universidad del Valle de Guatemala**  
**Gráficas por Computadora - Sección 20**  
**Semestre II - 2025**  