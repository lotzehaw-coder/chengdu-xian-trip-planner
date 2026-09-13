@echo off
rem Runs every 30 min via Windows Task Scheduler ("Trip planner - collect votes"). Log: C:\Users\User\wa-probe\logs\collect_votes.log
cd /d "C:\Users\User\Documents\chengdu-xian-trip-planner\tools"
echo ==== %DATE% %TIME% >> "C:\Users\User\wa-probe\logs\collect_votes.log"
"C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe" collect_votes.py >> "C:\Users\User\wa-probe\logs\collect_votes.log" 2>&1
