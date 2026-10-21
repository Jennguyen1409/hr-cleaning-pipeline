@echo off
echo ============================================
echo Starting Large Data Cleaning Pipeline at %date% %time%
echo ============================================

cd C:\Users\jenng\data_engineering_projects\project_31_hr_cleaning
venv\Scripts\python.exe scripts/cleaning_pipeline.py

echo ============================================
echo Pipeline completed at %date% %time%
echo ============================================
pause