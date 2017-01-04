#! /usr/bin/python
# -*-coding:utf-8-*-
import piexif
import re
import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS


def dump_image(input_file, date_time_original="0000:00:00 00:00:00"):
    exif_dic = piexif.load(input_file)
    exif_dic['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_time_original  #u"2099:09:29 10:10:10"
    exif_bytes = piexif.dump(exif_dic)
    piexif.insert(exif_bytes, input_file)


def get_exif(fn):
    try:
        img = Image.open(fn)
        info = img._getexif()
        ret = None
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == 'DateTimeOriginal':
                return value
    except AttributeError:
        print "This image file does not have exif info."
        dump_image(fn)
        sys.exit()
    finally:
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
    raw_date = []
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
    return str_date, con_date   #YYYY-MM-DD 24H:MI:SS, YYYYMMDD_24H:MI:SS


def get_file_name(f_file, f_file_new, sq=0, path="./."):
    files = os.listdir(path)
    seq = 0
    for f in files:
        # find same file name
        if os.path.isfile(os.path.join(path, f)):
            if sq == 0:
                f_file_tgt = f_file_new
            else:
                f_name = os.path.splitext(f_file_new)[0]
                f_ext = os.path.splitext(f_file_new)[1]
                f_file_tgt = f_name +"_"+ str(sq) + f_ext.lower()

            # print "f:", f
            # print "f_file:", f_file
            # print "f_file_new:", f_file_new
            # print "f_file_tgt:", f_file_tgt

            if f.lower() == f_file_tgt.lower() and f.lower() != f_file.lower():
                seq = sq + 1
                # print seq
                # print "f_file:", f_file
                # print "f_file_new:", f_file_new
                # f_name = os.path.splitext(f_file_new)[0]
                # f_ext = os.path.splitext(f_file_new)[1]
                # f_name_spl = f_name.split("_")
                # file_name_alt = f_name_spl[0] +"_"+ f_name_spl[1] +"_"+ str(seq) + f_ext
                # file_name_alt = f_name + "_" + str(seq) + f_ext
                # print "bbb", file_name_alt
            # if f.lower() == file_name.lower():
        # if os.path.isfile(os.path.join(path, f)) \
    # for f in files:
    if seq != 0:
        # print
        # print "seq:", seq
        file_name_new = get_file_name(f_file, f_file_new, seq)
    else:
        file_name_new = f_file_tgt
    return file_name_new
