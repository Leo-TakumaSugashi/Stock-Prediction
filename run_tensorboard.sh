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

countdownday() {
    total_seconds=$(( $1 * 86400 ))
    start="$(( $(date '+%s') + total_seconds ))"
    while [ $start -ge $(date +%s) ]; do
        time="$(( start - $(date +%s) ))"
        
        days=$(( time / 86400 ))
        hours=$(( (time % 86400) / 3600 ))
        minutes=$(( (time % 3600) / 60 ))
        seconds=$(( time % 60 ))
        
        printf '   cuntdown <<  %02dday(s) %02d:%02d:%02d  >>\r' "$days" "$hours" "$minutes" "$seconds"
        sleep 1
    done
    echo
}

days_to_countdown=30  # 例: 30日
countdownday $days_to_countdown

start_main_process() {
    clear
    echo "################################################################"
    echo $(date)
    echo "#### U.S. stocks will be updated after 3:00 p.m. (JST) #########"
    current_time=$(date +%s)
    next_day=$(date -d "tomorrow 16:10:00" +%s)
    remainsec=$((next_day - current_time))
    echo "Next execution in $remainsec seconds (until tomorrow 16:10:00)."
    sh "$0" "$remainsec"
}
if [ -z "$1" ]; then
    start_main_process
    exit 1
fi
countdown "$1"
day_str=$(date +"%Y-%m-%d")
DirName='TB_logs-'"$day_str"
killall tensorboard 
tensorboard --logdir="TB_logs-${day_str}" --port=8888 --host=192.168.0.32 &

countdown 10
start_main_process
