import random
from list_of_countries import COUNTRIES

countries = list(COUNTRIES.keys())
country_to_guess = random.choice(countries)

print(country_to_guess)
