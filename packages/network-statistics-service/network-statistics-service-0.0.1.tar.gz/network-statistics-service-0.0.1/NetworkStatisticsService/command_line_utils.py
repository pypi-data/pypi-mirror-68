import subprocess


class CommandLineUtils(object):

    @staticmethod
    def run_bash_command(command):
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output, error
