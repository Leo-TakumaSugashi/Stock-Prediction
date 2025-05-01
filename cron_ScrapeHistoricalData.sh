#!/bin/bash

# Conda 環境のパスを指定
CONDA_PATH="/home/<UserName>/anaconda3/bin/conda"
ENV_NAME="LSTM-Stock"

# Conda 環境をアクティブにする
source "$CONDA_PATH" activate "$ENV_NAME"

# Python スクリプトを実行
cd "/home/<UserName>/Python/LSTM-Stock"
python TS_ScrapeHistoricalData_1.py

