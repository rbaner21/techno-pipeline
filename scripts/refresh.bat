@echo off
REM Change to the project directory
cd /d %~dp0..

REM Activate conda environment
call conda activate techno-pipeline

REM Run the refresh script
bash scripts/refresh.sh

REM Deactivate conda environment
call conda deactivate 