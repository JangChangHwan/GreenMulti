#NoTrayIcon
#RequireAdmin

; 파이썬 2.7이 설치되어 있나?

If Not FileExists("C:\python27\pythonw.exe") Then 
PyInstall()
Else
UpgradeModules()
EndIf

Func PyInstall()
$hInstall = guicreate("파이썬 설치", 300, 100)
$lbl = guictrlcreatelabel("Python 2.7.11을 설치합니다. 작업을 마칠 때까지 기다려 주세요.", 10, 10, 280, 80)
guisetstate(@sw_show)

; 파이썬 2.7 주소에서 다운로드
$url = (@OSARCH = "x86")? "https://www.python.org/ftp/python/2.7.11/python-2.7.11.msi" : "https://www.python.org/ftp/python/2.7.11/python-2.7.11.amd64.msi"
$py_size = InetGetSize($url)

$tempfile = @TempDir & "\" & random(1000000, 99999999, 1) & ".msi"
$f = InetGet($url, $tempfile, 0, 1)
$p = 0

Do
Sleep(250)
$info = InetGetInfo($f, -1)
If $info[4] Then Exit Msgbox(0, "다운로드 오류", "파일을 다운로드할 수 없습니다. 프로그램을 종료합니다.")
$q = int($info[0] * 100 / $py_size)
if $p < $q Then
$p = $q
Beep($p * 10 + 500, 100)
EndIf
Until $info[2]

If FileGetSize($tempfile) = $py_size Then 
guictrlsetdata($lbl, "파이썬 설치 파일을 다운로드했습니다. 이제 설치합니다. 잠시만 기다려 주세요.")
Else
Exit MsgBox(0, "다운로드 실패", "전체 파일을 모두 다운로드 하지 못한 것 같습니다. 프로그래을 다시 실행해 주세요.")
EndIf

$pid = ShellExecute($tempfile, "/quiet")
if @error then exit msgbox(0, "설치 실패", "다운로드 받은 파이썬 설치 파일을 실행하지 못했습니다.")
ProcessWaitClose($pid)

If FileExists("c:\python27\pythonw.exe") Then
UpgradeModules()
Else
Exit MsgBox(0, "설치 실패", "파이썬 설치를 정상적으로 마치지 못했습니다. 설치를 중단합니다.", 5) 
EndIf
EndFunc

Func UpgradeModules()
sleep(500)
$hUpgrade = guicreate("필수 모듈 업그레이드", 300, 100)
guictrlcreatelabel("필수 모듈을 업그레이드합니다. 작업을 마칠 때까지 기다려 주세요.", 10, 10, 280, 80)
guisetstate(@sw_show)

$pid2 = Run(@scriptdir & "\" & "module.bat")
if @error then exit msgbox(0, "모듈 업그레이드 실패", "필수 모듈 업그레이드에 실패했습니다.", 5)
processwaitclose($pid2)
Exit msgbox(0, "설치 완료", "프로그램 실행을 위한 준비를 완료했습니다.", 5)
EndFunc
