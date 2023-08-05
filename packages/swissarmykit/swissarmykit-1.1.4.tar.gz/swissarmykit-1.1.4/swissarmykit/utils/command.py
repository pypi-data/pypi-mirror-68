import os

class Command:

    def __init__(self):
        pass

    @staticmethod
    def exec(command):
        os.system(command)
        print('INFO: Execute ', command)
        return command


if __name__ == '__main__':
    c = Command()
    # c.exec('mysqldump')
    c.exec('which mongodump')