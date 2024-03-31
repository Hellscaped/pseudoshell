#!/usr/bin/env python3

class PseudoFile():
    def __init__(self,mode: str,content: bytes):
        self.mode = mode
        self.content = content
    def read(self):
        if self.mode == "rb":
            return self.content
        return self.content.decode()
    def write(self,newcontent):
        if self.mode == "a":
            self.content += newcontent
            return self
        self.content = newcontent
        return self

def cat(psh,argv):
    argv.pop(0)
    for arg in argv:
        file = psh.vfs.open(arg,"r")
        print(file.read())
        del file

def clear(psh,argv):
    print("\033c",end="")

class vfs:
    def __init__(self,psh,tree):
        self.tree = tree
    def pathtoobject(self,path):
        path = path.split("/")
        if path[0] == "":
            path.pop(0)
        obj = self.tree
        for p in path:
            obj = obj[p]
        return obj

    def open(self,filepath,mode):
        return PseudoFile(mode,self.pathtoobject(filepath))
    
    def exists(self,filepath):
        path = path.split("/")
        if path[0] == "":
            path.pop(0)
        statement = True
        obj = self.tree
        for p in path:
            if p in obj:
                obj = obj[p]
            else:
                statement = False
                break
        return statement

class Pseudoshell:
    def __init__(self,user,hostname):
        self.user = user
        self.hostname = hostname
        self.path = "/bin"
        self.pwd = f"/home/{user}"
        self.vfs = vfs(self,{
            "home": {
                user: {
                    "readme.md": b"""lorem ipsum"""
                }
            },
            "bin": {
                "cat": cat,
                "clear": clear
            }
        })
    def repl(self):
        while True:
            cmd = input(f"{self.user}@{self.hostname}$ ")
            argv = cmd.split(" ")
            if cmd[0].startswith("/"):
                binary = self.vfs.pathtoobject(argv[0])
            else:
                binary = self.vfs.pathtoobject(self.path+"/"+argv[0])
            binary(self,argv)

if __name__ == "__main__":
    psh = Pseudoshell("hellscaped","pythonbtw")
    psh.repl()