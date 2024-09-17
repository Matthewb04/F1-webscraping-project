from bs4 import BeautifulSoup
import requests as rq
from datetime import datetime
import mysql.connector

class Scraper():
    def __init__(self, year):

        print("getting data for "+ str(year))  
        self.seasons.append(year)            
        self.drivers_results.append( self.get_drivers_standing(year))
        self.race_results.append( self.get_race_results(year) )

    def get_races_won(self, url):
        response = rq.get(url)
        races = []

        if response.status_code > 200:
            raise Exception("Couldn't load page")

        soup = BeautifulSoup(response.text, "lxml")
        race_list = soup.select("tr.bg-brand-white,  tr.bg-grey-10")[1:]

        for race in race_list:
            if race.select("p.f1-text")[-2].text.strip() == "1":
                races.append(race.select("p.f1-text")[0].text.strip())

        return races

    def get_drivers_standing(self, year):
        standing = []

        url = f"https://www.formula1.com/en/results/{year}/drivers"
        response = rq.get(url)

        if response.status_code > 200:
            raise Exception("Couldn't load page")

        soup = BeautifulSoup(response.text, "lxml")
        championship_placements = soup.select("tr.bg-brand-white,  tr.bg-grey-10")[1:]

        self.get_champion_details(year, championship_placements)

        count = 0
        for driver in championship_placements:
            
            driver_info = {
                "position":"",
                "name": "",
                "nationality":"",
                "car" : "",
                "points":"",
            }

            i = 0
            for key in driver_info:
                driver_info[key] = driver.select("p.f1-text")[i].text.strip().replace("\xa0",  " ")
                i+=1
            driver_info["year"] = year
            count+=1
            driver_info["name"] = driver_info["name"][:-3]
            standing.append(driver_info)

        return standing

    def get_race_results(self, year):
        results = []

        url = f"https://www.formula1.com/en/results/{year}/races"
        response = rq.get(url)

        if response.status_code > 200:
            raise Exception("Couldn't load page")

        soup = BeautifulSoup(response.text, "lxml")
        races = soup.select("tr.bg-brand-white,  tr.bg-grey-10")[1:]

        count = 0
        for race in races:
            race_info = {
                "grand prix":"",
                "date": "",
                "winner":"",
                "car" : "",
                "laps":"",
            }

            i = 0
            for key in race_info:
                race_info[key] = race.select("p.f1-text")[i].text.strip().replace("\xa0",  " ")
                i+=1

            count+=1
            race_info["year"] = year
            race_info["winner"] = race_info["winner"][:-3]
            results.append(race_info)

        return results
    
    def get_champion_details(self,year, championship_placements):
        champion_details = []
        # adding champions of the season to list
        championship_winner = championship_placements[0].select("p.f1-text")[1].text[:-3].strip().replace("\xa0",  " ")
        championship_points = championship_placements[0].select("p.f1-text")[4].text
        champion_details.append(championship_winner)
        champion_details.append(championship_points)
        champion_href = championship_placements[0].select("p.f1-text")[1].a["href"].strip()
        champion_url = f"https://www.formula1.com/en/results/{year}/" + champion_href
        races_won_in_season = self.get_races_won(champion_url)
        champion_details.append(races_won_in_season)
        
        # getting percentage of races won per season
        champion_details.append((len(races_won_in_season) / len(championship_placements) * 100 ))
        
        champion_details.append(year)
        self.champions[year] = champion_details
   
    champions ={}
    seasons = []
    races_won_per_champion = {}
    drivers_results = []
    race_results = []
