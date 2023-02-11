import os


def run_in_terminal(command):
    os.system(f"gnome-terminal -e 'bash -c \"{command}; exec bash\"'")


commands = [
    "cd wrapper && cd frontend && python3 functions.py > log.txt",
    "cd wrapper && cd Server && ./a.out",
    "cd wrapper && cd pose_estimation && python3 pose_estimation.py",
]


for command in commands:
    run_in_terminal(command)
