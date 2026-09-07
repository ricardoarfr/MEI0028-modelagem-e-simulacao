#!/bin/zsh
cd "$(dirname "$0")"; export WP1A_ROOT="$PWD"; export LR_MAX_ITER=5000; export NJOBS=4; PY=.venv/bin/python; LOG=results/metadata/log_codex.txt
{ echo "== $(date) LR busca"; $PY -u src/06c_busca_hp_lr.py
  for s in 42 123 2024 7 555; do rm -f results/metadata/treino_final/regressao_logistica_seed$s.json; echo "== $(date) LR final seed $s"; $PY -u src/07_treino_final.py --modelo regressao_logistica --seed $s; done
  echo "== $(date) piloto repetições"; $PY -u src/04b_piloto_vazamento_repeticoes.py
  echo "== $(date) bootstrap"; $PY -u src/10_bootstrap_execucao.py
  echo "== $(date) avaliação 08"; $PY -u src/08_avaliacao.py
  echo "== $(date) FIM CODEX"; } > $LOG 2>&1
