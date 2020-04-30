from data_retr import DataRetr as dr
import ana

if __name__ == "__main__":
    print("What Stock you want me to look at?")
    ticker=input()
    data=dr.retrieve_stock_data(ticker)
    if len(data)<1:
        print("Check your ticker name.")
        exit(0)
    divided_data=ana.divide_data_concurrent(data)
    f1_5=ana.get_f1_5(divided_data)
    f=ana.get_weighted_f(f1_5)
    print(f1_5)
    print("Final Weighted F factor: ",f)
