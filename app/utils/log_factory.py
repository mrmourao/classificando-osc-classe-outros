# -*- coding: utf-8 -*-
""" @author: Marcos Romero Mourão """

#------------------------------------------------------------------------------    
# Import libraries

import logging

#------------------------------------------------------------------------------    

class Log():
    
    def setLog(name, logFile):
        
        logger = logging.getLogger(name)
        
        if (logger.hasHandlers()):
            logger.handlers.clear()
            
        logger.setLevel(logging.INFO)
        # create a file handler
        handler = logging.FileHandler(logFile)
        handler.setLevel(logging.INFO)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(handler)
        logger.addHandler(streamHandler)