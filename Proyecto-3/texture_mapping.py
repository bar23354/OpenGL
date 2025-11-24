TEXTURE_MAPPING = {
    "securitronclean.dds": "textures/securitronclean.png",
    "securitronclean_n.dds": "textures/securitronclean_n.png",
    "securitron.dds": "textures/securitron.png",
    "securitron_n.dds": "textures/securitron_n.png",
    "secrocket.dds": "textures/secrocket.png",
    "secrocket_n.dds": "textures/secrocket_n.png",
    "victor_neutral.dds": "textures/faces/infantry_neutral.png",
}

def map_texture_path(original_path):
    import os
    filename = os.path.basename(original_path).lower()
    
    if filename in TEXTURE_MAPPING:
        return TEXTURE_MAPPING[filename]
    
    return original_path
