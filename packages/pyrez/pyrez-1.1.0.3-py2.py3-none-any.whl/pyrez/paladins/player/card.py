

import re

from boolify import boolify

from .champion import Base
from ....utils import slugify
from ..utils.http import img_download
from ....utils.num import num_or_string

def extract_description(description, pattern=r'\[(.+?)\] (.*)'):
  match = re.compile(pattern).match(description)
  if match:
    return match.group(2).strip(), match.group(1)
  #description = re.sub('[\[].*?[\]] ', '', description)
  return description, None

def extract_scale(description, pattern=('=(.+?)\|', '{(.*?)}')):
  _search = re.search(pattern[0], description)
  _scale = 0
  try:
    _scale = float(str(_search.group(1)).replace(',', '.'))
  except AttributeError:
    pass
  '''
  else:

    print(_scale % 2 in [0, 1], not _scale % 2 == _scale, _scale, int(_scale))
    if _scale % 2 in [0, 1]: _scale = int(_scale)#_scale % 2 == 0 and not (_scale % 2 == _scale)
  '''
  try:
    description = description.replace('{' + str(re.search(pattern[1], description).group(1)) + '}', '{SCALE}')
  except AttributeError:
    pass
  return _scale, description

'''
self.ability = None
match = re.compile(r'\[(.+?)\] (.*)').match(description)
if match:
  self.ability = match.group(1)
  description = match.group(2).strip()
self.is_talent = boolify(is_talent)
self.description = description
match = re.compile(r'\[(.+?)\] (.*)').match(short_desc)
if match:
  short_desc = match.group(2).strip()

scale = re.search('=(.+?)\|', description)
try:
  self.scale = float(str(scale.group(1)).replace(',', '.'))
  # if scale % 2 == 0 or scale % 2 == scale: scale = int(scale)
except AttributeError:
  pass
try:
  description = description.replace('{' + str(re.search('{(.*?)}', description).group(1)) + '}', '{SCALE}')
except AttributeError:
  pass
'''


class Card(Base):

  @property
  def active_flag_activation_schedule(self):
    return boolify(self.json.get('active_flag_activation_schedule'))

  @property
  def active_flag_lti(self):
    return boolify(self.json.get('active_flag_lti'))

  @property
  def card_id(self):
    return num_or_string(self.json.get('card_id1')) or 0

  """
  @property
  def card_description(self):
    return self.json.get('card_description')
  
  @property
  def card_name(self):
    return self.json.get('card_name')

  @property
  def card_name_english(self):
    return self.json.get('card_name_english')
  """

  @property
  def cooldown(self):
    return num_or_string(self.json.get('recharge_seconds')) or 0
  
  @property
  def description(self):
    return self.card_description
  
  @property
  def exclusive(self):
    return boolify(self.json.get('exclusive'))

  def icon(self, c=None):
    if card_name:
      __url__ = f'https://web2.hirez.com/paladins/champion-cards/{slugify(self.card_name_english)}.jpg'
      if c or not c and hasattr(self, '__api__'):
        return img_download(__url__, c or self.__api__.http)
      return __url__

  @property
  def id(self):
    return self.card_id

  @property
  def item_id(self):
    return num_or_string(self.json.get('card_id2')) or 0

  @property
  def rank(self):
    return num_or_string(self.json.get('rank')) or 0
  
  @property
  def rarity(self):
    return self.json.get('rarity') or None

"""
self.item_id = int(id)
self.icon_id = int(icon_id)
self.card_id = int(card_id)
self.name = name
self.name_english = name_english#.replace('-', ' ')
self.scale, description = extract_scale(description)
self.is_talent = boolify(is_talent)
self.description, self.ability = extract_description(description)
self.short_description, _ = extract_description(short_desc)
self.activation_schedule = boolify(actv_schedule)
self.lti = boolify(lti)
self.cooldown = int(cooldown)
self.__lang__ = lang
self.champ_id = -1
if champ_id:
  self.champ_id = int(champ_id)
self.add()


i = _api.getItems(l)
__js0n__ = get_url('https://cms.paladins.com/wp-json/wp/v2/champions?slug={}&lang_id={}'.format(g['Name_English'], l))
for ch_cards in [_ for _ in i if _['champion_id'] == int(g.godId) and not (_['item_type'].lower().rfind('deprecated')!= -1 or _['item_type'].lower().rfind('default')!= -1)]:
  card_id, name_english, actv_schedule, lti = 0, None, False, False
  for c in __js0n__.get('cards', {}):
    if c.get('card_id2', 0) == ch_cards.itemId:
      card_id = c.get('card_id1')
      name_english = c.get('card_name_english')
      actv_schedule = c.get('active_flag_activation_schedule')
      lti = c.get('active_flag_lti')
  Card(id=ch_cards.itemId, icon_id=ch_cards.iconId, card_id=card_id, name=ch_cards.deviceName, name_english=name_english, description=ch_cards['Description'], short_desc=ch_cards['ShortDesc'], actv_schedule=actv_schedule, lti=lti, cooldown=ch_cards['recharge_seconds'], is_talent=ch_cards['item_type'].lower().rfind('talent') != -1, lang=l, champ_id=g.godId)
"""


"""
{'Description': '[Weapon] Increase your Reload Speed by {scale=7|7}%.', 'DeviceName': "Acrobat's Trick", 'IconId': 4121, 'ItemId': 12668, 'Price': 0, 'ShortDesc': '[Weapon] Reload faster.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/acrobats-trick.jpg', 'item_type': 'Card Vendor Rank 1 Common', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Explosive Flask] Gain {scale=10|10}% Lifesteal against enemies Slowed by your Explosive Flask.', 'DeviceName': 'Acumen', 'IconId': 4235, 'ItemId': 12840, 'Price': 0, 'ShortDesc': '', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/acumen.jpg', 'item_type': 'Card Vendor Rank 1 Common', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Weightless] Reduce your damage taken by {scale=6|6}% while Weightless is active.', 'DeviceName': 'Escape Artist', 'IconId': 4136, 'ItemId': 14630, 'Price': 0, 'ShortDesc': '', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/escape-artist.jpg', 'item_type': 'Card Vendor Rank 1 Common', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Healing Potion] Increase the radius of Healing Potion by {scale=8|8}%.', 'DeviceName': 'Medicinal Excellence', 'IconId': 4543, 'ItemId': 13377, 'Price': 0, 'ShortDesc': '[Healing Potion] Increase the Radius of your Healing Potion.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/medicinal-excellence.jpg', 'item_type': 'Card Vendor Rank 1 Common', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Healing Potion] Allies hit by Healing Potion have their Movement Speed increased by {scale=6|6}% for 3s.', 'DeviceName': 'Pep in the Step', 'IconId': 4386, 'ItemId': 13134, 'Price': 0, 'ShortDesc': '', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/pep-in-the-step.jpg', 'item_type': 'Card Vendor Rank 1 Common', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Explosive Flask] Generate {scale=1|1} Ammo for each enemy hit by Explosive Flask.', 'DeviceName': 'Smithereens', 'IconId': 4909, 'ItemId': 15122, 'Price': 0, 'ShortDesc': 'Hitting an enemy with Explosive Flask generates ammo.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/smithereens.jpg', 'item_type': 'Card Vendor Rank 1 Common', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Weightless] Increase your jump speed by an additonal {scale=10|10}% while using Weightless.', 'DeviceName': 'Sprint', 'IconId': 3873, 'ItemId': 11302, 'Price': 0, 'ShortDesc': '[Weightless] Gain bonus Jump Speed during Weightless.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/sprint.jpg', 'item_type': 'Card Vendor Rank 1 Common', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Weapon] Your weapon no longer applies Knockback to yourself and deals {scale=20|20}% less Self-Damage.', 'DeviceName': 'Sturdy', 'IconId': 4564, 'ItemId': 13406, 'Price': 0, 'ShortDesc': '[Weapon] Your weapon no longer knocks you back and deals less self damage.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/sturdy.jpg', 'item_type': 'Card Vendor Rank 1 Common', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Weightless] Reduces the Cooldown of Weightless by {scale=.5|.5}s.', 'DeviceName': 'From Above', 'IconId': 4175, 'ItemId': 12733, 'Price': 1, 'ShortDesc': '[Weightless] Reduce the Cooldown of Weightless.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/from-above.jpg', 'item_type': 'Card Vendor Rank 1 Epic', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Healing Potion] Reduce the Cooldown of Healing Potion by {scale=0.6|0.6}s for each ally it hits.', 'DeviceName': 'Reload', 'IconId': 4112, 'ItemId': 12653, 'Price': 0, 'ShortDesc': "[Healing Potion] Reduce Healing Potion's Cooldown for each ally hit.", 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/reload.jpg', 'item_type': 'Card Vendor Rank 1 Epic', 'recharge_seconds': 5, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Armor] Reduce your active Cooldowns by {scale=8|8}% after getting an Elimination.', 'DeviceName': 'Shrewd Move', 'IconId': 4903, 'ItemId': 15058, 'Price': 0, 'ShortDesc': '[Armor] Eliminations reduce all active cooldowns.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/shrewd-move.jpg', 'item_type': 'Card Vendor Rank 1 Epic', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Explosive Flask] Reduce the Cooldown of Explosive Flask by {scale=0.6|0.6}s.', 'DeviceName': 'Side Tanks', 'IconId': 4171, 'ItemId': 12690, 'Price': 0, 'ShortDesc': '[Explosive Flask] Reduce the Cooldown of Explosive Flask.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/side-tanks.jpg', 'item_type': 'Card Vendor Rank 1 Epic', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': "[Healing Potion] Heal yourself for {scale=20|20}% of Healing Potion's effect if you hit an ally but not yourself.", 'DeviceName': 'Gift-Giver', 'IconId': 4538, 'ItemId': 13340, 'Price': 0, 'ShortDesc': '[Healing Potion] You gain a portion of Healing Potion’s effect if you hit a teammate but not yourself.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/gift-giver.jpg', 'item_type': 'Card Vendor Rank 1 Rare', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': "[Explosive Flask] Increase the duration of Explosive Flask's Slow by {scale=0.25|0.25}s.", 'DeviceName': 'Graviton', 'IconId': 3970, 'ItemId': 12008, 'Price': 0, 'ShortDesc': '', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/graviton.jpg', 'item_type': 'Card Vendor Rank 1 Rare', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Armor] Increase your Healing received by {scale=6|6}% while at or below 50% Health.', 'DeviceName': 'Moxie', 'IconId': 4904, 'ItemId': 15057, 'Price': 0, 'ShortDesc': '[Armor] Receive increased healing when below 50% Health.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/moxie.jpg', 'item_type': 'Card Vendor Rank 1 Rare', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Weightless] Heal for {scale=50|50} every 1s while Weightless is active.', 'DeviceName': 'Refreshing Jog', 'IconId': 4120, 'ItemId': 12662, 'Price': 0, 'ShortDesc': '[Weightless] Regenerate Health every second while in Weightless.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/refreshing-jog.jpg', 'item_type': 'Card Vendor Rank 1 Rare', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': '[Explosive Flask] Enemies hit with Explosive Flask take 40% increased damage from your weapon shots for 3s.', 'DeviceName': 'Catalyst', 'IconId': 5596, 'ItemId': 16391, 'Price': 0, 'ShortDesc': 'Targets hit with Explosive Flask take increased damage from your Weapon Shots for 3s.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/catalyst.jpg', 'item_type': 'Inventory Vendor - Talents', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 2}
''
{'Description': '[Weapon] Potion Launcher also Heals allies hit for 750.', 'DeviceName': 'Combat Medic', 'IconId': 5595, 'ItemId': 16516, 'Price': 0, 'ShortDesc': 'Hitting an ally with Healing Potion increases your attack speed.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/combat-medic.jpg', 'item_type': 'Inventory Vendor - Talents', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 8}
''
{'Description': "[Healing Potion] Healing Potion's Healing is increased by 100%.", 'DeviceName': 'Mega Potion', 'IconId': 5597, 'ItemId': 16376, 'Price': 0, 'ShortDesc': 'Healing Potion heals allies for more.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/mega-potion.jpg', 'item_type': 'Inventory Vendor - Talents', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}
''
{'Description': "[Healing Potion] Healing Potion's Healing is increased by 100%.", 'DeviceName': 'Mega Potion', 'IconId': 5597, 'ItemId': 16376, 'Price': 0, 'ShortDesc': 'Healing Potion heals allies for more.', 'champion_id': 2056, 'itemIcon_URL': 'https://web2.hirez.com/paladins/champion-cards/mega-potion.jpg', 'item_type': 'Inventory Vendor - Talents Default', 'recharge_seconds': 0, 'ret_msg': None, 'talent_reward_level': 0}





{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Weapon] Increase your Reload Speed by {scale=7|7}%.', 'card_id1': 18808, 'card_id2': 12668, 'card_name': "Acrobat's Trick", 'card_name_english': "Acrobat's Trick", 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/acrobats-trick.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Common', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Explosive Flask] Gain {scale=10|10}% Lifesteal against enemies Slowed by your Explosive Flask.', 'card_id1': 18891, 'card_id2': 12840, 'card_name': 'Acumen', 'card_name_english': 'Acumen', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/acumen.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Common', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Explosive Flask] Enemies hit with Explosive Flask take 40% increased damage from your weapon shots for 3s.', 'card_id1': 22980, 'card_id2': 16391, 'card_name': 'Catalyst', 'card_name_english': 'Catalyst', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/catalyst.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Legendary', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Weapon] Potion Launcher also Heals allies hit for 750.', 'card_id1': 23195, 'card_id2': 16516, 'card_name': 'Combat Medic', 'card_name_english': 'Combat Medic', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/combat-medic.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Legendary', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Weightless] Reduce your damage taken by {scale=6|6}% while Weightless is active.', 'card_id1': 20071, 'card_id2': 14630, 'card_name': 'Escape Artist', 'card_name_english': 'Escape Artist', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/escape-artist.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Common', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Weightless] Reduces the Cooldown of Weightless by {scale=.5|.5}s.', 'card_id1': 18827, 'card_id2': 12733, 'card_name': 'From Above', 'card_name_english': 'From Above', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/from-above.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Epic', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': "[Healing Potion] Heal yourself for {scale=20|20}% of Healing Potion's effect if you hit an ally but not yourself.", 'card_id1': 18778, 'card_id2': 13340, 'card_name': 'Gift-Giver', 'card_name_english': 'Gift-Giver', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/gift-giver.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Rare', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': "[Explosive Flask] Increase the duration of Explosive Flask's Slow by {scale=0.25|0.25}s.", 'card_id1': 18830, 'card_id2': 12008, 'card_name': 'Graviton', 'card_name_english': 'Graviton', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/graviton.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Rare', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Healing Potion] Increase the radius of Healing Potion by {scale=8|8}%.', 'card_id1': 18894, 'card_id2': 13377, 'card_name': 'Medicinal Excellence', 'card_name_english': 'Medicinal Excellence', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/medicinal-excellence.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Common', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': "[Healing Potion] Healing Potion's Healing is increased by 100%.", 'card_id1': 22969, 'card_id2': 16376, 'card_name': 'Mega Potion', 'card_name_english': 'Mega Potion', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/mega-potion.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Legendary', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Armor] Increase your Healing received by {scale=6|6}% while at or below 50% Health.', 'card_id1': 20518, 'card_id2': 15057, 'card_name': 'Moxie', 'card_name_english': 'Moxie', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/moxie.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Rare', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Healing Potion] Allies hit by Healing Potion have their Movement Speed increased by {scale=6|6}% for 3s.', 'card_id1': 18773, 'card_id2': 13134, 'card_name': 'Pep in the Step', 'card_name_english': 'Pep in the Step', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/pep-in-the-step.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Common', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Weightless] Heal for {scale=50|50} every 1s while Weightless is active.', 'card_id1': 17627, 'card_id2': 12662, 'card_name': 'Refreshing Jog', 'card_name_english': 'Refreshing Jog', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/refreshing-jog.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Rare', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Healing Potion] Reduce the Cooldown of Healing Potion by {scale=0.6|0.6}s for each ally it hits.', 'card_id1': 18845, 'card_id2': 12653, 'card_name': 'Reload', 'card_name_english': 'Reload', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/reload.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Epic', 'recharge_seconds': 5, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Armor] Reduce your active Cooldowns by {scale=8|8}% after getting an Elimination.', 'card_id1': 20517, 'card_id2': 15058, 'card_name': 'Shrewd Move', 'card_name_english': 'Shrewd Move', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/shrewd-move.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Epic', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Explosive Flask] Reduce the Cooldown of Explosive Flask by {scale=0.6|0.6}s.', 'card_id1': 18847, 'card_id2': 12690, 'card_name': 'Side Tanks', 'card_name_english': 'Side Tanks', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/side-tanks.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Epic', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Explosive Flask] Generate {scale=1|1} Ammo for each enemy hit by Explosive Flask.', 'card_id1': 20574, 'card_id2': 15122, 'card_name': 'Smithereens', 'card_name_english': 'Smithereens', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/smithereens.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Common', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Weightless] Increase your jump speed by an additonal {scale=10|10}% while using Weightless.', 'card_id1': 17576, 'card_id2': 11302, 'card_name': 'Sprint', 'card_name_english': 'Sprint', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/sprint.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Common', 'recharge_seconds': 0, 'ret_msg': None}
''
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Weapon] Your weapon no longer applies Knockback to yourself and deals {scale=20|20}% less Self-Damage.', 'card_id1': 18717, 'card_id2': 13406, 'card_name': 'Sturdy', 'card_name_english': 'Sturdy', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/sturdy.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Common', 'recharge_seconds': 0, 'ret_msg': None}
''
>>> _
{'active_flag_activation_schedule': 'y', 'active_flag_lti': 'y', 'card_description': '[Weapon] Your weapon no longer applies Knockback to yourself and deals {scale=20|20}% less Self-Damage.', 'card_id1': 18717, 'card_id2': 13406, 'card_name': 'Sturdy', 'card_name_english': 'Sturdy', 'championCard_URL': 'https://web2.hirez.com/paladins/champion-cards/sturdy.jpg', 'championIcon_URL': 'https://web2.hirez.com/paladins/champion-icons/pip.jpg', 'champion_id': 2056, 'champion_name': 'Pip', 'exclusive': 'n', 'rank': 1, 'rarity': 'Common', 'recharge_seconds': 0, 'ret_msg': None}

##########################################
[{"category_name":null,"item_id":0,"loot_table_item_id":0,"ret_msg":"Invalid date format","talent_description":null,"talent_name":null}]

{
  "Description": "[Healing Potion] Increase the radius of Healing Potion by {scale=8|8}%.",
  "DeviceName": "Medicinal Excellence",
  "IconId": 4543,
  "ItemId": 13377,
  "Price": 0,
  "ShortDesc": "[Healing Potion] Increase the Radius of your Healing Potion.",
  "champion_id": 2056,
  "itemIcon_URL": "https://web2.hirez.com/paladins/champion-cards/medicinal-excellence.jpg",
  "item_type": "Card Vendor Rank 1 Common",
  "recharge_seconds": 0,
  "ret_msg": null,
  "talent_reward_level": 0
}


{
  "Description": "[Weapon] Potion Launcher also Heals allies hit for 750.",
  "DeviceName": "Combat Medic",
  "IconId": 5595,
  "ItemId": 16516,
  "Price": 0,
  "ShortDesc": "Hitting an ally with Healing Potion increases your attack speed.",
  "champion_id": 2056,
  "itemIcon_URL": "https://web2.hirez.com/paladins/champion-cards/combat-medic.jpg",
  "item_type": "Inventory Vendor - Talents",
  "recharge_seconds": 0,
  "ret_msg": null,
  "talent_reward_level": 8
}


{
  "Description": "[Weapon] Your weapon shots deal {50}% increased Damage to Deployables, Pets, and Illusions.",
  "DeviceName": "Bulldozer",
  "IconId": 4361,
  "ItemId": 13079,
  "Price": 150,
  "ShortDesc": "",
  "champion_id": 0,
  "itemIcon_URL": "https://web2.hirez.com/paladins/champion-items/bulldozer.jpg",
  "item_type": "Burn Card Damage Vendor",
  "recharge_seconds": 0,
  "ret_msg": null,
  "talent_reward_level": 0
}

"""
