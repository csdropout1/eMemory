from emora_stdm import DialogueFlow

transitions = {
    'state': 'start',
    '`Hello, how can I help you?`': {
        '<{do,can,may,make,appointment,book, make}, {hair coloring, hair colorings, [color, hair]}>': {
            '`Sure. What date and time are you looking for?`': {
                '{[{wednesday, wed, wednes}, {10 am, 11 am, 1 pm}],[{thursday, thur}, {10 am, 11 am}]}': {
                    '`Your appointment is set. Thank you for using our automated system!`': 'end'
                },
                'error': {
                    '`Sorry, that time slot is not available for hair coloring. Please return when you have checked our schedule! `': 'end'
                }
            }
        },
        '<{do,can,may,make,appointment,book, make}, {haircut, haircuts, hair cut, hair cuts, [cut, hair]}>': {
            '`Sure. What date and time are you looking for?`': {
                '{<{monday, mon}, {10 am, 1 pm, 2 pm}>, [{tuesday, tues}, 2 pm]}': {
                    '`Your appointment is set. Thank you for using our automated system!`': 'end'
                },
                'error': {
                    '`Sorry, that time slot is not available for hair cuts. Please return when you have checked our schedule!`': 'end'
                }
            }
        },
        '<{do,can,may,make,appointment,book, make}, {perm, perms}>': {
            '`Sure. What date and time are you looking for?`': {
                '{[{friday, fri}, {10 am, 11 am, 1 pm, 2 pm}], [{saturday, sat}, {10 am, 2 pm}]}': {
                    '`Your appointment is set. Thank you for using our automated system!`': 'end'
                },
                'error': {
                    '`Sorry, that time slot is not available for perms. Please return when you have checked our schedule!`': 'end'
                }
            }
        },
        '{hello, hi, hey}': {
            '` `': 'start'
        },
        '{bye}': {
            '`Have a wonderful day!!!`': 'end'
        },
        'error': {
            '`Sorry, our salon only provides haircuts, hair coloring, and perms. Would you like to navigate back to the start menu?`': {
                '[{yes, ofcourse, please do, y, ok}]':{
                    '`You have been directed to a new agent:`': 'start'
                },
                '{no, let me leave, stop, end, n}': {
                    '`We thank you for your patience, have a great day!`': 'end'
                },
                'error': {
                    '`Sorry, I did not understand you. Please try again later.`': 'end'
                }
            }
        }
    }
}


df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)

df.run(debugging=False)