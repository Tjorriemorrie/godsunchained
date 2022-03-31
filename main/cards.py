from dataclasses import dataclass
from typing import Any, List

from main.constants import CONDITION_LESS_CARDS, CONDITION_RUNE_CARD, EFFECT_2DAMAGE_ENEMY_CREATURE, \
    EFFECT_5DAMAGE_ENEMY_CREATURE, EFFECT_6DAMAGE, EFFECT_DAMAGE_FROM_HEALTH, \
    EFFECT_DELVE, EFFECT_DRAW_2CARDS, EFFECT_DRAW_CARD, EFFECT_DRAW_MANA_INC1, EFFECT_FORESEE, \
    EFFECT_PROTECT_GOD, \
    EFFECT_RETURN_HAND, \
    EFFECT_RETURN_MANA_INC2, GOD_DECEPTION, GOD_MAGIC, QUALITY_PLAIN, \
    RARITY_COMMON, \
    SET_WELCOME, TARGET_ALL_OTHER_ENEMY_CREATURE, TARGET_ENEMY_CREATURE, TARGET_FOE, TARGET_ME, \
    TARGET_RANDOM_ENEMY_CREATURE, TRAIT_BLITZ, TRAIT_CONFUSED, TRAIT_DEADLY, TRAIT_FLANK, \
    TRAIT_HIDDEN, TRAIT_ROAR, TRIBE_GUILD, \
    TRIBE_MYSTIC, TRIBE_NETHER, TRIBE_OLYMPIAN, TYPE_CREATURE, TYPE_RELIC, TYPE_SPELL


@dataclass
class Pick:
    choices: List[Any]


@dataclass
class Trait:
    name: str
    effects: List[Any] = None


@dataclass
class BaseCard:
    name: str
    mana: int


@dataclass
class WelcomeSet:
    set: str = SET_WELCOME
    rarity: str = RARITY_COMMON
    quality: str = QUALITY_PLAIN


@dataclass
class DeceptionGod:
    god: str = GOD_DECEPTION


@dataclass
class MagicGod:
    god: str = GOD_MAGIC


@dataclass
class CreatureType:
    tribe: str
    attack: int
    health: int
    traits: List[Trait]
    type: str = TYPE_CREATURE


@dataclass
class SpellType:
    effects: List[Any]
    type: str = TYPE_SPELL


@dataclass
class RelicType:
    attack: int
    durability: int
    type: str = TYPE_RELIC
    traits: List[Trait] = None
    effects: List[Any] = None

# deception welcome
@dataclass
class CreatureDeceptionWelcome(WelcomeSet, DeceptionGod, CreatureType, BaseCard): pass
@dataclass
class SpellDeceptionWelcome(WelcomeSet, DeceptionGod, SpellType, BaseCard): pass
@dataclass
class RelicDeceptionWelcome(WelcomeSet, DeceptionGod, RelicType, BaseCard): pass


# Magic welcome
@dataclass
class CreatureMagicWelcome(WelcomeSet, MagicGod, CreatureType, BaseCard): pass
@dataclass
class SpellMagicWelcome(WelcomeSet, MagicGod, SpellType, BaseCard): pass
@dataclass
class RelicMagicWelcome(WelcomeSet, MagicGod, RelicType, BaseCard): pass


trait_blitz = Trait(name=TRAIT_BLITZ)
trait_deadly = Trait(name=TRAIT_DEADLY)
trait_flank = Trait(name=TRAIT_FLANK)
trait_hidden = Trait(name=TRAIT_HIDDEN)
trait_roar_foresee = Trait(name=TRAIT_ROAR, effects=[EFFECT_FORESEE])
trait_roar_less_draw = Trait(name=TRAIT_ROAR, effects=[(CONDITION_LESS_CARDS, EFFECT_DRAW_CARD)])
trait_roar_return_2enemy = Trait(name=TRAIT_ROAR, effects=[(TARGET_RANDOM_ENEMY_CREATURE, EFFECT_RETURN_HAND)] * 2)
trait_roar_delve_rune = Trait(name=TRAIT_ROAR, effects=[(CONDITION_RUNE_CARD, EFFECT_DELVE)])


cards = [
    #####################
    # WELCOME
    #####################

    #  deception
    CreatureDeceptionWelcome(name='Glider Assailant', mana=2, tribe=TRIBE_GUILD, attack=3, health=2, traits=[trait_flank]),
    CreatureDeceptionWelcome(name='Bedeviled Shadow', mana=3, tribe=TRIBE_NETHER, attack=3, health=3, traits=[trait_hidden]),
    CreatureDeceptionWelcome(name='Secrets Broker', mana=5, tribe=TRIBE_OLYMPIAN, attack=5, health=4, traits=[trait_roar_less_draw]),
    CreatureDeceptionWelcome(name='Wiznapper', mana=8, tribe=TRIBE_GUILD, attack=5, health=4, traits=[trait_roar_return_2enemy]),
    SpellDeceptionWelcome(name='Ransom', mana=4, effects=[(TARGET_ENEMY_CREATURE, [EFFECT_RETURN_MANA_INC2])]),
    SpellDeceptionWelcome(name='Stack the Deck', mana=5, effects=[(TARGET_ME, [EFFECT_DRAW_CARD] * 3), (TARGET_FOE, [EFFECT_DRAW_MANA_INC1] * 3)]),
    SpellDeceptionWelcome(name='Spiked Tea', mana=4, effects=[(TARGET_ENEMY_CREATURE, [EFFECT_DAMAGE_FROM_HEALTH]), (TARGET_ALL_OTHER_ENEMY_CREATURE, [TRAIT_CONFUSED])]),
    RelicDeceptionWelcome(name='Poisoned Dagger', mana=4, attack=3, durability=1, traits=[trait_blitz, trait_deadly]),

    # magic
    CreatureMagicWelcome(name='Third Eye Seer', mana=2, tribe=TRIBE_MYSTIC, attack=2, health=3, traits=[trait_roar_foresee]),
    CreatureMagicWelcome(name='Rune Writer', mana=5, tribe=TRIBE_MYSTIC, attack=4, health=4, traits=[trait_roar_delve_rune]),
    SpellMagicWelcome(name='Illuminate', mana=1, effects=[Pick(choices=[EFFECT_FORESEE, EFFECT_2DAMAGE_ENEMY_CREATURE])]),
    SpellMagicWelcome(name='Versatile Conjuration', mana=3, effects=[Pick(choices=[EFFECT_DRAW_CARD, EFFECT_PROTECT_GOD])]),
    SpellMagicWelcome(name='Mind Jolt', mana=5, effects=[Pick(choices=[EFFECT_5DAMAGE_ENEMY_CREATURE, EFFECT_DRAW_2CARDS])]),
    SpellMagicWelcome(name='Epiphany', mana=6, effects=[EFFECT_6DAMAGE, EFFECT_DRAW_CARD]),
    # RelicMagicWelcome(name='Lambasting Wand', mana=2, attack=1, durability=3, effects=[(TRIGGER_TURN_START, )])
]
