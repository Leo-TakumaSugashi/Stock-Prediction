#!/bin/bash
mapfile -t LIST < Symbol_List.txt

parallel_count=6
start_index=1  # 途中のインデックスを指定
pids=()

for ((i = start_index; i < ${#LIST[@]}; i++)); do
    symbol="${LIST[$i]}"
    python "TS_main_par_addFig.py"  "$symbol" &

    pids+=($!)  # PIDをリストに追加

    if (( ${#pids[@]} >= parallel_count )); then
        wait -n  # 最初に終了したプロセスを待つ
        pids=(${pids[@]/$!})  # 終了したプロセスをPIDリストから削除
    fi
done

# 残りの全プロセスが終了するまで待つ
wait
