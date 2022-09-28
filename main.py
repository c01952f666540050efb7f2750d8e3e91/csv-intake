import pandas as pd
from datetime import datetime

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

data = pd.read_csv("Internal hold cases - Team Alex.csv")

agentList = data["Last Engaged User (Case)"].unique()

class csAgent:
    def __init__(self, name):
        self.name = name
        self.cases = {
            316123: "8-18-2022 17:46"
        }
    
    def addCase(self, caseID, last_touch):

        # Add case to list of cases
        self.cases[caseID] = last_touch

    def totalCases(self) -> int:
        return int(len(self.cases))

    def earliestCase(self):
        all_times = {}
        for caseid in self.cases.keys():
            all_times['caseid'] = datetime.strptime(self.cases[caseid], "%m-%d-%Y %H:%M")
        
        return min(all_times.values())


obj_list = []

for agents in agentList:
    obj_list.append(csAgent(agents))

for x in range(len(data)):
    
    for agents in obj_list:
        if data['Last Engaged User (Case)'].iloc[x] == agents.name:

            agents.addCase(data['Case Id'].iloc[x], data['Case Modification Time'].iloc[x])

for agents in obj_list:
    print(f"{agents.name} // number of cases: {str(agents.totalCases())}")
    print(f"last touch was: {str(agents.earliestCase())}")