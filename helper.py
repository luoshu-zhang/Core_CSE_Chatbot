import pandas as pd

mission_statement = "To prepare undergraduate and post-graduate " \
                    "students for productive careers in industry, " \
                    "academia, and government by providing an excellent " \
                    "environment for teaching, learning, and research in " \
                    "the theory and applications of computing and information " \
                    "technology. In particular, we aim:"

vision_statement = "To be a recognized leader in " \
                   "Computer Science and Engineering education and research:"

objective = "The academic objectives of the Department of Computer Science" \
            " and Engineering is to provide outstanding education and research programs that:"


def contains(target_intent, possible_entities):
    try:
        for i in range(len(possible_entities)):
            if possible_entities[i]["value"] == target_intent:
                return True
        return False
    except KeyError:
        return False


def load_course_information():
    file = pd.read_excel("data/course.xlsx")
    attributes = file.columns.ravel().tolist()
    id_number = file["Course_ID"].tolist()
    name = file["Course_Name"].tolist()
    credit_number = file["Course_Credits"].tolist()
    exclusion = file["Course_Exclusion"].tolist()
    prerequisite = file["Course_Prerequisite"].tolist()
    description = file["Course_Description"].tolist()
    course_info = {}
    for i in range(len(id_number)):
        course_info[id_number[i]] = \
            (id_number[i], name[i], credit_number[i], exclusion[i], prerequisite[i], description[i])
    return attributes, course_info


def load_faculty_information():
    file = pd.read_excel("data/faculty.xlsx")
    attributes = file.columns.ravel().tolist()
    name = file["Faculty_Name"]
    post = file["Faculty_Post"]
    tel = file["Faculty_Tel"]
    email = file["Faculty_Email"]
    room = file["Faculty_Room"]
    research_area = file["Faculty_Research_Area"]
    bio = file["Faculty_Biography"]
    web_page = file["Faculty_Personal_Webpage"]
    profile = file["Faculty_Faculty_Profile"]
    scholar_profile = file["Faculty_Scholar_Profile"]
    research_interest = file["Faculty_Research_Interest"]

    faculty_info = {}
    for i in range(len(name)):
        room_number = room[i].replace("\n", "")
        tel_number = tel[i].replace("\n", "")
        email_address = email[i].replace("\n", "")
        faculty_info[name[i]] = \
            (name[i], post[i], tel_number, email_address, room_number, research_area[i],
             bio[i], web_page[i], profile[i], scholar_profile[i], research_interest[i])
    return attributes, faculty_info


def load_staff_information():
    file = pd.read_excel("data/staff.xlsx")
    attributes = file.columns.ravel().tolist()
    name = file["Staff_Name"]
    email = file["Staff_Email"]
    extension = file["Staff_Extn"]
    room = file["Staff_Room"]
    position = file["Staff_Position"]
    staff_type = file["Staff_Type"]
    link = file["Staff_Further_Info_Link"]

    staff_info = {}
    for i in range(len(name)):
        staff_info[name[i]] = \
            (name[i], email[i], extension[i], room[i], position[i], staff_type[i], link[i])
    return attributes, staff_info


def load_research_area_info():
    subareas = pd.read_excel("data/link_ra_subarea.xlsx")
    name_table, attributes = load_research_area_full_name()
    area_set = set(subareas["RA_Short"])
    interest_area_link = {}
    area_interest_matching_table = {}
    for area in area_set:
        research_area_full = name_table[area]
        area_interest_matching_table[research_area_full] = []
    for i in range(len(subareas["Sub_Name"])):
        research_area_full = name_table[subareas["RA_Short"][i]]
        area_interest_matching_table[research_area_full].append(subareas["Sub_Name"][i])
        interest_area_link[subareas["Sub_Name"][i]] = research_area_full
    return area_interest_matching_table, interest_area_link


def load_research_area_full_name():
    research_areas = pd.read_excel("data/ResearchArea.xlsx")
    name_table = {}
    attribute_table = {}
    for i in range(len(research_areas["ResearchAreas_Short"])):
        name_table[research_areas["ResearchAreas_Short"][i]] = research_areas["ResearchAreas_Name"][i]
        attribute_table[research_areas["ResearchAreas_Name"][i]] = research_areas["ResearchAreas_Introduction"][i]
    return name_table, attribute_table


def load_faculty_research_info():
    area_interest, interest_area = load_research_area_info()
    faculty_area = pd.read_excel("data/link_subarea_faculty.xlsx")
    interest_set = set(faculty_area["Subareas_Name"])
    interest_faculty_matching = {}
    area_faculty_matching = {}
    for area in set(area_interest.keys()):
        area_faculty_matching[area] = []
    for interest in interest_set:
        interest_faculty_matching[interest] = []
    for i in range(len(faculty_area["Faculty_Name"])):
        interest_faculty_matching[faculty_area["Subareas_Name"][i]].append(faculty_area["Faculty_Name"][i])
    for area, interests in area_interest.items():
        for interest in interests:
            area_faculty_matching[area] += interest_faculty_matching[interest]
    for area in area_faculty_matching:
        area_faculty_matching[area] = list(set(area_faculty_matching[area]))
    return area_faculty_matching, interest_faculty_matching


def load_program_info():
    program_info = pd.read_excel("data/major.xlsx")
    minor_program_info = pd.read_excel("data/minor.xlsx")
    pg_program_info = pd.read_excel("data/pg_major.xlsx")
    program_info_matching = {}
    for i in range(len(program_info["Major_Name"])):
        link = program_info["Major_link"][i]
        overview = program_info["Major_Overview"][i]
        admission = program_info["Major_AdmissionRequirement"][i]
        admission_link = program_info["Major_AdmissionRequirement_links"][i]
        coordinator = program_info["Major_coordinator"][i]
        program_info_matching[program_info["Major_Name"][i]] = \
            (link, overview, admission, admission_link, coordinator)
    for i in range(len(pg_program_info["Pgmajor_Name"])):
        link = pg_program_info["Pgmajor_Website"][i]
        overview = pg_program_info["Pgmajor_Curriculum"][i]
        admission = pg_program_info["Pgmajor_AdmissionRequirement"][i]
        admission_link = pg_program_info["Pgmajor_Application"][i]
        coordinator = pg_program_info["Coordinator"][i]
        program_info_matching[pg_program_info["Pgmajor_Name"][i]] = \
            (link, overview, admission, admission_link, coordinator)
    for i in range(len(minor_program_info["Minor_Name"])):
        link = minor_program_info["Minor_Link"][i]
        overview = minor_program_info["program intro"][i]
        admission = minor_program_info["minor requirement"][i]
        admission_link = minor_program_info["minor requirement link"][i]
        coordinator = "Dr. Qiong Luo"
        program_info_matching[minor_program_info["Minor_Name"][i]] = \
            (link, overview, admission, admission_link, coordinator)
    return program_info_matching


def load_enrichment_general_info():
    general_file = pd.read_excel("data/enrichment.xlsx")
    enrich_info_matching = {}
    for i in range(len(general_file["Enrichment_Name"])):
        name = general_file["Enrichment_Name"][i]
        information = general_file["Enrichment_Intro"][i]
        outcome = general_file["Enrichment_IntendedLearningOutcomes"][i]
        link = general_file["Enrichment_Link"][i]
        admission = general_file["Admission"][i]
        enrich_info_matching[name] = (name, information, outcome, link, admission)
    return enrich_info_matching


def check_job(info_target):
    return contains("job", info_target) or contains("duty", info_target) or contains("title", info_target)


def change_entity_list(entity_list):
    intent = entity_list["intents"]
    new_intent = []
    for i in range(len(intent)):
        new_intent.append({})
        new_intent[i]["value"] = intent[i]["name"]
    new_entities = {"intent": new_intent}
    for key, value in entity_list["entities"].items():
        new_entities[value[0]["name"]] = []
        for i in range(len(value)):
            new_entities[value[0]["name"]].append(value[i])
    return new_entities
