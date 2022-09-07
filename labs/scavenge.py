import os
import platform
from re import sub
import subprocess
import psutil 

from cloud_linux.secrets import vault
from cloud_linux.lab import test, ask as input

vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.scavenger')

debug = False 

@test.question
def kernel_version():
    """
    What is the full version of the Linux kernel running on this VM? 
    """
    exp = platform.uname().release
    if debug:
        print('DEBUG:', exp)
    assert input().strip() == exp, """Look for a version number."""

@test.question
def total_mem():
    """
    What is the total amount of memory on this VM (in KB)?
    """
    exp = int(psutil.virtual_memory().total / 1024)
    if debug:
        print('DEBUG:', exp)
    assert int(input()) == exp, """Remember the command that shows memory."""

@test.question
def distro():
    """
    What is the NAME of the Linux distribution on this VM? 
    """
    osname = subprocess.run(". /etc/os-release && echo $NAME", shell=True, stdout=subprocess.PIPE) \
            .stdout.decode('utf-8').strip().lower()
    if test.debug:
        print('DEBUG:', osname)
    got = input().strip().lower()
    assert got == osname, f"Look inside a file in /etc"
            
def main():
    hostname = platform.node()

    kernel_version(points=1)
    total_mem(points=1)
    distro(points=1)

    if test.score == test.total:
        test.print_success("Congratulations! You can now move to the next host in the scavenger hunt!")
        if hostname == 'opus':
            print("The next host is named 'voyager.scavenger.cis-90.net'")
        elif hostname == 'voyager':
            print("The next host is named 'enterprise.scavenger.cis-90.net'")
        elif hostname == 'enterprise':
            print("The next host is named 'excelsior.scavenger.cis-90.net'")
        elif hostname == 'excelsior':
            print("The next host is named 'reliant.scavenger.cis-90.net'")
        elif hostname == 'reliant':
            print("You have reached the last host!")
        else:
            print("I don't recognize this host")
        print("Your confirmation code is:", vault.confirmation({'score': test.score}))
    else:
        test.print_error("Please try again until you get all of the questions right.")


if __name__ == '__main__':
    main()

