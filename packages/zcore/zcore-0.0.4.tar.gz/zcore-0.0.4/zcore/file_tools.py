# encoding=utf-8
import glob


def read_file_by_line(fpath):
    with open(fpath) as file:
        for line in file:
            yield line


def read_file_by_matchpath(file_path):
    files = glob.glob(file_path)
    for file in files:
        yield file


def read_txtline_by_matchpath(file_path):
    files = glob.glob(file_path)
    for file in files:
        with open(file,encoding='utf8') as f:
            for line in f:
                yield line
