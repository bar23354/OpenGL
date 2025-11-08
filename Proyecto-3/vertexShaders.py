

vertex_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;
layout (location = 3) in float inMatId;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;
out vec3 fragTangent;
out vec3 fragBitangent;
flat out int vMatId;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(inPosition, 1.0);

    fragPosition = modelMatrix * vec4(inPosition, 1.0);

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    // Calculate tangent and bitangent for normal mapping
    vec3 c1 = cross(inNormals, vec3(0.0, 0.0, 1.0));
    vec3 c2 = cross(inNormals, vec3(0.0, 1.0, 0.0));
    
    vec3 tangent;
    if (length(c1) > length(c2)) {
        tangent = c1;
    } else {
        tangent = c2;
    }
    
    fragTangent = normalize(vec3(modelMatrix * vec4(tangent, 0.0)));
    fragBitangent = normalize(cross(fragNormal, fragTangent));

    fragTexCoords = inTexCoords;
    vMatId = int(inMatId + 0.5);
}

'''


radiation_pulse_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;
layout (location = 3) in float inMatId;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;
out vec3 fragTangent;
out vec3 fragBitangent;
out float glowIntensity;
flat out int vMatId;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;


void main()
{
    float pulse = abs(sin(time * 3.0));
    float radiationWave = sin(time * 2.0 + length(inPosition) * 5.0) * pulse;
    
    float intensity = 0.15 + value * 0.3;
    vec3 radDisplacement = inNormals * radiationWave * intensity;
    
    float distortion = sin(time * 4.0 + inPosition.y * 10.0) * 0.05 * (1.0 + value);
    radDisplacement.x += distortion;
    radDisplacement.z += distortion;
    
    fragPosition = modelMatrix * vec4(inPosition + radDisplacement, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    vec3 distortedNormal = inNormals + vec3(sin(time * 2.0), cos(time * 2.0), 0) * 0.2;
    fragNormal = normalize(vec3(modelMatrix * vec4(distortedNormal, 0.0)));

    // Calculate tangent and bitangent for normal mapping
    vec3 c1 = cross(inNormals, vec3(0.0, 0.0, 1.0));
    vec3 c2 = cross(inNormals, vec3(0.0, 1.0, 0.0));
    
    vec3 tangent;
    if (length(c1) > length(c2)) {
        tangent = c1;
    } else {
        tangent = c2;
    }
    
    fragTangent = normalize(vec3(modelMatrix * vec4(tangent, 0.0)));
    fragBitangent = normalize(cross(fragNormal, fragTangent));

    fragTexCoords = inTexCoords;
    glowIntensity = pulse;
    vMatId = int(inMatId + 0.5);
}

'''


nuclear_decay_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;
layout (location = 3) in float inMatId;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;
out vec3 fragTangent;
out vec3 fragBitangent;
out float decayFactor;
flat out int vMatId;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;


void main()
{
    float decay = fract(time * 0.3);
    float baseIntensity = 0.5 + value * 1.5;
    float meltFactor = pow(decay, 2.0) * baseIntensity;
    
    vec3 meltDirection = vec3(0, -1, 0);
    float heightFactor = (1.0 - inPosition.y) * 0.5 + 0.5;
    
    vec3 decayOffset = meltDirection * meltFactor * heightFactor;
    
    float noise = sin(inPosition.x * 10.0 + time) * cos(inPosition.z * 10.0 + time) * 0.05;
    decayOffset += inNormals * noise * meltFactor;
    
    float jitter = sin(time * 10.0 + length(inPosition) * 20.0) * meltFactor * 0.02;
    decayOffset += vec3(jitter, 0, jitter);
    
    fragPosition = modelMatrix * vec4(inPosition + decayOffset, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));

    // Calculate tangent and bitangent for normal mapping
    vec3 c1 = cross(inNormals, vec3(0.0, 0.0, 1.0));
    vec3 c2 = cross(inNormals, vec3(0.0, 1.0, 0.0));
    
    vec3 tangent;
    if (length(c1) > length(c2)) {
        tangent = c1;
    } else {
        tangent = c2;
    }
    
    fragTangent = normalize(vec3(modelMatrix * vec4(tangent, 0.0)));
    fragBitangent = normalize(cross(fragNormal, fragTangent));

    fragTexCoords = inTexCoords;
    decayFactor = meltFactor;
    vMatId = int(inMatId + 0.5);
}

'''


pulse_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;
layout (location = 3) in float inMatId;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;
out vec3 fragTangent;
out vec3 fragBitangent;
flat out int vMatId;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;

void main()
{
    float pulse = sin(time * 2.0) * 0.5 + 0.5;
    float pulseIntensity = 0.3 + value * 0.7;
    float scale = 1.0 + pulse * pulseIntensity;
    
    vec3 pulsedPosition = inPosition * scale;
    
    fragPosition = modelMatrix * vec4(pulsedPosition, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    
    // Calculate tangent and bitangent for normal mapping
    vec3 c1 = cross(inNormals, vec3(0.0, 0.0, 1.0));
    vec3 c2 = cross(inNormals, vec3(0.0, 1.0, 0.0));
    
    vec3 tangent;
    if (length(c1) > length(c2)) {
        tangent = c1;
    } else {
        tangent = c2;
    }
    
    fragTangent = normalize(vec3(modelMatrix * vec4(tangent, 0.0)));
    fragBitangent = normalize(cross(fragNormal, fragTangent));
    
    fragTexCoords = inTexCoords;
    vMatId = int(inMatId + 0.5);
}
'''


glitch_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;
layout (location = 3) in float inMatId;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;
out vec3 fragTangent;
out vec3 fragBitangent;
flat out int vMatId;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main()
{
    float glitchAmount = 0.2 + value * 0.5;
    float timeStep = floor(time * 10.0);
    
    vec3 offset = vec3(0.0);
    if (random(vec2(timeStep, inPosition.y)) > 0.7) {
        offset.x = (random(vec2(timeStep, inPosition.x)) - 0.5) * glitchAmount;
        offset.y = (random(vec2(timeStep + 1.0, inPosition.y)) - 0.5) * glitchAmount * 0.5;
        offset.z = (random(vec2(timeStep + 2.0, inPosition.z)) - 0.5) * glitchAmount * 0.3;
    }
    
    vec3 glitchedPosition = inPosition + offset;
    
    fragPosition = modelMatrix * vec4(glitchedPosition, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    
    // Calculate tangent and bitangent for normal mapping
    vec3 c1 = cross(inNormals, vec3(0.0, 0.0, 1.0));
    vec3 c2 = cross(inNormals, vec3(0.0, 1.0, 0.0));
    
    vec3 tangent;
    if (length(c1) > length(c2)) {
        tangent = c1;
    } else {
        tangent = c2;
    }
    
    fragTangent = normalize(vec3(modelMatrix * vec4(tangent, 0.0)));
    fragBitangent = normalize(cross(fragNormal, fragTangent));
    
    fragTexCoords = inTexCoords;
    vMatId = int(inMatId + 0.5);
}
'''
