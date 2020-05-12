from entity_extraction import get_entities

if __name__ == "__main__":
    user_response = input("Hi, I am CSE chatbot. How can I help you?" + "\n")
    entities = get_entities(user_response)["entities"]
    print(entities)
