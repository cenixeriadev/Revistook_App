# Revistook App

[![CodeQL Advanced](https://github.com/cenixeriadev/Revistook_App/actions/workflows/codeql.yml/badge.svg)](https://github.com/cenixeriadev/Revistook_App/actions/workflows/codeql.yml)[![Build and Release](https://github.com/cenixeriadev/Revistook_App/actions/workflows/build-release.yml/badge.svg)](https://github.com/cenixeriadev/Revistook_App/actions/workflows/build-release.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python Version](https://img.shields.io/badge/python-3.12.6-blue.svg)](https://www.python.org/downloads/release/python-390/)

A Python desktop application built with Flet that allows users to search for and download books from Library Genesis (libgen.li) using Selenium WebDriver. The app includes OpenCV capabilities to scan images and then use it for filter results.



## Features

- 📚 Search for books on Library Genesis (libgen.li or libgen.is)
- ⬇️ Download books directly to your specified location
- 📷 Filter results by image
- 🎤 Convert speech to text from audio files
- 🔍 Detailed book information display
- 📊 Real-time download progress tracking
- 📱 Cross-platform compatibility (Windows, macOS, Linux)

## Project Structure

```
Revistook_app/
├── src/
│   ├── application/
│   │   ├── interfaces/
│   │   ├── services/
│   │   │   ├── book_downloaderli.py
│   │   │   ├── book_downloaderis.py
│   │   │   ├── audio_recognition.py
│   │   │   └── ...
│   │   └── __init__.py
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── download_status.py
│   │   │   └── book.py
│   │   ├── repositories/
│   │   └── __init__.py
│   ├── infrastructure/
│   │   ├── repositories/
|   |   ├── ml/
│   │   └── __init__.py
│   └── presentation/
│       ├── views/
│       │   ├── main_view.py
│       │   └── ...
│       |── __init__.py  
|       ├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.8+
- Chrome or Firefox browser installed
- Internet connection

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cenixeriadev/Revistook_App.git
   cd Revistook_App
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\Activate.ps1
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- [Flet](https://flet.dev/) - Flutter-powered UI toolkit for Python
- [Selenium](https://selenium-python.readthedocs.io/) - Web automation
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) - Library for performing speech recognition
- [Open CV](https://pypi.org/project/opencv-python/) - Library for filter by image
## Usage

1. Run the application:
   ```bash
   python -m src.presentation.main
   ```

2. The main interface allows you to:
   - Type book titles, authors, or ISBN numbers directly
   - Use the "Filter by image" button to filter results by image
   - Use the "Select Audio" button to transcribe spoken book requests
   - Select your preferred download directory
>[!Note]
>it's better to search using the ISBN code.
3. Search results will show book covers, titles, and authors
   
4. Click "Download" on any book to begin the download process

5. Monitor download progress through the progress bar

## Configuration

The application automatically creates directories for storing temporary files:
- Images: `~/Pictures/BookDownloader/` (Windows/Linux/Mac)
- Audio: `~/Music/BookDownloader/` (Windows/Linux/Mac)
- Downloads: Default is `~/Downloads/` but can be changed in the UI


## Troubleshooting

### Common Issues

- **WebDriver issues**: Ensure you have the latest version of Chrome or Firefox installed
- **Download failures**: Check your internet connection and verify that the book is available


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Library Genesis for providing access to educational resources
- The Flet team for their excellent UI framework
- Open CV project for filter by image
