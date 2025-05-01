#!/bin/bash
pycode2="TS_main_par_addFig.py"
mapfile -t LIST < Symbol_List.txt
parallel_count=8
start_index=0
pids=()
for ((i = start_index; i < ${#LIST[@]}; i++)); do
    symbol="${LIST[$i]}"
    # Check if symbol is non-empty
    if [ -n "$symbol" ]; then
        python "$pycode2" "$symbol" &
        pids+=($!)
        if (( ${#pids[@]} >= parallel_count )); then
            wait -n
            pids=(${pids[@]/$!})
        fi
    fi
done

# Wait for remaining processes to finish
wait


python makeTable.py
