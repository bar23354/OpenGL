

vertex_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(inPosition, 1.0);

    fragPosition = modelMatrix * vec4(inPosition, 1.0);

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''


fat_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float value;


void main()
{
    fragPosition = modelMatrix * vec4(inPosition + inNormals * value, 1.0);

    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''


water_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;


void main()
{
    float displacement = sin(time + inPosition.x + inPosition.z) * value;
    fragPosition = modelMatrix * vec4(inPosition + vec3(0,displacement, 0)  , 1.0);

    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''


radiation_pulse_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;


void main()
{
    float pulse = abs(sin(time * 3.0));
    float radiationWave = sin(time * 2.0 + length(inPosition) * 5.0) * pulse;
    
    vec3 radDisplacement = inNormals * radiationWave * value * 0.3;
    
    float distortion = sin(time * 4.0 + inPosition.y * 10.0) * 0.1 * value;
    radDisplacement.x += distortion;
    radDisplacement.z += distortion;
    
    fragPosition = modelMatrix * vec4(inPosition + radDisplacement, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    vec3 distortedNormal = inNormals + vec3(sin(time * 2.0), cos(time * 2.0), 0) * 0.2;
    fragNormal = normalize(vec3(modelMatrix * vec4(distortedNormal, 0.0)));

    fragTexCoords = inTexCoords;
}

'''


nuclear_decay_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;


void main()
{
    float decay = fract(time * 0.3);
    float meltFactor = pow(decay, 2.0) * value;
    
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

    fragTexCoords = inTexCoords;
}

'''