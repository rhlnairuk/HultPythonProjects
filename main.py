import random
from list_of_countries import COUNTRIES

countries = list(COUNTRIES.keys())
country_to_guess = random.choice(countries)

guess_the_capital = input(f"Guess the capital of {country_to_guess}: ")

if guess_the_capital.lower() == COUNTRIES[country_to_guess].lower():
    print(f"You are Correct! The capital is {COUNTRIES[country_to_guess]}")
else:
    print(f"Incorrect! the capital is {COUNTRIES[country_to_guess]}")
