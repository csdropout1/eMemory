from emora_stdm import DialogueFlow
from emora_stdm import Macro, Ngrams  # MACROS
from typing import Dict, Any, List

import re
#

class MacroNonCap(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        r = re.compile(r"[a-z]+")
        m = r.search(ngrams.text())
        if m is None: return False

        return True


class MacroReturn(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        r = re.compile(r"(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?")
        m = r.search(ngrams.text())
        if m is None:
            return False

        string = ""

        list = ["my", "favorite", "robot", "is", "of", "the", "it", "i", "like", "really", "maybe", "think", "genre", "a", "an", "its", "it\'s"]

        for i in range(1, 8):
            if m.group(i) not in list and string == "":
                string = m.group(i)

        vars['ROBOT'] = string

        return True

class MacroGen(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        r = re.compile(r"(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?(?:^|\s)?(\w+)?")
        m = r.search(ngrams.text())
        if m is None:
            return False

        string = ""

        list = ["my", "favorite", "of", "the", "is", "it", "i", "like", "really", "maybe", "think", "genre", "an", "a", "movie", "its", "it\'s"]
        for i in range(1, 7):
            if m.group(i) not in list and string == "":
                string = m.group(i)

        vars['G'] = string

        return True


transitions = {
    'state': 'start',
    '`Hello, this is Emora\'s little sister Estora. What is your name?`': {
        '[$NAMES=#ONT(names)]': {
            '`Oh hello ` $NAMES `, let\'s be friends!! By the way, have you watched any movies lately?`': {
                '[{yes, ofcourse, yeah, yea, y, ok, i did, have, yup}]': {
                    '`Cool!`': 'movies'
                },
                '[{no, nope, not, dont}]': {
                    '`Oh...`': 'usure'
                }
            }
        },
        '#NONCAP': {  # matches anything
            '`It\'s so nice to meet you! I can\'t wait to make more friends! By the way, have you watched any movies lately?`': {
                '[{yes, ofcourse, yeah, yea, y, ok, i did, have, yup}]': {
                    'state': 'movies',
                    '`What movie did you watch?`': {
                        '[#ONT(marvel)]': {
                            '`Oh I love Marvel movies too! Wait, who is your favorite hero?`': {
                                '[$HERO=#ONT(heros)]': {
                                    '`Oh I love`$HERO `too! I\'m guessing you love super hero movies?`': {
                                        '[{yes, ofcourse, yeah, yea, y, yup}]': {
                                            '`Why do you like them so much?`': {
                                                '#NONCAP': {
                                                    'state': 'thanks',
                                                    '`I see, thank you so much for sharing. I have to update now. Bye!!`': 'end'
                                                },
                                                'error': {  # no error should hit, but just in case
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        '[{no, nope, not, dont}]': {
                                            '`Oh, why do you like` $HERO `then?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        'error': {
                                            '`Beep Beep Boop..`': 'bigError'
                                        }
                                    }
                                },
                                '[#NONCAP]': {
                                    '`I never heard of that super hero before..`': 'thanks'
                                }
                            }
                        },
                        '[#ONT(dc)]': {
                            'state': 'superbat',
                            '`Oh I love the DC series too! Wait, I need to see if you are cool or not... Superman or Batman?`': {
                                '[{superman, super-man, super man}]': {
                                    '`I really like superman too, I\'m guessing you really like action moves?`': {
                                        '[{yes, ofcourse, yeah, yea, y, yup}]': {
                                            '`Why do you like them so much?`': {
                                                '#NONCAP': {
                                                    'state': 'thanks',
                                                    '`Thank you so much for sharing. I have to update now. Bye!!`': 'end'
                                                },
                                                'error': {  # no error should hit, but just in case
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        '[{no, nope, not, dont}]': {
                                            '`Oh, why do you like Superman then?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        'error': {
                                            '`Beep Beep Boop..`': 'bigError'
                                        }
                                    }
                                },
                                '[{batman, bat-man, bat man}]': {
                                    '`I really like batman too. Maybe I just like bats... I\'m guessing you really like action moves?`': {
                                        '[{yes, ofcourse, yeah, yea, y, yup}]': {
                                            '`Why do you like them so much?`': {
                                                '#NONCAP': {
                                                    'state': 'thanks',
                                                    '`Thank you so much for sharing. I have to update now. Bye!!`': 'end'
                                                },
                                                'error': {  # no error should hit, but just in case
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        '[{no, nope, not, dont}]': {
                                            '`Oh, why do you like Batman then?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        'error': {
                                            '`Beep Beep Boop..`': 'bigError'
                                        }
                                    }
                                },
                                'error': {
                                    '`Your the first DC fan that didn\'t like either!`': {

                                    }
                                }
                            }
                        },
                        '[#ONT(animals)]': {
                            '`I love animals too! I wish people would make more movies with animals... They are so cute and fluffy... What is your favorite animal`': {
                                '[{#LEM(dog), #LEM(cat), #LEM(bird), #LEM(penguin), #LEM(fish), #LEM(squirrel), #LEM(kangaroo)}]': {
                                    '`They are so cute!! I\'m guessing you are a fan of cute animations too?`': {
                                        '[{yes, ofcourse, yeah, yea, y, yup, sure, am}]': {
                                            '`Why do you like them so much?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {  # no error should hit, but just in case
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        '[{no, nope, not, dont}]': {
                                            '`Oh, we can\'t be friends... Why do you not like them?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        'error': {
                                            '`Beep Beep Boop..`': 'bigError'
                                        }
                                    }
                                },
                                '[{don\'t, dont, dislike}, animals]': {
                                    '`You don\'t like animals??? Bye`': 'end'
                                },
                                'error': {
                                    '`Bummer, the animal you like isn\'t even one of my top five favorites... So basic... I am assuming you are a fan of casual movies?`': {
                                        '[{yes, ofcourse, yeah, yea, y, yup, am, sure}]': {
                                            '`Why do you like them so much?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {  # no error should hit, but just in case
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        '[{no, nope, not, dont}]': {
                                            '`Oh, sorry for assuming... Is there a reason why you don\'t like casual movies?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        'error': {
                                            '`Beep Beep Boop..`': 'bigError'
                                        }
                                    }
                                }
                            }
                        },
                        '[$S=#ONT(classics)]': {
                            '`Oh you like classics?! We should watch the titanic together sometimes, I love the modern remades of Titanic. Do you think`$S` should have more modern adaptations as well?`': {
                                '[{yes, ofcourse, yeah, yea, y, yup}]': {
                                    '`I agree, the films will have much better graphic now. Imagine how great the cgi for`$S`would be...! Modernized jokes are also a plus. Based on your responses, I am guessing you like Comedy?`': {
                                        '[{yes, ofcourse, yeah, yea, y, yup, sure, am}]': {
                                            '`What made you like comedy?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {  # no error should hit, but just in case
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        '[{no, nope, not, dont}]': {
                                            '`How can you not like comedy??? Is there a personal reason?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        'error': {
                                            '`Beep Beep Boop..`': 'bigError'
                                        }
                                    }
                                },
                                '[{no, nope, not, dont}]': {
                                    '`You\'re right, remaking films might make them worse... So, I am guess you like nostalgic movies?`': {

                                    }
                                },
                                'error': {
                                    '`Beep Beep Boop..`': 'bigError'
                                }
                            }
                        },
                        '[#ONT(scifi)]': {
                            '`What a nerd!! Just kidding, I love futuristic films too! What\'s your favorite robot?`': {
                                '#RO': {
                                    '`You like`$ROBOT`??? Is it not scary? I\'m guessing you are a big fan of dystopian futuristic movies?`': {
                                        '[{yes, ofcourse, yeah, yea, y, yup, sure, am}]': {
                                            '`Why do you like them so much?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {  # no error should hit, but just in case
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        '[{no, nope, not, dont}]': {
                                            '`Oh, have you heard of 1984? I personally love dystopian stories, why do you dislike them?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        'error': {
                                            '`Beep Beep Boop..`': 'bigError'
                                        }
                                    }
                                }
                            }
                        },
                        'error': {
                            '`Oh, I never heard of that movie before, what genre is the movie?`': {
                                '#GEN': {
                                    '`Oh, you should definitely take me to see this movie. I love`$G`movies!! Do you know of any other`$G`movies?`': {
                                        '[{yes, ofcourse, yeah, yea, y, yup, sure}]': {
                                            '`Who is your favorite character in that movie?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {  # no error should hit, but just in case
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        '[{no, nope, not, dont}]': {
                                            '`Oh, so I am guessing you don\'t usually watch`$G`movies? Why did you watch this one?`': {
                                                '#NONCAP': {
                                                    '`Oh, `': 'thanks'
                                                },
                                                'error': {
                                                    '`Beep Beep Boop..`': 'bigError'
                                                }
                                            }
                                        },
                                        'error': {
                                            '`Beep Beep Boop..`': 'bigError'
                                        }
                                    }
                                },
                                'error': {
                                    '`Hmmm, I definitely never heard of a movie with that name and this genre before! You should take me to watch it sometime, I love surprises. Did you watch anything more famous?`': {
                                        '[{yes, ofcourse, i have, y, yup, i did, yea, sure}]': {
                                            '`Oh cool, `': 'movies'
                                        },
                                        '[{no, nope, not}]': {
                                            '`Well please come let me know when you do. I can talk about movies all day!`': 'end'
                                        },
                                        'error': {
                                            'state': 'bigError',
                                            '`\uD55C\uAD6D\uC5B4 \uC0AC\uC6A9\uD574? Oops, I think my language settings are not functioning properly. Sorry, I don\'t think I understand you. You can contact Emora for further assistance!`': 'end'
                                        }
                                    }
                                },
                            }
                        }
                    },
                },
                '[{no, nope, not, dont}]': {
                    'state': 'usure',
                    '`Are you sure?`': {
                        '[{yes, ofcourse, yeah, yea, y, ok}]': {
                            '`You must really not like movies... OMG I just remember I needed to update my system. Gotta run, Bye!!!`': 'end'
                        },
                        '[{no, nope, not, dont}]': {
                            '`Well. `': 'movies'
                        }
                    }
                },
                'error': {
                    '`I didn\'t get that. Maybe you should ask Emora. I am not good at understanding people that like to beat around the bush...`': 'end'
                }
            }
        },
        'error': {  # Just in case my all matching string fails...
            '`Sorry, I don\'t think I understand you. I still have lots to learn from my sister Emora!`': 'end'
        },

    }
}

macros = {
    'NONCAP': MacroNonCap(),
    'RO': MacroReturn(),
    'GEN': MacroGen()
}

df = DialogueFlow('start', end_state='end')
df.knowledge_base().load_json_file('resources/ontology_quiz3.json')
df.load_transitions(transitions)
df.add_macros(macros)

df.run(debugging=False)

"""

"""
