@echo off
title NOVA AI

cd /d "D:\aiassistant"

echo Starting Backend...
start cmd /k "cd backened && python app.py"

timeout /t 4 >nul

echo Starting Frontend...
start cmd /k "cd frontend && npm run dev"

timeout /t 6 >nul

start http://localhost:5173

exit