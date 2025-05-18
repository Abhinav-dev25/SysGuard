import ctypes
import os
import sys

lib = ctypes.CDLL("./libblocker.so")
lib.apply_seccomp.argtypes = [ctypes.c_char_p]
lib.apply_seccomp.restype = ctypes.c_int

def run_seccomp_command(cmd):
    if lib.apply_seccomp(b"policy.json") != 0:
        print("Failed to apply seccomp filters.")
        return
    os.execvp(cmd[0], cmd)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sandbox.py <command>")
        sys.exit(1)
    run_seccomp_command(sys.argv[1:])
