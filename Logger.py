#! /usr/bin/python
# -*-coding:utf-8-*-

# import logging
import logging.handlers

def log_result(log_level, log_msg):
    # logger 인스턴스를 생성 및 로그 레벨 설정
    logger = logging.getLogger("crumbs")
    logger.setLevel(logging.DEBUG)

    # formmater 생성
    formatter = logging.Formatter('[%(levelname)s| %(asctime)s > \n%(message)s')

    # fileHandler와 StreamHandler를 생성
    file_handler = logging.FileHandler('modall.log')
    # streamHandler = logging.StreamHandler()

    # handler에 fommater 세팅
    file_handler.setFormatter(formatter)
    # streamHandler.setFormatter(formatter)

    # Handler를 logging에 추가
    logger.addHandler(file_handler)
    # logger.addHandler(streamHandler)

    # logging
    if log_level == "debug":
        logger.debug(log_msg)
    elif log_level == "info":
        logger.info(log_msg)
    elif log_level == "warning":
        logger.warning(log_msg)
    elif log_level == "error":
        logger.error(log_msg)
    elif log_level == "critical":
        logger.critical("log_msg")
    else:
        logger.debug("log_msg")