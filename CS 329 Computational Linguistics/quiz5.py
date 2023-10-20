import openai
from emora_stdm import DialogueFlow
from emora_stdm import Macro, Ngrams
from typing import Dict, Any, List

PATH_API_KEY = './resources/openai_api.txt'
openai.api_key_path = PATH_API_KEY

class MacroCheck(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        model = 'gpt-3.5-turbo'
        content = 'You are a customer service provider for a hair salon and you will be ask for a service, return a one ' \
                  'word response (in lower all lower case) with one of the four options \'haircut\', \'perm\', \'haircoloring\', or \'none\' based ' \
                  'on the following customer request: '

        content = content + ngrams.raw_text()
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{'role': 'user', 'content': content}]
        )
        output = response['choices'][0]['message']['content'].strip()
        if output[-1] == ".":
            output = output.replace(".", "")

        if output != 'none':
            vars[output] = True
            if 'haircut' in vars:
                time = "Monday 10am, Monday 1pm, Monday 2pm, and Tuesday 2pm"

            if 'perm' in vars:
                time = "Friday, 10 am, Friday 11 am, Friday 1 pm, Friday 2pm, Saturday 10 am, and Saturday 2pm"

            if 'haircoloring' in vars:
                time = "Wednesday 10 am, Wednesday 11 am, Wednesday 1 pm, Thursday 10 am, and Thursday 11 am"
            vars['timing'] = time
            return output

        return False

class MacroCheckTimes(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        time = vars.get('timing')

        model = 'gpt-3.5-turbo'
        content = 'You are task with taking appointments. Our available times are '+time+', only return with ' \
                  'one word (all lowercase) \'yes\' or \'no\' depending on whether or not the following appointment request is valid: '

        content = content + ngrams.raw_text()
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{'role': 'user', 'content': content}]
        )
        output = response['choices'][0]['message']['content'].strip()
        if output[-1] == ".":
            output = output.replace(".", "")

        if output == 'yes':
            return True
        return False

class MacroGeTimes(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):

        return vars.get('timing')

transitions = {
    'state': 'start',
    '`Hello, how can I help you?`': {
        '[$THIS=#ASK]': {
            'state':'valid',
            '`Certainly, if you want to make an appointment for a`$THIS`, please check our schedule online '
            'and give me the time slot you want to book!.`': {
                '[$C=#CHECK]': {
                    '`Alright! Your appointment has been made successfully, please have a good day!!`': 'end'
                },
                'error': {
                    '`For a`$THIS`, our appointment times are`$TIME=#GET`, please select valid time! '
                    'Please remember to specify if it is am or pm too!`': {
                        '[$C=#CHECK]': {
                            '`Alright! Your appointment has been made successfully, please have a good day!!`': 'end'
                        },
                        'error': {
                            '`I am sorry, that time can not be booked, please come again. Good bye.`': 'end'
                        }
                    }
                }
            }
        },
        'error': {
            'state': 'omg',
            '`Sorry, our salon only provides haircuts, hair coloring, and perms. Can I help you with any of that?`': {
                '[$THIS=#ASK]': {
                    '`Ok! `': 'valid'
                },
                'error': {
                    '`Sorry, good bye.`': 'end'
                }
            }
        }
    }
}

macros = {
        'ASK': MacroCheck(),
        'CHECK': MacroCheckTimes(),
        'GET': MacroGeTimes(),
    }

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.add_macros(macros)
df.run(debugging=False)