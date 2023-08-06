
from ...enums.god import God
from ...models.api_response import APIResponse
from ...utils.num import num_or_string
class MOTD(APIResponse):
  """MatchOfTheDay"""
  @property
  def description(self):
    return self.json.get('description')

  @property
  def game_mode(self):
    return self.json.get('gameMode')

  @property
  def name(self):
    return self.json.get('name')

  @property
  def max_players(self):
    return num_or_string(self.json.get('maxPlayers')) or 0
    
  @property
  def start_datetime(self):
    return self.json.get('startDateTime')

  @property
  def team_gods1(self):
    _ = self.json.get('team1GodsCSV')
    if _ and ',' in str(_):
      return [God(_) for _ in _.replace(' ', '').split(',') or [] if _]#tuple()

  @property
  def team_gods2(self):
    _ = self.json.get('team2GodsCSV')
    if _ and ',' in str(_):
      return [God(_) for _ in _.replace(' ', '').split(',') if _]

  @property
  def title(self):
    return self.json.get('title')
