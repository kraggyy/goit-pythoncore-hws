def input_error(func):
    def inner(command, text_to_add):
        if command not in list_of_commands:
            return "You entered wrong command"

        if (command == "hello" or command == "show all") and text_to_add[0] != '':
            return "You entered wrong command. Enter 'hello' or 'show all without any other text'"

        if command == "phone" and len(text_to_add)>1:
            return "You entered wrong command. Enter 'phone' and name of user"

        if (command == "add" or command == "change") and len(text_to_add)>2:
            return "You entered wrong command. Enter command, name and phone using 1 space"

        return func(command, text_to_add)
    return inner

def starting_answer(*text):
    return "How can i help you?"

def add_user(text):
    phonebook.append({"name": text[0].capitalize(), "phone": text[1]})
    return f"Added {text[0].capitalize()} with phone {text[1]}"

def change_phone_number(text):
    for user in phonebook:
        if user['name'] == text[0].capitalize():
            user['phone'] = text[1]
            return f'Number for {user["name"]} changed on {user["phone"]}'

def phone_number_return(text):
    for user in phonebook:
        if text[0].lower() == user['name'].lower():
            return f'{user["name"]}`s number is {user["phone"]}'
    return f'User not found'

def show_all(*text):
    return phonebook

@input_error
def chose_func(command, text_to_deal_with):
    return list_of_commands[command](text_to_deal_with)

phonebook = []

list_of_commands = {
        "hello": starting_answer,
        "add": add_user,
        "change": change_phone_number,
        "phone": phone_number_return,
        "show all": show_all,
    }

def main():
    # global phonebook
    while True:
        closing_words = ["good bye", "close", "exit"]
        input_text = input("Enter command:  ")
        main_command = ""
        text_to_deal_with = ""

        if input_text.lower() in closing_words:
            print('Good bye!')
            break

        for i in list_of_commands.keys():
            if input_text.lower().startswith(i):
                main_command = i
                text_to_deal_with = input_text.lower().removeprefix(i).strip().split(" ")
                # print(text_to_deal_with)
        # print(f"Command to do is: {main_command}")
        if main_command in closing_words:
            print(f'Good bye!')
            break
        else:
            print(chose_func(main_command, text_to_deal_with))

main()