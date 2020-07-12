importvlc
import sys
importsubprocess
ifsys.version_info[0] < 3:
#import Tkinter as Tk
importttk
fromTkinter import *
fromtkFileDialog import askopenfilename
else:
importtkinter as Tk
fromtkinter import ttk
fromtkinter.filedialog import askopenfilename
importos
importpathlib
from threading import Timer,Thread,Event
import time
import platform
srtpath = ""
keyoccs = []
occItr = 0
searchbox=""
classttkTimer(Thread):
def __init__(self, callback, tick):
Thread.__init__(self)
self.callback = callback
self.stopFlag = Event()
self.tick = tick
self.iters = 0
def run(self):
while not self.stopFlag.wait(self.tick):
self.iters += 1
self.callback()
def stop(self):
self.stopFlag.set()
def index(self):
returnself.iters
def get(self):
returnself.iters
class Player(Frame):
def __init__(self, parent, title=None):
Frame.__init__(self, parent)
self.parent = parent
if title == None:
title = "tk_vlc"
self.parent.title(title)
menubar = Menu(self.parent)
self.parent.config(menu=menubar)
search = Text()
fileMenu = Menu(menubar)
fileMenu.add_command(label="Open", underline=0, command=self.OnOpen)
fileMenu.add_command(label="Exit", underline=1, command=_quit)
menubar.add_cascade(label="File", menu=fileMenu)
self.player = None
self.videopanel = ttk.Frame(self.parent)
self.canvas = Canvas(self.videopanel).pack(fill=BOTH,expand=1)
self.videopanel.pack(fill=BOTH,expand=1)
ctrlpanel = ttk.Frame(self.parent)
pause =ttk.Button(ctrlpanel, text="Pause", command=self.OnPause)
play = ttk.Button(ctrlpanel, text="Play", command=self.OnPlay)
stop = ttk.Button(ctrlpanel, text="Stop", command=self.OnStop)
volume = ttk.Button(ctrlpanel, text="Volume", command=self.OnSetVolume)
pause.pack(side=LEFT)
play.pack(side=LEFT)
stop.pack(side=LEFT)
volume.pack(side=LEFT)
globalsearchbox
searchbox = ttk.Entry(self.canvas, width=20)
searchbttn = ttk.Button(self.canvas, width=10, text="Search",command=self.OnSearch)
searchnxtbttn = ttk.Button(self.canvas, width=10, text="Next",command=self.OnSearchNext)
searchbox.pack()
searchbttn.pack()
searchnxtbttn.pack()
self.volume_var = IntVar()
self.volslider = Scale(ctrlpanel, variable=self.volume_var, command=self.volume_sel,
from_=0, to=100, orient=HORIZONTAL, length=100)
self.volslider.pack(side=LEFT)
ctrlpanel.pack(side=BOTTOM)
ctrlpanel2 = ttk.Frame(self.parent)
self.scale_var = DoubleVar()
self.timeslider_last_val = ""
self.timeslider = Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel,
from_=0, to=1000, orient=HORIZONTAL, length=500)
self.timeslider.pack(side=BOTTOM, fill=X,expand=1)
self.timeslider_last_update = time.time()
ctrlpanel2.pack(side=BOTTOM,fill=X)
self.Instance = vlc.Instance()
self.player = self.Instance.media_player_new()
self.timer = ttkTimer(self.OnTimer, 1.0)
self.timer.start()
self.parent.update()
defOnSearchNext(self):
globaloccItr
print(keyoccs)
occtime = keyoccs[occItr]
num1 = (int(occtime[0])*10 + int(occtime[1])*1)*3600
num2 = (int(occtime[3])*10 + int(occtime[4])*1)*60
num3 = (int(occtime[6])*10 + int(occtime[7])*1)*1
time = num1 + num2 + num3
print(time)
occItr=occItr+1
self.timeslider.set(time)
defOnSearch(self):
file = open(srtpath,'r')
globalsearchbox
key = searchbox.get()
print("Key is : "+key)
hari = []
globalkeyoccs
keyoccs = []
for line in file:
hari.append(line)
fori in range(2,len(hari),4):
if key in str(hari[i]):
keyoccs.append(hari[i-1])
self.OnSearchNext()
defOnExit(self, evt):
self.Close()
defOnOpen(self):
self.OnStop()
p = pathlib.Path(os.path.expanduser("~"))
fullname = askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
globalsrtpath
srtpath = fullname[:-4]+'srt'
ifos.path.isfile(fullname):
print (fullname)
# cmd='py C:\Python27\Scripts\\autosub_app.py -S en -D en '+fullname
#print cmd
#subprocess.call(cmd, shell=True)
splt = os.path.split(fullname)
dirname =os.path.dirname(fullname)
filename = os.path.basename(fullname)
self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
self.player.set_media(self.Media)
ifplatform.system() == 'Windows':
self.player.set_hwnd(self.GetHandle())
else:
self.player.set_xwindow(self.GetHandle()) # this line messes up windows
# FIXME: this should be made cross-platform
self.OnPlay()

self.volslider.set(self.player.audio_get_volume())
defOnPlay(self):
if not self.player.get_media():
self.OnOpen()
else:
ifself.player.play() == -1:
self.errorDialog("Unable to play.")
defGetHandle(self):
returnself.videopanel.winfo_id()
`
defOnPause(self):
self.player.pause()
defOnStop(self):
self.player.stop()
self.timeslider.set(0)
defOnTimer(self):
ifself.player == None:
return
length = self.player.get_length()
dbl = length * 0.001
self.timeslider.config(to=dbl)
tyme = self.player.get_time()

iftyme == -1:
tyme = 0
dbl = tyme * 0.001
self.timeslider_last_val = ("%.0f" % dbl) + ".0"
iftime.time() > (self.timeslider_last_update + 2.0):
self.timeslider.set(dbl)
defscale_sel(self, evt):
ifself.player == None:
return
nval = self.scale_var.get()
sval = str(nval)
ifself.timeslider_last_val != sval:
self.timeslider_last_update = time.time()
mval = "%.0f" % (nval * 1000)
self.player.set_time(int(mval)) # expects milliseconds
defvolume_sel(self, evt):
ifself.player == None:
return
volume = self.volume_var.get()
if volume > 100:
volume = 100
ifself.player.audio_set_volume(volume) == -1:
self.errorDialog("Failed to set volume")
defOnToggleVolume(self, evt):
is_mute = self.player.audio_get_mute()
self.player.audio_set_mute(not is_mute)
self.volume_var.set(self.player.audio_get_volume())
defOnSetVolume(self):
volume = self.volume_var.get()
print("volume= ", volume)
if volume > 100:
volume = 100
ifself.player.audio_set_volume(volume) == -1:
self.errorDialog("Failed to set volume")
deferrorDialog(self, errormessage):
edialog = Tk.tkMessageBox.showerror(self, 'Error', errormessage)
defTk_get_root():
if not hasattr(Tk_get_root, "root"):
Tk_get_root.root= Tk()
returnTk_get_root.root
def _quit():
print("_quit: bye")
root = Tk_get_root()
root.quit()
root.destroy()
os._exit(1)
if __name__ == "__main__":
root = Tk()
root.protocol("WM_DELETE_WINDOW", _quit)
player = Player(root, title="tkintervlc")
root.mainloop()
