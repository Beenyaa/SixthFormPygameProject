import scores_handler


class Player:

    def __init__(self):
        self.scoreboard = scores_handler.Scoreboard()  # instance of Scoreboard class
        self.name = ""  # empty string
        self.score = 0  # empty integer

    def save_playtime_info(self, name, score):
        # this method takes in the parameters name and score, they then get assigned to the self.name and self.score
        # attributes for temporary storage. After they have been stored under those attributes the method "send_playtime
        # _info" gets called.
        self.name = name
        self.score = score
        self.send_playtime_info()

    def send_playtime_info(self):
        # this method once again passes the name and score attributes onwards to the next location: "scores_handler.py"
        # python file's Scoreboard class, where these attributes are handled.
        self.scoreboard.update(self.name, self.score)
