#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 2024
@author: leo

"""
import pandas as pd
import numpy as np
import torchmetrics
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
from torch.optim import Adam
import pytorch_lightning as pl
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from pytorch_lightning.loggers import TensorBoardLogger
import matplotlib.pyplot as plt
from datetime import date, timedelta
from subFunctions import get_name, get_ListInfoFile
import os,sys
import concurrent.futures
import threading

# symbol = sys.argv[1] if len(sys.argv) > 1 else ''



def main():
    save_dir = 'data'
    window_size = 7
    Today = date.today().strftime('%Y-%m-%d')
    Logs = "logs/TB_logs-"+Today
    symbol = sys.argv[1] if len(sys.argv) > 1 else ''
    try:
        InfoDic = get_name(symbol)
        Name = InfoDic["Name"]
        main_Process(symbol, save_dir, Logs, Name, window_size)
    except Exception as e:
        print(f" Error : Symbol is {symbol} :{e}")


def data_windowing(file, window_size):
    df = pd.read_csv(file)
    Dates = pd.to_datetime(df['Date'])
    output_dates = Dates.tolist()
    output_dates = output_dates[window_size:]
    num_records = df.shape[0]
    close_prices = df['Close'].values
    input_sequence, output = [], []
    for i in range(num_records - window_size):
        input_sequence.append(close_prices[i:i + window_size])
        output.append(close_prices[i + window_size])
        
    return np.array(input_sequence), np.array(output), output_dates

class LSTMModel(pl.LightningModule):

    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.linear = nn.Linear(hidden_size, 1) #Initialization of a linear layer used to reshape output from "hidden_size" dimensions to 1 dimension 

        self.train_rmse = torchmetrics.MeanSquaredError(squared=False)
        self.val_rmse = torchmetrics.MeanSquaredError(squared=False)

    def forward(self, input):
        lstm_out, (hn, cn) = self.lstm(input)
        prediction = self.linear(lstm_out[:, -1, :])
        return prediction

    def configure_optimizers(self):
        return Adam(self.parameters())

    def training_step(self, batch, batch_idx):
        input_i, label_i = batch
        output_i = self(input_i)
        loss = nn.MSELoss()(output_i, label_i)
        self.log("train_loss", loss)

        self.train_rmse(output_i, label_i)
        self.log("train_rmse", self.train_rmse, on_step=False, on_epoch=True)

        return loss

    def validation_step(self, batch, batch_idx):
        input_i, label_i = batch
        output_i = self(input_i)
        val_loss = nn.MSELoss()(output_i, label_i)
        self.log("val_loss", val_loss)

        self.log("validation/predictions", output_i.mean(), prog_bar=True)
        self.log("validation/labels", label_i.mean(), prog_bar=True)

        self.val_rmse(output_i, label_i)
        self.log("val_rmse", self.val_rmse, on_step=False, on_epoch=True)

        return val_loss

def main_Process(symbol, save_dir,Logs,Name,window_size):
    fname = os.path.join(os.getcwd(), save_dir, symbol + '_historical_data.csv')
    model_name = os.path.join(os.getcwd(), Logs, symbol + '_model_checkpoint.pth')
    figure_name = os.path.join(os.getcwd(), Logs, symbol + '_figure.png')
    fdata_name =  os.path.join(os.getcwd(), Logs, symbol + '_tmp.csv')
    logName = ''.join([symbol,'-',Name.replace(" ","_")])
    logger = TensorBoardLogger(Logs, name=logName)
    # Load and process data
    X, Y, Dates = data_windowing(fname, window_size)
    minY = Y.min()
    maxY = Y.max()
    EndDate = Dates[-1] 

    Y = np.array(Y).reshape(-1, 1)  # Reshaping Y to a 2D array so it can be scaled by MinMaxScaler

    # Normalize the data
    scaler_X = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)
    scaler_Y = MinMaxScaler()
    Y_scaled = scaler_Y.fit_transform(Y)

    num_samples = X_scaled.shape[0]
    train_val_size = int(0.85 * num_samples)  # 85% for training and validation
    test_size = num_samples - train_val_size

    # Split the data
    train_val_indices, test_indices = train_test_split(np.arange(num_samples), test_size=test_size, shuffle=False, random_state=42)
    train_indices, val_indices = train_test_split(train_val_indices, test_size=int(0.25 * train_val_size), random_state=42)

    X_train, X_val, X_test = X_scaled[train_indices], X_scaled[val_indices], X_scaled[test_indices]
    Y_train, Y_val, Y_test = Y_scaled[train_indices], Y_scaled[val_indices], Y_scaled[test_indices]

    # Convert to PyTorch tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32).unsqueeze(-1)  # Ensure shape is (batch_size, seq_len, input_size)
    Y_train_tensor = torch.tensor(Y_train, dtype=torch.float32)
    X_val_tensor = torch.tensor(X_val, dtype=torch.float32).unsqueeze(-1)  # Ensure shape is (batch_size, seq_len, input_size)
    Y_val_tensor = torch.tensor(Y_val, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32).unsqueeze(-1)  # Ensure shape is (batch_size, seq_len, input_size)
    Y_test_tensor = torch.tensor(Y_test, dtype=torch.float32)

    # Create TensorDataset and DataLoader for training, validation, and test sets
    train_dataset = TensorDataset(X_train_tensor, Y_train_tensor)
    val_dataset = TensorDataset(X_val_tensor, Y_val_tensor)
    test_dataset = TensorDataset(X_test_tensor, Y_test_tensor)

    bsiz = 1024
    max_ep = 1000
    train_loader = DataLoader(train_dataset, batch_size=bsiz, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=bsiz)
    test_loader = DataLoader(test_dataset, batch_size=bsiz)

    # Initialize model
    model = LSTMModel(input_size=1, hidden_size=7) #default hidden_size = 5
    
    #                             early_stopping = EarlyStopping(monitor='val_loss', patience=5, mode='min')
    # Setup trainer with logger    max_epochs=100, callbacks=[early_stopping])
    trainer = pl.Trainer(max_epochs=max_ep, logger=logger, log_every_n_steps=10)

    # Train the model
    trainer.fit(model, train_dataloaders=train_loader, val_dataloaders=val_loader)
    # Save the model state
    torch.save(model.state_dict(), model_name)
    #### # Load model state
    # model = LSTMModel(input_size=1, hidden_size=5)
    # model.load_state_dict(torch.load('model_checkpoint.pth'))
    # model.eval()

    # figure output
    print(len(test_loader))
    pred, actu, future, date_actual, date_future = generate_predictions_with_dates(model, test_loader, EndDate, future_steps=90)
    pred = pred*(maxY - minY)+minY
    actu = actu*(maxY - minY)+minY
    future = future*(maxY - minY)+minY
    try:
        D1 = np.array(date_future).reshape(-1,1)
        F1 = np.array(future).reshape(-1,1)
        fdata = pd.DataFrame({
            "date": D1.flatten(), 
            "future":F1.flatten()
            })
        fdata.to_csv(fdata_name,index=False)
    except Exception as e:
        print(e)
        print(len(date_future), len(future))  
        with open(fdata_name,'w') as f:
            f.write(symbol)
    plot_predictions(pred, actu, date_actual, future, date_future, f"{symbol}:{Name}", figure_name)

def generate_predictions_with_dates(model, dataloader, start_date, future_steps=90, frequency='D'):
    model.eval()  
    predictions, actuals = [], []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    with torch.no_grad():
        for batch in dataloader:
            inputs, labels = batch
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            predictions.append(outputs.cpu().numpy())
            actuals.append(labels.cpu().numpy())
    predictions = np.concatenate(predictions, axis=0)
    actuals = np.concatenate(actuals, axis=0)
    
    # 再帰的な予測のための最後の入力を取得
    last_input = inputs[-1].cpu().numpy()  # データローダーから最後の入力を取得
    future_predictions = []
    for _ in range(future_steps):
        with torch.no_grad():
            last_input_tensor = torch.tensor(last_input, dtype=torch.float32).unsqueeze(0).to(device)
            future_output = model(last_input_tensor).cpu().numpy()
            future_predictions.append(future_output)
            
            # 最後の入力を更新（次のウィンドウを作成）
            # 例えば、時系列データの場合は1次元ずつスライドさせる
            last_input = np.roll(last_input, -1)  # ウィンドウをスライド
            last_input[-1] = future_output  # 新しい予測を最後に挿入
    
    future_predictions = np.vstack(future_predictions)  
    
    date_range_future = pd.date_range(start=start_date + pd.Timedelta(1, unit=frequency) , periods=future_steps, freq=frequency)
    # actual_start = start_date 
    date_range_actual = pd.date_range(end=start_date, periods=len(actuals), freq=frequency)
    
    return predictions, actuals, future_predictions, date_range_actual, date_range_future

    
# Function to plot predictions vs actuals
def plot_predictions(predictions, actuals,date_base, future,date_future, title, figname):

    fgh = plt.figure(figsize=(8, 6))
    axh1 = fgh.add_axes([0.1, 0.13, 0.8, 0.8])  # Use add_axes instead of axes
    axh1.plot(date_base, actuals, label='Actual Values', linestyle="-",linewidth = 5)
    axh1.plot(date_base, predictions, label='Predicted Values', linestyle='--')
    axh1.plot(date_future, future, label='Predicted Future Values', linestyle=':',linewidth = 3)
    # Set title and labels for the plot
    axh1.set_title(title)  # Set title for the axes
    axh1.set_xlabel('Time Step')  # Set X-axis label
    axh1.set_ylabel('Price')  # Set Y-axis label

    # Set the x-axis limits (1 year range)
    TODAY = date.today()
    axh1.set_xlim([TODAY - timedelta(days=365), TODAY + timedelta(days=30)])
    axh1.grid()
    axh1.legend()  # Add legend
    
    # Save the figure
    fgh.savefig(figname)

 
# Predic, Actuals = generate_predictions(model, trainer)
# plot_predictions(Predic,Actuals,'AMD')

if __name__ == "__main__":
    main()