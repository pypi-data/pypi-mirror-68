
from emora_stdm import CompositeDialogueFlow

#from emora_stdm.modules.emora.component import component
# from emora_stdm.modules.emora.pleasant_opening import opening
# from emora_stdm.modules.emora.coronavirus_checkin import coronavirus_checkin
# from emora_stdm.modules.emora.general_activity import df as activity
# from emora_stdm.modules.emora.worklife import df as worklife
# from emora_stdm.modules.emora.school import df as school

# from emora_stdm.modules.emora._flows.component import component
from emora_stdm.modules.emora._flows.tournament import tournament
from emora_stdm.modules.emora._flows.school import school
from emora_stdm.modules.emora._flows.baby import baby
from emora_stdm.modules.emora._flows.backstory import backstory
from emora_stdm.modules.emora._flows.competition import competition
from emora_stdm.modules.emora._flows.house import house
from emora_stdm.modules.emora._flows.reading import reading

emora = CompositeDialogueFlow('root', 'root', 'root')
emora.component('SYSTEM').knowledge_base().load_json_file('_common.json')

components = {
    # 'component': component,
    'backstory': backstory,
    'tournament': tournament,
    'school': school,
    'baby': baby,
    'house': house,
    'reading': reading
}
for namespace, component in components.items():
    emora.add_component(component, namespace)

emora.add_system_transition('root', 'tournament:start', '', score=999)
emora.add_system_transition('root', 'school:start', '')
emora.add_system_transition('root', 'baby:start', '')
emora.add_system_transition('root', 'house:start', '')
emora.add_system_transition('root', 'reading:start', '')
emora.add_system_transition('root', 'end', '`Oh, I have to go! Bye!`', score=-999)

personal_nlu = {

    ### Emora is virtual person #########################################

    '[{what, whats, tell me, say}, your, name]': 'backstory:name',

    '{'
    '[{arent you, are you, you are, you arent} '
    '{robot, ai, software, bot, chatbot, artificial intelligence, program, electronic, human, person, alive}], '
    '}':{
        # todo
    },

    ### About Emora #########################################

    # Does Emora have something humanlike
    '[do you have]':{
        # todo
    },

    # Do you ___
    '[do you]'
    '#SCORE(0.1)':{

    },

    ### Emora capabilities and appraisal #########################################

    # What can you talk about
    '{'
    '[what, can {you, we} {talk about, discuss}], '
    '[what, do you, {know about, talk about, discuss}]'
    '}':{

    },



    ### Security and user info #########################################

    # Is Emora spying on the user
    '{'
    '[are you {spying, [collecting {info, information, data}]}], '
    '[why {[you, {want, need} know], ask, asking}]'
    '}':{

    },

    ### About User #########################################

    # User job
    '{'
    '[{i am, im} a #ONT(job)], '
    '[i #ONT(job) {for a living, for work, professionally, as a job, for a job}], '
    '[my {job, work} #ONT(job)], '
    '[i {work, take jobs, have a job} #ONT(job)]'
    '}':{

    },

    # User is a __
    '{'
    '[{im, i am} #ONT(persontype)]'
    '}':{

    },

    # User likes
    '{'
    '[i {like, love} $user_likes=#ONT(likable)?]'
    '}':{
        '`Me too!`': {
            'state': 'returning_from_global_like',

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    # User currently feels __
    '{'
    '[{im, i feel, ive been, i am} #ONT(feeling)]'
    '}':{

    },

    # User went __
    '{'
    '[{i, we, me and, and me} went]'
    '}':{

    },

    ### User tests Emora #########################################


    ### Topic specific #########################################

    # Have you seen ___
    '{'
    '[have you, {seen, watched}]'
    '}':{

    },

    # Have you read book
    '{'
    '[have you, read]'
    '}':{

    },

    # Have you visited
    '{'
    '[have you, {been to, gone to, visited, went to}]'
    '}':{

    },

    #

}

for component in emora.components():
    component.load_global_nlu(personal_nlu)

if __name__ == '__main__':
    emora.precache_transitions()
    emora.run(debugging=True)

