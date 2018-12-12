"""
    CommunistBadger v1.0.0
    This is the code for the generating stock data to train the network on.
"""
from __future__ import print_function
from os.path import (
    dirname,
    join,
)
from pandas_datareader.data import DataReader

here = join(dirname(__file__))


def main():
    symbols = ['MSFT','AMZN','AAPL','GOOGL','GOOG','FB','INTC','CSCO','CMCSA','PEP','AMGN','NFLX','ADBE','COST','PYPL','NVDA','AVGO','TXN','FOX','GILD','BKNG','SBUX','WBA','CHTR','QCOM','CME','QQQ','BIIB','MDLZ','ADP','TSLA','FOXA','KHC','ISRG','CSX','TMUS','ESRX','INTU','CELG','BIDU','ILMN','VRTX','AMOV','MU','REGN','CTSH','MAR','AABA','WDAY','ATVI','BND','AMAT','ADI','MNST','EQIX','ADSK','ROST','FISV','AMTD','EBAY','SIRI','XEL','ORLY','ALXN','UAL','EA','PAYX','NXPI','TROW','LRCX','XLNX','AMD','DLTR','VCSH','PCAR','INFO','WLTW','TEAM','NTRS','HBANO','LBTYB','JD','SBAC','VRSK','VRSN','CTAS','VCIT','NTES','LBTYA','CERN','EXPE','LBTYK','ALGN','DISCB','ULTA','CHKP','SHV','LULU','NTAP']
    # Specifically chosen to include the AAPL split on June 9, 2014.
    for symbol in symbols:
        data = DataReader(
            symbol,
            'yahoo',
            start='2010-01-01',
            end='2018-11-11',
        )
        data.rename(
            columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume',
            },
            inplace=True,
        )
        del data['Adj Close']

        dest = join(here, symbol + '.csv')
        print("Writing %s -> %s" % (symbol, dest))
        data.to_csv(dest, index_label='day')


if __name__ == '__main__':
    main()
