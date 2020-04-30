import sqlalchemy as db
from datetime import datetime
from tzlocal import get_localzone

local_tz = get_localzone()
NUM_TICKERS=3619

engine = db.create_engine('postgresql://kevincat:we23WE\@#@localhost:5432/stock_ana')
connection = engine.connect()

metadata = db.MetaData()

Ana_Records = db.Table('Ana_Records', metadata, autoload=True, autoload_with=engine)
Companies = db.Table('Companies', metadata, autoload=True, autoload_with=engine)
Ana_Rst = db.Table('Ana_Rst', metadata, autoload=True, autoload_with=engine)

def record_ana_rst(ticker,f1,f2,f3,f4,f5,f):
    now=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        #figure out new id for records
        query=db.select([Ana_Records.columns.id]).order_by(db.desc(db.cast(Ana_Records.columns.id,db.Integer))).limit(1)
        rst=connection.execute(query).scalar()
        new_id=0
        #print(rst)
        if rst!=None :
            new_id=int(rst)+1

        #fine cid through ticker
        query=db.select([Companies.columns.id]).where(Companies.columns.Symbol==ticker.upper())
        rst=connection.execute(query).scalar()
        cid=rst

        #insert into records
        query=db.insert(Ana_Records).values(id=new_id,cid=cid,f1=f1,f2=f2,f3=f3,f4=f4,f5=f5,f=f,datetime=now,timezone='UTC-4')
        rst=connection.execute(query)
    except:
        print(now,' insert ana record error. ticker: ',ticker,' new_id:', new_id,' cid:',cid)

    #update result table
    update_ana_results(cid,f1,f2,f3,f4,f5,f)


def update_ana_results(cid,f1,f2,f3,f4,f5,f):
    now=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        #find latest record of that cid
        query=db.select([Ana_Rst]).where(Ana_Rst.columns.cid==cid).limit(1)
        rst=connection.execute(query).fetchall()
        #if there is no existing record, add record
        if len(rst)==0:
            print(now,' Adding new Ana Rst...  cid: ',cid)
            query=db.insert(Ana_Rst).values(cid=cid,f1=f1,f2=f2,f3=f3,f4=f4,f5=f5,f=f,c1=0,c2=0,c3=0,c4=0,c5=0,c=0,update_time=now,timezone='UTC-4')
            rst=connection.execute(query)
        else:
            #figure out change values ie. c values: 0 no change, -1 rank down, 1 rank up
            if len(rst[0])<8:
                print(now,' ana_rst wrong data format exists, check database. cid: ',cid)
                return
            _f1=rst[0][1]
            _f2=rst[0][2]
            _f3=rst[0][3]
            _f4=rst[0][4]
            _f5=rst[0][5]
            _f=rst[0][6]
            c1=(f1-_f1)*10000 if abs(f1-_f1)>0.0001 else 0
            c2=(f2-_f2)*10000 if abs(f2-_f2)>0.0001 else 0
            c3=(f3-_f3)*10000 if abs(f3-_f3)>0.0001 else 0
            c4=(f4-_f4)*10000 if abs(f4-_f4)>0.0001 else 0
            c5=(f5-_f5)*10000 if abs(f5-_f5)>0.0001 else 0
            c=(f-_f)*10000 if abs(f-_f)>0.0001 else 0
            #update rst
            print(now,' Updating Ana Rst...  cid: ',cid)
            query=db.update(Ana_Rst).values(f1=f1,f2=f2,f3=f3,f4=f4,f5=f5,f=f,c1=c1,c2=c2,c3=c3,c4=c4,c5=c5,c=c,update_time=now,timezone='UTC-4')
            query=query.where(Ana_Rst.columns.cid==cid)
            rst=connection.execute(query)
    except:
        print(now,' update ana rst error. cid: ',cid)

def get_ticker(cid="0"):
    now=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if(int(cid)<0 or int(cid)>=NUM_TICKERS):
        return "IndexOutOfBound"
    try:

        query=db.select([Companies.columns.Symbol]).where(Companies.columns.id==cid)
        rst=connection.execute(query).scalar()
    except:
        print(now, ' get_ticker error. cid: ',cid)
    return rst

def get_single_result(cid="0"):
    now=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        query=db.select([Ana_Rst]).where(Ana_Rst.columns.cid==cid)
        rst=connection.execute(query).fetchall()
    except:
        print(now,' get_single_result error. cid: ',cid)
    return rst

def get_lst_result_ordered(count=1):
    now=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        query=db.select([Ana_Rst]).order_by(db.desc(Ana_Rst.columns.f)).limit(count)
        rst=connection.execute(query).fetchall()
    except:
        print(now,' get_lst_result_ordered retrieve error. count: ',count)
    return rst



#record_ana_rst('nvda',0,0,0,0,0,0)
#update_ana_results('2406',1,1,1,1,1,1)
#print(get_ticker('2406'))
