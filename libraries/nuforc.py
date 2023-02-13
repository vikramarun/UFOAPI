import requests
import json
import pandas as pd
from .geocoding import Geocoding
from bs4 import BeautifulSoup

class NUFORC():

    def __init__(self):
        self.base_url = 'https://nuforc.org/webreports/'
        self.geocoding = Geocoding()

    def get_dates(self):
        action = 'ndxevent.html'
        response = requests.get(self.base_url+action)
        soup = BeautifulSoup(response.content,"html.parser")
        links = [tag.find("a")["href"] for tag in soup.select("td:has(a)")]
        return links

    def get_reports_by_date(self,date_html):
        response = requests.get(self.base_url+date_html)
        soup = BeautifulSoup(response.content,"html.parser")
        data = []
        for row in soup.tbody.find_all('tr'):
            columns = row.find_all('td')
            if (columns != []):
                date = columns[0].text.strip()
                link = columns[0].find('a').get('href')
                city = columns[1].text.strip()
                state = columns[2].text.strip()
                country = columns[3].text.strip()
                shape = columns[4].text.strip()
                duration = columns[5].text.strip()
                summary = columns[6].text.strip()
                posted = columns[7].text.strip()
                images = columns[8].text.strip()
                if city != '':
                    geo_city,geo_lat,geo_long,geo_country = self.geocoding.get_geo_info(city,state,country)
                else:
                    geo_city = ''
                    geo_lat = ''
                    geo_long = ''
                    geo_country = ''
                data.append([date,city,state,country,geo_city,geo_lat,geo_long,geo_country,shape,duration,summary,posted,images,link])
        report_df = pd.DataFrame(data,columns=['date','city','state','country','geo_city','geo_lat','geo_long','geo_country','shape','duration','summary','posted','images','link'])
        return report_df

    def get_all_reports(self):
        dates = self.get_dates()
        combined_report_df = pd.DataFrame(columns=['date','city','state','country','geo_city','geo_lat','geo_long','geo_country','shape','duration','summary','posted','images','link'])
        for date in dates:
            report_df = self.get_reports_by_date(date)
            combined_report_df = pd.concat([combined_report_df,report_df])
        return combined_report_df

    # def get_reports_by_link(self,link_html):
    #     response = requests.get(self.base_url+link_html)
    #     soup = BeautifulSoup(response.content,"html.parser")
    #
    #     data = []
    #     for row in soup.tbody.find_all('tr'):
    #         sections = row.find_all('td')