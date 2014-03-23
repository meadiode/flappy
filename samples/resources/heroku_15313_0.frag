//http://glsl.heroku.com/e#15313_0

#ifdef GL_ES
precision mediump float;
#endif
uniform float time;uniform vec2 resolution;void main() {
vec2 R=resolution,P=gl_FragCoord.xy/min(R.x,R.y)*2.-vec2(max(R.x/R.y,1.),max(R.y/R.x,1.));
vec3 col=vec3(0);float T=time,bt=T*.06;
for(float i=2.;i<9.;++i){
    float t=mod(T*.4,1e3)*i,x=P.x-cos(t)*.7,y=P.y-sin(t)*.7,
    tt=t*(i+3.)/2.+x*tan(t*1.5)+y*tan(t*2.);
    vec2 d=vec2(x*cos(tt)+y*sin(tt),x*sin(tt)-y*cos(tt));
    d*=vec2(1.85+cos(bt)*.35)-abs(vec2(sin(t*.5),cos(t*.5)));
    float d2=dot(d,d)-.12;
    vec3 u=mod(T*vec3(2.,1.9,1.8),1e3)*(i*.1+2.),
    v=vec3(sin(u.x),cos(u.y),sin(u.z+.787));
    col+=v*v*.02/abs(d2);
    if(d2<.0)col+=.3*sin(u)*sin(u);
}
gl_FragColor = vec4(col*min(1.,cos(bt)/1.5+1.),1.);
}