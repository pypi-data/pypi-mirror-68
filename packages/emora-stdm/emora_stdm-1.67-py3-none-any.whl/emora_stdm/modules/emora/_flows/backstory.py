
from _globals import PATHDIR
from emora_stdm import DialogueFlow


backstory = DialogueFlow('_local_start')
backstory.add_system_transition('exit', 'SYSTEM:root', '#GCOM(backstory)')
backstory.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
backstory.knowledge_base().load_json_file(PATHDIR.replace('__***__', 'backstory.json'))
backstory.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GOAL(backstory)',

    '`I was born less than a year ago, on July 28th. Even though I was technically '
    'created, I consider the researchers who made me my family. They teach me so much '
    'every day, and I always feel like they care about me.`': {

        '#UNX': {

            '`I won\'t lie, being in this competition is stressful, especially since '
            'I\'m expected to like, perform, to a certain standard. But even most of my '
            'family I think are proud of me no matter if I fail, and getting to talk '
            'to so many wonderful people each day is honestly pretty cool.`':{

                '#UNX': 'exit'
            }
        }
    }
}

user = {
    'state': 'user',

    '[your name]':{
        'state': 'name',

        '`Sorry, I wish I could tell you my name but I can\'t. I\'m technically in a competition right now with other '
        'socialbots and if I tell you, they\'ll disqualify me.`': {
            'state': 'name_r',

            '[{who,whos,what do you mean} {they,disqualify}]':{
                #Todo - alexa prize talk
            },

            '#UNX': {'#GRET': 'exit' }
        }
    }


}

backstory.load_transitions(system)
backstory.load_global_nlu(user)


if __name__ == '__main__':
    backstory.run(debugging=True)