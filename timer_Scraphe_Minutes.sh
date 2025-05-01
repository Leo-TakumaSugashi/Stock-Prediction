#!/bin/bash

countdownold() {
    start="$(( $(date '+%s') + $1 ))"
    while [ $start -ge $(date +%s) ]; do
        time="$(( $start - $(date +%s) ))"
        printf '%s\r' "$(date -u -d "@$time" +%H:%M:%S)"
        sleep 1
    done
    echo
}

countdown() {
    start="$(( $(date '+%s') + $1 ))"
    while [ $start -ge $(date +%s) ]; do
        time="$(( $start - $(date +%s) ))"

        # 残り時間を計算
        days=$(( time / 86400 ))
        hours=$(( (time % 86400) / 3600 ))
        minutes=$(( (time % 3600) / 60 ))
        seconds=$(( time % 60 ))

        # 表示フォーマットの決定
        if [ $days -gt 0 ]; then
            printf ' Just %dday %02d:%02d:%02d to run!\r' "$days" "$hours" "$minutes" "$seconds"
        else
            printf ' Just %02d:%02d:%02d to run!\r' "$hours" "$minutes" "$seconds"
        fi

        sleep 1
    done
    echo
}

start_main_process() {
    clear
    echo "################################################################"
    echo $(date)
    echo "#### Freq.: 1m  #########"
    current_time=$(date +%s)
    # next_day=$(date -d "$(date -d "now + 1 month" +%Y-%m-01) 18:00:00" +%s)
    next_day=$(date -d "next monday 18:00" +%s)
    remainsec=$((next_day - current_time))
    echo "Next execution in $remainsec seconds (until Next monday, 18:00:00)."
    sh "$0" "$remainsec"
    exit 1
}

if [ -z "$1" ]; then
    start_main_process
fi



pycode1="TS_ScrapeHistoricalData_Minutes_1.py"

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

# Scrape Yahoo Finance Data
python "$pycode1"

echo '  '
echo '   Done.   ' "$date"
date
# loop for next day.
start_main_process
