""" Main module. """
import cocos
import Game

def main():
    """ Main function. """
    cocos.director.director.init()
    cocos.director.director.run(cocos.scene.Scene(Game.Game()))
    #game.run()

if __name__ == "__main__":
    # в каждом другом модуле будет так же проверка и запуск тестов.(в модуле теста для этого файла)
    main()
