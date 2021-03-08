import requests

#https://opentdb.com/api.php?amount=5&type=boolean


class Player():
    def __init__(self, name):
        self.name = name

    score = 0

    def getName(self):
        return self.name

    def newName(self, new):
        self.name = new

    def giveScore(self):
        self.score += 1

    def getScore(self):
        return self.score

class Data():

    GameData = {}

    def createData(self):
        response = requests.get('https://opentdb.com/api.php?amount=5&type=boolean')  # in response is plain text

        data = response.json()  # this will convert plain text to array of json objects
        self.GameData = data

    def getData(self):
        return self.GameData

class Ui:

    def askForName(self, player: Player):
        while True:
            try:
                return str(input("What is your name {0}? ".format(player.getName())))
            except:
                continue

    def questionToPlayer(self, player: Player, gamedata, round):
        print(gamedata['results'][round]['question'])
        while True:
            try:
                choice = input("Is your answer True or False {0}?".format(player.getName()))
                return choice
            except:
                continue
    def reaction(self, result):
        if result:
            print("That is Correct. Amazing")
        else:
            print("That is NOT Correct :(")

    def congratuletWinner(self, player: Player):
        print("That is all {0}. You finished with {1} correct answers. Good Game!".format(player.getName(),player.getScore()))

class Game:
    def __init__(self):
        self.data: Data = Data()
        self.ui: Ui = Ui()
        self.player1: Player = Player("Player1")

    def startGame(self):
        self.data.createData()
        gamedata = self.data.getData()
        print(self.data.getData())
        self.player1.newName(self.ui.askForName(self.player1))
        round  = 0
        while True:
            choice1 = self.ui.questionToPlayer(self.player1, gamedata, round)
            answer = gamedata['results'][round]['correct_answer']
            if answer == choice1:
                result = True
                self.player1.giveScore()
                self.ui.reaction(result)
            else:
                result = False
                self.ui.reaction(result)
                pass
            if round == 4:
                self.ui.congratuletWinner(self.player1)
                break
            else:
                round += 1
                continue


game = Game()
game.startGame()





