import os
import datetime

class LoggerService:
    def __init__(self,filename:str, debugMod:bool=False):
        self.filename = filename
        self.debugMod = debugMod
        self.createLogFile()
        self.log("LoggerService", "LoggerService started")

    def createLogFile(self):
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def info(self,message):
        self.log("INFO", message)

    def error(self,message):
        self.log("ERROR", message)

    def debug(self,message):
        if self.debugMod:
            self.log("DEBUG", message)

    def log(self,level,message):
        logStr = f"[{datetime.datetime.now()}] [{level}] {message}"
        self.write(logStr)

    def write(self,logStr):
        with open(self.filename, "a") as f:
            f.write(f"{logStr}\n")
            f.close()
