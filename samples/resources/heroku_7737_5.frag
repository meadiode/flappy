//http://glsl.heroku.com/e#7737.5

uniform vec2 resolution;
uniform vec2 mouse;
uniform float time;

// modified by @hintz

float lengthN(vec2 v, float n)
{
  vec2 l = pow(abs(v), vec2(n));
  
  return pow(abs(l.x-l.y), 1.0/n);
}
 
float rings(vec2 p)
{
  return sin(lengthN(mod(p*5.0, 2.0)-1.0, 4.0)*5.0*lengthN(p,2.0)+time*3.0);
}

void main()
{
  vec2 p = (gl_FragCoord.xy*2.0 -resolution) / resolution.y;;
    
  float c = rings(p);
  
  gl_FragColor = vec4(c,c*c*length(p),-c,1.0);
}