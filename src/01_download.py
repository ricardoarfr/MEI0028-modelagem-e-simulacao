"""01_download.py — baixa os 4 arquivos do dataset Rieth et al. (2017) e verifica MD5.
Fonte: Harvard Dataverse, DOI 10.7910/DVN/6C3JR1. Metadados via API em 2026-09-06.
Usa curl com user-agent de navegador (o Dataverse retorna 403 ao UA padrão do Python)."""
import hashlib, json, os, subprocess, sys, time
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,"..","data","raw")
META=os.path.join(HERE,"..","results","metadata")
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/120 Safari/537.36"
FILES={3031241:("TEP_FaultFree_Training.RData",24678017,"ec126484534331f85001d8c4ebce6d17"),
       3031240:("TEP_FaultFree_Testing.RData",47327663,"38ad9810fc871026157086ae2c2f0ee9"),
       3031242:("TEP_Faulty_Training.RData",494063194,"c5f594d54c47e620ff877feb58407fda"),
       3031243:("TEP_Faulty_Testing.RData",836882037,"556bdb64c83021bc0c5f92e427753565")}
def md5(p):
    h=hashlib.md5()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()
log=[]
for fid,(name,size,want) in FILES.items():
    dst=os.path.join(RAW,name)
    if os.path.exists(dst) and os.path.getsize(dst)==size and md5(dst)==want:
        print(f"OK cache {name}",flush=True); log.append(dict(arquivo=name,bytes=size,md5=want,status="ok-cache")); continue
    for tent in range(1,6):
        t=time.time(); print(f"baixando {name} ({size/1e6:.0f} MB) tent {tent}",flush=True)
        r=subprocess.run(["curl","-sS","-L","-A",UA,"--retry","3","-C","-","-o",dst,
                          f"https://dataverse.harvard.edu/api/access/datafile/{fid}"])
        if r.returncode==0 and os.path.exists(dst) and os.path.getsize(dst)==size:
            got=md5(dst); dt=time.time()-t
            if got==want: print(f"  OK {dt:.0f}s md5 confere",flush=True); log.append(dict(arquivo=name,bytes=size,md5=got,status=f"ok {dt:.0f}s")); break
            print(f"  MD5 diverge {got}",flush=True)
        else: print(f"  rc={r.returncode} size={os.path.getsize(dst) if os.path.exists(dst) else 0}",flush=True)
        if os.path.exists(dst): os.remove(dst)
        time.sleep(10)
    else: print(f"FALHA {name}",flush=True); sys.exit(1)
json.dump(log,open(os.path.join(META,"download_manifest.json"),"w"),indent=2)
print("DOWNLOAD COMPLETO",flush=True)
