#ifdef GL_ES
    precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

const float iterations = 100.0;

#define PI_TWO			1.570796326794897
#define PI				3.141592653589793
#define TWO_PI			6.283185307179586
#define E			    2.718281828459045235360287471352 

void main() {
    vec2 c = 2.5*(gl_FragCoord.xy/u_resolution.xy + vec2(-0.75, -0.5));
    //vec2 c = 1.*(gl_FragCoord.xy/u_resolution.xy + vec2(-0.388 - 0.5, -0.135 - 0.5));

    vec2 z = vec2(0.0);
    // (a+bi)^2 = a^2 - b^2 + 2i*ab
    vec3 color = vec3(0.0);
    for (float count = 0.0; count < iterations; count++) { 
        z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
        if (length(z) > 100.0) {
            float dist = count/iterations;
            color = vec3(dist, 0.0, 0.3-dist);
        }
    }

    gl_FragColor = vec4(color, 1.0);


}
