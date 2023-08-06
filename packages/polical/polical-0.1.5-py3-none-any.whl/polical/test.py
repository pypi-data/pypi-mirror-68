from polical import TareasCSVToBD
from polical import SendTaskToTrello
import SimpleIcsToCSV
from polical import configuration
users = configuration.load_config_file("polical.yaml")
for user in users.keys():
    SimpleIcsToCSV.convertICStoCSV(users[user]['calendar_url'])
    TareasCSVToBD.LoadCSVTasktoDB(user, users[user])
    SendTaskToTrello.SendTaskToTrello(user, users[user])
