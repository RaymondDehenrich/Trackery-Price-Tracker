import pandas as pd
import numpy as np
from datetime import date
from sklearn.linear_model import LinearRegression

#-1 return means empty array
#-10 return means no data or less than 5 data is available
#-404 return means dataframe conversion error


#note, need future integration. however pretty much done for the linear regression. just need array of 2d size.
#doesnt truly predict next day, just the latest data date +1. idk the format for incoming data date, so hold on for now
#also, doesnt have any model accuracy evaluation, might need it someday.
#the prediction should only be coming out positive, since there is no negative price. so negative price will be used as a return error.
def lin_reg(data):

    if not data:
        return -1
    
    try:
        df=pd.DataFrame(data,columns=['Date','Price'])
    except ValueError:
        return -404
    
    if df.shape[0]<5:
        return -10
    

    X = df['Date'].values.reshape(-1, 1)
    y = df['Price'].values.reshape(-1, 1)

    
    split = int(0.8 * len(X))
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    
    model = LinearRegression()
    model.fit(X_train,y_train)

    #model test here, not required tbh

    next_day = X_test[-1]+1
    predicted_price = model.predict([[next_day]])[0][0]
    
    return predicted_price
