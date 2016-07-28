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

import sys
import os
import re


# retreive exif info in the files
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


# retreive exif info in the files
def show_exif(fn):
    img = Image.open(fn)
    info = img._getexif()
    ret = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
        print decoded, value
    # print ret


def get_format_date(raw_num="00000000000000"):
    naked_num = re.findall('\d+', raw_num)
    con_num = "".join(naked_num)
    if len(con_num) < 15:
        raw_date = "{0:0<14}".format(con_num)
    elif len(con_num) >= 15:
        raw_date = naked_num[0:14]
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

try:
    path = "."
    allowed_file = ['.JPG', '.MP4', 'WMV']
    for f in os.listdir(path):
        f_split = os.path.splitext(f)
        if os.path.isfile(f):
            if allowed_file.count(f_split[1].upper()) > 0:
                exif_date = ""
                if f_split[1].upper() == ".JPG":
                    exif_date = get_exif(f)

                e_str_date, e_full_date = get_format_date(exif_date)
                f_str_date, f_full_date = get_format_date(f_split[0])
                f_full = f_full_date + f_split[1]

                if f_full_date != e_full_date:
                    print "File Name: %s" % f
                    print "Name Date: %s (%s)" % (f_str_date, f_full_date)
                    print "EXIF Date: %s (%s)" % (e_str_date, e_full_date)
                    num = "0"
                    while True:
                        num = raw_input("Which would you like to change with? (1: Name, 2: EXIF)")
                        if num != "1" and num != "2":
                            continue
                        if num == "1":
                            break
                        elif num == "2":
                            f_str_date = e_str_date
                            f_full_date = e_full_date
                            f_full = e_full_date + f_split[1]
                            break
                print f_str_date, f_full
                print
                break

                # f_str_date, f_full_date = get_format_date(f_split[0])

                # print f, f_str_date, f_full_date
                # f_name = re.findall('\d+', f_split[0])
                # f_join = "".join(f_name)
                # if len(f_join) < 12:
                #     pass
                # elif 12 <= len(f_join) < 15:
                #     f_raw_date = "{0:0<14}".format(f_join)
                # elif len(f_join) >= 15:
                #     f_raw_date = f_join[0:14]
                # f_year = f_raw_date[0:4]
                # f_month = f_raw_date[4:6]
                # f_date = f_raw_date[6:8]
                # f_hour = f_raw_date[8:10]
                # f_min = f_raw_date[10:12]
                # f_sec = f_raw_date[12:14]
                # f_str_date = f_year + "-" + f_month + "-" + f_date + " " + f_hour + ":" + f_min + ":" + f_sec
                # f_full = f_year + f_month + f_date + "_" + f_hour + f_min + f_sec + f_split[1]

                # # get arguments
                # cre_date = f_str_date  # create
                # mod_date = f_str_date  # modify
                # acc_date = f_str_date  # access
                # file_name = f
                #
                # # specify time format
                # date_format = "%Y-%m-%d %H:%M:%S"
                # offset = 0  # in seconds
                #
                # # visually check if conversion was ok
                # print
                # print "FileName: %s" % f
                # print "Date : %s (YYYY-MM-DD HH:Mi:SS)" % f_str_date
                #
                # try:
                #     # create struct_time object
                #     cre_date_t = time.localtime(time.mktime(time.strptime(cre_date, date_format)) + offset)
                #     mod_date_t = time.localtime(time.mktime(time.strptime(mod_date, date_format)) + offset)
                #     acc_date_t = time.localtime(time.mktime(time.strptime(acc_date, date_format)) + offset)
                #
                #     # visually check if conversion was ok
                #     # print "Create  : %s --> %s OK" % (cre_date, time.strftime(date_format, cre_date_t))
                #     # print "Modify  : %s --> %s OK" % (mod_date, time.strftime(date_format, mod_date_t))
                #     # print "Access  : %s --> %s OK" % (acc_date, time.strftime(date_format, acc_date_t))
                #     # print
                #
                #     # change timestamp of file
                #     fh = CreateFile(file_name, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
                #     cre_time, acc_time, mod_time = GetFileTime(fh)
                #
                #     print "Change Create from", cre_time, "to %s" % (time.strftime(date_format, cre_date_t))
                #     print "Change Modify from", mod_time, "to %s" % (time.strftime(date_format, mod_date_t))
                #     print "Change Access from", acc_time, "to %s" % (time.strftime(date_format, acc_date_t))
                #
                #     cre_time = Time(time.mktime(cre_date_t))
                #     acc_time = Time(time.mktime(acc_date_t))
                #     mod_time = Time(time.mktime(mod_date_t))
                #     SetFileTime(fh, cre_time, acc_time, mod_time)
                #     CloseHandle(fh)
                #
                #     # check if all was ok
                #     cre_date = time.strftime(date_format, time.localtime(os.path.getctime(file_name)))
                #     mod_date = time.strftime(date_format, time.localtime(os.path.getmtime(file_name)))
                #     acc_date = time.strftime(date_format, time.localtime(os.path.getatime(file_name)))
                #
                #     # print "CHECK MODIFICATION:"
                #     # print "FileName: %s" % file_name
                #     # print "Create  : %s" % (cre_date)
                #     # print "Modify  : %s" % (mod_date)
                #     # print "Access  : %s" % (acc_date)
                #
                #     os.rename(f, f_full)
                #
                #     print "Change file name from %s to %s" % (f, f_full)
                #
                # except:
                #     print "Invalid date format"
except EOFError:
    print "Process canceled"
    sys.exit()
except KeyboardInterrupt:
    print
    print "Keyboard Interrupted"
    sys.exit()
