import win32ui


def open_select_box():
    dlg = win32ui.CreateFileDialog(1)
    dlg.SetOFNInitialDir('C:/')
    dlg.DoModal()
    filename = dlg.GetPathName()
    return filename
