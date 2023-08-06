
from .champion import Base
from ....models.player import _Base
from ....utils.num import num_or_string
from ....utils import slugify
class Item(object):#APIResponse
  def __init__(self, **kw):
    super().__init__(**kw)
    self.item_id = num_or_string(kw.get('ItemId')) or 0
    self.item_name = kw.get('ItemName') or None
    self.points = num_or_string(kw.get('Points')) or 0

  def __str__(self):
    return f'{self.item_name} ({self.points})'

  def card(self):
    if self.item_name:
      return f'https://web2.hirez.com/paladins/champion-cards/{slugify(self.item_name)}.jpg'

  def frame(self):
    if self.points:
      return f'https://web2.hirez.com/paladins/cards/frame-{self.points}.png'

class Loadout(Base):

  @property
  def id(self):
    return self.loadout_id
  
  @property
  def loadout_id(self):
    return num_or_string(self.json.get('DeckId')) or 0
  
  @property
  def loadout_name(self):
    return self.json.get('DeckName') or None
  
  @property
  def name(self):
    return self.loadout_name
  
  @property
  def player(self):
    return _Base(self.player_id)

  @property
  def player_id(self):
    return num_or_string(self.json.get('playerId')) or 0

  @property
  def player_name(self):
    return self.json.get('playerName') or None

  @property
  def cards(self):
    return [Item(**_) for _ in sorted((self.json.get('LoadoutItems') or []), key=lambda x: x.get('Points'), reverse=True)]

  self.cards = [ LoadoutCard(self._api.get_card(c["ItemId"], language), c["Points"]) for c in loadout_data["LoadoutItems"] for c in sorted(loadout_data["LoadoutItems"], key=lambda c: c["Points"], reverse=True) ]
