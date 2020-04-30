import sqlalchemy as db
import pandas as pd

def Load_Data(file_name):
    data = pd.read_csv(file_name,skipinitialspace=True)
    print(data)
    return data

def build_stock_ana_db():

    meta = db.MetaData()

    engine = db.create_engine('postgresql://kevincat:we23WE\@#@localhost:5432/stock_ana')
    connection = engine.connect()

    companies=db.Table(
        'Companies', meta,
        db.Column('id',db.String, primary_key=True),
        db.Column('Symbol', db.String),
        db.Column('Name', db.String),
        db.Column('LastSale', db.Float),
        db.Column('MarketCap', db.String),
        db.Column('IPOyear', db.String),
        db.Column('Sector', db.String),
        db.Column('industry', db.String),
        db.Column('Summary_Quote', db.String),

    )

    ana_records=db.Table(
        'Ana_Records', meta,
        db.Column('id',db.String,primary_key=True),
        db.Column('cid',db.String, db.ForeignKey('Companies.id')),
        db.Column('f1',db.Float),
        db.Column('f2',db.Float),
        db.Column('f3',db.Float),
        db.Column('f4',db.Float),
        db.Column('f5',db.Float),
        db.Column('f',db.Float),
        db.Column('datetime',db.String),
        db.Column('timezone',db.String)
    )

    ana_rst=db.Table(
        'Ana_Rst', meta,
        db.Column('cid',db.String, db.ForeignKey('Companies.id')),
        db.Column('f1',db.Float),
        db.Column('f2',db.Float),
        db.Column('f3',db.Float),
        db.Column('f4',db.Float),
        db.Column('f5',db.Float),
        db.Column('f',db.Float),
        db.Column('c1',db.Integer),
        db.Column('c2',db.Integer),
        db.Column('c3',db.Integer),
        db.Column('c4',db.Integer),
        db.Column('c5',db.Integer),
        db.Column('c',db.Integer),
        db.Column('update_time',db.String),
        db.Column('timezone',db.String)
    )

    meta.create_all(engine)
    #open data file
    fname='./data/companylist.csv'
    data=Load_Data(fname)
    try:
        for i,row in data.iterrows():
            #print(row[0])
            query=db.insert(companies).values(id=i,Symbol=row[0],Name=row[1],LastSale=row[2],MarketCap=row[3],IPOyear=row[4],Sector=row[5],industry=row[6],Summary_Quote=row[7])
            rst=connection.execute(query)
    except:
        print("Data loaded in database or other failure.")





build_stock_ana_db()
