
import ast
from datetime import datetime

import filemgr


class interface():


    def __init__(self) :    

        user_input = input("Enter a F1 season you would like information about:\n (enter e.g. 1970, if you want multiple seperate each by a space, press enter to continue) ")

        entered_year = []
        while user_input != "":
            for item in user_input.split(" "):
                if item.isdigit() :
                    if int(item) <= datetime.now().year and int(item) >= 1950:
                        entered_year.append(int(item))

                    else:
                        print("Input not accepted please enter year between now and 1950 in digit format!")            
    	    
            user_input = input()

        for year in entered_year:    
            self.get_info_for_year(year)

    def get_info_for_year(self, year):
        file_mgr = filemgr.filemgr(year)

        races = file_mgr.get_races_for_year(year)
        standings = file_mgr.get_standings(year)  
        user_input = str(input("Year:"+ str(year) + "\nDo you want to see the race results or championship standings\n (enter results, standings or both if you want both)"))
        if user_input.lower() == "both":
            self.get_champion(year, file_mgr)
            self.print_race_details(races=races)
            self.print_standings(standings)

        if user_input.lower() == "results":
            self.get_champion(year, file_mgr)
            self.print_race_details(races=races)

        if user_input.lower() == "standings":
            self.get_champion(year, file_mgr)
            self.print_standings(standings)

    def get_champion(self, years, file_mgr):
        champion_details = file_mgr.get_champion(years)

        for info in champion_details:
            print("Driver: " + info[0] + " Won! \nWith " + info[1] + " points. He won " + str(round(float(info[3]), 3)) +"% of races. Winning at:")
            
            print(info[2].replace("[", "").replace("]", "").replace("'", ""))

    def print_race_details(self, races):
        ignore_key = {'year'}    
        print("Grand Prix\t\tDate\t\tWinner\t\tCar\t\tLaps")

        for race in races:
            race = ast.literal_eval(race)
            race = {k:v for k,v in race.items() if k not in ignore_key}
            print("-------------------------------------------------------------------------------------------------------------------")
            for detail in race:
                print("| "+ race[detail] + " |", end='\t')
            print()


    def print_standings(self, championship_results):
        ignore_key = {'year'}
        print("\n\nPosition\t\tName\t\tNationality\t\tCar\t\tPoints")
        for standing in championship_results:
            standing = ast.literal_eval(standing)
            standing = {k:v for k,v in standing.items() if k not in ignore_key}
            print("-----------------------------------------------------------------------------------------------------------------")
            for detail in standing:
                print("| "+ standing[detail] + " |",end='\t')
            print()
interface()