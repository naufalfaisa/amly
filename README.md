# Apple Music Lyrics Downloader

A Python program for downloading Apple Music time-synced lyrics in LRC format.

## Installation & Usage

1. Download the latest release from [Releases](https://github.com/naufalfaisa/amly/releases)
2. Open Command Prompt in the directory folder.
3. Run the command: 
```
amly [-h] [-v] [-s] [urls...]
```

Positional Arguments:
- `urls`: Apple Music URLs for albums or songs

Options:
- `-h, --help`: show this help message and exit
- `-v, --version`: show program's version number and exit
- `-s, --sync`: Save timecode's in `00:00.000` format (three ms points)

## Output

The output files are saved in:

```
./downloads/
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credit

This project is based on and modified from [Manzana-Apple-Music-Lyrics](https://github.com/dropcreations/Manzana-Apple-Music-Lyrics) by [dropcreations](https://github.com/dropcreations).

