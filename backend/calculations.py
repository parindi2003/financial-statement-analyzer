import pandas as pd
def load_financials(csv_path):
    df = pd.read_csv(csv_path)
    return df 

def pivot_by_year(df):
    wide = df.pivot_table(index="Year",columns = "Line_Item" ,values = "Amount",aggfunc = "sum"
    )
    return wide

def calculate_net_profit_margin(wide_df,year):
    row = wide_df.loc[year]
    revenue = row["Revenue"]
    net_profit = row["Net Profit"]

    margin = (net_profit/revenue)*100
    return round(margin,2)










if __name__ == "__main__":
    data = load_financials("../data/sample_financials.csv")
    print(data)
    wide = pivot_by_year(data)
    print(wide)

    margin_2023 = calculate_net_profit_margin(wide,2023)
    print(f"\n2023 Net Profit Margin : {margin_2023}%")

    margin_2022 = calculate_net_profit_margin(wide,2022)
    print(f"\n2022 Net Profit Margin : {margin_2022}%")