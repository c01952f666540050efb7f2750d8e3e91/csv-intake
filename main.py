import pandas as pd
from datetime import datetime
import argparse

# Debug option to display columns in pandas
pd.set_option('display.max_columns', None)

# argparse description
parser = argparse.ArgumentParser(description="Process downloaded csv files to check agent's internal hold cases")

# Adding argument to take in the correct csv
parser.add_argument("--csv", help="The CSV file that you're looking to intake and process")
args = parser.parse_args()

# Read the CSV
data = pd.read_csv(args.csv)



# Get the list of agents
agentList = data["Last Engaged User (Case)"].unique()

# Data structure for CS Agent
class csAgent:
    def __init__(self, name):
        self.name = name

        # TODO - it might be better to put them into a dataframe
        self.cases = {}
    
    # Add case that agent last touched
    def addCase(self, caseID, last_touch):

        # Add case to list of cases
        self.cases[caseID] = last_touch

    # Get the total number of cases for agent
    def totalCases(self) -> int:
        return int(len(self.cases))

    # Get the earliest case touch
    # This is not working exactly correctly TODO - to fix as well as make sure to include -which- case we have last touched
    def earliestCase(self):
        all_times = {}
        for caseid in self.cases.keys():
            all_times['caseid'] = datetime.strptime(self.cases[caseid], "%m-%d-%Y %H:%M")
        
        return max(all_times.values())

# --- SCRIPT PART ---

# Get list of agent objects
obj_list = []
for agents in agentList:

    # Add based on unique names
    obj_list.append(csAgent(agents))

# Cycle through list
for x in range(len(data)):
    
    for agents in obj_list:

        # When we find a match of who last touched the case
        if data['Last Engaged User (Case)'].iloc[x] == agents.name:

            agents.addCase(data['Case Id'].iloc[x], data['Case Modification Time'].iloc[x])

# Current output is to the command line
for agents in obj_list:

    # Print the 
    print(f"{agents.name} // number of cases: {str(agents.totalCases())}")

    # TODO - Not sure if this is working correctly at the moment
    print(f"last touch was: {str(agents.earliestCase())}")