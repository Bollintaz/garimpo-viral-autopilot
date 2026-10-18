#!/usr/bin/env python3
"""Monta um Reel a partir de CENAS GERADAS POR IA já fornecidas.
Nunca gera cenas falsas/estáticas e nunca publica no Facebook.
"""
import pathlib, subprocess, sys
from kokoro import KPipeline
import soundfile as sf
import numpy as np

root=pathlib.Path(".")
scenes=sorted((root/"cenas-ia").glob("*.mp4"))
if not scenes:
    sys.exit("FALTA VIDEO IA: envie pelo menos um MP4 real em cenas-ia/. Nao sera produzido um video falso.")
out=root/"saida";out.mkdir(exist_ok=True)
script=(root/"roteiro.txt")
if not script.exists() or not script.read_text(encoding="utf-8").strip():
    sys.exit("Falta roteiro.txt com texto da narracao.")
texto=script.read_text(encoding="utf-8").strip()
pipe=KPipeline(lang_code="p")
audios=[a for _,_,a in pipe(texto,voice="pf_dora",speed=1.05)]
if not audios:sys.exit("A narracao nao foi gerada.")
sf.write(out/"voz.wav",np.concatenate(audios),24000)
segments=[]
for i,scene in enumerate(scenes):
    name=out/f"cena_{i:03d}.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(scene),
        "-vf","scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30",
        "-an","-c:v","libx264","-preset","veryfast","-crf","22","-pix_fmt","yuv420p",str(name)],check=True)
    segments.append(name)
concat=out/"lista.txt"
concat.write_text("".join("file '"+p.name+"'\n" for p in segments),encoding="utf-8")
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),
    "-i",str(out/"voz.wav"),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac",
    "-b:a","160k","-shortest","-movflags","+faststart",str(out/"garimpo-reel-previa.mp4")],check=True)
print("Preview criado:",out/"garimpo-reel-previa.mp4")
