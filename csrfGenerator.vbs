Set objShell = CreateObject("WScript.Shell")

pythonCmd1 = "py.exe .\server.py"
objShell.Run pythonCmd1, 0, True ' Running listener.py 

' Get HTTP Method selection from user (1, 2, or 3)
methodChoice = InputBox("Select HTTP Method by entering the number:" & vbCrLf & vbCrLf & _
    "1 - POST" & vbCrLf & "2 - HEAD" & vbCrLf & "3 - GET", "CSRF PoC Generator", "")

' Map user input to HTTP method
If methodChoice = "1" Then
    method = "POST"
ElseIf methodChoice = "2" Then
    method = "HEAD"
ElseIf methodChoice = "3" Then
    method = "GET"
Else
    MsgBox "Invalid selection. Please enter 1, 2, or 3.", vbCritical, "Error"
    WScript.Quit
End If

' Get Encoding Type selection from user (1, 2, or 3)
encodingChoice = InputBox("Select Encoding Type by entering the number:" & vbCrLf & vbCrLf & _
    "1 - application/x-www-form-urlencoded" & vbCrLf & _
    "2 - multipart/plain" & " " & "upcoming" & vbCrLf & _
    "3 - multipart/form-data" & " " & "upcoming", "CSRF PoC Generator", "")

' Map user input to Encoding Type
If encodingChoice = "1" Then
    encoding = "application/x-www-form-urlencoded"
' ElseIf encodingChoice = "2" Then
'     encoding = "multipart/plain"
' ElseIf encodingChoice = "3" Then
'     encoding = "multipart/form-data"
Else
    MsgBox "Invalid selection. Please enter 1, 2, or 3.", vbCritical, "Error"
    WScript.Quit 
End If

data = InputBox("Enter Data (e.g., value1=foo&value2=bar):", "CSRF PoC Generator", "")
uri = InputBox("Enter Target URI (e.g., https://domain.com):", "CSRF PoC Generator", "")
filename = InputBox("Enter the output file name to be saved (e.g., filename.html):", "CSRF PoC Generator", "") 
' Check if the filename contains .html, if not, append it
If LCase(Right(filename, 5)) <> ".html" Then
    filename = filename & ".html"
End If

MsgBox "The file will be saved as: " & filename, vbInformation, "File Name Confirmation"

' Construct the Python command
pythonCmd = "py.exe .\listener.py """ & method & """ """ & encoding & """ """ & data & """ """ & uri & """ """ & filename & """"
objShell.Run pythonCmd, 1, True ' Run listener.py with the inputs

' Display confirmation message
MsgBox "Data sent successfully!", vbInformation, "Success"
