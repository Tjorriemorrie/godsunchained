TS_RELEASE_DATE = 1514700000

# sell address is the platform/collection
SELL_TOKEN_ADDRESS = '0xacb3c6a43d15b907e8433077b6d38ae40936fe2c'
SELL_TOKEN_TYPE_ERC721 = 'ERC721'

BUY_TOKEN_TYPE_ETH = 'ETH'
BUY_TOKEN_TYPE_ERC20 = 'ERC20'

ORDER_STATUS_ACTIVE = 'active'
ORDER_STATUS_FILLED = 'filled'

CURRENCY_ETH = 'ETH'
CURRENCY_GODS = 'GODS'
CURRENCY_USDC = 'USDC'
CURRENCY_IMX = 'IMX'
CURRENCY_OMI = 'OMI'
CURRENCY_GOG = 'GOG'

TOKEN_CURRENCIES = {
    '0xacb3c6a43d15b907e8433077b6d38ae40936fe2c': CURRENCY_ETH,
    '0xccc8cb5229b0ac8069c51fd58367fd1e622afd97': CURRENCY_GODS,
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': CURRENCY_USDC,
    '0xf57e7e7c23978c3caec3c3548e3d615c346e79ff': CURRENCY_IMX,
    '0xed35af169af46a02ee13b9d79eb57d6d68c1749e': CURRENCY_OMI,
    '0x9ab7bb7fdc60f4357ecfef43986818a2a3569c62': CURRENCY_GOG,
}

SET_CORE = 'core'
SET_ETHERBOTS = 'etherbots'
SET_GENESIS = 'genesis'
SET_MYTHIC = 'mythic'
SET_PROMO = 'promo'
SET_TRIAL = 'trial'
SET_WELCOME = 'welcome'
CHOICES_SETS = (
    (SET_CORE, 'Core'),
    (SET_ETHERBOTS, 'Etherbots'),
    (SET_GENESIS, 'Genesis'),
    (SET_MYTHIC, 'Mythic'),
    (SET_PROMO, 'Promo'),
    (SET_TRIAL, 'Trial'),
    (SET_WELCOME, 'Welcome'),
)

GOD_NEUTRAL = 'neutral'
GOD_DEATH = 'death'
GOD_DECEPTION = 'deception'
GOD_LIGHT = 'light'
GOD_MAGIC = 'magic'
GOD_NATURE = 'nature'
GOD_WAR = 'war'
CHOICES_GODS = (
    (GOD_NEUTRAL, 'Neutral'),
    (GOD_DEATH, 'Death'),
    (GOD_DECEPTION, 'Deception'),
    (GOD_LIGHT, 'Light'),
    (GOD_MAGIC, 'Magic'),
    (GOD_NATURE, 'Nature'),
    (GOD_WAR, 'War'),
)

TYPE_ADVANCEMENT = 'advancement'
TYPE_CREATURE = 'creature'
TYPE_GOD_POWER = 'god power'
TYPE_HERO = 'hero'
TYPE_RELIC = 'relic'
TYPE_SPELL = 'spell'
TYPE_WEAPON = 'weapon'
CHOICES_TYPES = (
    (TYPE_ADVANCEMENT, 'Advancement'),
    (TYPE_CREATURE, 'Creature'),
    (TYPE_GOD_POWER, 'God Power'),
    (TYPE_HERO, 'Hero'),
    (TYPE_RELIC, 'Relic'),
    (TYPE_SPELL, 'Spell'),
    (TYPE_WEAPON, 'Weapon'),
)

TRIBE_NEUTRAL = 'neutral'
TRIBE_AETHER = 'aether'
TRIBE_AMAZON = 'amazon'
TRIBE_ANUBIAN = 'anubian'
TRIBE_ATLANTIAN = 'atlantian'
TRIBE_DRAGON = 'dragon'
TRIBE_GUILD = 'guild'
TRIBE_MYSTIC = 'mystic'
TRIBE_NETHER = 'nether'
TRIBE_OLYMPIAN = 'olympian'
TRIBE_STRUCTURE = 'structure'
TRIBE_VIKING = 'viking'
TRIBE_WILD = 'wild'
CHOICES_TRIBES = (
    (TRIBE_NEUTRAL, 'Neutral'),
    (TRIBE_AETHER, 'Aether'),
    (TRIBE_AMAZON, 'Amazon'),
    (TRIBE_ANUBIAN, 'Anubian'),
    (TRIBE_ATLANTIAN, 'Atlantian'),
    (TRIBE_DRAGON, 'Dragon'),
    (TRIBE_GUILD, 'Guild'),
    (TRIBE_MYSTIC, 'Mystic'),
    (TRIBE_NETHER, 'Nether'),
    (TRIBE_OLYMPIAN, 'Olympian'),
    (TRIBE_STRUCTURE, 'Structure'),
    (TRIBE_VIKING, 'Viking'),
    (TRIBE_WILD, 'Wild'),
)

QUALITY_PLAIN = 'plain'
QUALITY_METEORITE = 'meteorite'
QUALITY_SHADOW = 'shadow'
QUALITY_GOLD = 'gold'
QUALITY_DIAMOND = 'diamond'
CHOICES_QUALITIES = (
    (QUALITY_PLAIN, 'Plain'),
    (QUALITY_METEORITE, 'Meteorite'),
    (QUALITY_SHADOW, 'Shadow'),
    (QUALITY_GOLD, 'Gold'),
    (QUALITY_DIAMOND, 'Diamond'),
)

RARITY_COMMON = 'common'
RARITY_RARE = 'rare'
RARITY_EPIC = 'epic'
RARITY_LEGENDARY = 'legendary'
RARITY_MYTHIC = 'mythic'
CHOICES_RARITIES = (
    (RARITY_COMMON, 'Common'),
    (RARITY_RARE, 'Rare'),
    (RARITY_EPIC, 'Epic'),
    (RARITY_LEGENDARY, 'Legendary'),
    (RARITY_MYTHIC, 'Mythic'),
)

TRAIT_AFTERLIFE = 'afterlife'
TRAIT_BACKLINE = 'backline'
TRAIT_BLITZ = 'blitz'
TRAIT_BURN = 'burn'
TRAIT_CONFUSED = 'confused'
TRAIT_COPY = 'copy'
TRAIT_DEADLY = 'deadly'
TRAIT_FLANK = 'flank'
TRAIT_FORESEE = 'foresee'
TRAIT_FRONTLINE = 'frontline'
TRAIT_GODBLITZ = 'godblitz'
TRAIT_HIDDEN = 'hidden'
TRAIT_LEECH = 'leech'
TRAIT_OVERKILL = 'overkill'
TRAIT_PROTECTED = 'protected'
TRAIT_REGEN = 'regen'
TRAIT_ROAR = 'roar'
TRAIT_SOULLESS = 'soulless'
TRAIT_TWIN_STRIKE = 'twin strike'
TRAIT_WARD = 'ward'

CONDITION_RUNE_CARD = 'rune card'
CONDITION_LESS_CARDS = 'less cards'

EFFECT_BUFF_ATTACK = 'buff attack'
EFFECT_BUFF_HEALTH = 'buff health'
EFFECT_DAMAGE = 'damage'
EFFECT_2DAMAGE_ENEMY_CREATURE = '2 damage enemy creature'
EFFECT_5DAMAGE_ENEMY_CREATURE = '5 damage enemy creature'
EFFECT_6DAMAGE = '6 damage'
EFFECT_DAMAGE_FROM_HEALTH = 'damage from health'
EFFECT_DELVE = 'delve'
EFFECT_DESTROY = 'destroy'
EFFECT_DRAW_CARD = 'draw card'
EFFECT_DRAW_2CARDS = 'draw 2 cards'
EFFECT_DRAW_MANA_INC1 = 'draw card inc mana 1'
EFFECT_FORESEE = 'foresee'
EFFECT_HEAL = 'heal'
EFFECT_INC_MANA_1 = 'inc mana 1'
EFFECT_INC_MANA_2 = 'inc mana 2'
EFFECT_PROTECT_GOD = 'protect god'
EFFECT_PULL_VOID = 'pull void'
EFFECT_SLEEP = 'sleep'
EFFECT_TRANSFORM = 'transform'
EFFECT_RETURN_HAND = 'return hand'
EFFECT_RETURN_MANA_INC2 = 'return hand inc mana 2'

TARGET_BOTH_PLAYERS = 'target both players'
TARGET_ENEMY_CREATURE = 'target enemy creature'
TARGET_ALL_OTHER_ENEMY_CREATURE = 'target all other enemy creature'
TARGET_FOE = 'target foe'
TARGET_ME = 'target me'
TARGET_RANDOM_ENEMY_CREATURE = 'target random enemy creature'

TRIGGER_CARD_PLAYED = 'card played'
TRIGGER_CREATURE_DEATH = 'creature death'
TRIGGER_GOD_ATTACKED = 'god attacked'
TRIGGER_TURN_START = 'turn start'

MAX_CARDS_CREATURES = 6
MAX_CARDS_HAND = 9
