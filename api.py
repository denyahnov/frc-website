import json
import requests

import tbaapiv3client
from tbaapiv3client.rest import ApiException

def Throw(text1,text2=None,solution=None):
	exit(f"[!] {text1}{f' -> {text2}' if text2 != None else ''}" + f'\n[ ] {solution}' if solution != None else '')

class Color:
	UNKNOWN = 0x0
	RED 	= 0x1
	BLUE 	= 0x2

class Config():
	def __init__(self,path:str,template:list=[]):
		self.path = path
		self.data = dict.fromkeys(template)

		self.Load()

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return json.dumps(self.data,indent=4)

	def Load(self):
		with open(self.path,"r") as file:
			self.data = self.data | json.load(file)

	def Save(self):
		with open(self.path,"w") as file:
			json.dump(self.data,file,indent=4)

	def Add(self,key:str,value:...):
		self.data[key] = value

	def Get(self,key:str):
		return self.data[key]

class Team():
	def __init__(self,id:int):
		self.id = id

	def __repr__(self):
		return self.id

	def __str__(self):
		return str(self.id)

	def ranking(self):
		return 0

	def url(self):
		return ""

class Alliance():
	def __init__(
			self,
			teams:list[Team] = [],
			captain:Team = None,
			color:Color = Color.UNKNOWN,
		):

		self.teams = teams
		self.captain = captain
		self.color = color

	def from_id(id):
		return Alliance()

class TBA:
	KEY = None
	EVENT = None
	CONFIG = None
	TEAM = None

	def __check__():
		if TBA.KEY == None: Throw("TBA","No Key Provided","TBA.set_key(key)")
		if TBA.EVENT == None: Throw("TBA","No Event Provided","TBA.set_event(event)")
		if TBA.CONFIG == None: Throw("TBA","No Config Provided")

		if type(TBA.KEY) != str or len(TBA.KEY) < 20: Throw("TBA","Invalid Key Provided")
		if type(TBA.EVENT) != str or 10 < len(TBA.EVENT) or len(TBA.EVENT) < 5: Throw("TBA","Invalid Event Provided")

	def set_key(key:str):
		TBA.KEY = key

	def set_team(team:str or int):
		TBA.TEAM = int(team)

	def set_event(event:str):
		TBA.EVENT = event

		TBA.CONFIG = tbaapiv3client.Configuration(
			host = "https://www.thebluealliance.com/api/v3",
			api_key = {
				'X-TBA-Auth-Key': TBA.KEY
			}
		)

	def save_event(path:str=""):
		TBA.__check__()

		teams = TBA.get_teams()
		schedule = TBA.get_schedule()

		with open(path + f"{TBA.EVENT}.json","w") as file:
			json.dump({"teams":teams,"schedule":schedule},file,indent=4)

	def get_teams():
		TBA.__check__()

		with tbaapiv3client.ApiClient(TBA.CONFIG) as api_client:
			api_instance = tbaapiv3client.EventApi(api_client)

			try:
				all_teams = api_instance.get_event_teams_keys(TBA.EVENT)
			except ApiException as e:
				Throw("TBA","get_event_teams_keys: %s\n" % e)

			
			return [team.strip('frc') for team in all_teams]

	def get_schedule(team=None):
		TBA.__check__()

		if team != None:
			with tbaapiv3client.ApiClient(TBA.CONFIG) as api_client:
				api_instance = tbaapiv3client.EventApi(api_client)

				try:
					matches = api_instance.get_team_event_matches_simple(f"frc{team}",TBA.EVENT)
				except ApiException as e:
					Throw("TBA","get_team_event_matches_simple: %s\n" % e)

				temp_schedule = {}

				for match in matches:
					temp_schedule[str(match.match_number)] = [team.strip('frc') for team in match.alliances.blue.team_keys] + [team.strip('frc') for team in match.alliances.red.team_keys]

				return {i: temp_schedule[i] for i in sorted(list(temp_schedule.keys()),key=lambda x: int(x))}
		elif TBA.TEAM != None:
			with tbaapiv3client.ApiClient(TBA.CONFIG) as api_client:
				api_instance = tbaapiv3client.EventApi(api_client)

				try:
					matches = api_instance.get_team_event_matches_simple(f"frc{TBA.TEAM}",TBA.EVENT)
				except ApiException as e:
					Throw("TBA","get_team_event_matches_simple: %s\n" % e)

				temp_schedule = {}

				for match in matches:
					temp_schedule[str(match.match_number)] = [team.strip('frc') for team in match.alliances.blue.team_keys] + [team.strip('frc') for team in match.alliances.red.team_keys]

				return {i: temp_schedule[i] for i in sorted(list(temp_schedule.keys()),key=lambda x: int(x))}
		else:
			with tbaapiv3client.ApiClient(TBA.CONFIG) as api_client:
				api_instance = tbaapiv3client.EventApi(api_client)

				try:
					matches = api_instance.get_event_matches_simple(TBA.EVENT)
				except ApiException as e:
					Throw("TBA","get_event_matches_simple: %s\n" % e)

				temp_schedule = {}

				for match in matches:
					temp_schedule[str(match.match_number)] = [team.strip('frc') for team in match.alliances.blue.team_keys] + [team.strip('frc') for team in match.alliances.red.team_keys]

				return {i: temp_schedule[i] for i in sorted(list(temp_schedule.keys()),key=lambda x: int(x))}

	def get_alliances(id=None):
		TBA.__check__()

		with tbaapiv3client.ApiClient(TBA.CONFIG) as api_client:
			api_instance = tbaapiv3client.EventApi(api_client)

			try:
				all_alliances = api_instance.get_event_alliances(TBA.EVENT)
			except ApiException as e:
				Throw("TBA","get_event_alliances: %s\n" % e)

			
			return all_alliances if id == None else all_alliances[id-1]

	def get_rankings():
		TBA.__check__()

		with tbaapiv3client.ApiClient(TBA.CONFIG) as api_client:
			api_instance = tbaapiv3client.EventApi(api_client)

			try:
				rankings = api_instance.get_event_rankings(TBA.EVENT)
			except ApiException as e:
				Throw("TBA","get_event_rankings: %s\n" % e)

			return rankings