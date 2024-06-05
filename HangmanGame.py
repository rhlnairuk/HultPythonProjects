import random

words = ["prosperity", "ant", "Electricity"]

def get_input_from_user(input_char_list):
    char_input = input(f"(Guess) Enter a letter in word {''.join(input_char_list)} ")
    if len(char_input) != 1:
        char_input = input(f"(Guess) Enter *Only* a single letter in word {''.join(input_char_list)} ")
        return char_input
    else:
        return char_input

def check_input(user_input, word_list, input_char_list):
    if user_input in word_list:
        if user_input in input_char_list:
            print(f"{user_input} is already in the word")
            return False
        else:
            char_idx = [i for i in range(len(word_list)) if word_list[i] == user_input]
            for idx in char_idx:
                input_char_list[idx] = user_input
    else:
        print(f"{user_input} is not in the word")
        return False

def main():
    word = random.choice(words)
    word = word.lower()
    word_list = list(word)
    misses = 0
    input_char_list = [ "*" for i in range(len(word_list)) ]
    while input_char_list != word_list:
        user_input=get_input_from_user(input_char_list)
        if not check_input(user_input, word_list, input_char_list):
            misses += 1
    print(f"The word is {word}. You missed {misses} time")



if __name__ == "__main__":
    main()