@echo off
rem Joins the 14 parts into patch-y.mpq (the file was too big to transfer in one piece).
cd /d "%~dp0"
if exist patch-y.mpq del patch-y.mpq
copy /b patch-y.mpq.part0 + patch-y.mpq.part1 + patch-y.mpq.part2 + patch-y.mpq.part3 + patch-y.mpq.part4 + patch-y.mpq.part5 + patch-y.mpq.part6 + patch-y.mpq.part7 + patch-y.mpq.part8 + patch-y.mpq.part9 + patch-y.mpq.part10 + patch-y.mpq.part11 + patch-y.mpq.part12 + patch-y.mpq.part13 patch-y.mpq >nul
if exist patch-y.mpq (del patch-y.mpq.part0 patch-y.mpq.part1 patch-y.mpq.part2 patch-y.mpq.part3 patch-y.mpq.part4 patch-y.mpq.part5 patch-y.mpq.part6 patch-y.mpq.part7 patch-y.mpq.part8 patch-y.mpq.part9 patch-y.mpq.part10 patch-y.mpq.part11 patch-y.mpq.part12 patch-y.mpq.part13 & echo patch-y.mpq is ready.) else echo Join failed.
pause
