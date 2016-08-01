#! /usr/bin/python
# -*-coding:utf-8-*-

from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time, datetime

from Tkinter import *
from tkFileDialog import askdirectory
from PIL import Image
from PIL.ExifTags import TAGS
import piexif

import sys
import os
import re
import datetime
# import logging
import logging.handlers

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
    full_date = year + month + date + "_" + hour + mi + se
    return str_date, full_date

# top = Tk()
# F = Frame(top)
# F.pack(expand="true")
# path = askdirectory(title="select directory", mustexist=1)

# is_go = raw_input("Do you want to change file name and all date in those files? (Y or N)")
# if is_go.upper() != "Y":
#     print "Process canceled"
#     sys.exit()

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

try:
    path = "."
    allowed_file = ['.JPG', '.MP4', 'WMV']
    for f in os.listdir(path):
        log_msg = ""
        log_level = "info"
        f_split = os.path.splitext(f)
        if os.path.isfile(f):
            f_ext = f_split[1]
            if allowed_file.count(f_ext.upper()) > 0:
                exif_date = ""
                f_str_date, f_full_date = get_format_date(f_split[0])
                # print
                # print "File Name: %s" % f
                # print "File Date : %s (YYYY-MM-DD HH:Mi:SS)" % (f_str_date)
                log_msg += "\n" \
                           "File Name: %s\n" \
                           "File Date : %s (YYYY-MM-DD HH:Mi:SS)\n" % (f, f_str_date)
                if f_ext.upper() == ".JPG":
                    exif_date = get_exif(f)

                    e_str_date, e_full_date = get_format_date(exif_date)
                    f_full = f_full_date + f_ext
                    date_src = ""
                    if f_full_date != e_full_date:
                        # print "EXIF Date: %s (%s)" % (e_str_date, e_full_date)
                        log_msg += "EXIF Date: %s (%s)\n" % (e_str_date, e_full_date)
                        num = "0"
                        while True:
                            num = raw_input("Which would you like to change with? (1: File Name, 2: EXIF)")
                            if num != "1" and num != "2":
                                continue
                            if num == "1":
                                date_src = "file"
                                break
                            elif num == "2":
                                f_str_date = e_str_date
                                f_full_date = e_full_date
                                f_full = e_full_date + f_ext
                                date_src = "exif"
                                break
                f_name = re.findall('\d+', f_full_date)
                f_join = "".join(f_name)
                if len(f_join) < 12:
                    pass
                elif 12 <= len(f_join) < 15:
                    f_raw_date = "{0:0<14}".format(f_join)
                elif len(f_join) >= 15:
                    f_raw_date = f_join[0:14]
                f_year = f_raw_date[0:4]
                f_month = f_raw_date[4:6]
                f_date = f_raw_date[6:8]
                f_hour = f_raw_date[8:10]
                f_min = f_raw_date[10:12]
                f_sec = f_raw_date[12:14]
                f_str_date = f_year + "-" + f_month + "-" + f_date + " " + f_hour + ":" + f_min + ":" + f_sec
                f_file = f_year + f_month + f_date + "_" + f_hour + f_min + f_sec
                f_full = f_year + f_month + f_date + "_" + f_hour + f_min + f_sec + f_ext

                # get arguments
                cre_date = f_str_date  # create
                mod_date = f_str_date  # modify
                acc_date = f_str_date  # access
                file_name = f

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
                    fh = CreateFile(file_name, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
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
                    cre_date = time.strftime(date_format, time.localtime(os.path.getctime(file_name)))
                    mod_date = time.strftime(date_format, time.localtime(os.path.getmtime(file_name)))
                    acc_date = time.strftime(date_format, time.localtime(os.path.getatime(file_name)))

                    # print "CHECK MODIFICATION:"
                    # print "FileName: %s" % file_name
                    # print "Create  : %s" % (cre_date)
                    # print "Modify  : %s" % (mod_date)
                    # print "Access  : %s" % (acc_date)

                    if date_src == "file":
                        dump_image(file_name, f_year + ":" + f_month + ":" + f_date + " " + f_hour + ":" + f_min + ":" + f_sec)
                    if file_name != f_full:
                        os.rename(file_name, f_full)
                        # print "Change file name from %s to %s" % (file_name, f_full)
                        log_msg += "Change file name from %s to %s\n" % (file_name, f_full)

                except WindowsError:
                    # print "Duplicates Found"
                    post_fix = str(datetime.datetime.now().microsecond)[0:3]
                    f_alt_file = f_file + "_" + post_fix + f_ext
                    os.rename(file_name, f_alt_file)
                    # print "Change file name from %s to %s" % (file_name, f_full)
                    log_msg += "Change file name from %s to %s\n" % (file_name, f_alt_file)
                    log_level = "error"
                except EOFError:
                    # print "Invalid date format"
                    log_msg += "Invalid date format\n"
                    log_level = "error"
                finally:
                    if log_level == "error":
                        logger.error(log_msg)
                    elif log_level == "info":
                        logger.info(log_msg)
                    else:
                        logger.critical(log_msg)
except EOFError:
    print "Process canceled"
    sys.exit()
except KeyboardInterrupt:
    print
    print "Keyboard Interrupted"
    sys.exit()
