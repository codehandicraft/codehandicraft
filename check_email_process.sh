#! /bin/bash
ts=`date '+%Y-%m-%d %H:%M:%S'`

exist=`ps axu | fgrep ' emailProcess.py' | fgrep -v grep  | wc -l`
if [ $exist -lt 1 ]; then
	echo "$ts : gdims process not exist"
    # ps aux | fgrep 'emailProcess.py' | fgrep -v fgrep | awk '{print $2}' | xargs kill -9
    nohup /usr/bin/python3 -u emailProcess.py >> log/codehandicraft.log.$(date +"%Y%m%d") 2>&1 &
fi
echo "$ts : check gdims ok"

rm -rf */input/$(date -d '-10days' +"%Y%m%d")*
rm -rf log/codehandicraft.log.$(date -d '-10days' +"%Y%m%d")