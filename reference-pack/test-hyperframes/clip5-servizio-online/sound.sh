#!/bin/zsh
# Suono sintetico dello spot "Peso" (solo ffmpeg, nessuna libreria esterna).
# sub che sale 2.5-5.93 s, 4 fotogrammi di silenzio, colpo a 6.0 s con crepa e carta che ricade,
# fruscio dei fogli che salgono 8.5-12 s, whoosh della card, "tic" sulla spunta a 13.27 s, tic leggero sul logo.
# Uso: ./sound.sh <uscita.wav>   (poi normalizzato a -14 LUFS / -1 dBTP in montaggio)
OUT=${1:-suono.wav}
D=20; SR=48000
N="anoisesrc=d=$D:r=$SR:c=white:a=1"
NP="anoisesrc=d=$D:r=$SR:c=pink:a=1"
NB="anoisesrc=d=$D:r=$SR:c=brown:a=1"
E() { echo "aevalsrc='$1':d=$D:s=$SR"; }
ffmpeg -y -loglevel error -filter_complex "
$(E 'if(between(t,2.5,5.933),0.75*pow((t-2.5)/3.433,1.6)*sin(2*PI*(30*(t-2.5)+3.64*(t-2.5)^2)),0)')[sub];
$NB,lowpass=f=110,lowpass=f=110[rb];$(E 'if(between(t,2.5,5.933),1.6*pow((t-2.5)/3.433,2),0)')[rbe];[rb][rbe]amultiply[rumble];
$(E 'if(gte(t,6),exp(-(t-6)*2.0)*sin(2*PI*(36*(t-6)+5.5*(1-exp(-(t-6)*8)))),0)')[boom];
$N,highpass=f=1200,lowpass=f=9000[cn];$(E 'if(gte(t,6),0.9*exp(-(t-6)*16),0)')[cne];[cn][cne]amultiply[crack];
$NB,lowpass=f=400[bn];$(E 'if(gte(t,6),1.4*exp(-(t-6)*3.5),0)')[bne];[bn][bne]amultiply[body];
$N,bandpass=f=2800:width_type=h:w=3000[pn];$(E 'if(between(t,6.08,9),0.55*exp(-(t-6.08)*1.1)*pow(abs(sin(2*PI*5.3*t)*sin(2*PI*2.1*t+1)),3),0)')[pne];[pn][pne]amultiply[paper];
$N,bandpass=f=4200:width_type=h:w=4000[rn];$(E 'if(between(t,8.5,12.3),0.5*sin(PI*(t-8.5)/3.8)*(0.55+0.45*abs(sin(2*PI*9*t)*sin(2*PI*3.7*t))),0)')[rne];[rn][rne]amultiply[rustle];
$NP,lowpass=f=1800[wn];$(E 'if(between(t,9.5,13.1),0.6*pow(sin(PI*min(1,(t-9.5)/3.0)/2),3)*if(gt(t,12.5),exp(-(t-12.5)*6),1),0)')[wne];[wn][wne]amultiply[whoosh];
$(E 'if(gte(t,13.27),0.55*exp(-(t-13.27)*90)*sin(2*PI*2900*(t-13.27))+0.3*exp(-(t-13.27)*45)*sin(2*PI*1450*(t-13.27)),0)')[tic];
$(E 'if(gte(t,15.55),0.6*exp(-(t-15.55)*3)*sin(2*PI*52*(t-15.55)),0)')[thump];
$(E 'if(gte(t,18.07),0.25*exp(-(t-18.07)*90)*sin(2*PI*2900*(t-18.07))+0.14*exp(-(t-18.07)*45)*sin(2*PI*1450*(t-18.07)),0)')[tic2];
$NP,lowpass=f=600,volume=0.012[room];
[sub][rumble][boom][crack][body][paper][rustle][whoosh][tic][thump][tic2][room]amix=inputs=12:normalize=0,
aformat=channel_layouts=stereo,extrastereo=m=1.0,alimiter=limit=0.95:level=disabled[out]" -map "[out]" -ar $SR -c:a pcm_s24le "$OUT"
