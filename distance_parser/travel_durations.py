import requests
import urllib.parse
import pandas as pd


def find_coords(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'

    response = requests.get(url).json()

    return (response[0]["lat"], response[0]["lon"])


def calculate_travel_time(df):
    df.reset_index(inplace=True)
    url = f'http://router.project-osrm.org/table/v1/driving/{df["coords_home"][0][1]},{df["coords_home"][0][0]}'
    for i in range(len(df)):
        url += f';{df["coords_store"][i][1]},{df["coords_store"][i][0]}'
    url+= '?sources=0'

    df.set_index('index', inplace=True)
    response = requests.get(url).json()
    df['to_store'] =  response['durations'][0][1:]

    return df


def add_all_stores_to_home_df(df_store, df_home):
    df = df_home.merge(df_store, how='cross', suffixes=('_home', '_store'))

    return df


if __name__ == '__main__':

    df_stores = pd.read_csv('department_stores.csv')
    df_homes = pd.read_csv('house_locations.csv')

    df_homes['coords'] = df_homes['address'].apply(lambda x: find_coords(x))
    df_stores['coords'] = df_stores['address'].apply(lambda x: find_coords(x))

    df = add_all_stores_to_home_df(df_stores, df_homes)
    df_final = pd.DataFrame()
    for g, df_g in df.groupby('address_home'):
        dftemp = calculate_travel_time(df_g)
        df_final = pd.concat([df_final, dftemp])

    df_final.to_csv('travel_times.csv')
