#NotrayIcon
#RequireAdmin

if not $cmdline[0] then exit

$s = $CmdLine[1]
$DestFile = StringTrimRight($s, 4) & ".mp3"

convert()
exit 

func Convert()
$cmd = '"' & @ScriptDir & '\ffmpeg.exe" -y -i "' & $s & '" -vn -ar 44100 -ac 2 -ab 192 -f mp3 "' & $DestFile & '"'
$p = Run($cmd, "", @SW_HIDE, 0x8)
If @error Then Exit EBeep(4)

$dura = 0
$per = 0

while ProcessExists($p)
sleep(100)
$ts = StdOutRead($p)
if not $dura then 
$aDura = stringregexp($ts, 'Duration: (\d{2}:\d{2}:\d{2})', 1)
if @error then continueloop
$ti = stringsplit($aDura[0], ":", 2)
$dura = $ti[0] * 3600 + $ti[1] * 60 + $ti[2]
endif

$aTime = StringRegExp($ts, 'time=(\d+)', 1)
if @error then continueloop
$cp = floor($aTime[0] / $dura * 100)
if $cp >= $per then 
say($cp)
$per += 5
endif
wend

if $per then 
soundplay(@scriptdir & "\sound\convert.wav", 1)
FileDelete($s)
endif
endfunc



Func EBeep($n=1)
if $n < 1 then return
For $i=1 to $n
Beep(1000, 100)
Next
EndFunc


func say($n)
beep(300 + $n * 12, 100)
endfunc
