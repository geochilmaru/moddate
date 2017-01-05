#! /usr/bin/python
# -*-coding:utf-8-*-

from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time

# from PIL import Image
# from PIL.ExifTags import TAGS
# import piexif

import msvcrt
import sys
import os
import re
# import datetime
from datetime import datetime
# import logging
import logging.handlers
import CSVFileIO
import ImageInfo
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


if __name__ == "__main__":
    result_log = []
    is_go = ""
    try:
        src_opt = ""
        tgt_opt = []
        if len(sys.argv) == 1:
            # is_go = raw_input("Do you want to change file name and date? (Y or N)")
            print 'Do you want to change file name and date? (Y or N)'
            is_go = msvcrt.getch()
            if is_go.upper() == "Y":
                option = "each"
            else:
                print "Process canceled"
                sys.exit()
        elif len(sys.argv) == 2:
            if str(sys.argv[1]).upper() == "HELP":
                print "\nChange the create date of a file and rename the file names" \
                        " within the same directory to order easily\n" \
                        "(1) Changes the created, modified, accessed date of files" \
                        " to the file name or exif DateTimeOriginal\n" \
                        "(2) Changes the file name to exif DateTimeOriginal\n" \
                        "(3) Changes the file name to formated date\n\n" \
                        "Usage:\n" \
                        "moddate.exe <argument>\n" \
                        "(1) help: show this descripton\n" \
                        "(2) NOT YET!!! <nothing>: change each file on selection\n" \
                        "(3) -nl: make only log file(csv) with using file name\n" \
                        "(4) -el: make only log file(csv) with using exif\n" \
                        "(5) -na: change file name, exif and date of all files to the file name\n" \
                        "(6) -ne: change exif and date of all files to the file name\n" \
                        "(7) -nn: change file name and date of all files to the file name\n" \
                        "(8) -nd: change only date of all files to the file name\n" \
                        "(9) -ea: change file name and date of all files to the file name\n" \
                        "(10) -ed: change only date of all files to the file name\n"
                sys.exit()
            elif str(sys.argv[1]).upper() == "-NL":
                is_go = "Y"
                src_opt = "n"
                tgt_opt.append("l")
            elif str(sys.argv[1]).upper() == "-NA":
                # is_go = raw_input("Do you want to change all files name and all date to file name? (Y or N)")
                # print "Do you want to change file name, exif and date of all files to the file name? (Y or N)"
                # is_go = msvcrt.getch()
                is_go = "Y"
                if is_go.upper() == "Y":
                    src_opt = "n"
                    tgt_opt.append("e")
                    tgt_opt.append("n")
                    tgt_opt.append("d")
                else:
                    print "Process canceled"
                    sys.exit()
            elif str(sys.argv[1]).upper() == "-NE":
                # is_go = raw_input("Do you want to change all files name and all date to file name? (Y or N)")
                # print "Do you want to change file name, exif and date of all files to the file name? (Y or N)"
                # is_go = msvcrt.getch()
                is_go = "Y"
                if is_go.upper() == "Y":
                    src_opt = "n"
                    tgt_opt.append("e")
                    tgt_opt.append("d")
                else:
                    print "Process canceled"
                    sys.exit()
            elif str(sys.argv[1]).upper() == "-NN":
                # is_go = raw_input("Do you want to change all files name and all date to file name? (Y or N)")
                # print "Do you want to change file name, exif and date of all files to the file name? (Y or N)"
                # is_go = msvcrt.getch()
                is_go = "Y"
                if is_go.upper() == "Y":
                    src_opt = "n"
                    tgt_opt.append("n")
                    tgt_opt.append("d")
                else:
                    print "Process canceled"
                    sys.exit()
            elif str(sys.argv[1]).upper() == "-ND":
                # is_go = raw_input("Do you want to change all files name and all date to file name? (Y or N)")
                # print "Do you want to change file name, exif and date of all files to the file name? (Y or N)"
                # is_go = msvcrt.getch()
                is_go = "Y"
                if is_go.upper() == "Y":
                    src_opt = "n"
                    tgt_opt.append("d")
                else:
                    print "Process canceled"
                    sys.exit()
            elif str(sys.argv[1]).upper() == "-EL":
                is_go = "Y"
                src_opt = "e"
                tgt_opt.append("l")
            elif str(sys.argv[1]).upper() == "-EA":
                # is_go = raw_input("Do you want to change all files name and all date to file name? (Y or N)")
                # print "Do you want to change file name, exif and date of all files to the file name? (Y or N)"
                # is_go = msvcrt.getch()
                is_go = "Y"
                if is_go.upper() == "Y":
                    src_opt = "e"
                    tgt_opt.append("n")
                    tgt_opt.append("d")
                else:
                    print "Process canceled"
                    sys.exit()
            elif str(sys.argv[1]).upper() == "-ED":
                # is_go = raw_input("Do you want to change all files name and all date to file name? (Y or N)")
                # print "Do you want to change file name, exif and date of all files to the file name? (Y or N)"
                # is_go = msvcrt.getch()
                is_go = "Y"
                if is_go.upper() == "Y":
                    src_opt = "e"
                    tgt_opt.append("d")
                else:
                    print "Process canceled"
                    sys.exit()
        else:
            print "too many arguments"
            sys.exit()

        logger = logging.getLogger("crumbs")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s| %(asctime)s > %(message)s')
        file_handler = logging.FileHandler('modall.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        file_info_order = ["src_name", "src_exif", "src_date", "src_created", "src_modified", "src_accessed",
                           "tgt_name", "tgt_exif", "tgt_created", "tgt_modified", "tgt_accessed"]
        path = "./."
        allowed_file = ['.JPG', '.JPEG', '.MP4', '.WMV']
        # retreive files from selected directory
        for f in os.listdir(path):
            file_info = {"src_name":"", "src_exif":"", "src_date":"", "src_created":"", "src_modified":"", "src_accessed":"",
                           "tgt_name":"", "tgt_exif":"", "tgt_created":"", "tgt_modified":"", "tgt_accessed":""}
            # file_info = {}
            ignore = "N"
            log_msg = ""
            log_level = "info"
            f_name = os.path.splitext(f)[0]
            f_ext = os.path.splitext(f)[1]
            f_file = f
            f_path = os.path.join(path, f_file)
            # file type
            if os.path.isfile(os.path.join(path, f_file)):
                # media file type
                if allowed_file.count(f_ext.upper()) > 0:
                    file_info["src_name"] = f_file  # add file info
                    # exif_date = ""
                    f_str_date, f_name_new = ImageInfo.get_format_date(f_name)    #YYYY-MM-DD 24H:MI:SS, YYYYMMDD_24HMISS
                    file_info["src_date"] = f_str_date  # add file info
                    f_file_new = f_name_new + f_ext
                    # file_info["tgt_name"] = f_file_new  # add file info
                    print
                    print "File Name: %s" % f_file
                    print "File Date : %s (YYYY-MM-DD HH:Mi:SS)" % (f_str_date)
                    log_msg += "\n" \
                               "File Name: %s\n" \
                               "File Date: %s (YYYY-MM-DD HH:Mi:SS)\n" % (f_file, f_str_date)
                    # jpg format type
                    if f_ext.upper() == ".JPG" or f_ext.upper() == ".JPEG":
                        exif_date = ImageInfo.get_exif(os.path.join(path, f_file))
                        e_str_date, e_name_new = ImageInfo.get_format_date(exif_date) #YYYY-MM-DD 24H:MI:SS, YYYYMMDD_24HMISS
                        file_info["src_exif"] = e_str_date  # add file info
                        e_file_new = e_name_new + f_ext
                        print "EXIF Date: %s (YYYY-MM-DD HH:Mi:SS)" % (file_info["src_exif"])
                        log_msg += "EXIF Date: %s (YYYY-MM-DD HH:Mi:SS)\n" % (e_str_date)
                        if src_opt == "e":
                            f_str_date, f_name_new, f_file_new = e_str_date, e_name_new, e_file_new
                            file_info["src_date"] = f_str_date  # add file info
                    # if f_ext.upper() == ".JPG" or f_ext.upper() == ".JPEG":
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
                    file_info["tgt_name"] = f_file_new  # add file info

                    # get arguments
                    cre_date = f_str_date  # create
                    mod_date = f_str_date  # modify
                    acc_date = f_str_date  # access

                    # specify time format
                    date_format = "%Y-%m-%d %H:%M:%S"
                    offset = 0  # in seconds

                    try:
                        # modify exif date
                        if tgt_opt.count("e") > 0:
                            ImageInfo.dump_image(os.path.join(path, f_file), f_year + ":" + f_month + ":" + f_date + " " + f_hour + ":" + f_min + ":" + f_sec)
                            file_info["tgt_exif"] = file_info["src_date"]  # add file info

                        # get timestamp of file
                        fh = CreateFile(os.path.join(path, f_file), GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
                        # cre_time, acc_time, mod_time = GetFileTime(fh)

                        cre_time = str(datetime.strptime(time.ctime(os.path.getctime(f_file)), '%a %b %d %H:%M:%S %Y'))
                        mod_time = str(datetime.strptime(time.ctime(os.path.getmtime(f_file)), '%a %b %d %H:%M:%S %Y'))
                        acc_time = str(datetime.strptime(time.ctime(os.path.getatime(f_file)), '%a %b %d %H:%M:%S %Y'))

                        # create struct_time object
                        cre_time_t = time.localtime(time.mktime(time.strptime(cre_time, date_format)) + offset)
                        mod_time_t = time.localtime(time.mktime(time.strptime(mod_time, date_format)) + offset)
                        acc_time_t = time.localtime(time.mktime(time.strptime(acc_time, date_format)) + offset)

                        file_info["src_created"] = time.strftime(date_format, cre_time_t)  # add file info
                        file_info["src_modified"] = time.strftime(date_format, mod_time_t)  # add file info
                        file_info["src_accessed"] = time.strftime(date_format, acc_time_t)  # add file info

                        # create struct_time object
                        cre_date_t = time.localtime(time.mktime(time.strptime(cre_date, date_format)) + offset)
                        mod_date_t = time.localtime(time.mktime(time.strptime(mod_date, date_format)) + offset)
                        acc_date_t = time.localtime(time.mktime(time.strptime(acc_date, date_format)) + offset)

                        file_info["tgt_created"] = time.strftime(date_format, cre_date_t)  # add file info
                        file_info["tgt_modified"] = time.strftime(date_format, mod_date_t)  # add file info
                        file_info["tgt_accessed"] = time.strftime(date_format, acc_date_t)  # add file info

                        log_msg += "Change Create from %s to %s\n" % (cre_time, time.strftime(date_format, cre_date_t))
                        log_msg += "Change Modify from %s to %s\n" % (mod_time, time.strftime(date_format, mod_date_t))
                        log_msg += "Change Access from %s to %s\n" % (acc_time, time.strftime(date_format, acc_date_t))

                        cre_time = Time(time.mktime(cre_date_t))
                        acc_time = Time(time.mktime(acc_date_t))
                        mod_time = Time(time.mktime(mod_date_t))

                        # check if all was ok
                        # cre_date = time.strftime(date_format, time.localtime(os.path.getctime(os.path.join(path, f_file))))
                        # mod_date = time.strftime(date_format, time.localtime(os.path.getmtime(os.path.join(path, f_file))))
                        # acc_date = time.strftime(date_format, time.localtime(os.path.getatime(os.path.join(path, f_file))))

                        # modify date time
                        if tgt_opt.count("e") > 0 or tgt_opt.count("n") > 0 or tgt_opt.count("d") > 0:
                            # set timestamp of file
                            SetFileTime(fh, cre_time, acc_time, mod_time)
                        CloseHandle(fh)

                        # modify file name
                        if tgt_opt.count("n") > 0 and file_info["src_name"] != file_info["tgt_name"]:
                            f_file_new_dup = ImageInfo.get_file_name(f_file, f_file_new)
                            file_info["tgt_name"] = f_file_new_dup  # add file info
                            if f_file != f_file_new_dup:
                                os.rename(os.path.join(path, f_file), os.path.join(path, f_file_new_dup))
                                print "Change file name from %s to %s" % (f_file, f_file_new_dup)
                                log_msg += "Change file name from %s to %s\n" % (f_file, f_file_new_dup)

                        if tgt_opt.count("e") > 0 or tgt_opt.count("l") > 0:
                            file_info["tgt_exif"] = file_info["src_date"]  # add file info

                        # clear logs
                        if file_info["src_name"] == file_info["tgt_name"]:
                            file_info["tgt_name"] = ""
                        if file_info["src_exif"] == file_info["tgt_exif"] and file_info["tgt_exif"] != "":
                            file_info["tgt_exif"] = ""
                        if file_info["src_created"] == file_info["tgt_created"]:
                            file_info["tgt_created"] = ""
                        if file_info["src_modified"] == file_info["tgt_modified"]:
                            file_info["tgt_modified"] = ""
                        if file_info["src_accessed"] == file_info["tgt_accessed"]:
                            file_info["tgt_accessed"] = ""

                    except WindowsError as e:
                        # print e
                        log_msg += "Duplicates Found\n"
                        print f_file, f_file_new
                        post_fix = str(datetime.now().microsecond)[0:3]
                        print post_fix
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
                    finally:
                        logger.error(log_msg)
                    result_log.append(file_info)
                    # print result_log
                # if allowed_file.count(f_ext.upper()) > 0:
            # if os.path.isfile(os.path.join(path, f_file)):
        # for f in os.listdir(path):
    except EOFError:
        print "Process canceled"
        sys.exit()
    except KeyboardInterrupt:
        print
        print "Keyboard Interrupted"
        sys.exit()
    finally:
        if is_go != "":
            CSVFileIO.write_csv("preview.csv", result_log, ",", file_info_order)

