import json
import os

class PageObject:
    def __init__(self,name,link):
        self.name = name
        self.link = link

    def __str__(self):
        return "PageObject: " + self.name + " " + self.link

    def __getattribute__(self, name: str):
        return object.__getattribute__(self, name)
    
    def __setattr__(self, name: str, value):
        object.__setattr__(self, name, value)

class PageService:
    def __init__(self,filename):
        self.filename = "data/" + filename
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)
    
    def addPage(self,name,link):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        data.append({"name":name,"link":link})
        with open(self.filename, 'w') as f:
            json.dump(data, f)
    
    def getPages(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        pages = []
        for page in data:
            pages.append(PageObject(page["name"],page["link"]))
        return pages
    
    def getPage(self,link):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        for page in data:
            if page["link"] == link:
                return PageObject(page["name"],page["link"])
        return None
    
    def deletePage(self,link):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        for page in data:
            if page["link"] == link:
                data.remove(page)
                break
        with open(self.filename, 'w') as f:
            json.dump(data, f)
    
    def updatePage(self,link,name):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        for page in data:
            if page["link"] == link:
                page["name"] = name
                break
        with open(self.filename, 'w') as f:
            json.dump(data, f)
    
    def testIfLinkExist(self,link):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        for page in data:
            if page["link"] == link:
                return True
        return False