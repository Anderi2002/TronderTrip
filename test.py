from datetime import datetime

print(".".join((str(datetime.now().date()).split("-")[::-1])))