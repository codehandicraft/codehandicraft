ps aux | fgrep 'emailProcess.py' | fgrep -v grep | awk '{print $2}' | xargs kill -9
nohup /usr/bin/python3  -u emailProcess.py >> log/codehandicraft.log.$(date +"%Y%m%d") 2>&1 &

echo 'rm input file, date='$(date -v-3d +"%Y%m%d")
rm -rf */input/$(date -v-3d +"%Y%m%d")*
echo 'rm log file, date='$(date -v-15d +"%Y%m%d")
rm -rf log/codehandicraft.log.$(date -v-15d +"%Y%m%d")