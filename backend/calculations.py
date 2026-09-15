import pandas as pd
def load_financials(csv_path):
    df = pd.read_csv(csv_path)
    return df 

def pivot_by_year(df):
    wide = df.pivot_table(index="Year",columns = "Line_Item" ,values = "Amount",aggfunc = "sum"
    )
    return wide



def calculate_ratios(wide_df,year):

    row = wide_df.loc[year]
    revenue = row["Revenue"]
    cogs = row["Cost of Goods Sold"]
    net_profit = row["Net Profit"]
    operating_income = row["Operating Income"]
    total_assets = row["Total Assets"]
    total_liabilities = row["Total Liabilities"]
    equity = row["Shareholders Equity"]
    current_assets = row["Total Current Assets"]
    current_liabilities = row["Total Current Liabilities"]
    inventory = row["Inventory"]

    gross_profit = revenue - cogs

    ratios = {
        "Gross Profit Margin (%)": round((gross_profit / revenue) * 100, 2),
        "Operating Margin (%)": round((operating_income / revenue) * 100, 2),
        "Net Profit Margin (%)": round((net_profit / revenue) * 100, 2),
        "Return on Assets - ROA (%)": round((net_profit / total_assets) * 100, 2),
        "Return on Equity - ROE (%)": round((net_profit / equity) * 100, 2),
        "Debt-to-Equity Ratio": round(total_liabilities / equity, 2),
        "Current Ratio": round(current_assets / current_liabilities, 2),
        "Quick Ratio": round((current_assets - inventory) / current_liabilities, 2),
    }
    return ratios















    if __name__ == "__main__":
     data = load_financials("../data/sample_financials.csv")
    wide = pivot_by_year(data)

    print("=== 2023 Ratios ===")
    ratios_2023 = calculate_ratios(wide, 2023)
    for key, value in ratios_2023.items():
        print(f"{key}: {value}")

    print("\n=== 2022 Ratios ===")
    ratios_2022 = calculate_ratios(wide, 2022)
    for key, value in ratios_2022.items():
        print(f"{key}: {value}")