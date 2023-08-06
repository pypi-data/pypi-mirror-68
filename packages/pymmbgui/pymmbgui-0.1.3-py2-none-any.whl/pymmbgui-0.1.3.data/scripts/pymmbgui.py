#!python

import sys
import wx
import os, os.path

import PyMMB
from fileinput import filename

from ._version import get_versions
__version__ = get_versions()['version']

ID_NEW = wx.NewId()
ID_NEW_MMB = wx.NewId()
ID_NEW_SSD = wx.NewId()
ID_OPEN = wx.ID_OPEN
ID_CLOSE = wx.ID_CLOSE
ID_EXIT = wx.NewId()

ID_DISC_COPY_IN = wx.NewId()
ID_DISC_COPY_OUT = wx.NewId()
ID_DISC_LOCK = wx.NewId()
ID_DISC_UNLOCK = wx.NewId()
ID_DISC_FORMAT = wx.NewId()
ID_DISC_UNFORMAT = wx.NewId()

ID_FILE_COPY_IN = wx.NewId()
ID_FILE_COPY_OUT = wx.NewId()
ID_FILE_INFO = wx.NewId()

ID_ABOUT = wx.ID_ABOUT

ID_RECENT = []

class MenuMakerMixin(object):
    "A mixin that knows how to construct a menu"
    MENU = []
    _doneSep = False
    def __init__(self, config):
        "Construct a menu and set it as this object's menubar"
        self.menubar = wx.MenuBar()
        for menuList in self.MENU:
            menu = self.createSubMenu(menuList[1])
            self.menubar.Append(menu, menuList[0])
        self.SetMenuBar(self.menubar)
        self.replaceRecent(config)

    def replaceRecent(self, config):
        "Replace the recent files list"
        # Find out how many items we should maintain
        maxRecent = config.ReadInt("/recent/max", 5)
        while len(ID_RECENT) < maxRecent:
            ID_RECENT.append(wx.NewId())
        imgMenu = self.menubar.GetMenu(0)
        for recent in range(1, maxRecent + 1):
            if imgMenu.FindItemById(ID_RECENT[recent - 1]) != None:
                item = imgMenu.Remove(ID_RECENT[recent - 1])
                item.Destroy()
        insPos = imgMenu.GetMenuItemCount() - 2
        for recent in range(1, maxRecent + 1):
            filename = config.Read("/recent/%d" % recent, "")
            if filename != "":
                if not self._doneSep:
                    self._doneSep = True
                    imgMenu.InsertSeparator(insPos)
                    insPos = insPos + 1
                mi = imgMenu.Insert(insPos, ID_RECENT[recent - 1], os.path.basename(filename), "Open " + filename)
                wx.EVT_MENU(self, ID_RECENT[recent - 1], self.OnRecent)
                insPos = insPos + 1

    def createSubMenu(self, menuStruct):
        menu = wx.Menu()
        for menuItemDict in menuStruct:
            if menuItemDict.has_key('menu'):
                menu.AppendSubMenu(self.createSubMenu(menuItemDict['menu']), menuItemDict['label'], menuItemDict['help'])
            elif menuItemDict['id'] == None:
                menu.AppendSeparator()
            else:
                mi = menu.Append(menuItemDict['id'], menuItemDict['label'], menuItemDict['help'])
                if menuItemDict.has_key('handler'):
                    wx.EVT_MENU(self, menuItemDict['id'], eval("self.%s" % (menuItemDict['handler'])))
                else:
                    mi.Enable(False)
        return menu

class ImageView(wx.MDIChildFrame, MenuMakerMixin):
    "Base class for all image types"
    def __init__(self, parent, image, name, title):
        wx.MDIChildFrame.__init__(self, parent, -1, title)
        MenuMakerMixin.__init__(self, parent.config)
        self.parent = parent
        self.name = name
        self.image = image

        self.SetSize(self.GetSize())
        self.SetupControls()

        wx.EVT_CLOSE(self, self.OnClose)

        # Show is required on Unix, but throws an exception on Windows
        # if the previous MDI child is maximized. This is safe to ignore
        try:
            self.Show()
        except:
            pass

    def SetupControls(self):
        "Set the columns for the list control"
        tID = wx.NewId()
        self.ctlList = wx.ListCtrl(
            self,
            tID,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.LC_REPORT | wx.SUNKEN_BORDER
        )
        self.currentItem = 0
        wx.EVT_LIST_ITEM_SELECTED(self, tID, self.OnItemSelected)
        wx.EVT_LIST_ITEM_DESELECTED(self, tID, self.OnItemDeselected)
        wx.EVT_LEFT_DCLICK(self.ctlList, self.OnDoubleClick)

    @classmethod
    def Open(cls, parent, filename):
        "Open a new window with this file, if it is not already open"
        image = None
        if type(filename) != type("") and type(filename) != type(u""):
            image = filename
            if image.filename != None:
                filename = image.filename
                title = os.path.basename(filename)
            else:
                filename = image._mmb.filename + ":" + image.title
                title = os.path.basename(image._mmb.filename) + " : " + image.title
        else:
            title = os.path.basename(filename)
        if parent.windows.has_key(filename):
            parent.windows[filename].Activate()
        else:
            if image == None:
                image = cls._getImage(filename)
            parent.windows[filename] = cls(parent, image, filename, title)
        return parent.windows[filename]

    @classmethod
    def _getImage(cls, filename):
        "Return an image of the correct type"
        return None

    def Destroy(self, *args, **kwargs):
        del self.parent.windows[self.name]
        return wx.MDIChildFrame.Destroy(self, *args, **kwargs)

    def OnItemDeselected(self, event):
        ""
        pass

    def OnItemSelected(self, event):
        ""
        pass

    def OnDoubleClick(self, event):
        ""
        pass

    def OnRecent(self, event):
        "Pass up to the parent"
        self.parent.OnRecent(event)

    def OnNewMMB(self, event):
        "Pass up to the parent"
        self.parent.OnNewMMB(event)

    def OnNewSSD(self, event):
        "Pass up to the parent"
        self.parent.OnNewSSD(event)

    def OnOpen(self, event):
        "Pass up to the parent"
        self.parent.OnOpen(event)

    def OnClose(self, event):
        "Handle requests to close an image"
        self.Destroy()

    def OnExit(self, event):
        "Pass up to the parent"
        self.parent.OnExit(event)

    def OnAbout(self, event):
        "Pass up to the parent"
        self.parent.OnAbout(event)

class MMBView(ImageView):
    MENU = [
        ['&Image', [
                {'label': '&New', 'help': 'Create a new image file', 'menu': [
                        {'id': ID_NEW_MMB, 'label': '&MMB\tCTRL+ALT+M', 'help': 'Create a new MMB image file', 'handler': 'OnNewMMB'},
                        {'id': ID_NEW_SSD, 'label': '&SSD\tCTRL+ALT+S', 'help': 'Create a new SSD image file', 'handler': 'OnNewSSD'},
                    ]
                },
                {'id': ID_OPEN, 'label': '&Open\tALT+O', 'help': 'Open an image file', 'handler': 'OnOpen'},
                {'id': ID_CLOSE, 'label': '&Close\tALT+C', 'help': 'Close the current image file', 'handler': 'OnClose'},
                {'id': None},
                {'id': ID_EXIT, 'label': 'E&xit\tALT+X', 'help': 'Close all image files and exit', 'handler': 'OnExit'},
            ]
        ],
        ['&Disc', [
                {'id': ID_DISC_COPY_IN, 'label': 'Copy &In', 'help': 'Copy an SSD image into a disc slot in the MMB image', 'handler': 'OnCopyIn'},
                {'id': ID_DISC_COPY_OUT, 'label': 'Copy &Out', 'help': 'Copy a disc slot from the MMB image out to an SSD image', 'handler': 'OnCopyOut'},
                {'id': None},
                {'id': ID_DISC_LOCK, 'label': '&Lock', 'help': ''},
                {'id': ID_DISC_UNLOCK, 'label': 'Unlo&ck', 'help': ''},
                {'id': None},
                {'id': ID_DISC_FORMAT, 'label': '&Format', 'help': ''},
                {'id': ID_DISC_UNFORMAT, 'label': '&Unformat', 'help': ''},
            ]
        ],
        ['&Help', [
                {'id': ID_ABOUT, 'label': '&About', 'help': '', 'handler': 'OnAbout'},
            ]
        ],
    ]

    def __init__(self, parent, image, name, title):
        "Construct the view"
        ImageView.__init__(self, parent, image, name, title)
        self.GetMenuBar().EnableTop(1, False)
        for disc in self.image.discs:
            if disc.exists:
                idx = self.ctlList.InsertStringItem(disc.id, str(disc.id))
                if disc.formatted:
                    self.ctlList.SetStringItem(idx, 1, disc.title)
                    flags = ""
                    if disc.locked:
                        flags = "R/O"
                    self.ctlList.SetStringItem(idx, 2, flags)
                else:
                    self.ctlList.SetStringItem(idx, 1, "-")
                    self.ctlList.SetStringItem(idx, 2, "Empty")

    @classmethod
    def _getImage(cls, filename):
        "Return an MMB object"
        return PyMMB.mmb.mmb(filename)

    def SetupControls(self):
        "Add the correct columns for MMB images"
        ImageView.SetupControls(self)
        self.ctlList.InsertColumn(0, "ID", wx.LIST_FORMAT_RIGHT, 50)
        self.ctlList.InsertColumn(1, "Title", wx.LIST_FORMAT_LEFT, 100)
        self.ctlList.InsertColumn(2, "Flags", wx.LIST_FORMAT_RIGHT, 100)

    def OnItemDeselected(self, event):
        ""
        #disc = self.image.disc[]
        if self.ctlList.GetSelectedItemCount() == 0:
            self.GetMenuBar().EnableTop(1, False)
        else:
            self.GetMenuBar().EnableTop(1, True)

    def OnItemSelected(self, event):
        ""
        self.GetMenuBar().EnableTop(1, True)
        disc = self.image.discs[self.ctlList.GetFocusedItem()]
        #print disc.title
        pass

    def OnDoubleClick(self, event):
        "Open a disc image when it is double clicked"
        disc = self.image.discs[self.ctlList.GetFocusedItem()]
        SSDView.Open(self.parent, disc)

    def OnCopyIn(self, event):
        dlg = wx.FileDialog(self, style = wx.OPEN)
        dlg.SetWildcard("SSD disc image (*.ssd)|*.ssd")
        if dlg.ShowModal() == wx.ID_OK:
            pass
#            self.path = dlg.GetPath()
#            self.SetTitle(self.title + ' - ' + self.path)
#            self.bookset = BookSet()
#            self.bookset.load(self.path)
#            win = JournalView(self, self.bookset, ID_EDIT)
#            self.views.append((win, ID_JRNL))
        dlg.Destroy()

    def OnCopyOut(self, event):
        dlg = wx.FileDialog(self, style = wx.SAVE)
        dlg.SetWildcard("SSD disc image (*.ssd)|*.ssd")
        if dlg.ShowModal() == wx.ID_OK:
            pass
#            self.path = dlg.GetPath()
#            self.SetTitle(self.title + ' - ' + self.path)
#            self.bookset = BookSet()
#            self.bookset.load(self.path)
#            win = JournalView(self, self.bookset, ID_EDIT)
#            self.views.append((win, ID_JRNL))
        dlg.Destroy()

class SSDView(ImageView):
    MENU = [
        ['&Image', [
                {'label': '&New', 'help': 'Create a new image file', 'menu': [
                        {'id': ID_NEW_MMB, 'label': '&MMB\tCTRL+ALT+M', 'help': 'Create a new MMB image file', 'handler': 'OnNewMMB'},
                        {'id': ID_NEW_SSD, 'label': '&SSD\tCTRL+ALT+S', 'help': 'Create a new SSD image file', 'handler': 'OnNewSSD'},
                    ]
                },
                {'id': ID_OPEN, 'label': '&Open\tALT+O', 'help': 'Open an image file', 'handler': 'OnOpen'},
                {'id': ID_CLOSE, 'label': '&Close\tALT+C', 'help': 'Close the current image file', 'handler': 'OnClose'},
                {'id': None},
                {'id': ID_EXIT, 'label': 'E&xit\tALT+X', 'help': 'Close all image files and exit', 'handler': 'OnExit'},
            ]
        ],
        ['&File', [
                {'id': ID_FILE_COPY_IN, 'label': 'Copy &In', 'help': 'Copy a file into the SSD image', 'handler': 'OnCopyIn'},
                {'id': ID_FILE_COPY_OUT, 'label': 'Copy &Out', 'help': 'Copy a file out of the SSD image', 'handler': 'OnCopyOut'},
                {'id': None},
                {'id': ID_FILE_INFO, 'label': '&Info', 'help': ''},
            ]
        ],
        ['&Help', [
                {'id': ID_ABOUT, 'label': '&About', 'help': '', 'handler': 'OnAbout'},
            ]
        ],
    ]

    def __init__(self, parent, image, name, title, parentMMBView = None):
        "Construct the view"
        ImageView.__init__(self, parent, image, name, title)
        self.parentMMBView = parentMMBView
        self.ctlTitle.SetValue(image.title)
        self.ctlCycle.SetValue(str(image.cycle))
        self.ctlBootOpt.SetSelection(image.opt)
        for dfsfile in self.image.files:
            idx = self.ctlList.InsertStringItem(sys.maxint, dfsfile.dir)
            self.ctlList.SetStringItem(idx, 1, dfsfile.name)
            if dfsfile.locked:
                self.ctlList.SetStringItem(idx, 2, "L")
            self.ctlList.SetStringItem(idx, 3, "%06x" % dfsfile.load_addr)
            self.ctlList.SetStringItem(idx, 4, "%06x" % dfsfile.exec_addr)
            self.ctlList.SetStringItem(idx, 5, "%06x" % dfsfile.length)
            self.ctlList.SetStringItem(idx, 6, "%03x" % dfsfile.start_sector)

    @classmethod
    def _getImage(cls, filename):
        "Return an MMB object"
        return PyMMB.dfs.dfs(filename)

    def SetupControls(self):
        "Add the correct columns for MMB images"
        ImageView.SetupControls(self)

        self.lblTitle = wx.StaticText(self, -1, "  Title")
        self.ctlTitle = wx.TextCtrl(self, -1, "--TITLE--")
        self.lblCycle = wx.StaticText(self, -1, "  Cycle")
        self.ctlCycle = wx.TextCtrl(self, -1, "0")
        self.lblBootOpt = wx.StaticText(self, -1, "  Boot Option")
        self.ctlBootOpt = wx.ComboBox(self, -1, choices = ["Nothing", "*LOAD $.!BOOT", "*RUN $.!BOOT", "*EXEC $.!BOOT"], style = wx.CB_DROPDOWN | wx.CB_DROPDOWN)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer_1)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_1.Add(self.ctlList, 1, wx.EXPAND, 0)
        sizer_2.Add(self.lblTitle, 0, wx.ALIGN_CENTER_VERTICAL, 1)
        sizer_2.Add(self.ctlTitle, 2, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.AddSpacer(10)
        sizer_2.Add(self.lblCycle, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(self.ctlCycle, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.AddSpacer(10)
        sizer_2.Add(self.lblBootOpt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(self.ctlBootOpt, 4, wx.ALIGN_CENTER_VERTICAL, 0)
        #sizer_1.Fit(self)

        self.ctlTitle.SetToolTipString("The title for this disc")
        self.ctlCycle.SetToolTipString("The current cycle value for this disc")
        self.ctlCycle.Enable(False)
        self.ctlBootOpt.SetToolTipString("The boot options for this disc - When SHIFT-BREAK is pressed, I should ...")

        self.ctlList.InsertColumn(0, "D", wx.LIST_FORMAT_RIGHT, 20)
        self.ctlList.InsertColumn(1, "Name", wx.LIST_FORMAT_LEFT, 100)
        self.ctlList.InsertColumn(2, "Flg", wx.LIST_FORMAT_RIGHT, 30)
        self.ctlList.InsertColumn(3, "Load Addr", wx.LIST_FORMAT_RIGHT, 75)
        self.ctlList.InsertColumn(4, "Exec Addr", wx.LIST_FORMAT_RIGHT, 75)
        self.ctlList.InsertColumn(5, "Size", wx.LIST_FORMAT_RIGHT, 75)
        self.ctlList.InsertColumn(6, "Sector", wx.LIST_FORMAT_RIGHT, 60)

    def OnCopyIn(self, event):
        dlg = wx.FileDialog(self, style = wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            pass
#            self.path = dlg.GetPath()
#            self.SetTitle(self.title + ' - ' + self.path)
#            self.bookset = BookSet()
#            self.bookset.load(self.path)
#            win = JournalView(self, self.bookset, ID_EDIT)
#            self.views.append((win, ID_JRNL))
        dlg.Destroy()

    def OnCopyOut(self, event):
        dlg = wx.FileDialog(self, style = wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            pass
#            self.path = dlg.GetPath()
#            self.SetTitle(self.title + ' - ' + self.path)
#            self.bookset = BookSet()
#            self.bookset.load(self.path)
#            win = JournalView(self, self.bookset, ID_EDIT)
#            self.views.append((win, ID_JRNL))
        dlg.Destroy()

class PyMMBWindow(wx.MDIParentFrame, MenuMakerMixin):
    "Main window of the program"
    MENU = [
        ['&Image', [
                {'label': '&New', 'help': 'Create a new image file', 'menu': [
                        {'id': ID_NEW_MMB, 'label': '&MMB\tCTRL+ALT+M', 'help': 'Create a new MMB image file', 'handler': 'OnNewMMB'},
                        {'id': ID_NEW_SSD, 'label': '&SSD\tCTRL+ALT+S', 'help': 'Create a new SSD image file', 'handler': 'OnNewSSD'},
                    ]
                },
                {'id': ID_OPEN, 'label': '', 'help': 'Open an image file', 'handler': 'OnOpen'},
                {'id': None},
                {'id': ID_EXIT, 'label': 'E&xit\tALT+X', 'help': 'Close all image files and exit', 'handler': 'OnExit'},
            ]
        ],
        ['&Help', [
                {'id': ID_ABOUT, 'label': '', 'help': '', 'handler': 'OnAbout'},
            ]
        ],
    ]

    def __init__(self, parent, ID, title):
        self.config = wx.Config(appName = "PyMMBgui", vendorName = "TLSPU")
        wx.MDIParentFrame.__init__(self,
            parent,
            ID,
            title,
            size = (600, 450),
            style = wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER
        )
        self.windows = {}
        MenuMakerMixin.__init__(self, self.config)
        sb = self.CreateStatusBar()

    def _recordRecentFile(self, filename):
        ""
        maxRecent = self.config.ReadInt("/recent/max", 5)
        # Check if this file is currently in the recent list
        for recent in range(1, maxRecent + 1):
            if self.config.Read("/recent/%d" % recent, "") == filename:
                break
        if recent < 1:
            recent = maxRecent
        for recent in range(recent - 1, 0, -1):
            self.config.Write("/recent/%d" % (recent + 1), self.config.Read("/recent/%d" % recent, ""))
        self.config.Write("/recent/1", filename)
        self.replaceRecent(self.config)
        for wnd in self.windows.values():
            wnd.replaceRecent(self.config)

    def OnRecent(self, event):
        "A recent file name has been clicked - Find which and open it"
        event.GetId(), ID_RECENT[0]
        recent = ID_RECENT.index(event.GetId()) + 1
        filename = self.config.Read("/recent/%d" % recent, "")
        self._recordRecentFile(filename)
        if filename[-4:].lower() == ".mmb":
            MMBView.Open(self, filename)
        else:
            SSDView.Open(self, filename)

    def OnNewMMB(self, event):
        "Ask what type of image to create"
        dlg = wx.FileDialog(self, message = "Create new MMB file", style = wx.SAVE)
        dlg.SetWildcard("MMB disc image bundle (*.MMB,*.mmb)|*.MMB;*.mmb")
        if dlg.ShowModal() == wx.ID_OK:
            if os.path.exists(dlg.GetPath()):
                wx.MessageBox("File already exists");
                return
            dlg2 = wx.SingleChoiceDialog(self, message = "How many entries should the MMB contain?", caption = "Number of entries", choices = ["50", "100", "200", "400", "511"])
            if dlg2.ShowModal() == wx.ID_OK:
                self._recordRecentFile(dlg.GetPath())
                PyMMB.mmb.mmb.create(dlg.GetPath(), int(dlg2.GetStringSelection())).close()
                MMBView(self, dlg.GetPath())

    def OnNewSSD(self, event):
        "Ask what type of image to create"
        dlg = wx.FileDialog(self, message = "Create new MMB file", style = wx.SAVE)
        dlg.SetWildcard("SSD disc image (*.ssd)|*.ssd")
        if dlg.ShowModal() == wx.ID_OK:
            if os.path.exists(dlg.GetPath()):
                wx.MessageBox("File already exists");
                return
            self._recordRecentFile(dlg.GetPath())
            PyMMB.dfs.dfs.new(dlg.GetPath()).close()
            SSDView.Open(self, dlg.GetPath())

    def OnOpen(self, event):
        dlg = wx.FileDialog(self, style = wx.OPEN)
        dlg.SetWildcard("MMB disc image bundle (*.MMB,*.mmb)|*.MMB;*.mmb|SSD disc image (*.ssd)|*.ssd")
        if dlg.ShowModal() == wx.ID_OK:
            self._recordRecentFile(dlg.GetPath())
            if dlg.GetPath()[-4:].lower() == ".mmb":
                MMBView.Open(self, dlg.GetPath())
            else:
                SSDView.Open(self, dlg.GetPath())
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.SetDevelopers(["Adrian Hungate <adrian@tlspu.com>"])
        info.SetName("PyMMBgui")
        info.SetVersion("%s (PyMMB: %s)" % (__version__, PyMMB.__version__))
        info.SetWebSite(("https://projects.limbicly.com/bbc-micro/PyMMB", "PyMMB Site"))
        info.SetCopyright("Copyright (C) 2013-2020 Adrian Hungate")
        info.SetDescription("PyMMBgui - The cross platform BBC disc image program")
        info.SetLicence("""Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
""")
        wx.AboutBox(info)

class PyMMBgui(wx.App):
    def OnInit(self):
        frame = PyMMBWindow(None, -1, "PyMMB GUI")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = PyMMBgui(0)
    app.MainLoop()
