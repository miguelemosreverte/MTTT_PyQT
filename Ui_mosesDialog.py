# -*- coding: utf-8 -*-

import os
import platform
import sys
from PyQt4.QtGui import QFileDialog

from util import (
    doAlert,
    doQuestion,
    )


class MosesDialog():
    def __init__(self):
        pass

    def findRegistryPath(self):
        import _winreg
        key = None
        path = None
        try:
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
            key = _winreg.OpenKey(
                reg, r'Software\Moses Core Team\MosesDecoder')
            value, type = _winreg.QueryValueEx(key, 'Path')
            path = value
        except Exception, e:
            print >> sys.stderr, str(e)
            return None
        finally:
            if key:
                _winreg.CloseKey(key)
        return path

    def checkMosesInstall(self):
        # TODO: TRY catch OSError when permission denied!!
        file_content = [f for f in os.listdir(directory)]
        moses_files = ["/scripts/tokenizer/tokenizer.perl",
                       "/scripts/recaser/truecase.perl",
                       "/scripts/training/clean-corpus-n.perl",
                       "/bin/lmplz",
                       "/bin/build_binary",
                       "/scripts/training/train-model.perl",
                       "/bin/moses"
                      ]
        if self.is_windows:
            moses_files = [f.replace("/", "\\")
                           for f in moses_files]
            moses_files = [f + ".exe"
                           for f in moses_files
                           if "/bin" in f]
        is_valid = True
        for mfile in moses_files:
            is_valid = is_valid and os.path.isfile(directory + mfile)
        return is_valid

    def detect(self):
        doQuestion(
                'Cannot find Moses installation, click "Yes" to '
                'manually set the Moses path, click "No" to exit.')
        # If not found, use a dialog.
        startdir = 'C:\\'
        if "ProgramFiles(x86)" in os.environ:
            startdir = os.environ["ProgramFiles(x86)"]
        elif "ProgramFiles" in os.environ:
            startdir = os.environ["ProgramFiles"]
        else:
            pass
        dialog = QFileDialog(None, directory=startdir)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setOptions(QFileDialog.ShowDirsOnly)
        if dialog.exec_():
            self.mosesPath = str(dialog.selectedFiles()[0])
            return self.mosesPath
        else:
            doAlert("Failed to find Moses Installation path, exit.")
            return "Failed to find Moses Installation path, exit."

    def getMosesPath(self):
        return self.mosesPath

    def getMosesCmd(self):
        return os.path.join(self.mosesPath, 'moses-cmd.exe')

    def getTokenizer(self):
        return os.path.join(self.mosesPath, 'tokenizer.exe')

    def getDetokenizer(self):
        return os.path.join(self.mosesPath, 'detokenizer.exe')

    def getTruecase(self):
        return os.path.join(self.mosesPath, 'truecase.exe')

    def getDetruecase(self):
        return os.path.join(self.mosesPath, 'detruecase.exe')
