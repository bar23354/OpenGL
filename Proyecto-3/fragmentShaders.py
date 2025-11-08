fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;
in vec3 fragTangent;
in vec3 fragBitangent;
flat in int vMatId;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform sampler2D tex3;
uniform sampler2D tex4;
uniform sampler2D tex5;
uniform sampler2D tex6;
uniform vec3 pointLight;
uniform float ambientLight;
uniform int useMatId;
uniform int hasNormalMap;

vec4 sampleByMat(int id, vec2 uv) {
    if (id == 0) return texture(tex0, uv);
    else if (id == 1) return texture(tex1, uv);
    else if (id == 2) return texture(tex2, uv);
    else if (id == 3) return texture(tex3, uv);
    else if (id == 4) return texture(tex4, uv);
    else if (id == 5) return texture(tex5, uv);
    else if (id == 6) return texture(tex6, uv);
    else return texture(tex0, uv);
}

void main()
{
    vec3 normal = fragNormal;
    
    if (hasNormalMap == 1) {
        vec3 normalMapValue = texture(tex1, fragTexCoords).rgb * 2.0 - 1.0;
        mat3 TBN = mat3(normalize(fragTangent), normalize(fragBitangent), normalize(fragNormal));
        normal = normalize(TBN * normalMapValue);
    }
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(normal, lightDir)) + ambientLight;
    vec4 baseColor = (useMatId == 1) ? sampleByMat(vMatId % 7, fragTexCoords)
                                     : texture(tex0, fragTexCoords);
    fragColor = baseColor * intensity;
}

'''


hologram_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;
in vec3 fragTangent;
in vec3 fragBitangent;
flat in int vMatId;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;
uniform int hasNormalMap;

void main()
{
    vec3 normal = fragNormal;
    
    if (hasNormalMap == 1) {
        vec3 normalMapValue = texture(tex1, fragTexCoords).rgb * 2.0 - 1.0;
        mat3 TBN = mat3(normalize(fragTangent), normalize(fragBitangent), normalize(fragNormal));
        normal = normalize(TBN * normalMapValue);
    }
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(normal, lightDir)) + ambientLight;
    
    vec3 baseColor = texture(tex0, fragTexCoords).rgb * intensity;
    
    float scanline = sin(fragTexCoords.y * 200.0 + time * 5.0) * 0.5 + 0.5;
    scanline = pow(scanline, 3.0);
    
    float flicker = sin(time * 20.0) * 0.03 + 0.97;
    
    vec3 holoColor = baseColor * vec3(0.3, 0.8, 1.0);
    holoColor *= scanline * flicker;
    
    float edgeGlow = 1.0 - abs(dot(normalize(normal), normalize(-fragPosition.xyz)));
    edgeGlow = pow(edgeGlow, 3.0);
    holoColor += vec3(0.2, 0.6, 1.0) * edgeGlow;
    
    fragColor = vec4(holoColor, 0.7 + scanline * 0.3);
}
'''


pixelate_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;
in vec3 fragTangent;
in vec3 fragBitangent;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float value;
uniform int hasNormalMap;

void main()
{
    float basePixelSize = 0.02;
    float pixelSize = basePixelSize + value * 0.03;
    
    vec2 pixelatedCoords = floor(fragTexCoords / pixelSize) * pixelSize;
    
    vec3 normal = fragNormal;
    
    if (hasNormalMap == 1) {
        vec3 normalMapValue = texture(tex1, pixelatedCoords).rgb * 2.0 - 1.0;
        mat3 TBN = mat3(normalize(fragTangent), normalize(fragBitangent), normalize(fragNormal));
        normal = normalize(TBN * normalMapValue);
    }
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(normal, lightDir)) + ambientLight;
    
    vec4 texColor = texture(tex0, pixelatedCoords);
    
    fragColor = texColor * intensity;
}
'''


thermal_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;
in vec3 fragTangent;
in vec3 fragBitangent;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform int hasNormalMap;

void main()
{
    vec3 normal = fragNormal;
    
    if (hasNormalMap == 1) {
        vec3 normalMapValue = texture(tex1, fragTexCoords).rgb * 2.0 - 1.0;
        mat3 TBN = mat3(normalize(fragTangent), normalize(fragBitangent), normalize(fragNormal));
        normal = normalize(TBN * normalMapValue);
    }
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(normal, lightDir)) + ambientLight;
    
    float heat = intensity + sin(time + fragPosition.y) * 0.2;
    
    vec3 coldColor = vec3(0.0, 0.0, 0.5);
    vec3 warmColor = vec3(0.5, 0.0, 0.5);
    vec3 hotColor = vec3(1.0, 0.5, 0.0);
    vec3 veryHotColor = vec3(1.0, 1.0, 0.0);
    
    vec3 thermalColor;
    if (heat < 0.33) {
        thermalColor = mix(coldColor, warmColor, heat / 0.33);
    } else if (heat < 0.66) {
        thermalColor = mix(warmColor, hotColor, (heat - 0.33) / 0.33);
    } else {
        thermalColor = mix(hotColor, veryHotColor, (heat - 0.66) / 0.34);
    }
    
    fragColor = vec4(thermalColor, 1.0);
}
'''


chromatic_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;
in vec3 fragTangent;
in vec3 fragBitangent;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;
uniform int hasNormalMap;

void main()
{
    vec3 normal = fragNormal;
    
    if (hasNormalMap == 1) {
        vec3 normalMapValue = texture(tex1, fragTexCoords).rgb * 2.0 - 1.0;
        mat3 TBN = mat3(normalize(fragTangent), normalize(fragBitangent), normalize(fragNormal));
        normal = normalize(TBN * normalMapValue);
    }
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(normal, lightDir)) + ambientLight;
    
    float baseAberration = 0.01 + value * 0.02;
    
    vec2 offset = vec2(sin(time), cos(time)) * baseAberration;
    
    float r = texture(tex0, fragTexCoords + offset).r;
    float g = texture(tex0, fragTexCoords).g;
    float b = texture(tex0, fragTexCoords - offset).b;
    
    vec3 color = vec3(r, g, b) * intensity;
    
    fragColor = vec4(color, 1.0);
}
'''


radiation_fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;
in vec3 fragTangent;
in vec3 fragBitangent;
in float glowIntensity;
flat in int vMatId;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform int hasNormalMap;

void main()
{
    vec3 normal = fragNormal;
    
    // Note: tex1 is normal map if hasNormalMap==1, otherwise it's radiation texture
    if (hasNormalMap == 1) {
        vec3 normalMapValue = texture(tex1, fragTexCoords).rgb * 2.0 - 1.0;
        mat3 TBN = mat3(normalize(fragTangent), normalize(fragBitangent), normalize(fragNormal));
        normal = normalize(TBN * normalMapValue);
    }
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(normal, lightDir)) + ambientLight;
    
    vec4 baseColor = texture(tex0, fragTexCoords) * intensity;
    
    vec3 radiationColor = vec3(0.0, 1.0, 0.2);
    vec3 glowColor = mix(baseColor.rgb, radiationColor, glowIntensity * 0.5);
    
    float pulseAdd = glowIntensity * 0.3;
    glowColor += radiationColor * pulseAdd;
    
    fragColor = vec4(glowColor, 1.0);
}
'''


nuclear_fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;
in vec3 fragTangent;
in vec3 fragBitangent;
in float decayFactor;
flat in int vMatId;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform int hasNormalMap;

void main()
{
    vec3 normal = fragNormal;
    
    // Note: tex1 is normal map if hasNormalMap==1, otherwise it's uranium texture
    if (hasNormalMap == 1) {
        vec3 normalMapValue = texture(tex1, fragTexCoords).rgb * 2.0 - 1.0;
        mat3 TBN = mat3(normalize(fragTangent), normalize(fragBitangent), normalize(fragNormal));
        normal = normalize(TBN * normalMapValue);
    }
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(normal, lightDir)) + ambientLight;
    
    vec4 baseColor = texture(tex0, fragTexCoords) * intensity;
    
    vec3 hotColor = vec3(1.0, 0.5, 0.0);
    vec3 nuclearGlow = vec3(0.0, 1.0, 0.0);
    
    vec3 decayColor = mix(baseColor.rgb, hotColor, decayFactor * 0.5);
    decayColor += nuclearGlow * decayFactor * 0.3;
    
    fragColor = vec4(decayColor, 1.0);
}
'''



