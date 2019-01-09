import csv
import os.path

e_london_postcodes = [f"E{n}" for n in range(1, 21)]
n_london_postcodes = [f"N{n}" for n in range(1, 23)]
w_london_postcodes = [f"W{n}" for n in range(1, 15)]
nw_london_postcodes = [f"NW{n}" for n in range(1, 12)]
se_london_postcodes = [f"SE{n}" for n in range(1, 29)]
sw_london_postcodes = [f"SW{n}" for n in range(1, 21)]

LONDON_POSTCODES = (
    e_london_postcodes
    + n_london_postcodes
    + w_london_postcodes
    + nw_london_postcodes
    + se_london_postcodes
    + sw_london_postcodes
)

my_path = os.path.abspath(os.path.dirname(__file__))
POSTCODE_CSV = os.path.join(my_path, "../csv/je_postcode_slugs.csv")
MENU_CSV = os.path.join(my_path, "../csv/je_menu_slugs.csv")

JUSTEAT_URL = "https://www.just-eat.co.uk/"
