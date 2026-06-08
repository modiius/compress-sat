# Compress SAT

## Setup with Pixi

### Installation

1. Install [Pixi](https://pixi.sh) if you haven't already.

2. Install dependencies:
```bash
pixi install
```

## Running Scripts

### Download Data

To download GEE data, run the following script with your GEE project and location of choice:
```bash
pixi run python compress-sat/src/download.py --project geeproject --lat 49.27724196962399 --lon 22.521417804769374
```

The script will prompt you to authenticate with GEE if you haven't already. If you do not wish to authenticate with GEE, simply run `main.py` (in the next step). We have included some example data with the repository.

### Run Main Application

To run the main application, execute:
```bash
pixi run python compress-sat/src/main.py
```

This will use the data downloaded from the previous step. Example output from the data downloaded above:
```bash
Original size (float32): 9972 bytes
Lossy size (uint8): 2493 bytes
Compressed size: 1764 bytes
Compression ratio: 5.6531
```
