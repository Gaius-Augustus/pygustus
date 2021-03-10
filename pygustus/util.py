import subprocess


def execute_bin(cmd, options):
    # execute given binary with given options
    process = subprocess.Popen(
        [cmd] + options, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    output = process.stdout.read()
    error = process.stderr.read()
    print(output)
    print(error)
