#NoTrayIcon
#RequireAdmin

; ���̽� 2.7�� ��ġ�Ǿ� �ֳ�?

If Not FileExists("C:\python27\pythonw.exe") Then 
PyInstall()
Else
UpgradeModules()
EndIf

Func PyInstall()
MsgBox(0, "�ٿ�ε� ����", "���̽� 2.7.11 �ٿ�ε带 �����մϴ�.", 5)
; ���̽� 2.7 �ּҿ��� �ٿ�ε�
$url = "https://www.python.org/ftp/python/2.7.11/python-2.7.11.msi" 

$py_size = InetGetSize($url)

$tempfile = @TempDir & "\" & random(1000000, 99999999, 1) & ".msi"
$f = InetGet($url, $tempfile, 0, 1)
$p = 0

Do
Sleep(250)
$info = InetGetInfo($f, -1)
If $info[4] Then Exit Msgbox(0, "�ٿ�ε� ����", "������ �ٿ�ε��� �� �����ϴ�. ���α׷��� �����մϴ�.")
$q = int($info[0] * 100 / $py_size)
if $p < $q Then
$p = $q
Beep($p * 10 + 500, 100)
EndIf
Until $info[2]

If FileGetSize($tempfile) = $py_size Then 
MsgBox(0, "�ٿ�ε� ����", "���̽� ��ġ ������ �ٿ�ε��߽��ϴ�. ���� ��ġ�մϴ�. ��ø� ��ٷ� �ּ���.", 5)
Else
Exit MsgBox(0, "�ٿ�ε� ����", "��ü ������ ��� �ٿ�ε� ���� ���� �� �����ϴ�. ���α׷��� �ٽ� ������ �ּ���.")
EndIf

$pid = ShellExecute($tempfile, "/quiet")
if @error then exit msgbox(0, "��ġ ����", "�ٿ�ε� ���� ���̽� ��ġ ������ �������� ���߽��ϴ�.")
ProcessWaitClose($pid)

If FileExists("c:\python27\pythonw.exe") Then
UpgradeModules()
Else
Exit MsgBox(0, "��ġ ����", "���̽� ��ġ�� ���������� ��ġ�� ���߽��ϴ�. ��ġ�� �ߴ��մϴ�.") 
EndIf
EndFunc

Func UpgradeModules()
sleep(500)
MsgBox(0, "��� ���׷��̵�", "�� ���α׷��� �ʿ��� ����� �ֽ����� ���׷��̵��մϴ�.", 5)
$pid2 = Run(@scriptdir & "\���_���׷��̵�.bat")
if @error then exit msgbox(0, "��� ���׷��̵� ����", "�ʼ� ��� ���׷��̵忡 �����߽��ϴ�. �������� ���_���׷��̵�.bat ������ ������ ������.")
processwaitclose($pid2)
Exit msgbox(0, "��ġ �Ϸ�", "���α׷� ������ ���� �غ� �Ϸ��߽��ϴ�.", 5)
EndFunc
