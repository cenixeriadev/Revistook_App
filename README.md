# Revistook App

[![Build Windows Executable for Flet](https://github.com/cenixeriadev/Revistook_App/actions/workflows/main.yml/badge.svg)](https://github.com/cenixeriadev/Revistook_App/actions/workflows/main.yml)

A Python desktop application built with Flet that allows users to search for and download books from Library Genesis (libgen.li) using Selenium WebDriver. The app includes OCR capabilities to scan text from images and audio transcription for voice input.



## Features

- 📚 Search for books on Library Genesis (libgen.li)
- ⬇️ Download books directly to your specified location
- 📷 Extract text from images using OCR
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
│   │   │   ├── book_downloader.py
│   │   │   ├── text_recognition.py
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
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- [Flet](https://flet.dev/) - Flutter-powered UI toolkit for Python
- [Selenium](https://selenium-python.readthedocs.io/) - Web automation
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - Optical Character Recognition engine
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) - Library for performing speech recognition

## Usage

1. Run the application:
   ```bash
   python -m src.presentation.main
   ```

2. The main interface allows you to:
   - Type book titles, authors, or ISBN numbers directly
   - Use the "Capture Image" button to extract text from book covers or pages
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
- **OCR not working**: Verify that Tesseract OCR is properly installed and accessible in your PATH
- **Download failures**: Check your internet connection and verify that the book is available

### Error Logs

Check the application's console output for detailed error messages.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Library Genesis for providing access to educational resources
- The Flet team for their excellent UI framework
- Tesseract OCR project for text recognition capabilities
