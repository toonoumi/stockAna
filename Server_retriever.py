from data_retr import DataRetr as dr
import ana
import DBFunctions as db
import time
import threading
import random

GAP_TIME=2

save_and_quit=0

current_pos=0

def gather_info(start_cid=0):
    count=start_cid

    while count<db.NUM_TICKERS:
        #first, get a ticker
        global save_and_quit
        if save_and_quit==1:
            #try to save
            try:
                with open('last_save_loc','w') as f:
                    s=f.write(str(count))
                    print('Saving... Loc: ',count)
            except:
                print('Saving Failed.')

            save_and_quit=-1
            return
        ticker=db.get_ticker(str(count))
        data=dr.retrieve_stock_data(ticker)
        if len(data)<1:
            print("Check your ticker name. count:",count)
            time.sleep(2)
            count+=1
            continue
        divided_data=ana.divide_data_concurrent(data)
        f1_5=ana.get_f1_5(divided_data)
        f=ana.get_weighted_f(f1_5)

        db.record_ana_rst(ticker,f1_5[0],f1_5[1],f1_5[2],f1_5[3],f1_5[4],f)

        time.sleep(GAP_TIME+random.random())
        count+=1
        global current_pos
        current_pos=count
    try:
        with open('last_save_loc','w') as f:
            s=f.write(str(0))
            print('Saving... Loc: ',0)
    except:
        print('Saving Failed.')



if __name__ == "__main__":
    #try to read last saved location
    start_loc=0
    try:
        with open('last_save_loc') as f:
            s=f.read()
            start_loc=int(s)
            print('Starting from last saved: ',start_loc)
    except:
        #when file not found,
        print('Save file not found, starting from 0...')

    #starting the thread
    t1=threading.Thread(target=gather_info, args=(start_loc,))
    t1.start()
    while True:
        print('Type \"info\" to get progress.')
        print('When done, type \"exit\" to save and exit.')
        ans=input()
        if ans=='info':
            print('Current loc: ',current_pos,', Progress: ',current_pos/db.NUM_TICKERS*100,'%')
        if ans=='exit':
            save_and_quit=1
            break

    t1.join()
    print('Done.')
