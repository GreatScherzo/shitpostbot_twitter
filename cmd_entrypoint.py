from cmd import Cmd
import sys
from main import *



class CommandClass(Cmd):
    def do_run(*args):
        """
        Run the bot
        :param args:
        :return:
        """
        entrypoint()

    def do_export(*args):
        """Help text for export"""
        print('Exporting')

    def do_exit(*args):
        return -1


if __name__ == '__main__':
    c = CommandClass()
    command = ' '.join(sys.argv[1:])
    if command:
        sys.exit(c.onecmd(command))
    c.cmdloop()
