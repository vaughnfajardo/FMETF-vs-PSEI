import requests
from bs4 import BeautifulSoup
import pandas as pd


# getStockDataFrame inputs the desired stock with its ticker.
# After which, this scrapes and cleans up the data to
# return the stock as a dataframe.

def getStockDataFrame(stock):

    # Sets up the dataframe
    n = 152
    stockURL = ('https://www.investagrams.com/Stock/PSE:' + stock)
    content = requests.get(stockURL)
    soup = BeautifulSoup(content.text, 'html.parser')
    table = soup.find('table', {"class": "table table-hover"})
    df = pd.read_html(str(table))[0].head(n)

    # Cleans up the dataframe
    df.drop(df.tail(1).index, inplace=True) # Drops last row
    df.drop(df.head(1).index, inplace=True) # Drops first row
    del df['Last Price']
    del df['Change']
    del df['Open']
    del df['Low']
    del df['High']
    del df['Net Foreign']
    del df['Date']
    del df['Volume']

    # Removes % sign from %Change
    for key, value in df['%Change'].iteritems():
        if value[-1] == '%':
            df.at[key, '%Change'] = float(value[:-1])

    # Returns DataFrame
    # DataFrame returns %Change
    return df


def main():
    dfFMETF = getStockDataFrame('FMETF')
    dfPSEI = getStockDataFrame('PSEI')
    dataframe = pd.concat([dfFMETF['%Change'],dfPSEI['%Change']], axis=1)
    dataframe.to_excel('dataframe.xlsx')

if __name__ == "__main__":
    main()
