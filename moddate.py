#! /usr/bin/python
# -*-coding:utf-8-*-

from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time

# from Tkinter import *
# from tkFileDialog import askdirectory
from PIL import Image
from PIL.ExifTags import TAGS
import piexif

import sys
import os
import re
import datetime
# import logging
import logging.handlers

"""
Change create date and rename the file names within the same directory to order easily
(1) Changes create, modify, access date to the file name or exif DateTimeOriginal
(2) Changes the file name to exif DateTimeOriginal
(3) Changes the file name to formated date
Usage:
moddate.exe <argument>
(1) help: show this descripton
(2) <nothing>: change each file on selection
(3) -f: change all files to the file name
(4) -e: change all files to exif date
"""

def dump_image(input_file, date_time_original):
    exif_dic = piexif.load(input_file)
    exif_dic['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_time_original  #u"2099:09:29 10:10:10"
    exif_bytes = piexif.dump(exif_dic)
    piexif.insert(exif_bytes, input_file)


def get_exif(fn):
    img = Image.open(fn)
    info = img._getexif()
    ret = None
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if decoded == 'DateTimeOriginal':
            return value
    if ret is None:
        ret = "00000000000000"
    return ret


def show_exif(fn):
    img = Image.open(fn)
    info = img._getexif()
    ret = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
        # print decoded, value
    # print ret


def get_format_date(raw_num="00000000000000"):
    naked_num = re.findall('\d+', raw_num)
    con_num = "".join(naked_num)
    if len(con_num) < 15:
        raw_date = "{0:0<14}".format(con_num)
    elif len(con_num) >= 15:
        raw_date = con_num[0:14]
    year = raw_date[0:4]
    month = raw_date[4:6]
    date = raw_date[6:8]
    hour = raw_date[8:10]
    mi = raw_date[10:12]
    se = raw_date[12:14]
    str_date = year + "-" + month + "-" + date + " " + hour + ":" + mi + ":" + se
    con_date = year + month + date + "_" + hour + mi + se
    return str_date, con_date


if __name__ == "__main__":
    try:
        option = ""
        if len(sys.argv) == 1:
            is_go = raw_input("Do you want to change file name and date? (Y or N)")
            if is_go.upper() == "Y":
                option = "each"
            else:
                print "Process canceled"
                sys.exit()
        elif len(sys.argv) == 2:
            if str(sys.argv[1]).upper() == "HELP":
                print "\nChange create date and rename the file names within the same directory to order easily\n" \
                        "(1) Changes create, modify, access date to the file name or exif DateTimeOriginal\n" \
                        "(2) Changes the file name to exif DateTimeOriginal\n" \
                        "(3) Changes the file name to formated date\n\n" \
                        "Usage:\n" \
                        "moddate.exe <argument>\n" \
                        "(1) help: show this descripton\n" \
                        "(2) <nothing>: change each file on selection\n" \
                        "(3) -f: change all files to the file name\n" \
                        "(4) -e: change all files to exif date\n"
                sys.exit()
            elif str(sys.argv[1]).upper() == "-F":
                is_go = raw_input("Do you want to change all files name and all date to file name? (Y or N)")
                if is_go.upper() == "Y":
                    option = "file"
                else:
                    print "Process canceled"
                    sys.exit()
            elif str(sys.argv[1]).upper() == "-E":
                is_go = raw_input("Do you want to change all files name and all date to exif date? (Y or N)")
                if is_go.upper() == "Y":
                    option = "exif"
                else:
                    print "Process canceled"
                    sys.exit()
            else:
                print "wrong arbuments"
                sys.exit()
        else:
            print "too many arguments"
            sys.exit()
        # top = Tk()
        # F = Frame(top)
        # F.pack(expand="true")
        # path = askdirectory(title="select directory", mustexist=1)

        # logger 인스턴스를 생성 및 로그 레벨 설정
        logger = logging.getLogger("crumbs")
        logger.setLevel(logging.DEBUG)

        # formmater 생성
        formatter = logging.Formatter('[%(levelname)s| %(asctime)s > %(message)s')

        # fileHandler와 StreamHandler를 생성
        file_handler = logging.FileHandler('modall.log')
        # streamHandler = logging.StreamHandler()

        # handler에 fommater 세팅
        file_handler.setFormatter(formatter)
        # streamHandler.setFormatter(formatter)

        # Handler를 logging에 추가
        logger.addHandler(file_handler)
        # logger.addHandler(streamHandler)

        # path = "C:/Users/shyang/.virtualenvs/projects/moddate/new"
        path = "./."
        allowed_file = ['.JPG', '.MP4', '.WMV']
        # retreive files from selected directory
        for f in os.listdir(path):
            ignore = "N"
            log_msg = ""
            log_level = "info"
            f_name = os.path.splitext(f)[0]
            f_ext = os.path.splitext(f)[1]
            f_file = f
            f_path = os.path.join(path, f_file)
            # if they are file type
            if os.path.isfile(os.path.join(path, f_file)):
                # if they are media file type
                if allowed_file.count(f_ext.upper()) > 0:
                    # exif_date = ""
                    f_str_date, f_name_new = get_format_date(f_name)
                    print
                    print "File Name: %s" % f_file
                    print "File Date : %s (YYYY-MM-DD HH:Mi:SS)" % (f_str_date)
                    log_msg += "\n" \
                               "File Name: %s\n" \
                               "File Date: %s (YYYY-MM-DD HH:Mi:SS)\n" % (f_file, f_str_date)
                    # if they are jpg format type
                    date_src = ""
                    if f_ext.upper() == ".JPG":
                        exif_date = get_exif(os.path.join(path, f_file))
                        e_str_date, e_name_new = get_format_date(exif_date)
                        f_file_new = f_name_new + f_ext
                        # if they have different date between file date and exif date
                        if f_name_new != e_name_new:
                            print "EXIF Date: %s (YYYY-MM-DD HH:Mi:SS)\n" % (e_str_date)
                            log_msg += "EXIF Date: %s (YYYY-MM-DD HH:Mi:SS)\n" % (e_str_date)
                            num = "0"
                            # select which one you want to change with
                            if option == "each":
                                while True:
                                    num = raw_input("Which would you like to change with? "
                                                    "(1: File Name, 2: EXIF, 3: Ignore)")
                                    if num != "1" and num != "2" and num != "3":
                                        continue
                                    if num == "1":
                                        date_src = "file"
                                        break
                                    elif num == "2":
                                        f_str_date = e_str_date
                                        f_name_new = e_name_new
                                        date_src = "exif"
                                        break
                                    elif num == "3":
                                        ignore = "Y"
                                        break
                            elif option == "file":
                                date_src = "file"
                            elif option == "exif":
                                f_str_date = e_str_date
                                f_name_new = e_name_new
                                date_src = "exif"
                    # if you want to ignore this process at this file....
                    if ignore == "Y":
                        print "ignore"
                        log_msg += "process ignored\n"
                        logger.info(log_msg)
                        continue
                    f_name_naked = "".join(re.findall('\d+', f_name_new))
                    if len(f_name_naked) < 12:
                        pass
                    elif 12 <= len(f_name_naked) < 15:
                        f_raw_date = "{0:0<14}".format(f_name_naked)
                    elif len(f_name_naked) >= 15:
                        f_raw_date = f_name_naked[0:14]
                    f_year = f_raw_date[0:4]
                    f_month = f_raw_date[4:6]
                    f_date = f_raw_date[6:8]
                    f_hour = f_raw_date[8:10]
                    f_min = f_raw_date[10:12]
                    f_sec = f_raw_date[12:14]
                    f_file_new = f_year + f_month + f_date + "_" + f_hour + f_min + f_sec + f_ext

                    # get arguments
                    cre_date = f_str_date  # create
                    mod_date = f_str_date  # modify
                    acc_date = f_str_date  # access

                    # specify time format
                    date_format = "%Y-%m-%d %H:%M:%S"
                    offset = 0  # in seconds

                    try:
                        # create struct_time object
                        cre_date_t = time.localtime(time.mktime(time.strptime(cre_date, date_format)) + offset)
                        mod_date_t = time.localtime(time.mktime(time.strptime(mod_date, date_format)) + offset)
                        acc_date_t = time.localtime(time.mktime(time.strptime(acc_date, date_format)) + offset)

                        # visually check if conversion was ok
                        # print "Create  : %s --> %s OK" % (cre_date, time.strftime(date_format, cre_date_t))
                        # print "Modify  : %s --> %s OK" % (mod_date, time.strftime(date_format, mod_date_t))
                        # print "Access  : %s --> %s OK" % (acc_date, time.strftime(date_format, acc_date_t))
                        # print

                        # change timestamp of file
                        fh = CreateFile(os.path.join(path, f_file), GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
                        cre_time, acc_time, mod_time = GetFileTime(fh)

                        # print "Change Create from", cre_time, "to %s" % (time.strftime(date_format, cre_date_t))
                        # print "Change Modify from", mod_time, "to %s" % (time.strftime(date_format, mod_date_t))
                        # print "Change Access from", acc_time, "to %s" % (time.strftime(date_format, acc_date_t))
                        log_msg += "Change Create from %s to %s\n" % (cre_time, time.strftime(date_format, cre_date_t))
                        log_msg += "Change Modify from %s to %s\n" % (mod_time, time.strftime(date_format, mod_date_t))
                        log_msg += "Change Access from %s to %s\n" % (acc_time, time.strftime(date_format, acc_date_t))

                        cre_time = Time(time.mktime(cre_date_t))
                        acc_time = Time(time.mktime(acc_date_t))
                        mod_time = Time(time.mktime(mod_date_t))
                        SetFileTime(fh, cre_time, acc_time, mod_time)
                        CloseHandle(fh)

                        # check if all was ok
                        cre_date = time.strftime(date_format, time.localtime(os.path.getctime(os.path.join(path, f_file))))
                        mod_date = time.strftime(date_format, time.localtime(os.path.getmtime(os.path.join(path, f_file))))
                        acc_date = time.strftime(date_format, time.localtime(os.path.getatime(os.path.join(path, f_file))))

                        # print "CHECK MODIFICATION:"
                        # print "FileName: %s" % file_name
                        # print "Create  : %s" % (cre_date)
                        # print "Modify  : %s" % (mod_date)
                        # print "Access  : %s" % (acc_date)

                        # if you choose file as the source, modify exif date
                        if date_src == "file":
                            dump_image(os.path.join(path, f_file), f_year + ":" + f_month + ":" + f_date + " " + f_hour + ":" + f_min + ":" + f_sec)
                        if f_file != f_file_new:
                            os.rename(os.path.join(path, f_file), os.path.join(path, f_file_new))
                            # print "Change file name from %s to %s" % (file_name, f_file_new)
                            log_msg += "Change file name from %s to %s\n" % (f_file, f_file_new)

                    except WindowsError as e:
                        # print e
                        log_msg += "Duplicates Found\n"
                        post_fix = str(datetime.datetime.now().microsecond)[0:3]
                        f_file_new_alt = f_file_new + "_" + post_fix + f_ext
                        os.rename(os.path.join(path, f_file), os.path.join(path, f_file_new_alt))
                        print "Change file name from %s to %s" % (f_file, f_file_new_alt)
                        log_msg += "Change file name from %s to %s\n" % (f_file, f_file_new_alt)
                        logger.error(log_msg)
                    except EOFError as e:
                        print e
                        # print "Invalid date format"
                        log_msg += "Invalid date format\n"
                        logger.error(log_msg)
                    except:
                        print "unknown error occured"
                        log_msg += "unknown error occured\n"
                        logger.error(log_msg)
                    else:
                        logger.info(log_msg)
    except EOFError:
        print "Process canceled"
        sys.exit()
    except KeyboardInterrupt:
        print
        print "Keyboard Interrupted"
        sys.exit()
