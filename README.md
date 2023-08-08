# string_to_pdf_app
simple desktop utility

# generate .exe

Clone this repo, cd to the script folder and run (requires pyinstaller):

```sh
python -m PyInstaller --onefile string_to_pdf.py
```

This will generate a file `string_to_pdf.exe` under dist folder valid for your distribution in case it does not exist in `dist`.
