ps aux | fgrep 'emailProcess.py' | fgrep -v grep | awk '{print $2}' | xargs kill -9
nohup python -u emailProcess.py >> log/codehandicraft.log.$(date +"%Y%m%d") 2>&1 &
