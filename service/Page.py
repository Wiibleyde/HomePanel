import json
import os

class PageObject:
    def __init__(self,name,link,logo):
        self.name = name
        self.link = link
        self.logo = logo

    def __getattribute__(self, __name: str):
        return super().__getattribute__(__name)
    
    def __setattr__(self, __name: str, value):
        super().__setattr__(__name, value)

class PageService:
    def __init__(self):
        self.__pageList = []
        self.__loadPageList()

    def __loadPageList(self):
        with open(os.path.join(os.path.dirname(__file__),"pageList.json"),'r',encoding='utf-8') as f:
            pageList = json.load(f)
            for page in pageList:
                self.__pageList.append(PageObject(page['name'],page['link'],page['logo']))

    def getPageList(self):
        return self.__pageList

    def getPage(self,name):
        for page in self.__pageList:
            if page.name == name:
                return page
        return None

    def addPage(self,page):
        self.__pageList.append(page)
        self.__savePageList()

    def deletePage(self,name):
        for page in self.__pageList:
            if page.name == name:
                self.__pageList.remove(page)
                self.__savePageList()
                return True
        return False

    def __savePageList(self):
        with open(os.path.join(os.path.dirname(__file__),"pageList.json"),'w',encoding='utf-8') as f:
            json.dump(self.__pageList,f,ensure_ascii=False,indent=4)
