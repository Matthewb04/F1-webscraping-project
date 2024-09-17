import ast
import Scraper
import csv


class filemgr():

    def  __init__(self, year):
        scraper = Scraper.Scraper(year)

        races = scraper.race_results
        drivers = scraper.drivers_results
        champions = scraper.champions

        with open('champs.csv',"w" ,newline='') as csvfile:
            writer = csv.writer(csvfile)
            for year in champions.keys():
                writer.writerow(champions[year ])

        with open('races.csv',"w" ,newline='') as csvfile:
            writer = csv.writer(csvfile)
            for year in races:
                writer.writerow(year)


        with open('drivers.csv',"w" ,newline='') as csvfile:
            writer = csv.writer(csvfile)
            for year in drivers:
                writer.writerow(year)


    def get_races_for_year(self, year):
        returned_races= []

        with open('races.csv', "r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if str(year) in row[0]:
                    returned_races.append(row)

        return returned_races[0]
    

    def get_standings(self, year):
        returned_standings= []

        with open('drivers.csv', "r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if str(year) in row[0]:
                    returned_standings.append(row)

        return returned_standings[0]

    def get_champion(self, year):
        returned_champion = []

        with open('champs.csv', "r", newline='') as csvfile:
            reader = csv.reader(csvfile )
            for row in reader:
                if int(row[-1]) == year:
                    returned_champion.append(row)

        return returned_champion

