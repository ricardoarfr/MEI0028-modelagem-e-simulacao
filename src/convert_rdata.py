"""convert_rdata.py — converte .RData → Parquet float32 com MEMÓRIA CONSTANTE.
R nativo carrega o objeto e grava uma parte .rds por classe (faultNumber); Python lê cada parte com
pyreadr e anexa a um único Parquet (pyarrow ParquetWriter). Evita materializar 9,6 M linhas duas vezes."""
import os, sys, glob, subprocess, shutil, time, numpy as np, pyreadr, pyarrow as pa, pyarrow.parquet as pq
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
RAW=os.path.join(ROOT,"data","raw"); PROC=os.path.join(ROOT,"data","processed"); os.makedirs(PROC,exist_ok=True)
RS='args<-commandArgs(TRUE); nm<-load(args[1]); df<-get(nm[1]); cat("objeto:",nm[1],"dims:",dim(df),"\n"); ' \
   'for(k in sort(unique(df$faultNumber))){ saveRDS(df[df$faultNumber==k,], file.path(args[2], sprintf("part_%02d.rds",k)), compress=FALSE) }'
ID=["faultNumber","simulationRun","sample"]
for name in ["TEP_FaultFree_Training","TEP_FaultFree_Testing","TEP_Faulty_Training","TEP_Faulty_Testing"]:
    pq_path=os.path.join(PROC,name+".parquet")
    if os.path.exists(pq_path): print("parquet existe",name,flush=True); continue
    src=os.path.join(RAW,name+".RData"); parts=os.path.join(PROC,"_parts_"+name); shutil.rmtree(parts,ignore_errors=True); os.makedirs(parts)
    t=time.time(); r=subprocess.run(["Rscript","-e",RS,src,parts],capture_output=True,text=True); print(name,r.stdout.strip(),r.stderr.strip()[-300:],flush=True)
    if r.returncode!=0: sys.exit(f"Rscript falhou em {name}")
    writer=None; n=0
    for part in sorted(glob.glob(os.path.join(parts,"part_*.rds"))):
        df=list(pyreadr.read_r(part).values())[0]
        for c in df.columns: df[c]=df[c].astype("int32" if c in ID else "float32")
        tb=pa.Table.from_pandas(df,preserve_index=False)
        if writer is None: writer=pq.ParquetWriter(pq_path,tb.schema,compression="snappy")
        writer.write_table(tb); n+=len(df); del df,tb; os.remove(part)
    writer.close(); shutil.rmtree(parts,ignore_errors=True)
    print(f"  → {name}.parquet {n:,} linhas em {time.time()-t:.0f}s",flush=True)
print("CONVERSAO COMPLETA",flush=True)
