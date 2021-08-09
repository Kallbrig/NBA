import pandas as pd
from datetime import date

# It literally disghusts me that I found read_html.
# It would have saved me 50+ hours of workarounds.

def main():
    for year in range(1980, date.today().year + 1):

        df = pd.read_html(f'https://www.basketball-reference.com/awards/awards_{year}.html#mvp')[0]
        col = []
        for i in df.columns:
            col.append(i[1])
        df.columns = col

        df.to_csv(f'MVPs/{year}_mvp.csv')


if __name__ == '__main__':
    main()

