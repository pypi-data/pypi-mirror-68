import time
import sys
import tomlkit


def tail_f(file_obj, interval=0.1):
    interval = 1.0

    while True:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(interval)
            file.seek(where)
        else:
            yield line


def main():
    ...


if __name__ == '__main__':
    sys.exit(main())
