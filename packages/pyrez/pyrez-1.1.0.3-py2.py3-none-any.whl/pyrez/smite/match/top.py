

from collections import namedtuple
Team = namedtuple('Team', 'avg_level gold kills score is_winner')

from ...enums.god import God
from ...models.match.id import Base
from ...utils.num import num_or_string
from ...utils.time import iso_or_string
class Top(Base):
  @property
  def bans(self):
    return [God(self.ban_id1) or ban_id1, God(self.ban_id2) or ban_id2]
  
  @property
  def ban_id1(self):
    return num_or_string(self.json.get('Ban1Id')) or 0
  
  @property
  def ban_id2(self):
    return num_or_string(self.json.get('Ban2Id')) or 0
  
  @property
  def ban_name1(self):
    return self.json.get('Ban1')
  
  @property
  def ban_name2(self):
    return self.json.get('Ban2')
  
  @property
  def entry_datetime(self):
    return iso_or_string(self.json.get('Entry_Datetime')) or None

  @property
  def ban_id1(self):
    return num_or_string(self.json.get('Ban1Id')) or 0

  @property
  def live_spectators(self):
    return num_or_string(self.json.get('LiveSpectators')) or 0

  @property
  def offline_spectators(self):
    return num_or_string(self.json.get('OfflineSpectators')) or 0
  
  @property
  def queue_name(self):
    return self.json.get('Queue')

  @property
  def recording_finished(self):
    return iso_or_string(self.json.get('RecordingFinished')) or None

  @property
  def recording_started(self):
    return iso_or_string(self.json.get('RecordingStarted')) or None

  @property
  def team1(self):
    return Team(avg_level=self.team1_avg_level, gold=self.team1_gold, kills=self.team1_kills, score=self.team1_score, is_winner=self.winning_team == 1)
  
  @property
  def team1_avg_level(self):
    return num_or_string(self.json.get('Team1_AvgLevel')) or 0
  
  @property
  def team1_gold(self):
    return num_or_string(self.json.get('Team1_Gold')) or 0
  
  @property
  def team1_kills(self):
    return num_or_string(self.json.get('Team1_Kills')) or 0
  
  @property
  def team1_score(self):
    return num_or_string(self.json.get('Team1_Score')) or 0
  
  @property
  def team2(self):
    return Team(avg_level=self.team2_avg_level, gold=self.team2_gold, kills=self.team2_kills, score=self.team2_score, is_winner=self.winning_team == 2)

  @property
  def team2_avg_level(self):
    return num_or_string(self.json.get('Team2_AvgLevel')) or 0
  
  @property
  def team2_gold(self):
    return num_or_string(self.json.get('Team2_Gold')) or 0
  
  @property
  def team2_kills(self):
    return num_or_string(self.json.get('Team2_Kills')) or 0
  
  @property
  def team2_score(self):
    return num_or_string(self.json.get('Team2_Score')) or 0
  
  @property
  def winner(self):
    return getattr(self, f'team{self.winning_team}', None)

  @property
  def winning_team(self):
    return num_or_string(self.json.get('WinningTeam')) or 0

__all__ = (
  'Top',
)