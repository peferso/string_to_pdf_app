import PySimpleGUI as sg
import os
from datetime import datetime
import base64


FONT = 'Consolas'
THEME = 'DarkAmber'
sg.theme(THEME)
sg.set_options(font=FONT)
WSIZE=(500, 200)
DEFAULT_FOLDER = os.path.expanduser('~')
col_welcome = [
    [
        sg.Text("Welcome to text_to_pdf")
    ],
    [
        sg.Button("Continue"), sg.Button("Exit")
    ]
]

col_main = [
    [
        sg.Text('Output folder'),
        sg.In(
            size=(25,1),
            enable_events=True,
            key='-FOLDER-'
        ),
        sg.FolderBrowse()
    ],
    [
        sg.Text('Insert string'),
        sg.Multiline(
            size=(25,1),
            enable_events=True, 
            expand_x=True,
            justification='left',
            key='-PDFSTRING-',
            do_not_clear=False
        ),
        sg.Button('Ok', key='-OK-')
    ],
    [
        sg.Button("Generate pdf"),
        sg.Button("Open pdf")
    ],
    [
        sg.Button("Exit")
    ],
    [sg.Text("", key='-TEXT-')]
]

layout_welcome = [[sg.Column(col_welcome, element_justification='c')]]
layout_main = [[sg.Column(col_main, element_justification='c')]]

# Create the window
window_welcome = sg.Window(
    "text_to_pdf: Welcome",
    layout_welcome,
    resizable=True,
    # size=WSIZE
)
window_main = sg.Window(
    "text_to_pdf: main",
    layout_main,
    resizable=True,
    # size=WSIZE
)

def main():
    # Create an event loop
    while True:
        event, values = window_welcome.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Continue":
            launch_pdf_generator_menu()

def launch_pdf_generator_menu():
    window_welcome.close()
    dest_folder = DEFAULT_FOLDER
    input_pdf_string = None
    file = None
    while True:
        event, values = window_main.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break    
        elif event == '-FOLDER-':
            dest_folder = values['-FOLDER-']
            if not os.path.exists(dest_folder):
                dest_folder = DEFAULT_FOLDER
            msg = f'Output folder: {dest_folder}'
        elif event == '-PDFSTRING-':
            input_pdf_string = values['-PDFSTRING-']
            if len(input_pdf_string) == 0:
                msg = 'empty pdf string!'
            else:
                msg = f'Input string received. Click on "Generate pdf" once finished.'
        elif event == 'Generate pdf':
            if input_pdf_string is None:
                msg = 'Please, insert the input pdf string first.'
            else:
                file, status = generate_pdf(
                    input_string=input_pdf_string,
                    dest_folder=dest_folder
                )
                values['-PDFSTRING-'] = ""
                input_pdf_string = None
                if status == 'OK':
                    msg = f'pdf generated: {file}'
                else:
                    msg = f'Unable to generate pdf from input string!'
        elif event == "Open pdf":
            if file is None:
                msg = "No pdf generated!"
            elif os.path.exists(file):
                os.startfile(file)
                msg = f"File {file} opened."
            else:
                msg = f"File {file} not found!"
            
        window_main['-TEXT-'].update(msg)
    window_main.close()

def generate_pdf(input_string, dest_folder):
    ts = str(datetime.now()).replace('-', '').replace(':', '').replace(' ', '-').replace('.', '')
    filename = dest_folder + '/' + ts + '.pdf'
    try:
        stuffout = base64.b64decode(input_string)    
        fileout = open(filename, "wb")
        fileout.write(stuffout)
        fileout.close()
        status = 'OK'
    except Exception:
        status = 'KO'
        filename = None
    return filename, status

main()
