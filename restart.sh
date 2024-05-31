ps aux | fgrep 'emailProcess.py' | fgrep -v grep | awk '{print $2}' | xargs kill -9
nohup /usr/bin/python3  -u emailProcess.py >> log/codehandicraft.log.$(date +"%Y%m%d") 2>&1 &

echo 'rm input file, date='$(date -v-5d +"%Y%m%d")
rm -rf */input/$(date -v-5d +"%Y%m%d")*
rm -rf */input/$(date -v-6d +"%Y%m%d")*
rm -rf */input/$(date -v-7d +"%Y%m%d")*
rm -rf */input/$(date -v-8d +"%Y%m%d")*
rm -rf */input/$(date -v-9d +"%Y%m%d")*
echo 'rm log file, date='$(date -v-15d +"%Y%m%d")
rm -rf log/codehandicraft.log.$(date -v-15d +"%Y%m%d")
rm -rf log/codehandicraft.log.$(date -v-16d +"%Y%m%d")
rm -rf log/codehandicraft.log.$(date -v-17d +"%Y%m%d")
rm -rf log/codehandicraft.log.$(date -v-18d +"%Y%m%d")
rm -rf log/codehandicraft.log.$(date -v-19d +"%Y%m%d")
rm -rf log/codehandicraft.log.$(date -v-20d +"%Y%m%d")
rm -rf log/codehandicraft.log.$(date -v-21d +"%Y%m%d")