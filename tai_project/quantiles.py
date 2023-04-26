import numpy as np
import pandas as pd

df_prediction  = pd.read_csv('forecast/prediction.csv')
df_prediction = df_prediction.drop(columns=df_prediction.columns[0])

print(df_prediction.head())
prediction = np.array(df_prediction)

print(np.shape(prediction))

quantiles_arr = np.zeros((60, 5))

def quantiles(prediction):
    quantiles_arr = np.zeros((60, 5))
    for i in range(20):
        # temperature
        quantiles_arr[i, :] = np.array([np.quantile(prediction[i*50:i*50+50,0],0.025), np.quantile(prediction[i*50:i*50+50,0],0.25), 
                                        np.quantile(prediction[i*50:i*50+50,0],0.5), np.quantile(prediction[i*50:i*50+50,0],0.75), 
                                        np.quantile(prediction[i*50:i*50+50,0],0.975)]) 
        
        # wind
        quantiles_arr[i+20, :] = np.array([np.quantile(prediction[i*50:i*50+50,1],0.025), np.quantile(prediction[i*50:i*50+50,1],0.25), 
                                        np.quantile(prediction[i*50:i*50+50,1],0.5), np.quantile(prediction[i*50:i*50+50,1],0.75), 
                                        np.quantile(prediction[i*50:i*50+50,1],0.975)])
        
        # precipitation 
        quantiles_arr[i+40, :] = np.array([np.quantile(prediction[i*50:i*50+50,2],0.025), np.quantile(prediction[i*50:i*50+50,2],0.25), 
                                        np.quantile(prediction[i*50:i*50+50,2],0.5), np.quantile(prediction[i*50:i*50+50,2],0.75), 
                                        np.quantile(prediction[i*50:i*50+50,2],0.975)]) 
    
    df_quantiles = pd.DataFrame(quantiles_arr, columns=['q0.025', 'q0.25', 'q0.5', 'q0.75', 'q0.975'])
    date_list    = []
    target_list  = []
    horizon_list = []
    for i in range(60):
        date_list.append("2023-04-15")
        if i < 20: 
            target_list.append("t2m")
            horizon_list.append(str(6*(i+1)) + ' hour')
        elif i < 40: 
            target_list.append('wind')
            horizon_list.append(str(6*((i+1)%20)) + ' hour')
        else: 
            target_list.append('precip')   
            horizon_list.append(str(6*((i+1)%20)) + ' hour') 
    df_quantiles = df_quantiles.assign(forecast_date = date_list)
    df_quantiles = df_quantiles.assign(horizon = horizon_list)
    df_quantiles = df_quantiles.assign(target = target_list)
    df_quantiles = df_quantiles[['forecast_date', 'target', 'horizon', 'q0.025', 'q0.25', 'q0.5', 'q0.75', 'q0.975']]

    
    return df_quantiles

test = quantiles(prediction)

test.to_csv('forecast/20230415_PaoloConte.csv')












