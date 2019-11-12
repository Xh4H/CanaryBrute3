# CanaryBrute3
A simple script to brtueforce 64 bits binaries with python 3


# Introduction
I wanted to share with you a script made in Python 3 without pwntools (pwntools has a dev3 branch which supports python3).

The following script will bruteforce asynchronously the following addresses:

- Stack canary address
- EBP
- Return address

This has been built to bruteforce 64 bits binaries with the following details:

- The binary establishes a listener in certain address and port (localhost, 1337).
- The binary sends one single line and then expects user input.

Since this process is being done asynchronously, the needed time to extract these 3 addresses is reduced a lot compared to a single threaded-single task bruteforce.

# How to run
There are 3 global variables that need to be modified according to our needs.

**HOST** has to point to a valid and resolvable host, such as localhost, 10.10.10.10, etc.

**PORT** has to point to a valid port, such as 1337, 8006, 5050, etc.

**BUFFER_OVERFLOW_OFFSET** has to contain a numeric offset where the binary being bruteforced crashes by overflowing the buffer. If the binary crashes after 80 characters, this variable will contain that number.

Since this is made for python 3, please run it with `python3`. No command line arguments are required.
# Output
The script will output the latest tested payload, Canary, EBP and return address hexadecimal addresses and time needed to bruteforce:

![](https://posts.xh4h.com/assets/images/brute-1.png)
