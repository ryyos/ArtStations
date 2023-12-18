from libs import Parser

class Main:
    def __init__(self) -> None:
        self.__parser = Parser()
        pass

    def main(self):
        # self.__parser.extract_data(search="anime", page=1)
        self.__parser.curl()

if __name__ == '__main__':
    main = Main()
    main.main()