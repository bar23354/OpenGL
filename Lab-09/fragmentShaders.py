# GLSL

fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''


toon_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    if (intensity < 0.33)
        intensity = 0.2;
    else if (intensity < 0.66)
        intensity = 0.6;
    else
        intensity = 1.0;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''


negative_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;

void main()
{
    fragColor = 1 - texture(tex0, fragTexCoords);
}

'''


magma_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;

uniform vec3 pointLight;
uniform float ambientLight;

uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
    fragColor += texture(tex1, fragTexCoords) * ((sin(time) + 1) / 2);
}

'''


hologram_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(fragNormal, lightDir)) + ambientLight;
    
    vec3 baseColor = texture(tex0, fragTexCoords).rgb * intensity;
    
    float scanline = sin(fragTexCoords.y * 200.0 + time * 5.0) * 0.5 + 0.5;
    scanline = pow(scanline, 3.0);
    
    float flicker = sin(time * 20.0) * 0.03 + 0.97;
    
    vec3 holoColor = baseColor * vec3(0.3, 0.8, 1.0);
    holoColor *= scanline * flicker;
    
    float edgeGlow = 1.0 - abs(dot(normalize(fragNormal), normalize(-fragPosition.xyz)));
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

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float value;

void main()
{
    float basePixelSize = 0.02;
    float pixelSize = basePixelSize + value * 0.03;
    
    vec2 pixelatedCoords = floor(fragTexCoords / pixelSize) * pixelSize;
    
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(fragNormal, lightDir)) + ambientLight;
    
    vec4 texColor = texture(tex0, pixelatedCoords);
    
    fragColor = texColor * intensity;
}
'''


thermal_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(fragNormal, lightDir)) + ambientLight;
    
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

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;
uniform float value;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(fragNormal, lightDir)) + ambientLight;
    
    float baseAberration = 0.01 + value * 0.02;
    
    vec2 offset = vec2(sin(time), cos(time)) * baseAberration;
    
    float r = texture(tex0, fragTexCoords + offset).r;
    float g = texture(tex0, fragTexCoords).g;
    float b = texture(tex0, fragTexCoords - offset).b;
    
    vec3 color = vec3(r, g, b) * intensity;
    
    fragColor = vec4(color, 1.0);
}
'''


outline_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(fragNormal, lightDir)) + ambientLight;
    
    vec3 viewDir = normalize(-fragPosition.xyz);
    float edge = 1.0 - abs(dot(viewDir, fragNormal));
    edge = pow(edge, 3.0);
    
    vec3 texColor = texture(tex0, fragTexCoords).rgb * intensity;
    vec3 outlineColor = vec3(0.0, 0.0, 0.0);
    
    if (edge > 0.7) {
        fragColor = vec4(outlineColor, 1.0);
    } else {
        fragColor = vec4(texColor, 1.0);
    }
}
'''


radiation_fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;
in float glowIntensity;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(fragNormal, lightDir)) + ambientLight;
    
    vec4 baseColor = texture(tex0, fragTexCoords) * intensity;
    vec4 radiationTexture = texture(tex1, fragTexCoords);
    
    vec3 radiationColor = vec3(0.0, 1.0, 0.2);
    vec3 glowColor = mix(baseColor.rgb, radiationTexture.rgb * radiationColor, glowIntensity * 0.7);
    
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
in float decayFactor;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(fragNormal, lightDir)) + ambientLight;
    
    vec4 baseColor = texture(tex0, fragTexCoords) * intensity;
    vec4 uraniumTexture = texture(tex1, fragTexCoords);
    
    vec3 hotColor = vec3(1.0, 0.5, 0.0);
    vec3 nuclearGlow = vec3(0.0, 1.0, 0.0);
    
    vec3 decayColor = mix(baseColor.rgb, uraniumTexture.rgb, decayFactor * 0.8);
    decayColor = mix(decayColor, hotColor, decayFactor * 0.5);
    decayColor += nuclearGlow * decayFactor * 0.3;
    
    fragColor = vec4(decayColor, 1.0);
}
'''




