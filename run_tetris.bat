@echo off
REM Script de lancement pour Tetris sur Windows
REM Ce fichier batch permet un lancement facile sur les systèmes Windows

echo ===== LANCEMENT DU JEU TETRIS =====
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas trouvé! Vérifiez que Python est installé et dans le PATH.
    echo Téléchargez Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Vérifier si colorama est installé pour améliorer l'affichage
pip show colorama >nul 2>&1
if %errorlevel% neq 0 (
    echo Installation de colorama pour un meilleur affichage...
    pip install colorama
)

REM Lancer le script principal
python run_tetris.py

REM En cas d'erreur
if %errorlevel% neq 0 (
    echo.
    echo Une erreur s'est produite lors de l'exécution.
    pause
)

exit /b 0