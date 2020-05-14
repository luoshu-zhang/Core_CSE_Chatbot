from helper import contains
import helper
import response_generator
from response_generator import provide_faculty_info
from entity_extraction import get_entities
from response_generator import provide_course_info


def process_unhandled_cases(entities):
    # 在这里处理low confidence的情况
    pass


def check_entities(entities):
    if not entities or "intent" not in entities:
        new_state = "error"
        return new_state, entities
    new_state = "validated"
    return new_state, entities


def classify_intent(entities):
    if contains("get_basic", entities["intent"]):
        new_state = "basic_query"
        return new_state, entities
    if contains("get_admission", entities["intent"]):
        new_state = "admission_query"
        return new_state, entities
    if contains("get_people", entities["intent"]):
        new_state = "people_query"
        return new_state, entities
    if contains("get_contact", entities["intent"]):
        new_state = "contact_query"
        return new_state, entities
    if contains("get_info", entities["intent"]):
        new_state = "info_query"
        return new_state, entities
    if contains("get_enrichment", entities["intent"]):
        new_state = "enrichment_query"
        return new_state, entities
    if contains("ensure_quality", entities["intent"]):
        new_state = "quality_query"
        return new_state, entities
    if contains("get_access", entities["intent"]):
        new_state = "access_query"
        return new_state, entities
    if contains("get_general", entities["intent"]):
        new_state = "general_query"
        return new_state, entities
    new_state = "error"
    return new_state, entities


def divide_basic_questions(entities):
    # TODO: implement the "inbound"/"outbound" differentiation for exchange
    # Enrichment opportunities
    if "enrich_target" in entities:
        response = ""
        enrich_general = helper.load_enrichment_general_info()
        for i in range(len(entities["enrich_target"])):
            if i != 0:
                response += "\n\n"
            enrichment = entities["enrich_target"][i]["value"]
            if enrichment == "Exchange Programs":
                if "exchange_type" in entities:
                    if contains("inbound", entities["exchange_type"]) and contains("outbound", entities["exchange_type"]):
                        response += response_generator.provide_inbound_exchange()
                        response += "\n"
                        response += response_generator.provide_outbound_exchange()
                    elif contains("inbound", entities["exchange_type"]):
                        response += response_generator.provide_inbound_exchange()
                    elif contains("outbound", entities["exchange_type"]):
                        response += response_generator.provide_outbound_exchange()
            else:
                response += enrich_general[enrichment][1]
        print(response)
        new_state = "end"
        return new_state, entities
    # Program information
    if "program" in entities:
        program_info = helper.load_program_info()
        response = ""
        for i in range(len(entities["program"])):
            if i != 0:
                response += "\n\n"
            program = entities["program"][i]["value"]
            intro = program_info[program][1]
            response += intro
        print(response)
        new_state = "end"
        return new_state, entities
    # Course information
    if "course" in entities and "honor_course" not in entities:
        course_attributes, course_info = helper.load_course_information()
        response = ""
        for i in range(len(entities["course"])):
            if i != 0:
                response += "\n\n"
            code = entities["course"][i]["value"]
            response += response_generator.provide_course_info_by_table(code, course_info)
        print(response)
        new_state = "end"
        return new_state, entities
    # To deal with the problem of unhandled "honor course" problem.
    if "honor_course" in entities and "course" not in entities:
        course_attributes, course_info = helper.load_course_information()
        response = ""
        for i in range(len(entities["honor_course"])):
            if i != 0:
                response += "\n\n"
            code = entities["honor_course"][i]["value"]
            response += response_generator.provide_course_info_by_table(code, course_info)
        print(response)
        new_state = "end"
        return new_state, entities
    # Dealing with the problem of "mixed" type of information.
    if "honor_course" in entities and "course" in entities:
        course_attributes, course_info = helper.load_course_information()
        response = ""
        course_entities_augmented = entities["honor_course"] + entities["course"]
        for i in range(len(course_entities_augmented)):
            if i != 0:
                response += "\n\n"
            code = course_entities_augmented[i]["value"]
            response += response_generator.provide_course_info_by_table(code, course_info)
        print(response)
        new_state = "end"
        return new_state, entities
    # Dealing with the problem of research area
    if "research_area" in entities:
        response = ""
        fullname, attributes = helper.load_research_area_full_name()
        for i in range(len(entities["research_area"])):
            if i != 0:
                response += "\n\n"
            research_area = entities["research_area"][i]["value"]
            response += attributes[research_area]
        print(response)
        new_state = "end"
        return new_state, entities
    # Basic information about the department
    if "basic_target" not in entities and "program" not in entities and "course" not in entities:
        if "department_name" in entities:
            response = response_generator.provide_basic_dept_info()
            print(response)
            new_state = "end"
            return new_state, entities
    new_state = "error"
    return new_state, entities


# TODO: implement the FSM of admission information
def divide_admission_questions(entities):
    if "enrich_target" in entities:
        if contains("Exchange Programs", entities["enrich_target"]):
            if "exchange_type" in entities:
                if contains("inbound", entities["exchange_type"]):
                    response = response_generator.provide_inbound_exchange()
                    print(response)
                    new_state = "end"
                    return new_state, entities
                else:
                    response = response_generator.provide_outbound_exchange()
                    print(response)
                    new_state = "end"
                    return new_state, entities
            else:
                response = response_generator.query_in_out()
                print(response)
                in_or_out = input("")
                entity_list = get_entities(in_or_out)["entities"]
                if "exchange_type" in entity_list:
                    if contains("outbound", entity_list["exchange_type"]):
                        response = response_generator.provide_outbound_exchange()
                        print(response)
                        new_state = "end"
                        return new_state, entities
                    else:
                        response = response_generator.provide_inbound_exchange()
                        print(response)
                        new_state = "end"
                        return new_state, entities
                else:
                    response = response_generator.provide_inbound_outbound_exchange()
                    print(response)
                    new_state = "end"
                    return new_state, entities
        else:
            enrichment_info = helper.load_enrichment_general_info()
            response = ""
            for i in range(len(entities["enrich_target"])):
                if i != 0:
                    response += "\n\n"
                name = entities["enrich_target"][i]["value"]
                response += enrichment_info[name][4]
            print(response)
            new_state = "end"
            return new_state, entities

    # Process the queries related to specific information
    if "info_target" in entities:
        if contains("faculty", entities["info_target"]):
            response = response_generator.provide_faculty_recruitment()
            print(response)
            new_state = "end"
            return new_state, entities
        if contains("job", entities["info_target"]):
            new_state = "admission_job"
            return new_state, entities

    # Process the query of enrolling some course
    if "course" in entities or "honor_course" in entities:
        attributes, course_info = helper.load_course_information()
        if "course" not in entities:
            total_course = entities["honor_course"]
        elif "honor_course" not in entities:
            total_course = entities["course"]
        else:
            total_course = entities["course"] + entities["honor_course"]
        response = ""
        for i in range(len(total_course)):
            if i != 0:
                response += "\n"
            course_code = total_course[i]["value"]
            prerequisite = course_info[course_code][4]
            response += response_generator.provide_course_prerequisite(course_code, prerequisite)
        print(response)
        new_state = "end"
        return new_state, entities

    # Process the admission to specific program
    if "program" in entities:
        response = ""
        for i in range(len(entities["program"])):
            if i != 0:
                response += "\n"
            program = entities["program"][i]["value"]
            admission = helper.load_program_info()[program][2]
            response += admission
        print(response)
        new_state = "end"
        return new_state, entities
    new_state = "admission_general"
    return new_state, entities


def process_admission_general(entities):
    response = response_generator.query_job_student()
    print(response)
    job_or_student = input("")
    entity_list = helper.change_entity_list(get_entities(job_or_student))
    if "info_target" in entity_list:
        if contains("job", entity_list["info_target"]) or contains("title", entity_list["info_target"]):
            print(response_generator.query_job())
            new_state = "end"
            return new_state, entities
        else:
            print(response_generator.query_student())
            program_choice = input("")
            entities_list_original = get_entities(program_choice)
            entity_list_new = helper.change_entity_list(entities_list_original)
            if "program" in entity_list_new:
                response = ""
                for i in range(len(entity_list_new["program"])):
                    if i != 0:
                        response += "\n"
                    program = entity_list_new["program"][i]["value"]
                    admission = helper.load_program_info()[program][2]
                    response += admission
                print(response)
                new_state = "end"
                return new_state, entities
        return "end", entities
    print(response_generator.sorry())
    return "end", entities


def process_people_query_questions(entities):
    if "staff_name" in entities:
        staff_attributes, staff_info = helper.load_staff_information()
        response = ""
        for i in range(len(entities["staff_name"])):
            if i != 0:
                response += "\n"
            staff_name = entities["staff_name"][i]["value"].replace("\n", "")
            position = staff_info[staff_name][4].replace("\n", "").lower()
            staff_type = staff_info[staff_name][5].replace("\n", "")
            response += response_generator.provide_staff_people_info(staff_name, position, staff_type)
        print(response)
        new_state = "end"
        return new_state, entities
    if "research_area" in entities:
        response = ""
        area_faculty, faculty_area = helper.load_faculty_research_info()
        for i in range(len(entities["research_area"])):
            if i != 0:
                response += "\n"
            research_area = entities["research_area"][i]["value"]
            faculty_list = area_faculty[research_area]
            response += response_generator.provide_faculty_in_research_area(research_area, faculty_list)
        print(response)
        new_state = "end"
        return new_state, entities
    if "faculty_name" in entities:
        faculty_attributes, faculty_info = helper.load_faculty_information()
        response = ""
        for i in range(len(entities["faculty_name"])):
            if i != 0:
                response += "\n"
            name = entities["faculty_name"][i]["value"]
            response += faculty_info[name][6]
        print(response)
        new_state = "end"
        return new_state, entities
    if "info_target" in entities:
        if contains("head", entities["info_target"]):
            response = "The head of the department is Prof. Dit-Yan Yeung."
            print(response)
            new_state = "end"
            return new_state, entities
        if contains("ug coordinator", entities["info_target"]):
            response = "The coordinator for UG programs is Dr. Qiong Luo."
            print(response)
            new_state = "end"
            return new_state, entities
        if contains("pg coordinator", entities["info_target"]):
            response = "The coordinator for PG programs is Dr. Kai Chen."
            print(response)
            new_state = "end"
            return new_state, entities
        if contains("coordinator", entities["info_target"]):
            if "program" in entities:
                response = ""
                for i in range(len(entities["program"])):
                    if i != 0:
                        response += "\n"
                    program = entities["program"][i]["value"]
                    coordinator = helper.load_program_info()[4]
                    response += response_generator.provide_coordinator_info(program, coordinator)
                print(response)
                new_state = "end"
                return new_state, entities
            new_state = "query_coordinator"
            return new_state, entities
    new_state = "error"
    return new_state, entities


# Process the query of coordinator
def process_coordinator(entities):
    print("Which program do you want to know?")
    response_user = input("")
    entity_list = get_entities(response_user)["entities"]
    if "status" in entity_list:
        if contains("undergraduate", entity_list["status"]):
            response = "The coordinator for UG programs is Dr. Qiong Luo."
            print(response)
            new_state = "end"
            return new_state, entities
        if contains("postgraduate", entity_list["status"]):
            response = "The coordinator for PG programs is Dr. Kai Chen."
            print(response)
            new_state = "end"
            return new_state, entities
    if "program" in entity_list:
        program_info_matching = helper.load_program_info()
        response = ""
        for i in range(len(entity_list["program"])):
            if i != 0:
                response += "\n"
            program = entity_list["program"][i]["value"]
            coordinator = program_info_matching[program][4]
            response += response_generator.provide_coordinator_info(program, coordinator)
        print(response)
        new_state = "end"
        return new_state, entities
    response = response_generator.provide_general_coordinator_info()
    print(response)
    new_state = "end"
    return new_state, entities


def process_contact_query_questions(entities):
    if "staff_name" in entities:
        staff_attributes, staff_info = helper.load_staff_information()
        if "info_target" in entities:
            # Query about telephone number
            if contains("tel", entities["info_target"]):
                response = ""
                for i in range(len(entities["staff_name"])):
                    if i != 0:
                        response += "\n"
                    staff_name = entities["staff_name"][i]["value"]
                    try:
                        tel = str(int(staff_info[staff_name][2]))
                    except ValueError:
                        tel = "information not available"
                    response += response_generator.provide_staff_telephone_number(staff_name, tel)
                print(response)
            # Query about email
            if contains("email", entities["info_target"]):
                response = ""
                for i in range(len(entities["staff_name"])):
                    if i != 0:
                        response += "\n"
                    staff_name = entities["staff_name"][i]["value"]
                    email = str(staff_info[staff_name][1])
                    if "\\N" in email:
                        email = "information not available"
                    response += response_generator.provide_staff_email(staff_name, email)
                print(response)
            # Query about room number
            if contains("room number", entities["info_target"]):
                response = ""
                for i in range(len(entities["staff_name"])):
                    if i != 0:
                        response += "\n"
                    staff_name = entities["staff_name"][i]["value"]
                    try:
                        room_number = str(int(staff_info[staff_name][3]))
                    except ValueError:
                        room_number = "information not available"
                    response += response_generator.provide_staff_room(staff_name, room_number)
                print(response)
            # Query about website
            if contains("links", entities["info_target"]):
                response = ""
                for i in range(len(entities["staff_name"])):
                    if i != 0:
                        response += "\n"
                    staff_name = entities["staff_name"][i]["value"]
                    link = str(staff_info[staff_name][6])
                    if "\\N" in link:
                        link = "information not available"
                    response += response_generator.provide_staff_link(staff_name, link)
                print(response)
            new_state = "end"
            return new_state, entities
        else:
            response = ""
            for i in range(len(entities["staff_name"])):
                if i != 0:
                    response += "\n"
                staff_name = entities["staff_name"][i]["value"]
                # Get email
                email = str(staff_info[staff_name][1])
                if "\\N" in email:
                    email = "information not available"
                # Get telephone number
                try:
                    tel = str(int(staff_info[staff_name][2]))
                except ValueError:
                    tel = "information not available"
                # Get room number
                try:
                    room_number = str(int(staff_info[staff_name][3]))
                except ValueError:
                    room_number = "information not available"
                link = str(staff_info[staff_name][6])
                if "\\N" in link:
                    link = "information not available"
                response += response_generator.provide_staff_info(staff_name, email, tel, room_number, link)
            print(response)
            new_state = "end"
            return new_state, entities
    if "faculty_name" in entities:
        faculty_attributes, faculty_info = helper.load_faculty_information()
        if "info_target" in entities:
            # Query about telephone number
            if contains("tel", entities["info_target"]):
                response = ""
                for i in range(len(entities["faculty_name"])):
                    if i != 0:
                        response += "\n"
                    staff_name = entities["faculty_name"][i]["value"]
                    tel = faculty_info[staff_name][2]
                    if "\\N" in tel:
                        tel = "information not available"
                    response += response_generator.provide_faculty_tel(staff_name, tel)
                print(response)

            # Query about email
            if contains("email", entities["info_target"]):
                response = ""
                for i in range(len(entities["faculty_name"])):
                    if i != 0:
                        response += "\n"
                    staff_name = entities["faculty_name"][i]["value"]
                    email = str(faculty_info[staff_name][3])
                    if "\\N" in email:
                        email = "information not available"
                    response += response_generator.provide_faculty_email(staff_name, email)
                print(response)

            # Query about room number
            # Query about website is given to "get_access" intent
            if contains("room number", entities["info_target"]):
                response = ""
                for i in range(len(entities["faculty_name"])):
                    if i != 0:
                        response += "\n"
                    staff_name = entities["faculty_name"][i]["value"]
                    room_number = str(faculty_info[staff_name][4])
                    if "\\N" in room_number:
                        room_number = "information not available"
                    response += response_generator.provide_staff_room(staff_name, room_number)
                print(response)
            if contains("links", entities["info_target"]):
                response = ""
                for i in range(len(entities["faculty_name"])):
                    if i != 0:
                        response += "\n"
                    staff_name = entities["faculty_name"][i]["value"]
                    link = "http://www.cse.ust.hk/~"
                    link += faculty_info[staff_name][3].replace("@cse.ust.hk", "")
                    link += "/"
                    response += response_generator.provide_staff_link(staff_name, link)
                print(response)
        else:
            response = ""
            for i in range(len(entities["faculty_name"])):
                if i != 0:
                    response += "\n"
                staff_name = entities["faculty_name"][i]["value"]
                # Get email
                email = str(faculty_info[staff_name][3])
                if "\\N" in email:
                    email = "information not available"
                # Get telephone number
                try:
                    tel = str(faculty_info[staff_name][2])
                except ValueError:
                    tel = "information not available"
                # Get room number
                try:
                    room_number = str(faculty_info[staff_name][4])
                except ValueError:
                    room_number = "information not available"
                link = str(faculty_info[staff_name][7])
                if "\\N" in link:
                    link = "information not available"
                profile_link = str(faculty_info[staff_name][8])
                if "\\N" in profile_link:
                    profile_link = "information not available"
                scholar_link = str(faculty_info[staff_name][9])
                if "\\N" in scholar_link:
                    scholar_link = "information not available"
                response += provide_faculty_info(staff_name, email, tel, room_number, link, profile_link, scholar_link)
            print(response)
            new_state = "end"
            return new_state, entities
    if "department_name" in entities:
        response = response_generator.provide_dept_contact_info()
        print(response)
        new_state = "end"
        return new_state, entities
    new_state = "end"
    return new_state, entities


# Query about research area and interest
def process_info_query(entities):
    if "faculty_name" in entities:
        faculty_attributes, faculty_info = helper.load_faculty_information()
        if contains("research area", entities["info_target"]):
            response = ""
            for i in range(len(entities["faculty_name"])):
                if i != 0:
                    response += "\n"
                staff_name = entities["faculty_name"][i]["value"]
                research_area = str(faculty_info[staff_name][5])
                response += response_generator.provide_faculty_research_area(staff_name, research_area)
            print(response)
        if contains("research interest", entities["info_target"]):
            response = ""
            for i in range(len(entities["faculty_name"])):
                if i != 0:
                    response += "\n"
                staff_name = entities["faculty_name"][i]["value"]
                research_interest = str(faculty_info[staff_name][10])
                response += response_generator.provide_faculty_research_interest(staff_name, research_interest)
            print(response)
        if contains("title", entities["info_target"]) or contains("job", entities["info_target"]):
            response = ""
            for i in range(len(entities["faculty_name"])):
                if i != 0:
                    response += "\n"
                staff_name = entities["faculty_name"][i]["value"]
                title = str(faculty_info[staff_name][1])
                response += response_generator.provide_faculty_title(staff_name, title)
            print(response)
        new_state = "end"
        return new_state, entities
    if "staff_name" in entities:
        staff_attributes, staff_info = helper.load_staff_information()
        if helper.check_job(entities["info_target"]):
            response = ""
            for i in range(len(entities["staff_name"])):
                if i != 0:
                    response += "\n"
                staff_name = entities["staff_name"][i]["value"]
                position = str(staff_info[staff_name][4].replace("\n", ""))
                staff_type = str(staff_info[staff_name][5])
                response += response_generator.provide_staff_position(staff_name, position, staff_type)
            print(response)
            new_state = "end"
            return new_state, entities
    new_state = "error"
    return new_state, entities


def process_general(entities):
    response = "Hi! I am CSE chatbot. I could help you solving some questions related to HKUST CSE."
    print(response)
    new_state = "end"
    return new_state, entities


def ensure_quality_generation(entities):
    response = response_generator.provide_quality_ensuring()
    print(response)
    new_state = "end"
    return new_state, entities


def enrichment_query_answer(entities):
    response = response_generator.provide_enrichment_query()
    print(response)
    new_state = "end"
    return new_state, entities


# TODO: process the accessing webpages
def process_access_websites(entities):
    new_state = "end"
    return new_state, entities


# TODO: implement all possible links (list all possible website name in wit.ai)
# TODO: implement the websites
