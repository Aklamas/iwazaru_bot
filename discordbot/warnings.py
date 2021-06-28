import re
from typing import Optional

WARNINGS = {
    # Sexist/exclusionary language
    r'\b(females)\b': 'pretty objectifying. If you are referring to women, use that instead',
    r'\b(hysterical)\b': 'sexist language. Some alternatives: hilarious, funny',
    r'\b(bimbos?|bitche?s?|cunts?|hags?|sluts?|twats?|whores?)\b': 'sexist language',
    # LGBT-related slurs
    r'\b(sissy|sissies|pansy|pansies|sodomites?|poofters?|pillow-biters?|fudgepackers?|cocksuckers?|fags?|faggots?|flamers?|ponces?|tapettes?|nolas?|queans?|jockers?|pooves?|woofters?)\b': 'a homophobic word or slur used against gay men',
    r'\b(dykes?|lesbos?)\b': 'a homophobic slur used against gay women',
    r'\b(fauxbians?)\b': 'a biphobic slur used against bisexual women',
    r'\b(tranny|trannies?|shim|heshe|shehe|she-man|sheman|transtrender|cuntboy|hefemale|shemales?|dickgirls?|ladyboys?|trans-identified)\b': 'A slur or derogatory way of referring to transgender people',
    r'\b(hermies?)\b': 'A slur for intersex people',
    r'\b(transvestites?)\b': 'a slur for cross-dressers',
    # Mental conditions
    r'\b(stupid|retarded|idiotic)\b': 'ableist language. Some alternatives: pathetic, uninspiring, vapid, obtuse, silly',
    r'\b(crazy|insane|bonkers)\b': 'ableist language. Some alternatives: ludicrous, wild, ridiculous, absurd, chaotic, silly, nonsensical, unreal, unbelievable',
    r'\b(mad)\b': 'ableist language. Some alternatives: angry, furious, annoyed',
    r'\b(idiots?|idiotic|imbeciles?|morons?|retards?|lunatics?)\b': 'ableist language. Some alternatives: uninformed, ignorant, incorrect, wrong',
    r'\b(cretins?|midgets?|freaks?|nutters?|schizos?|tards?|spaz|spazzes)\b': 'ableist language. check out some alternatives! <http://www.autistichoya.com/p/ableist-words-and-terms-to-avoid.html> (scroll down)',
    r'\b(spergs?|autists?)\b': 'a slur against autistic people',
    # Physical conditions
    r'\b(dumb)\b': 'ableist language. Some alternatives: silly, foolish, ignorant, uninformed, ridiculous, pathetic, absurd',
    r'\b(lame)\b': 'ableist language. Some alternatives: silly, foolish, ridiculous, pathetic, absurd, uncool',
    r'\b(cripples?|crippled|crips?)\b': 'ableist language. Some alternatives: broken, not working',
    # Racism
    r'\b(gypsy|gypsies|gipp|pikey|piky)\b': 'a racial slur against the Romani people.',
    r'\b(beaners?|beaney|tacoheads?|wetbacks?)\b': 'a racial slur for Mexican/mestizo people',
    r'\b(chinks?|chonky|japs?|dotheads?|gooks?|gooky|nips?|slant-eyes?|slopeheads?|slopey|sloper|zipperhead)\b': 'a racial slur against Asians',
    r'\b(guidos?|wops?)\b': 'a racial slur for Italians',
    r'\b(gusanos?)\b': 'a racial slur for Cubans that fled the Cuban Revolution',
    r'\b(injuns?|nitchies?|neche|neechees?|neejees?|nitchy|nitchies|nitchees?|nidges?|redskins?|squaws?)\b': 'a racial slur for Native Americans',
    r'\b(kanakas?)\b': 'a racial slur for Pacific Islanders',
    r'\b(lubras?)\b': 'a racial slur for Australian Aboriginal people',
    r'\b(micks?)\b': 'a racial slur for people of Irish descent',
    r'\b(polacks?|polaks?|polocks?)\b': 'a racial slur for people of Polish or Slavic origin',
    r'\b(portagees?)\b': 'a racial slur for people of Portugese origin',
    r'\b(russkis?|russkies)\b': 'a slur for people of Russian origin',
    r'\b(spics?|spicks?|spiks?|spigs?|spigotty)\b': 'a racial slur for a person of Hispanic descent',
    r'\b(wiggers?|whiggers?|wiggas?|wiggaz)\b': 'a racial slur against white people perceived to be "acting black"',
    r'\b(pakis?|pakkis?|paks?)\b': 'a slur against Pakistanis and Middle-Easterners in general',
    r'\b(niggers?|niggas?|niggress|nigette|niglet|nig|nigor|nigra|nigre|nigar|niggur|niggah|niggar|nigguh|negro|negroid|groid|coon|coons|burrhead|bluegum|golliwog|kaffir|kaffer|kafir|kaffre|kuffar|mau-mau|mouli|mulignan|mulignon|moolinyan|pickaninny|quashie|rastus|sheboon|spearchucker|thicklips|wog)\b': 'a racial slur against black people.',
    r'\b(savages?)\b': "a word that has racist roots in colonial violence against indigenous peoples and shouldn't be used. Some alternatives are: ridiculous, absurd, ruthless, brutal, rough, wild.",
    # Ethno-religious identity
    r'\b(mussies?|hajis?|hajjis?|hodgies?|ragheads?|towelheads?|mohammedans?)\b': 'a slur against Muslim people and people whose appearance leads them to be perceived as Muslim like Sikhs',
    r'\b(ayrabs?|a-rabs?)\b': 'intentional mispelling of an Arab person meant as a slur',
    r'\b(christ-killers?|heebs?|hebes?|kikes?|jewboys?|sheeny|shylocks?|yid|yakubian)\b': 'a slur for Jews',
    # catchall ableist (No suggestions)
    r'\b(psychos?|schitzos?|schizos?|spaz|spazzes|derps?|spastics?|spackers?)\b': 'ableist language. check out some alternatives! <http://www.autistichoya.com/p/ableist-words-and-terms-to-avoid.html> (scroll down)',
}

GUYS_RESPONSE = """Many people feel excluded when you refer to a group of people as "Guys".
Some alternatives if you meant to refer to explicitly men: men, dudes
Some alternatives if you meant to refer to people in general: all, everyone, friends, folks, people"""


def parse_message(text: str) -> Optional[str]:
    for key in WARNINGS:
        m = re.search(key, text, re.IGNORECASE)
        if m:
            return 'gentle reminder: {} is {}'.format(m.group(0), WARNINGS[key])

    if re.search(r'\b(hey|hi|you)\W+(guys)\b', text, re.IGNORECASE):
        return GUYS_RESPONSE

    return None
