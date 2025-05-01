LAST UPDATE : May 1st. 2025
# *** STOCK - Prediction ***
---
## Summary
-Let's explore machine-based stock forecasting. (Under development)

- 1. Predict Future Trends
 Using historical stock data, financial news, and social media signals, we aim to develop models that forecast future price movements.

- 2. Visualization and Evaluation
 Develop intuitive dashboards and visual interfaces to monitor model performance and interpret predictions during development.

- 3. Simulation for Realistic Use Cases
 Build simulation tools that mimic actual investment scenarios, allowing for risk evaluation and strategy testing.

- 4. Social Contribution
 Ultimately, use insights and any generated funds to support and expand medical research initiatives.
---
## Project Structure
<pre>.
├── TS_PyFun
│   ├── symbols_list.json
│   └── ts_tmp.py
├── data
│   └── GOOGL_historical_data.csv
├── data-1h
│   └── GOOGL_historical_data_1h.csv
├── data-1m
│   └── GOOGL_historical_data_1m.csv
│
│ %% linux shell
├── cron_ScrapeHistoricalData.sh
├── debug_main.sh
├── open_jupyter_notebook.sh
├── parpool_main_python.sh
├── run_tensorboard.sh
├── timer_Scraphe_Minutes.sh
├── timer_main.sh
│
│ %% Python
├── Symbol2Name.py
├── TS_ScrapeHistoricalData_1.py
├── TS_ScrapeHistoricalData_Minutes_1.py
├── TS_ScrapeSymbol_0.py
├── TS_main_par_addFig.py
├── TS_main_par_addFig_keepmodel.py
├── KEEPMODEL_checkpoint.pth 
├── get_hist_alpha_vantage.py
├── makeTable.py
├── mpf_alpha.py
├── subFunctions.py
│
│ %% PHP
├── display_images.php
├── index.php
├── symbols-list.php
├── 404.php
│
│ %% Others
├── google_last30d.png
├── ListInfo.csv
├── Summary2024-10-27.csv
├── Symbol_List.txt
├── Symbol_List_Info.csv
├── Technology-Sector-Data.csv
└── ReadMe.md

and
  environment.yml  
  requirements.txt

</pre>

## Features (Planned)
 - *LSTM-based time series forecasting
 - Sentiment analysis from Twitter/News
 - Multi-source data integration
 - Interactive dashboard (*tensorboard/Plotly/Streamlit)
 - Report generator

## Requirements
**Please refer to the following file.**
 - environment.yml  
 - requirements.txt


## 🔧 Code currently being actively edited and developed
- [`TS_ScrapeHistoricalData_1.py`](./TS_ScrapeHistoricalData_1.py): The section to add historical data is being revised.
- [`TS_main_on_jupyter.ipynb`](./TS_main_on_jupyter.ipynb ): Edit location of TS_main_par_addFig.py. Prediction section being modified.


## How to Run
```bash
#!bin/bash 
# See also timer_main.sh

# Python code name.
pycode1="TS_ScrapeHistoricalData_1.py"
pycode2="TS_main_par_addFig.py"

# Scrape Yahoo Finance Data
python "$pycode1"

# set up tensorboard
killall tensorboard 

# replace your server ip (--host= ##.##.##.## )
myIP="192.168.##.##"
tensorboard --logdir="TB_logs-${day_str}" --port=8888 --host=$myIP &

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

# If aleready running tensorboard, 
killall tensorboard 

# Run tensorboard
tensorboard --logdir="TB_logs-${day_str}" --port=8888 --host=$myIP &

## If You want check on PHP.
python makeTable.py
```
**We have not published a Directory to run PHP for several reasons.**
**These will be necessary commands in the future.**

## Contact
Leo-Takuma SUGASHI  
[GitHub Profile](https://github.com/Leo-TakumaSugashi)  
Mail : oshou.0131@gmail.com

