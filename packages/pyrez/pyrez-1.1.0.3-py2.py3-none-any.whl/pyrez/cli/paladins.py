
from ..utils.http import Client
from ..utils.file import get_path, read_file

enum_template = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8

from . import Named
class Champion(Named):
  '''Represents a Paladins Champion. This is a sub-class of :class:`.Enum`.

  Supported Operations:
  +-----------+-------------------------------------------------+
  | Operation |                 Description                     |
  +===========+=================================================+
  | x == y    | Checks if two Champions are equal.              |
  +-----------+-------------------------------------------------+
  | x != y    | Checks if two Champions are not equal.          |
  +-----------+-------------------------------------------------+
  | hash(x)   | Return the Champion's hash.                     |
  +-----------+-------------------------------------------------+
  | str(x)    | Returns the Champion's name with discriminator. |
  +-----------+-------------------------------------------------+
  | int(x)    | Return the Champion's value as int.             |
  +-----------+-------------------------------------------------+
  '''
  UNKNOWN = 0
  [CHAMPS]

  def carousel(self, c=None):
    if self:
      __url__ = f'https://web2.hirez.com/paladins/assets/Carousel/{self.slugify}.png'
      if c:
        from ..utils.http import img_download
        return img_download(__url__, c)
      return __url__

  def header(self, c=None):
    if self:
      __url__ = f'https://web2.hirez.com/paladins/champion-headers/{self.slugify}.png'
      if c:
        from ..utils.http import img_download
        return img_download(__url__, c)
      return __url__

  def header_bkg(self, c=None):
    if self:
      __url__ = f'https://web2.hirez.com/paladins/champion-headers/{self.slugify}/bkg.jpg'
      if c:
        from ..utils.http import img_download
        return img_download(__url__, c)
      return __url__

  def icon(self, c=None):
    if self:
      __url__ = f'https://web2.hirez.com/paladins/champion-icons/{self.slugify}.jpg'
      if c:
        from ..utils.http import img_download
        return img_download(__url__, c)
      return __url__

  @property
  def is_damage(self):
    return self and self in [[DMGS]]
  @property
  def is_flank(self):
    return self and self in [[FLANKS]]
  @property
  def is_tank(self):
    return self and self in [[TANKS]]
  @property
  def is_support(self):
    return self and self in [[SUPS]]

__all__ = (
  'Champion',
)

"""

def fix_name(o):
  return str(o).replace(' ', '_').replace("'", '')
def create_value(_, add_alias=False):
  #Named enum doesn't allow alias?
  if add_alias:
    return f'{fix_name(_.get("feName")).upper()} = "{fix_name(_.get("name")).lower()}"'
  if "'" in _.get('feName'):
    _x = f'{fix_name(_.get("feName")).upper()} = {_.get("id")}, "{_.get("feName")}"'
  else:
    _x = f'{fix_name(_.get("feName")).upper()} = {_.get("id")}'
  '''
  if ' ' in _.get('feName') or "'" in _.get('feName'):
    _n = _.get('feName').replace(' ', '').lower()#.replace("'", '')
    _x += f'\n  {fix_name(_.get("feName")).upper()} = "{_n}", "{_.get("feName")}"'
  '''
  return _x
def update(*args, **kw):
  root_path = f'{get_path(root=True)}'
  __json__ = read_file(f'{root_path}\\data\\links.json').get('paladins')

  _session_ = Client(*args, **kw)
  _enum_ = []
  for n in [1, 5, 11]:
    champs = _session_.get(f'{__json__["website"]["api"]}champion-hub/{n}') or {}
    if champs:
      if n == 1:
        flanks = [f'Champion.{fix_name(_.get("feName")).upper()}' for _ in champs if 'flank' in _.get('role','').lower()]
        supports = [f'Champion.{fix_name(_.get("feName")).upper()}' for _ in champs if 'support' in _.get('role','').lower()]
        damages = [f'Champion.{fix_name(_.get("feName")).upper()}' for _ in champs if 'damage' in _.get('role','').lower()]
        fronts = [f'Champion.{fix_name(_.get("feName")).upper()}' for _ in champs if 'front' in _.get('role','').lower()]
      _enum_ += [f'{create_value(_, add_alias=n != 1)}' for _ in sorted(champs, key=lambda x: x.get('id')) if _]
  __ = enum_template.replace('[CHAMPS]', '\n  '.join(_enum_)).replace('[FLANKS]', ', '.join(flanks)).replace('[SUPS]', ', '.join(supports)).replace('[DMGS]', ', '.join(damages)).replace('[TANKS]', ', '.join(fronts))

  try:
    with open(f'{root_path}\\enums\\champion.py', 'w', encoding='utf-8') as f:
      f.write(__)
  except OSError as exc:
    print(exc)
