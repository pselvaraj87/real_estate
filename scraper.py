from redfin_scraper.redfin_scraper import RedfinScraper
from selenium import webdriver
import pandas as pd

# driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")


def get_rental_estimate(url):
    # driver.get(url)

    return None


if __name__ == '__main__':
    scraper = RedfinScraper()
    scraper.setup('./uszips.csv', multiprocessing=False)

    scraper.scrape(zip_codes=['98105'])

    df_all = pd.DataFrame()

    for i in range(1, 2):
        try:
            scraper.get_data(id=f"D00{i}")
            df_all = pd.concat([df_all, scraper.df])
        except:
            print("Failed")

    df_all.rename(columns={'URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)':
                           'url'}, inplace=True)
    df_all.to_csv('redfin_sample.csv')

    df_all['Rental_Estimate'] = df_all['url'].apply(lambda x: get_rental_estimate(x))

