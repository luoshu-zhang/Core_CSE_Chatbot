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
    # TODO: implement the get_list
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
    fsm_entities.add_state("enrichment_query", None, end_state=1)
    fsm_entities.add_state("quality_query", None, end_state=1)
    fsm_entities.add_state("access_query", None, end_state=1)
    fsm_entities.add_state("general_query", finite_state_machine_helpers.process_general)

    # some implementation about query
    fsm_entities.add_state("query_coordinator", process_coordinator)

    # some other states about admission
    fsm_entities.add_state("admission_general", finite_state_machine_helpers.process_admission_general)
    fsm_entities.add_state("admission_job", None, end_state=1)

    fsm_entities.add_state("error", None, end_state=1)
    fsm_entities.set_start("start")
    return fsm_entities


def process_dialog(entities):
    if "intent" not in entities:
        response = response_generator.sorry()
        print(response)
        return

    # Respond the user's "plain statement"
    if contains("explain", entities["intent"]):
        if "info_target" not in entities:
            response = response_generator.sorry()
            print(response)
            return
        if contains("school", entities["info_target"]) or contains("degree", entities["info_target"]) or contains("student", entities["info_target"]):
            response = "DSCT: <DSCT>" + "\n" + "COMP: <COMP>" + "\n" + "COSC: <COSC>"
            print(response)
            return
        if contains("job", entities["info_target"]):
            print("Job info: <info>")
            return

    # Basically, if there is only one entity in the sentence,
    # we will answer the question directly
    if contains("get_basic", entities["intent"]):
        if "enrich_target" in entities:
            if contains("hackathon", entities["enrich_target"]):
                response = "Hackathon opportunities:"
                print(response)
                return
            if contains("contest", entities["enrich_target"]):
                response = "Contest opportunities:"
                print(response)
                return
            if contains("exchange", entities["enrich_target"]):
                response = "Exchange opportunities:"
                print(response)
                return
            if contains("independent work", entities["enrich_target"]):
                response = "Independent work:"
                print(response)
                return
            if contains("internship", entities["enrich_target"]):
                response = "Internship opportunities:"
                print(response)
                return
            if contains("honor courses", entities["enrich_target"]):
                response = "Honor courses:"
                print(response)
                return
            if contains("urop", entities["enrich_target"]):
                response = "Research opportunities:"
                print(response)
                return

        if "basic_target" not in entities and "program" not in entities:
            if contains("cse", entities["department_name"]):
                response = response_generator.give_basic_info("cse", "cse")
                print(response)
                return
        if "basic_target" not in entities:
            if contains("dsct", entities["program"]):
                response = "DSCT: <info>"
                print(response)
                return
            if contains("comp", entities["program"]):
                response = "COMP: <info>"
                print(response)
                return
            if contains("cosc", entities["program"]):
                response = "COSC: <info>"
                print(response)
                return
        if contains("vision", entities["basic_target"]) and contains("mission", entities["basic_target"]):
            response = response_generator.give_basic_info("vision statement", helper.vision_statement)
            response += "\n"
            response += response_generator.give_basic_info("mission statement", helper.mission_statement)
            print(response)
            return
        if contains("vision", entities["basic_target"]):
            response = response_generator.give_basic_info("vision statement", helper.vision_statement)
            print(response)
            return
        if contains("mission", entities["basic_target"]):
            response = response_generator.give_basic_info("mission statement", helper.mission_statement)
            print(response)
            return
        if contains("objective", entities["basic_target"]):
            response = response_generator.give_basic_info("objective", helper.objective)
            print(response)
            return
        if contains("news", entities["basic_target"]):
            response = response_generator.give_basic_info("news", "news")
            print(response)
            return

    # This part, we implement
    # how the chatbot will react if asked about admission
    if contains("get_admission", entities["intent"]):
        if "enrich_target" in entities:
            if contains("internship", entities["enrich_target"]):
                response = "Internship opportunities:"
                print(response)
                return
            if contains("honor courses", entities["enrich_target"]):
                response = "Honor courses:"
                print(response)
                return
            if contains("urop", entities["enrich_target"]):
                response = "Research opportunities:"
                print(response)
                return

        if "info_target" not in entities and "program" not in entities:
            response = "Are you a job seeker and a prospective student?"
            print(response)
            return
        if "info_target" in entities and "program" in entities:
            if contains("undergraduate", entities["program"]) or contains("postgraduate", entities["program"]):
                response = "Which program are you in?"
                print(response)
                return
            if contains("dsct", entities["program"]):
                response = "DSCT: <admission info>"
                print(response)
                return
            if contains("comp", entities["program"]):
                response = "COMP: <admission info>"
                print(response)
                return
            if contains("cosc", entities["program"]):
                response = "COSC: <admission info>"
                print(response)
                return

    # For the purpose of people information
    if contains("get_people", entities["intent"]):
        if "staff_name" in entities:
            response = "Information of " + entities["staff_name"][0]["value"] + " is ..."
            print(response)
            return
        if "research_area" in entities:
            response = "(Professor names) is doing " + entities["research_area"][0]["value"]
            print(response)
            return
        if "lab_name" in entities:
            response = "(Professor names) is doing " + entities["lab_name"][0]["value"]
            print(response)
            return
        if "faculty_name" in entities:
            response = "Information of " + entities["faculty_name"][0]["value"] + " is ..."
            print(response)
            return

    # For the purpose of getting contact
    if contains("get_contact", entities["intent"]):

        if "staff_name" in entities:
            if "info_target" in entities:
                if contains("tel", entities["info_target"]):
                    response = "Tel of " + entities["staff_name"][0]["value"] + " is ..."
                    print(response)
                    return
                if contains("email", entities["info_target"]):
                    response = "Email of " + entities["staff_name"][0]["value"] + " is ,,,"
                    print(response)
                    return
                if contains("title", entities["info_target"]):
                    response = "Title of " + entities["staff_name"][0]["value"] + " is ..."
                    print(response)
                    return
            response = "Contact of " + entities["staff_name"][0]["value"] + " is ..."
            print(response)
            return
        if "faculty_name" in entities:
            if "info_target" in entities:
                if contains("tel", entities["info_target"]):
                    response = "Tel of " + entities["faculty_name"][0]["value"] + " is ..."
                    print(response)
                    return
                if contains("email", entities["info_target"]):
                    response = "Email of " + entities["faculty_name"][0]["value"] + " is ,,,"
                    print(response)
                    return
                if contains("title", entities["info_target"]):
                    response = "Title of " + entities["faculty_name"][0]["value"] + " is ..."
                    print(response)
                    return
            response = "Contact of " + entities["faculty_name"][0]["value"] + " is ,,,"
            print(response)
            return
        if "department_name" in entities:
            response = "Contact of cse ..."
            print(response)
            return
    if contains("get_info", entities["intent"]):
        if "faculty_name" in entities:
            if contains("research interest", entities["info_target"]):
                response = "Research interest of " + entities["faculty_name"][0]["value"] + " is ..."
                print(response)
                return
            if contains("research area", entities["info_target"]):
                response = "Research area of " + entities["faculty_name"][0]["value"] + " is ..."
                print(response)
                return
            if contains("tel", entities["info_target"]):
                response = "Tel of " + entities["faculty_name"][0]["value"] + " is ..."
                print(response)
                return

    # Check out the possible enrichment in CSE, HKUST
    if contains("get_enrichment", entities["intent"]):
        if "enrich_target" in entities:
            if contains("hackathon", entities["enrich_target"]):
                response = "Hackathon opportunities:"
                print(response)
                return
            if contains("contest", entities["enrich_target"]):
                response = "Contest opportunities:"
                print(response)
                return
            if contains("exchange", entities["enrich_target"]):
                response = "Exchange opportunities:"
                print(response)
                return
            if contains("independent work", entities["enrich_target"]):
                response = "Independent work:"
                print(response)
                return
            if contains("internship", entities["enrich_target"]):
                response = "Internship opportunities:"
                print(response)
                return
            if contains("honor courses", entities["enrich_target"]):
                response = "Honor courses:"
                print(response)
                return
            if contains("urop", entities["enrich_target"]):
                response = "Research opportunities:"
                print(response)
                return
        print("Available enrichment:")
        return

    # Check the quality assurance
    if contains("ensure_quality", entities["intent"]):
        if "dependent_independent" in entities:
            if contains("independently", entities["dependent_independent"]):
                print("Self assurance network")
                return
            else:
                print("External assurance sources")
                return
        print("Assurance methods:")
        return

    # Find out the url link of different website
    if contains("get_access", entities["intent"]):
        if "site_name" in entities:
            if contains("fypms", entities["site_name"]):
                print("The URL of FYPMS is: ")
                return
        if "access_target" in entities:
            if contains("computing facilities", entities["access_target"]):
                print("There are several possible computation resources:")
                return

    # When the user attempts to know the general information about the chatbot
    if contains("get_general", entities["intent"]):
        response = response_generator.greeting()
        print(response)
        return


if __name__ == "__main__":
    print(response_generator.greeting())
    while True:
        user_response = input("")
        entities = get_entities(user_response)
        entity_list = helper.change_entity_list(entities)
        fsm = define_states()
        fsm.run(entity_list)
