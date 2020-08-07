import pandas as pd
import pandas_datareader as dr
import plotly_express as px
import streamlit as st
import datetime


def pct_change(df):
    df['Pct Chg'] = 100 * (1 - df.iloc[0].Close / df.Close)
    return df

def main():
    st.title('Here is Stocks')
    df = pd.read_csv('https://robintrack.net/api/most_popular.csv?limit=100000')
    df=df.head(2500).reset_index()
    df['symbol_name'] = df['symbol'] + ' | ' + df['name']
    # st.write(df.head(3))
    # l=df['symbol_name'].to_list()
    l=df['symbol'].to_list()
    stocks = st.sidebar.multiselect('Select stocks',l)
    # st.write(stocks)
    stocks = str(stocks)
    stocks = stocks.replace('[','').replace(']','').replace('\'','').replace(' ','')
    stocks = st.sidebar.text_input('Or add more below (comma separated, please)',stocks)
    # st.write(stocks)
    # st.write(type(stocks))
    # stocks = stocks.str.replace('[','').replace(']','').replace('\'','').replace(' ','')
    # st.write(stocks)
    stocks = list(stocks.split(','))
    # st.write(type(stocks))
    # st.write(stocks)
    # st.write(stocks)
    # s=df.loc[df.symbol_name.isin(stocks)]
    # s=s['symbol'].to_list()
    # more_stocks = st.sidebar.text_input('Add more below',str(s))
    # more_stocks = [more_stocks]
    # st.write(more_stocks)
    # st.write([more_stocks])

    import datetime

    end = datetime.date.today()
    start = datetime.date.today() - datetime.timedelta(days=30)
    start_date = st.sidebar.date_input('Start date', start)
    end_date = st.sidebar.date_input('End date', end)

    # if start_date < end_date:
    #     st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    # else:
    #     st.error('Error: End date must fall after start date.')

    # start = '2020-07-01'
    # end = '2020-07-21'
    if st.sidebar.button('Go'):
        if len(stocks) > 0:
            dft=dr.get_data_yahoo(stocks, start_date, end_date)
            dft=dft.stack()
            dft=dft.reset_index()

            dft = dft.groupby('Symbols').apply(pct_change)

            # st.write(dft)
            fig = px.line(dft,
                          x='Date',
                          y='Close',
                          color='Symbols')
            # fig.show()
            st.plotly_chart(fig)

            fig = px.line(dft,
                x='Date',
                y='Pct Chg',
                color='Symbols')
            st.plotly_chart(fig)

            x=dft.groupby('Date').agg({'Close':'sum'}).reset_index()
            x['portfolio_pct_chg']=100 * (1 - x.iloc[0].Close / x.Close)
            dft=pd.merge(dft, x, how='inner',left_on='Date',right_on='Date')

            fig=px.line(dft,
            x='Date',
            y='portfolio_pct_chg')
            st.plotly_chart(fig)

            st.write(dft)



if __name__ == "__main__":
    #execute
    main()
