from emora_stdm import DialogueFlow
from emora_stdm import Macro, Ngrams
from typing import Dict, Any, List
import json
import requests
import random
import time
import names
import pickle

def save(df: DialogueFlow, varfile: str):
    df.run()
    d = {k: v for k, v in df.vars().items() if not k.startswith('_')}
    pickle.dump(d, open(varfile, 'wb'))


def load(df: DialogueFlow, varfile: str):
    d = pickle.load(open(varfile, 'rb'))
    df.vars().update(d)
    df.run()
    save(df, varfile)

class MacroDefineS(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        theSong = vars.get('SONG')
        re = "I am out of song recommendations..."
        if theSong == "Let it Go - Frozen":
            re = theSong + " is a popular Disney song enjoyed by many across the world."
        if theSong == "Way back home - SHAUN" or theSong == "OMG - New Jeans" or theSong == "Lilac - IU":
            re = theSong + " is a well known Korean pop song that is regularly used in TikToks and instagram dances."
        if theSong == "Fireflies - Owl City":
            re = theSong + " is a classic song created in the early 2010s. It is a pop song that many - if not everyone - people will have heard of."
        if theSong == "Love Story - Taylor Swift" or theSong == "Dark Horse - Katie Perry":
            re = theSong + " is a pop song sang by a very well known artist that is admired by millions of fans. She has also sang multiple different pop love songs."
        return re
class MacroDefineM(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        theMovie = vars.get('MOVIE')
        re = "I am out of movie recommendations..."
        if theMovie == "Batman" or theMovie == "Superman":
            re = theMovie + " is a DC comics series that is very popular among youth, I use to watch it all the time."
        if theMovie == "The Amazing Spiderman" or theMovie == "Ironman":
            re = theMovie + " is a classic Marvel movie, you can't go world with these. Full of action and sarcasm."
        if theMovie == "The Amazing Spiderman" or theMovie == "Ironman":
            re = theMovie + " is a classic Marvel movie, you can't go world with these. Full of action and sarcasm."
        if theMovie == "Titanic" or theMovie == "The Simpsons":
            re = theMovie + " is a classic show. You can enjoy it with your family over long holidays! If you like sad stories, you will love this."
        if theMovie == "Attack on Titans" or theMovie == "StarWars":
            re = theMovie + " is fantasy movie with weird creatures and an unique storyline. If you like action, you would love this movie!"
        if theMovie == "Slender Man" or theMovie == "Lucifer":
            re = theMovie + " is a movie about supernatural creatures. If you like movies with anti heros, this ones definitely for you."
        if theMovie == "???":
            re = "Yes, the movie is called "+ theMovie + "... Don't ask too many questions, or you will regret it o-o"
        return re
class MacroMusic(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        list = vars.get('SongList')
        id = vars.get('NAMES')
        people = vars.get('usedNames')

        n = len(list)

        if n == 0:
            return "a movie? I am currently out of song recommendations."
        m = random.randint(0, n - 1)
        people.update({id: list[m]})

        return list[m]
class MacroShow(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        list = vars.get('MovieList')
        id = vars.get('NAMES')
        people = vars.get('usedNames')

        n = len(list)

        if n == 0:
            return "a movie? I am currently out of song recommendations."
        m = random.randint(0, n - 1)
        people.update({id: list[m]})

        return list[m]
class MacroTimeAndWeather(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        if 'allNames' not in vars:
            vars['allNames'] = []
        if 'usedNames' not in vars:
            vars['usedNames'] = {}

        if 'SongList' not in vars:
            vars['SongList'] = ["Let it Go - Frozen", "Fireflies - Owl City", "Way back home - SHAUN", "OMG - New Jeans",
                            "Lilac - IU", "Love Story - Taylor Swift", "Dark Horse - Katie Perry"]
        if 'MovieList' not in vars:
            vars['MovieList'] = ["Batman", "Superman", "The Amazing Spiderman", "Ironman", "Titanic", "The Simpsons",
                             "Lucifer", "Attack on Titans", "StarWars", "Slender Man", "???"]

        # extract the hour as an integer from the time string
        hour = int(time.strftime("%H", time.strptime(current_time, "%Y-%m-%d %H:%M:%S")))
        if hour >= 6 and hour < 12:
            sentiment = "Good Morning!! "
        elif hour >= 12 and hour < 18:
            sentiment = "Good Afternoon!! "
        elif hour >= 18 and hour < 22:
            sentiment = "Good Evening!! "
        else:
            sentiment = "You need to go to bed, but maybe a 5 minute conversation wouldn't hurt... "

        url = 'https://api.weather.gov/gridpoints/FFC/52,88/forecast'
        r = requests.get(url)
        d = json.loads(r.text)
        periods = d['properties']['periods']
        today = periods[0]

        asklist = ["What is your name?", "What can I call you?", "What should I call you?",
                   "Of whom should I grace my presence with?",
                   "What is your legal name, SSN, date of .. uh I mean just your name?", "State your name mortal!",
                   "I'm Estora, what's your name?", "Let's be friends, what should I call you?"]
        n = len(asklist)
        m = random.randint(0, n - 1)

        return sentiment + "The weather looks " + today['shortForecast'] + " today. " + asklist[m]
class MacroNAME(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):

        first_names = []
        for i in range(50000):  # might take a sec or two but works
            first_names.append(names.get_first_name().lower())

        original_string = ngrams.text()
        split_string = original_string.split()

        for i in split_string:
            if i != 'my':
                for j in first_names:
                    if i == j:
                        if i not in vars.get('allNames'):

                            vars.get('allNames').append(i)
                            vars['usedNames'].update({i: ""})

                            return i
        return False

class MacroWelcomeBack(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        temp = vars.get('allNames')
        original_string = ngrams.text()
        split_string = original_string.split()

        for i in split_string:
            if i != 'my':
                for j in temp:

                    if i == j:
                        vars['CURRENT'] = vars['usedNames'].get(i)
                        return i
        return False

class MacroCap(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        id = ngrams.text().split()[0]

        if id not in vars:
            vars.get('allNames').append(id)
            vars['usedNames'].update({id: ""})
            return id
        return False

class MacroAddS(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        variable = vars.get('SONG')

        temp = vars.get('SongList')
        if temp:
            temp.remove(variable)
        return True
class MacroAddM(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        variable = vars.get('MOVIE')

        temp = vars.get('MovieList')
        if temp:
            temp.remove(variable)
        return True

def visits() -> DialogueFlow:
    transitions = {
        'state': 'start',
        '#TIME': {
            '[$NAMES=#CHANGE]': {
                '`Hi`$NAMES`! Would you like a song or a movie?`': {
                    '[{#LEM(song), #LEM(music), #LEM(beat)}]': {
                        'state': 'music',
                        '`How about `$SONG=#RANDMUSIC`?` #ADDS($SONG)': {
                            '[{another, heard, know, give, can, other, have, already}, {before, that, already, more, another, one, it, recommend, recommendations}]': {
                                '`Hmm, ok. `': 'music'
                            },
                            '[{what, tell, whats, is}, {is, about, kind, genre, it, more}]': {
                                '#DEFINESONG': {
                                    '[{can, may, another, do, one}, {one, different, #LEM(song), music, another, please}]': {
                                        '`Sure, `': 'music'
                                    },
                                    '[{#LEM(movie), #LEM(show), watch}]': {
                                        '`Ok, `': 'show'
                                    },
                                    'error': {
                                        '`Enjoy!`': 'end'
                                    }
                                }
                            },
                            '[{ok, sure, #LEM(movie), yes, good}]': {
                                '`It is a very good one. Please enjoy it!`': 'end'
                            },
                            '[{#LEM(movie), #LEM(show), watch}]': {
                                '`Ok, `': 'show'
                            },
                            'error': {
                                '`Gotta run, enjoy the music!!!`': 'end'
                            }
                        }
                    },
                    '[{#LEM(movie), #LEM(show), watch}]': {
                        'state': 'show',
                        '`How about `$MOVIE=#RANDSHOW`?` #ADDM($MOVIE)': {
                            '[{another, seen, know, give, can, other, have, I, already}, {before, seen, heard, already, more, another, one, it, recommend, recommendations}]': {
                                '`Hmm, ok. `': 'show'
                            },
                            '[{what, tell, whats, is}, {is, about, kind, genre, it, more}]': {
                                '#DEFINESHOW': {
                                    '[{can, may, another, do, one}, {one, different, #LEM(song), music, another, please}]': {
                                        '`Sure, `': 'show'
                                    },
                                    '[{#LEM(song), #LEM(music), listen}]': {
                                        '`Ok, `': 'music'
                                    },
                                    'error': {
                                        '`Enjoy!`': 'end'
                                    }
                                }
                            },
                            '[{#LEM(song), #LEM(music), listen}]': {
                                '`Ok, `': 'music'
                            },
                            'error': {
                                '`Gotta run, enjoy the movie recommendation!!!`': 'end'
                            }
                        }
                    }
                },
                'error': {
                    '`Please choose a song or movie, I really want to talk about that!`': {
                        '[{#LEM(song), #LEM(music), #LEM(beat)}]': {
                            '`Ok, `': 'music'
                        },
                        '[{#LEM(movie), #LEM(show), watch}]': {
                            '`Hmm, lets see... `': 'show'
                        },
                        'error': {
                            '`It seems we do not see eye to eye to I to I... Goodbye!`': 'end'
                        }

                    }
                }
            },
            '[$NAMES=#WEL]': {
                '`Oh! Hello `$NAMES` welcome back `$NAMES`. Did you enjoy `$CURRENT`?`': {
                    '[{great, wonderful, loved, love, liked, fire, not bad, good, yes, yea, ofcourse, yeah, did}]': {
                        '`Wonderful, what else would you want me to recommend?`': {
                            '[{#LEM(song), #LEM(music), #LEM(beat)}]': {
                                '`Ok, `': 'music'
                            },
                            '[{#LEM(movie), #LEM(show), watch}]': {
                                '`Sure, `': 'show'
                            },
                            'error': {
                                '`Enjoy!`': 'end'
                            }
                        },
                    },
                },
                'error': {
                    '`lol`': 'end'
                }
            },
            'error': {
                '`I didn\'t quite get your name, it seems to be quite unique, can you type it again as one word?`': {
                    '[$NAMES=#CAPTURE]': {
                        '`Hi, `$NAMES`. Nice to meet you. Would you like a song or a movie?`': {
                            '[{#LEM(song), #LEM(music), #LEM(beat)}]': {
                                'state': 'music'
                            },
                            '[{#LEM(movie), #LEM(show), watch}]': {
                                'state': 'show'
                            },
                            'error': {
                                '`Sorry I can only recommend songs and movies at this time. What would you like?`': {
                                    '[{#LEM(song), #LEM(music), #LEM(beat)}]': {
                                        'state': 'music'
                                    },
                                    '[{#LEM(movie), #LEM(show), watch}]': {
                                        'state': 'show'
                                    },
                                    'error': {
                                        '`GoodBye!`': 'end'
                                    }
                                }
                            }
                        }
                    },
                    '[$NAMES=#WEL]': {
                        '`Oh! Hello `$NAMES` welcome back `$NAMES`. Did you enjoy `$CURRENT`?`': {
                            '[{great, wonderful, loved, love, liked, fire, not bad, good, yes, yea, ofcourse, yeah, did}]': {
                                'state': 'rec',
                                '`Wonderful, what else would you want me to recommend?`': {
                                    '[{#LEM(song), #LEM(music), #LEM(beat)}]': {
                                        '`Ok, `': 'music'
                                    },
                                    '[{#LEM(movie), #LEM(show), watch}]': {
                                        '`Sure, `': 'show'
                                    },
                                    'error': {
                                        '`Enjoy!`': 'end'
                                    }
                                },
                            },
                            '[{no, not, not really, nope, n}]': {
                                '`I am sorry to hear that. Let me recommend you something else! `': 'show'
                            },
                            'error': {
                                '`Hmm... Well I need to go now... but you should recommend me something next time!`': 'end'
                            }
                        },
                        'error': {
                            '`I see. Well would you like another recommendation?`': {
                                '[{yes. please, great, yeah, y, I do, give, sure, nice}]': {
                                    '`One moment... Alright... `': 'rec'
                                },
                                '[{no, nope, n, hate, stop, go, away, never, not}]': {
                                    '`I am sad you do not like my recommendations. Bye, I will go cry...`': 'end'
                                },
                                'error': {
                                    '`Yesterday is history, tomorrow is a mystery, and today is a gift... that is why they call it present!`': 'end'
                                }
                            }
                        }
                    },
                    'error': {
                        '`WOW I AM IMPRESSED, THIS ERROR SHOULD NEVER BE ACCESSED. Estora is happy to know you exist.`': 'end'
                    }

                }
            }
        }
    }

    macros = {
        'CHANGE': MacroNAME(),
        'TIME': MacroTimeAndWeather(),
        'RANDMUSIC': MacroMusic(),
        'DEFINESONG': MacroDefineS(),
        'RANDSHOW': MacroShow(),
        'DEFINESHOW': MacroDefineM(),
        'CAPTURE': MacroCap(),
        'ADDS': MacroAddS(),
        'ADDM': MacroAddM(),
        'WEL': MacroWelcomeBack(),
    }

    df = DialogueFlow('start', end_state='end')
    df.load_transitions(transitions)
    df.add_macros(macros)
    return df

save(visits(), 'resources/visits.pkl')
print("User exits.. One day later... Or whenever...")
load(visits(), 'resources/visits.pkl')


