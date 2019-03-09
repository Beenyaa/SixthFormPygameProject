
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Scoreboard:

    def __init__(self):
        # makes sure connection is made between the google spread sheet and the application:
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("gsheet_access.json", self.scope)
        self.client = gspread.authorize(self.creds)

        # opens the google spread sheet file to prepare it for editing
        self.sheet = self.client.open("Pinball Scoreboard").sheet1

        self.scoreboard_info = ""  # empty string

    def display(self):
        cell_list = self.sheet.range("A1:B6")

        for cell in cell_list:

            if cell.value == "":
                self.scoreboard_info += "-"

            else:
                self.scoreboard_info += str(cell.value)

            return self.scoreboard_info

    def update(self, name, score):
        # this method updates the google spread sheet:
        cell_list = self.sheet.range("A1:B36")  # a list of cells between the range of A1 (row 1 column 1) and B36 (row
        # 36 column 2)
        for counter, cell in enumerate(cell_list):

            if cell.value == "":
                self.sheet.update_cell(counter, 1, name)
                self.sheet.update_cell(counter, 2, score)
                break

            else:
                self.sheet.update_cell(counter, 1, name)
                self.sheet.update_cell(counter, 2, score)