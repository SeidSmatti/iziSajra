
# iziSajra

A GUI application built with Python and CustomTkinter that allows users to browse directories, view their file structures in a tree like presentation, read the contents and print everything in a comprehensive chunk of text.

Useful for lazily submitting projetcs to chatbots such as ChatGPT. 

Update 12/12/2024 : Added a terminal based adaptation if you prefer that.

## Features

- **Browse Directories**: Select a directory and view its structure and files.
- **Hidden Files Option**: Toggle to include or exclude hidden files and directories.
- **Save as TXT**: Export the directory structure and file contents as a `.txt` file.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SeidSmatti/iziSajra.git
   cd iziSajra
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install customtkinter
   ```

   or


   ```bash
   pip install -r /path/to/requirements.txt
   ```

## Usage

Run the application with:
```bash
python3 sajra.py
```

Use the CLI solution (on de the working directory):
```bash
python3 /path/to/sajraCLI.py
```

## Requirements

- Python 3.6+
- CustomTkinter library

## License

This project is licensed under the GNU GPL3.

