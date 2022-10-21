from filecmp import cmp, cmpfiles
from os import mkdir, chdir, getcwd, walk, rmdir, path, listdir, remove as osremv, replace as rpl, stat, scandir
from time import sleep, time as tm
from threading import Thread
# vars and globals
_file_self = __file__.split('\\')[-1]  # self file name
_pth = getcwd()
swr = 'something went wrong '
crtf = 'failed to create folder, try again'
swcr = swr + crtf
ctgs = {
    'Programming files': ['Programming files', '.ASP', '.Classic', '.asp', '.NET', '.aspx', '.axd', '.asx', '.asmx', '.ashx', '.CSS', '.css', '.Coldfusion', '.cfm', '.Erlang', '.yaws', '.Flash', '.swf', '.HTML', '.html', '.htm', '.xhtml', '.jhtml', '.Java', '.jsp', '.jspx', '.wss', '.do', '.action', '.JavaScript', '.js', '.Perl', '.pl', '.PHP', '.php', '.php4', '.php3', '.phtml', '.Ruby', '.rb', '.rhtml', '.SSI', '.shtml', '.TS', '.XML', '.xml', '.rss', '.svg', '.Other', '.C', '.perl', '.etc', '.cgi', 'dll', '.cpp', '.go'],

    'Images': ['Images', '.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.max', '.obj', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.3ds', '.3dm', '.heic'],

    'Videos': ['Videos', '.avi', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg '',mpeg	', '.rm', '.swf', '.vob', '.wmv', '.3g2', '.3gp'],

    'Audios': ['Audios', '.aif', '.cda', '.iff', '.mid ', '.midi', '.mp3', '.mpa', '.wav', '.wma', '.wpl'],

    'Docs': ['Docs', '.doc', '.docx', '.odt', '.msg', '.pdf', '.rtf', '.tex', '.txt', '.wks', '.wps', '.wpd'],

    'Spreadsheets': ['Spreadsheets', '.ods', '.xlr', '.xls', '.xlsx', '.Gsheet'],

    'Web files': ['Web files', '.asp ', '.aspx	', '.cer', '.cfm', '.cgi', '.pl', '.css', '.htm', '.html', '.js	', '.jsp', '.part', '.php', '.rss', '.xhtml'],

    'System files': ['System files', '.bak', '.cab', '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ico', '.ini', '.lnk', '.msi', '.sys', '.tmp'],

    'Database files': ['Database files', '.accdb', '.csv', '.dat', '.db', '.dbf', '.log', '.mdb', '.pdb', '.sav', '.sql', '.tar'],

    'Presentation files': ['Presentation files', '.key', '.odp', '.pps', '.ppt', '.pptx'],

    'Executable files': ['Executable files', '.apk', '.bat', '.bin', '.cgi', '.com', '.exe', '.jar', '.wsf']

}


def ext(f):
    return (path.splitext(f)[1]).lower()


def getAvg(l):
    return sum(l) / len(l)


def dltIfEmp(f):
    if path.isdir(f) and (path.getsize(f) == 0):
        try:
            rmdir(f)
        except OSError:
            pass
        except Exception:
            pass


class Folderer():
    total_size_scanned = 0

    def __init__(self, usrnme=None):
        self.usrnme = usrnme

    def createNewFolder(self):
        try:
            if path.exists('New Folder'):
                mkdir('New Folder (2)')
            else:
                mkdir('New Folder')

        except FileExistsError:

            for i in range(2, 500):
                if (f'New Folder ({i})') not in listdir():
                    mkdir(f'New Folder ({i})')
                    break
        except MemoryError:
            return 'Not enough memory '+swr
        except Exception:
            return swcr

    def makeFolder(self, s=False):
        s = str(s) if s else ''
        if len(s) == 0:
            return self.createNewFolder()
        print(len(s))
        try:
            if s is None:
                return self.createNewFolder()
            else:
                mkdir(s)
                return f"Created folder '{s}'"
        except FileExistsError:
            return f"A directory with this name '{s}' already has been created"
        except WindowsError as e:
            if e.winerror == 123:
                return 'Use a valid name to create folder'
            else:
                return e
        except Exception:
            return swcr

    # single folder remove or delete
    def rmFold(self, s: str):
        s = str(s)
        try:
            m = f"Removed '{s}'\t---\tsize : {path.getsize(s)} bytes\t"
            rmdir(s)
            return m
        except FileNotFoundError:
            if path.exists(s):
                return m
            else:
                return f"Folder not found named '{s}'"
        except Exception:
            return swr

    # to remove file, maybe not work to delete or remove folders
    def rmv(self, s: str):
        s = str(s)
        try:
            if path.exists(s):
                if path.isdir(s):
                    return self.rmFold(s)
                else:
                    osremv(s)
                    return f"Removed '{s}'\t---\tsize : {path.getsize(s)} bytes\t"
            else:
                f"Not found named '{s}'"
        except FileNotFoundError:
            return f"Not found named '{s}'"
        except Exception as e:
            return swr

    #  to delete empty folders in current list, I mean junk folders (maybe also not found in recycle bin)
    def deleteEmpFolders(self):
        list(map(dltIfEmp, listdir()))

    # get folder type like is it directory or file or ....
    def getFTp(self, s: str):
        return 'file' if path.isfile(s) else 'folder' if path.isdir(s) else 'link' if path.islink(s) else 'abs path' if path.isabs(s) else 'mount point path'

    # get FldrSize (99% accurate)
    # 'B' | 'KB' | 'MB' | 'GB'
    def getFldrSize(self, fldrOrPath=getcwd(), bytesTo='KB', onlyCurrFold=False):
        s = 0
        if onlyCurrFold:
            for _ in scandir(getcwd()):
                s += stat(_).st_size

        else:
            try:
                for (r, _, __) in walk(fldrOrPath, topdown=True):
                    for _ in scandir(r):
                        s += stat(_).st_size
            except TypeError:
                raise TypeError(
                    'unsuppoerted format, must be B | MB | KB | GB')
            except Exception:
                return 0
        return s if (bytesTo == 'B') else s/(1024*1024) if bytesTo == 'MB' else s/(1024*1024*1024) if bytesTo == 'GB' else s/1024

   # get which kind of file it is. If it matches will ctgs (File Categories)
    def ctg(self, f: str):
        n = False
        for l in ctgs:
            i = ctgs[l]
            if ext(f) in i:
                n = i[0].lower()
                break
        return n+'/' if n else ''

    def repl(self, f: str):
        try:
            n = self.ctg(f)
            (mkdir(n), rpl(f, n+f)) if not path.exists(n) else rpl(f, n+f)
        except Exception:
            pass

    # to beutify files of current folder except those files you provided in excepts
    def folderizeFilesThisPath(self, delEmpFolders=True, *excepts):

        l = listdir()
        l = [f for f in l if f not in excepts]
        list(map(self.repl, l))
        if (delEmpFolders):
            self.deleteEmpFolders()
        for i in excepts:
            print(i)

    #
    def findTextOrScript(self, searchText: str = None, runInsideFolders=False):
        pass

    # to remove duplicate files, if onlyImage is True it will only perform action with images, if walkInside True then it will run all folders inside folders and inside like this, maybe it's so slow if folder's size is too large (it may slower in big directory sizes and may take much time to scan , because this functions scan very clearly each of files)
    def removeDuplicateFiles(self, path=getcwd(), onlyImg=False, walkInside=False, showStatus=False):
        self.notStartedThread = True
        self.showStatus = showStatus
        if (self.showStatus):
            self.isDoneScanning = False
        start = tm()
        size = 0
        tt = 0
        totScanMsg = ''
        if walkInside:
            size = self.getFldrSize(
                path, bytesTo='MB', onlyCurrFold=True if walkInside == False else False)
        else:
            size = self.getFldrSize(path, bytesTo='MB')
        # ======== taken 16 seconds
        if size > 1000:
            totScanMsg = f'{round(size/1024,2)} (GB)'
        else:
            totScanMsg = f'{round(size,2)} (MB)'

        for (r, d, file) in walk(path, topdown=True):
            chdir(r)
            file = [f for f in file if (
                ext(f) in ctgs['Images'])] if onlyImg else file
            file.remove(_file_self) if _file_self in file else None
            for n in range(len(file)):
                fileToScan = file[n]
                if (self.showStatus):
                    self.total_size_scanned += stat(fileToScan).st_size
                    self.convToMB = (self.total_size_scanned / 1024/1024)
                    self.percentDone = round(((self.convToMB/size) * 100), 2)
                    self.remainingSize = round((size - self.convToMB), 2)
                    if self.remainingSize < 500:
                        self.isDoneScanning = True
                otherFiles = file[n + 1:]
                for fl in otherFiles:
                    if self.notStartedThread:
                        t1 = Thread(target=self.removeduplicateMessage)
                        t1.start()
                    try:
                        if cmp(fileToScan, fl):
                            osremv(fl)
                            tt += 1
                    except Exception:
                        pass
            if walkInside == False:
                break

        print(
            f'--------------------\nSuccessfully removed duplicate items\n--------------------\nTotal removed {tt} from path : ({path}) full inside possible\n--------------------\nFull directory size was : {totScanMsg} [ DONE ]')
        print('total time taken ', tm() - start)

    # on time live messaging of status about how much size remaining to scan, how much percentage remaining to scan, specially its helpful for big dirctories / folders
    def removeduplicateMessage(self):
        self.notStartedThread = False
        if (self.showStatus):
            while self.isDoneScanning == False:
                print(f'done {self.percentDone}% of 100% to scan')
                print(
                    f'remaining {self.remainingSize} (MB) or ({round((100 - self.percentDone),2)}%) more to scan')
                if self.isDoneScanning:
                    break
                sleep(2)


you = Folderer()
#you.methodRun()