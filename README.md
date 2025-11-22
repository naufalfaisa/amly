
<h1 align="center">Apple Music Lyrics Downloader</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/github/license/naufalfaisa/amly" alt="License" />
  <img src="https://img.shields.io/github/stars/naufalfaisa/amly?style=social" alt="GitHub stars" />
</p>

A Python program for downloading Apple Music time-synced lyrics in LRC format.

## Installation & Usage

### Option 1: Download the latest release

1. Download the latest release from [Releases](https://github.com/naufalfaisa/amly/releases)
2. Open Command Prompt in the directory folder.
3. Run the program: 
```
amly [-h] [-v] [-s] [urls...]
```

### Option 2: Clone the repository and install

1. Clone this repository:
```bash
git clone https://github.com/naufalfaisa/amly.git
```
2. Enter the project directory:
```bash
cd amly
```
3. Install dependencies:
pip install -r requirements.txt
4. Run the program:
```
python -m amly [-h] [-v] [-s] [urls...]
```

### Positional Arguments:

- `urls`: Apple Music URLs for albums or songs

## Get Japanese to Romaji Conversion

To get Japanese to Romaji Conversion you need to install [MeCab](https://github.com/ikegami-yukino/mecab/releases).

### Options:

- `-h, --help`: show this help message and exit
- `-v, --version`: show program's version number and exit
- `-s, --sync`: Save timecode's in `00:00.000` format (three ms points)
- `-r, --romaji`: Convert Japanese lyrics to Romaji (requires MeCab/Cutlet)

### The output files are saved in:

```
./downloads/
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credit

This project is based on and modified from [Manzana-Apple-Music-Lyrics](https://github.com/dropcreations/Manzana-Apple-Music-Lyrics) by [dropcreations](https://github.com/dropcreations).

