#!/usr/local/bin/python3
__author__ = 'raccoon'

import os
import sys

from clint.arguments import Args
from clint.textui import puts, colored, indent


class WarcRecord:
    warc_version = ""
    warc_record_id = ""
    warc_type = ""
    warc_date = ""
    warc_target_uri = ""
    content_length = 0
    content = ""

    def __int__(self):
        return


def printHelp():
    print("Usage:")
    print(__file__ + "COMMAND WARC_file [ARGS]")
    print("\nARGS:")
    print(" WARC_file: warc file path")
    print("\nCOMMAND: ")
    print(" list\tList all record in warc file.")
    print(" \tUsage:")
    print(" \t " + __file__ + " list WARC_FILE [ARGS]")
    print(" \tARGS:")
    print(" \t -o number: offset record.")
    print(" \t -c number: show that how much record")
    print(" \t Example:")
    print(" \t  " + __file__ + " list sample.warc 10 10")
    print(" \t ")
    print(" dump\tDump record's content to respective file.")
    print(" \tUsage:")
    print(" \t " + __file__ + " dump WARC_FILE DEST_DIR [ARGS]")
    print("")
    print(" \tARGS:")
    print(" \t DEST_DIR: destination directory.")
    print(" \t -o number: offset record.")
    print(" \t -c number: show that how much record")
    print(" \t Example:")
    print(" \t  " + __file__ + " list sample.warc out 10 10")
    print(" \t ")
    print(" help\tShow this help.")


def getSize(_fn):
    return os.stat(_fn).st_size


def saveToHtml(_content, _filename):
    '''

    :param _content: string
    :param _filename: str
    :return:
    '''
    while True:
        # for i in range(1):
        _sp = _content.split('\n', 1)
        _content = _sp[1]
        if _sp[0].split(':')[0] == "Content-Length":
            _content = _content.split('\n', 1)[1]
            break
    f2 = open(_filename, 'w')
    f2.write(_content)
    f2.close()


def fetch(_f):
    _warcRecord = WarcRecord()
    while True:
        l1 = _f.readline().decode('ISO-8859-1')
        if l1[0] == 'W':
            break
    warc_version = l1[:-1]  # remove \n and get version

    _warcRecord.warc_version = warc_version
    warc_header = {}
    while True:
        tmp = _f.readline()[:-1].decode('ISO-8859-1').split(":", 1)
        # print(tmp)
        try:
            warc_header[tmp[0].strip()] = tmp[1].strip()
        except UnicodeDecodeError:
            continue

        if tmp[0] == "WARC-Type":
            _warcRecord.warc_type = tmp[1].strip()
        elif tmp[0] == "WARC-Date":
            _warcRecord.warc_date = tmp[1].strip()
        elif tmp[0] == "WARC-Record-ID":
            _warcRecord.warc_record_id = tmp[1].strip()
        elif tmp[0] == "Content-Length":
            _warcRecord.content_length = int(tmp[1].strip())
        elif tmp[0] == "WARC-Target-URI":
            _warcRecord.warc_target_uri = tmp[1].strip()
        else:
            warc_header[tmp[0]] = tmp[1].strip()

        if tmp[0] == 'Content-Length':
            _f.read(1)
            content = _f.read(int(tmp[1])).decode('ISO-8859-1')
            _warcRecord.content = content
            if warc_header['Content-Type'] == 'application/http;msgtype=response':
                saveToHtml(_warcRecord.content, _warcRecord.warc_record_id.split(':')[2][:-1] + ".html")
            return _warcRecord


def listwarc(_filename):
    f = open(_filename, 'rb')
    filesize = getSize(filename)
    count = 1
    print("ID\tWARC-Version\tRecord-ID\t\t\t\t\tWARC-Type\tWARC-Date\t\t\tContent-Length\tTarget-URI")
    # while True:
    for i in range(3):
        wr = fetch(f)
        print('{0:d}\t{1}\t{2:<40}\t{3}\t{4}\t{5:14}\t{6}'.format(count, wr.warc_version, wr.warc_record_id,
                                                                  wr.warc_type, wr.warc_date,
                                                                  wr.content_length,
                                                                  wr.warc_target_uri))
        count += 1
        if filesize == f.tell():
            break


if __name__ == "__main__":
    args = Args()
    try:
        offset = int(args.grouped['-o'].get(0))
    except KeyError:
        offset = 0
    except:
        puts(colored.red("Error: -o must be number"))
        quit()
    try:
        count = int(args.grouped['-c'].get(0))
    except KeyError:
        count = 0
    except:
        puts(colored.red("Error: -c must be number"))
        quit()

    if args.get(0).lower() == 'list':
        print('list', offset, count)
    elif args.get(0).lower() == 'dump':
        print('dump', offset, count)
    else:
        printHelp()