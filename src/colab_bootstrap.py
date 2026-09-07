"""colab_bootstrap.py — prepara o VM do Colab: baixa os .RData (curl+UA), converte p/ parquet float32.
Execute com: colab exec -s wp1a -f src/colab_bootstrap.py   (o manifesto é enviado por colab upload)"""
import os, subprocess, hashlib, time
ROOT="/content/ProjetoA_WP1A"; RAW=f"{ROOT}/data/raw"; PROC=f"{ROOT}/data/processed"
for d in (RAW,PROC,f"{ROOT}/results/metadata",f"{ROOT}/configs",f"{ROOT}/results/tables",f"{ROOT}/results/figures"): os.makedirs(d,exist_ok=True)
subprocess.run("pip install -q pyreadr pyarrow 2>/dev/null",shell=True)
import pyreadr, pandas as pd
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/120 Safari/537.36"
FILES={3031241:("TEP_FaultFree_Training",24678017,"ec126484534331f85001d8c4ebce6d17"),3031240:("TEP_FaultFree_Testing",47327663,"38ad9810fc871026157086ae2c2f0ee9"),
       3031242:("TEP_Faulty_Training",494063194,"c5f594d54c47e620ff877feb58407fda"),3031243:("TEP_Faulty_Testing",836882037,"556bdb64c83021bc0c5f92e427753565")}
def md5(p):
    h=hashlib.md5(); f=open(p,"rb")
    for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()
for fid,(name,size,want) in FILES.items():
    pq=f"{PROC}/{name}.parquet"
    if os.path.exists(pq): print("parquet existe",name,flush=True); continue
    dst=f"{RAW}/{name}.RData"; t=time.time()
    for tent in range(4):
        subprocess.run(["curl","-sS","-L","-A",UA,"-C","-","-o",dst,f"https://dataverse.harvard.edu/api/access/datafile/{fid}"])
        if os.path.exists(dst) and os.path.getsize(dst)==size and md5(dst)==want: break
        if os.path.exists(dst): os.remove(dst)
    else: raise SystemExit(f"falha download {name}")
    print(f"baixado {name} {time.time()-t:.0f}s md5 ok",flush=True)
    df=list(pyreadr.read_r(dst).values())[0]
    for c in df.columns: df[c]=df[c].astype("int32" if c in ("faultNumber","simulationRun","sample") else "float32")
    df.to_parquet(pq,index=False); os.remove(dst); print(f"  parquet {name} {df.shape}",flush=True)
print("BOOTSTRAP COMPLETO",flush=True)
