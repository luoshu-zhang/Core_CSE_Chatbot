import helper


def greeting():
    response = "I am CSE chatbot. I can help you with the problems about CSE department."
    return response


def give_basic_info(info, info_body):
    response = "The " + info + " of HKUST CSE is: " + "\n"
    response += info_body
    return response


# TODO： provide mission information


# provide general coordinator info
def provide_general_coordinator_info():
    program_info = helper.load_program_info()
    response = "I am sorry that I may not understand what you said. "
    response += "But here are some general news about the coordinator in different programs.\n\n"
    response += "The coordinator for UG programs is Dr. Qiong Luo.\n"
    response += "The coordinator for PG programs is Dr. Kai Chen.\n\n"
    response += "The coordinator for each program is:\n"
    index = 0
    for program in program_info:
        if index != 0:
            response += "\n"
        coordinator = program_info[program][4]
        response += provide_coordinator_info(program, coordinator)
        index += 1
    return response


# Staff related info
def provide_staff_telephone_number(name, number):
    response = ""
    if number == "information not available":
        response += "The telephone number of " + name + " is not available."
    else:
        response += "The telephone number of " + name + " is: "
        response += "(852) 2358 " + str(number)
    return response


# Staff related info
def provide_staff_email(name, address):
    response = "The email of " + name + " is: "
    response += address + "@cse.ust.hk"
    return response


# Staff related info
def provide_staff_room(name, room_number):
    response = "The room number of " + name + " is: "
    response += str(room_number)
    return response


# Staff related info
def provide_staff_link(name, link_number):
    response = "The personal web of " + name + " is: "
    response += str(link_number)
    return response


# Staff complete info
def provide_staff_info(name, email, tel, room_no, link):
    response = "The complete set of information of " + name + " is:\n"
    response += provide_staff_email(name, email) + "\n"
    response += provide_staff_telephone_number(name, tel) + "\n"
    response += provide_staff_room(name, room_no) + "\n"
    response += provide_staff_link(name, link) + "\n"
    return response


# Staff position info
def provide_staff_position(name, position, type_staff):
    response = "The position of " + name + " is: "
    response += position + ", "
    response += "under the category of " + type_staff
    return response


# Faculty related info
def provide_faculty_email(name, address):
    response = "The email of " + name + " is: "
    response += address
    return response


# Faculty related info
def provide_faculty_title(name, title):
    response = "The title of " + name + " is: "
    response += title
    return response


# Faculty related info
def provide_faculty_research_area(name, title):
    response = "The research area of " + name + " is: "
    response += title
    return response


# Faculty related info
def provide_faculty_research_interest(name, title):
    response = "The research interest of " + name + " is: "
    response += title
    return response


# Faculty related info
def provide_faculty_tel(name, number):
    response = "The telephone number of " + name + " is: "
    response += str(number)
    return response


# Faculty related info
def provide_faculty_profile(name, link):
    response = "The faculty profile page of " + name
    response += " is " + str(link)
    return response


# Faculty related info
def provide_faculty_scholar_profile(name, link):
    response = "The faculty scholar profile page of " + name
    response += " is " + str(link)
    return response


# Faculty complete info
def provide_faculty_info(name, email, tel, room_no, link, profile_link, scholar_link):
    response = "The complete information of " + name + " is listed as:\n"
    response += provide_faculty_email(name, email) + "\n"
    response += provide_faculty_tel(name, tel) + "\n"
    response += provide_staff_room(name, room_no) + "\n"
    response += provide_staff_link(name, link) + "\n"
    response += provide_faculty_profile(name, profile_link) + "\n"
    response += provide_faculty_scholar_profile(name, scholar_link)
    return response


# Department contact info
def provide_dept_contact_info():
    response = "The complete information of HKUST CSE is listed as:\n"
    response += "Address: Room 3528 (Lift 25-26)\n"
    response += "Department of Computer Science and Engineering\n"
    response += "The Hong Kong University of Science and Technology\n"
    response += "Clear Water Bay, Kowloon\n"
    response += "Hong Kong\n\n"

    response += "Email: csdept@cse.ust.hk\n"
    response += "Tel: (852) 2358 7000\n"
    response += "Fax: (852) 2358 1477\n"
    return response


# The basic information about the course
def provide_course_info(code, name, credit, exclusion, prerequisite, description):
    response = "The name of " + code + " is " + name + ".\n"
    if type(credit) == int:
        response += "The credit number is " + str(int(credit)) + ".\n"
    if "\\N" not in exclusion:
        response += "It has an exclusion of " + exclusion + ". "
    if "\\N" not in prerequisite:
        response += "Also, it has a prerequisite of " + prerequisite + ".\n"
    if "\\N" not in description:
        response += "A brief description of the course: " + "\n"
        response += description
    return response


# Provide information of course
def provide_course_info_by_table(code, information_table):
    try:
        course_information_list = information_table[code]
    except KeyError:
        response = "Cannot find course name. Please enter another question."
        return response
    course_name = course_information_list[1]
    course_credit = course_information_list[2]
    exclusion = course_information_list[3]
    prerequisite = course_information_list[4]
    description = course_information_list[5]
    response = provide_course_info(code, course_name, course_credit, exclusion, prerequisite, description)
    return response


# The basic information about the CSE department
def provide_basic_dept_info():
    response = "Computer science is the discipline that studies the structure, function, and applications " \
               "of computers as well as the interconnection of computers. Covering topics in the areas of " \
               "foundations of computer science and computer engineering, artificial intelligence, networking, " \
               "computer graphics, multimedia computing, software and web technologies, and data and knowledge-base " \
               "systems, the Computer Science programs at this University are dedicated to educate students and to " \
               "advance research in computer and information technology; as well as to assist in the development and " \
               "growth of the information industry in the region." + "\n\n"
    response += "Through the efforts of researchers and engineers, computers have evolved from large, slow, " \
                "expensive, and very specialized systems to small, fast, affordable, and ordinary tools that are " \
                "part of virtually everyone's life. Advances in networking technologies and human-computer " \
                "interfacing " \
                "technologies have further created a digital culture. The ubiquitous nature of computers in today's " \
                "workplace and home environment is making computer literacy a requirement not only for all " \
                "professionals in industrial societies but also for everybody living in the digital culture." + "\n\n"
    response += "Computer Science is still a young field. Although we have witnessed numerous advances in the past, " \
                "this is only the beginning of a new revolution as the potential of information technology has not " \
                "yet been fully realized. Information technology is in the midst of a revolution as we move from " \
                "explicit interactions with disconnected computing devices to implicit and pervasive interactions " \
                "with highly interconnected, integrated digital resources embedded in the environments in which we " \
                "work, live, learn, and play. The impact of computer science and information engineering will be " \
                "broad and deep. Computer Science programs at HKUST prepare students for exciting challenges and " \
                "new opportunities that help to bring such impact to our lives." + "\n\n"
    response += "The Department offers a full range of courses to meet the needs of its own students and those from " \
                "other departments. Its programs lead to the BEng, BSc, MSc, MPhil, and PhD degrees. Aside from " \
                "taking computer science courses, students are encouraged to design individual study plans tailored " \
                "to their own interests."
    return response


# provide staff information (get the information of staff)
def provide_staff_people_info(name, position, staff_type):
    response = ""
    if position[0] not in ["a", "e", "i", "o", "u"]:
        response += name + " is a " + position + " in CSE department, belonging to the category of "
    else:
        response += name + " is an " + position + " in CSE department, belonging to the category of "
    response += staff_type
    return response


# provide the list of faculty based on the research area
def provide_faculty_in_research_area(area, faculties):
    response = "The following faculties are conducting research on " + area + ": "
    for i in range(len(faculties)):
        if i != len(faculties) - 1:
            response += faculties[i] + ", "
        else:
            response += faculties[i] + "."
    return response


# provide coordinator information
def provide_coordinator_info(program, coordinator):
    response = "The coordinator of " + program + " is " + coordinator + "."
    return response


# provide information of faculty recruitment
def provide_faculty_recruitment():
    response = "The Department of Computer Science and Engineering of HKUST (https://www.cse.ust.hk/) is inviting " \
               "applications for substantiation-track faculty openings at all levels of Professor, " \
               "Associate Professor and Assistant Professor for the 2020-2021 academic year."
    response += "Detailed information can be found in https://www.cse.ust.hk/admin/recruitment/faculty/."
    return response


# provide information of course prerequisite
def provide_course_prerequisite(course_code, prerequisite):
    if "\\N" not in prerequisite:
        response = "The course of " + course_code + " has a prerequisite of " + prerequisite + "."
        return response
    response = "There is no prerequisite for " + course_code + ". Feel free to enroll in this course."
    return response


# provide inbound exchange information
def provide_inbound_exchange():
    response = "Exchange students can apply by following the steps below.\n"
    response += "Step 1: Nomination by home institution;\n"
    response += "Step 2: HKUST application;\n"
    response += "Step 3: Post-application procedures.\n"
    response += "Detailed information can be found at: https://studyabroad.ust.hk/inbound"
    return response


# provide outbound exchange information
def provide_outbound_exchange():
    response = "Exchange students can apply by following the steps below.\n"
    response += "Step 1: Nomination by HKUST;\n"
    response += "Step 2: Target institution application;\n"
    response += "Step 3: Post-application procedures.\n"
    response += "Detailed information can be found at: https://studyabroad.ust.hk/outbound"
    return response


def provide_inbound_outbound_exchange():
    response = "I am sorry that I may not get your idea. Here are some related information for exchange programs.\n\n"
    response += provide_outbound_exchange()
    response += "\n\n"
    response += provide_inbound_exchange()
    return response


# ask questions about inbound or outbound
def query_in_out():
    response = "Do you want to query the inbound exchange (exchange-in) or outbound exchange (exchange-out)?"
    response += "\n"
    response += "<>Inbound Exchange"
    response += "\n"
    response += "<>Outbound Exchange"
    return response


# ask questions about job or student
def query_job_student():
    response = "Are you a student or a job seeker?\n"
    response += "<>Student\n"
    response += "<>Job seeker"
    return response


# ask questions about jobs
def query_job():
    response = "Do you want to apply for a faculty position or an ordinary staff?"
    response += "<>Faculty position\n"
    response += "<>Ordinary staff\n"
    return response


# ask questions about student
def query_student():
    response = "Which program do you want to participate?\n"
    response += "Here are some possible choices:\n"
    response += "<>BEng in Computer Science (COMP)\n"
    response += "<>BEng in Computer Engineering (CPEG)\n"
    response += "<>BSc in Data Science and Technology (DSCT)\n"
    response += "<>BSc in Risk Management and Business Intelligence (RMBI)\n"
    response += "<>Master of Science (MSc) Program in Big Data Technology\n"
    response += "<>Master of Science (MSc) Program in Information Technology\n"
    response += "<>Minor Program in Information Technology\n"
    response += "<>Minor Program in Big Data Technology\n"
    response += "<>Master of Philosophy in Computer Science and Engineering\n"
    response += "<>Doctor of Philosophy in Computer Science and Engineering\n"
    return response


# provide answers when the chat-bot is not able to answer the question
def sorry():
    response = "Sorry I can't help you. Please try a different one."
    return response
