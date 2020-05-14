# Created by Luoshu Zhang

from entity_extraction import get_entities
from helper import contains
import helper
import finite_state_machine_helpers
from FiniteStateMachine import StateMachine
from finite_state_machine_helpers import process_coordinator

import response_generator


def define_states():
    fsm_entities = StateMachine()
    # define the starting state
    fsm_entities.add_state("start", finite_state_machine_helpers.check_entities)
    fsm_entities.add_state("end", None, end_state=1)

    # define the validated state (make sure that the sentence contains valid information)
    fsm_entities.add_state("validated", finite_state_machine_helpers.classify_intent)

    # here are the branched states: based on classified intents
    fsm_entities.add_state("basic_query", finite_state_machine_helpers.divide_basic_questions)
    fsm_entities.add_state("admission_query", finite_state_machine_helpers.divide_admission_questions)
    fsm_entities.add_state("people_query", finite_state_machine_helpers.process_people_query_questions)
    fsm_entities.add_state("contact_query", finite_state_machine_helpers.process_contact_query_questions)
    fsm_entities.add_state("info_query", finite_state_machine_helpers.process_info_query)
    fsm_entities.add_state("enrichment_query", finite_state_machine_helpers.enrichment_query_answer)
    fsm_entities.add_state("quality_query", finite_state_machine_helpers.ensure_quality_generation)
    fsm_entities.add_state("access_query", None, end_state=1)
    fsm_entities.add_state("general_query", finite_state_machine_helpers.process_general)
    fsm_entities.add_state("prerequisite_query", finite_state_machine_helpers.get_prerequisite)

    # some implementation about query
    fsm_entities.add_state("query_coordinator", process_coordinator)

    # some other states about admission
    fsm_entities.add_state("admission_general", finite_state_machine_helpers.process_admission_general)

    fsm_entities.add_state("error", None, end_state=1)
    fsm_entities.set_start("start")
    return fsm_entities


if __name__ == "__main__":
    print(response_generator.greeting())
    while True:
        user_response = input("")
        entities = get_entities(user_response)
        entity_list = helper.change_entity_list(entities)
        fsm = define_states()
        fsm.run(entity_list)
