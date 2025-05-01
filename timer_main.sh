#!/bin/bash

countdown() {
    start="$(( $(date '+%s') + $1 ))"
    while [ $start -ge $(date +%s) ]; do
        time="$(( $start - $(date +%s) ))"
        printf '%s\r' "$(date -u -d "@$time" +%H:%M:%S)"
        sleep 1
    done
    echo
}

start_main_process() {
    clear
    echo "################################################################"
    echo $(date)
    echo "#### U.S. stocks will be updated after 3:00 p.m. (JST) #########"
    current_time=$(date +%s)
    next_day=$(date -d "tomorrow 15:30:00" +%s)
    remainsec=$((next_day - current_time))
    echo "Next execution in $remainsec seconds (until tomorrow 15:30:00)."
    sh "$0" "$remainsec"
    exit 1
}

if [ -z "$1" ]; then
    start_main_process
fi



pycode1="TS_ScrapeHistoricalData_1.py"
pycode2="TS_main_par_addFig.py"
#pycode3="makeTable.py"

# Check if the first Python script exists
if [ ! -f "$pycode1" ]; then
    echo "Error: $pycode1 not found."
    exit 1
fi
# Check if Symbol_List.txt exists
if [ ! -f "Symbol_List.txt" ]; then
    echo "Error: Symbol_List.txt not found."
    exit 1
fi

# countdown until tommorow
countdown "$1"
day_str=$(date +"%Y-%m-%d")
DirName='TB_logs-'"$day_str"
if [ ! -d "$DirName" ]; then
    #mkdir "$DirName"
    echo "not existing $DirName"
fi
# Scrape Yahoo Finance Data
python "$pycode1"

# set up tensorboard
# killall tensorboard 
# tensorboard --logdir="TB_logs-${day_str}" --port=8888 --host=192.168.0.32 &

# main parallel computing
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
# killall tensorboard 
# tensorboard --logdir="TB_logs-${day_str}" --port=8888 --host=192.168.0.32 &
python makeTable.py
echo 'Skip : python TS_main_par_addFig_keepmodel.py'
echo '  '
echo '   Done.   ' "$date"
date
# loop for next day.
start_main_process
