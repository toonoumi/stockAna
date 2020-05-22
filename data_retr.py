import yfinance as yf
#import matplotlib.pyplot as plt



def retrieve_stock_data(ticker,period="max"):
    msft = yf.Ticker(ticker)

    # get historical market data, here max is 5 years.
    data=msft.history(period="max")
    """
    returns:
                    Open    High    Low    Close      Volume  Dividends  Splits
    Date
    1986-03-13    0.06    0.07    0.06    0.07  1031788800        0.0     0.0
    1986-03-14    0.07    0.07    0.07    0.07   308160000        0.0     0.0
    ...
    2019-11-12  146.28  147.57  146.06  147.07    18641600        0.0     0.0
    2019-11-13  146.74  147.46  146.30  147.31    16295622        0.0     0.0
    """
    
    close_num=data.loc[:,"Close"]
    #plt.plot(close_num)
    #plt.ylabel('Closing Value')
    #plt.show()
    return close_num
