#NoTrayIcon
#RequireAdmin

; ���̽� 2.7�� ��ġ�Ǿ� �ֳ�?

If Not FileExists("C:\python27\pythonw.exe") Then 
PyInstall()
Else
UpgradeModules()
EndIf

Func PyInstall()
$hInstall = guicreate("���̽� ��ġ", 300, 100)
$lbl = guictrlcreatelabel("Python 2.7.11�� ��ġ�մϴ�. �۾��� ��ĥ ������ ��ٷ� �ּ���.", 10, 10, 280, 80)
guisetstate(@sw_show)

; ���̽� 2.7 �ּҿ��� �ٿ�ε�
$url = (@OSARCH = "x86")? "https://www.python.org/ftp/python/2.7.11/python-2.7.11.msi" : "https://www.python.org/ftp/python/2.7.11/python-2.7.11.amd64.msi"
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
guictrlsetdata($lbl, "���̽� ��ġ ������ �ٿ�ε��߽��ϴ�. ���� ��ġ�մϴ�. ��ø� ��ٷ� �ּ���.")
Else
Exit MsgBox(0, "�ٿ�ε� ����", "��ü ������ ��� �ٿ�ε� ���� ���� �� �����ϴ�. ���α׷��� �ٽ� ������ �ּ���.")
EndIf

$pid = ShellExecute($tempfile, "/quiet")
if @error then exit msgbox(0, "��ġ ����", "�ٿ�ε� ���� ���̽� ��ġ ������ �������� ���߽��ϴ�.")
ProcessWaitClose($pid)

If FileExists("c:\python27\pythonw.exe") Then
UpgradeModules()
Else
Exit MsgBox(0, "��ġ ����", "���̽� ��ġ�� ���������� ��ġ�� ���߽��ϴ�. ��ġ�� �ߴ��մϴ�.", 5) 
EndIf
EndFunc

Func UpgradeModules()
sleep(500)
$hUpgrade = guicreate("�ʼ� ��� ���׷��̵�", 300, 100)
guictrlcreatelabel("�ʼ� ����� ���׷��̵��մϴ�. �۾��� ��ĥ ������ ��ٷ� �ּ���.", 10, 10, 280, 80)
guisetstate(@sw_show)

$pid2 = Run(@scriptdir & "\" & "module.bat")
if @error then exit msgbox(0, "��� ���׷��̵� ����", "�ʼ� ��� ���׷��̵忡 �����߽��ϴ�.", 5)
processwaitclose($pid2)
Exit msgbox(0, "��ġ �Ϸ�", "���α׷� ������ ���� �غ� �Ϸ��߽��ϴ�.", 5)
EndFunc
