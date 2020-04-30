#from data_retr import DataRetr as dr
import matplotlib.pyplot as plt

LT_SAMPLE_SIZE=104 # sampling for long term calculation
LT_WEIGHT_FOR_DIVIDED_PERIOD=[0.3,0.3,0.2,0.1,0.1] #1m 3m 1y 3y full

def get_kf(Data):
    """
    using K's formula to retrieve f as float.
    intervals calculation base on length of data
    for P: [# of intervals that are wining]/[count of intervals]
    for b: average rate of wining when wining
    """
    #P and b
    #print(Data)
    filter=[]
    interval_len=int(len(Data)/LT_SAMPLE_SIZE)
    if interval_len==0:
        interval_len=3
    count=0;
    for i in Data:
        if count % interval_len == 0:
            filter.append(i)
        count+=1

    #plt.plot(filter)
    #plt.ylabel('Closing Value')
    #plt.show()

    win_count=0
    sum_win_rate=0
    for i in range (1,len(filter)):
        diff=filter[i]-filter[i-1]

        if(diff>0):
            win_count+=1
            if filter[i-1]!=0:
                sum_win_rate+=diff/filter[i-1]
            else:
                sum_win_rate+=diff
    P=0
    if len(filter)-1 != 0:
        P=win_count/(len(filter)-1)
    b=1
    if win_count!=0:
        b=sum_win_rate/win_count+1
    #print(win_count,", ",b)
    f=(P*b-(1-P))/b
    return f

def divide_data_concurrent(Data):
    """
    dividing data base on concurrency, including
    last month
    last 3 month
    last 1 years
    last 3 years
    last max years
    """
    rst=[]
    lst=Data[len(Data)-31:len(Data)]
    rst.append(lst)
    lst=Data[len(Data)-93:len(Data)]
    rst.append(lst)
    lst=Data[len(Data)-365:len(Data)]
    rst.append(lst)
    lst=Data[len(Data)-1095:len(Data)]
    rst.append(lst)

    rst.append((Data))
    return rst

def get_f1_5(divided_data):
    rst=[]
    for i in divided_data:
        rst.append(get_kf(i))
    return rst

def get_weighted_f(f1_5):
    rst=0
    count=0
    for i in f1_5:
        rst+=LT_WEIGHT_FOR_DIVIDED_PERIOD[count]*i
    return rst

#divided_data=divide_data_concurrent(dr.retrieve_stock_data("NVDA"))
#for i in divided_data:
#    print(get_kf(i))


#print(get_kf(dr.retrieve_stock_data("NVDA")))
