from destination import Destination
import pickle
import json

with open("data/destinations.pickle", "rb") as file:
    destinations: list[Destination] = pickle.load(file)

# with open("data/destinations_info.txt", "w") as file:
#     for destination in destinations:
#         file.write(f"{destination.name}; https://www.google.com/maps/dir/Johan+Dybvads+veg,+Trondheim/{destination.name}\n")

with open("data/destinations_info.json", "w") as file:
    dictionary = {f"{destination.name}": \
    {"google_maps_link": f"https://www.google.com/maps/dir/Johan+Dybvads+veg,+Trondheim/{destination.name}", \
     "yr_link": None,
     "time_walk": None,
     "time_bike": None,
     "elevation": None,
     "distance": None
     } for destination in destinations}
    json.dump(dictionary, file, indent=4)