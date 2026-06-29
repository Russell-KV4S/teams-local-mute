#Requires AutoHotkey v2.0
#SingleInstance Force

; Run as admin so the hotkey works even when an elevated app (like Teams) has focus
if !A_IsAdmin {
    Run('*RunAs "' . A_ScriptFullPath . '"')
    ExitApp()
}

; ---------------------------------------------------------------------------
; CONFIGURATION
; ---------------------------------------------------------------------------
; The Python script must be in the same folder as this AHK file
PythonScriptName := "teams_toggle.py"
PythonPath := A_ScriptDir . "\" . PythonScriptName

; ---------------------------------------------------------------------------
; HOTKEY ASSIGNMENT
; ---------------------------------------------------------------------------
; Default: Pause/Break Key. Change this to F13, F12, etc. as needed.
Pause::
{
    ; Check if the python file actually exists before trying to run it
    if !FileExist(PythonPath)
    {
        MsgBox("Error: Could not find " . PythonScriptName . "`n`nPlease make sure the Python script is in the same folder as this AHK file.")
        return
    }

    ; Run Python hidden
    ; We wrap PythonPath in double quotes to handle spaces in folder names (e.g. "OneDrive - Personal")
    try
    {
        Run('pythonw.exe "' . PythonPath . '"', A_ScriptDir, "Hide")
        SoundBeep(750, 150) ; Audio confirmation
    }
    catch as err
    {
        MsgBox("Failed to run Python script.`n`nError: " . err.Message)
    }
}