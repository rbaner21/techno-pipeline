# Technosignature Detection Pipeline

This project implements a production-ready, end-to-end AI pipeline for discovering and ranking technosignature exoplanet candidates by mining public astronomical data.

## Project Structure

```
techno-pipeline/
├── notebooks/               # Jupyter notebooks for the pipeline
│   ├── 1_data_access.ipynb     # Data downloading and access
│   ├── 2_preprocessing.ipynb   # Data cleaning and harmonization
│   ├── 3_feature_engineering.ipynb  # Feature computation
│   └── 4_modeling.ipynb        # Anomaly detection and scoring
├── src/                    # Python source code
│   ├── report.py           # HTML report generation
│   └── dashboard.py        # Web dashboard
├── data/                   # Data directories
│   ├── neowise/           # NEOWISE data
│   ├── kepler/            # Kepler/K2 data
│   ├── tess/              # TESS data
│   ├── gaia/              # Gaia data
│   ├── sdss/              # SDSS data
│   ├── exoplanets/        # Exoplanet archive data
│   ├── radio/             # Radio observation data
│   └── harps/             # HARPS spectra
├── outputs/               # Pipeline outputs
├── logs/                  # Log files
└── scripts/               # Utility scripts
    ├── refresh.sh         # Pipeline refresh script (Linux/Mac)
    └── refresh.bat        # Pipeline refresh script (Windows)
```

## Setup

1. Create and activate the conda environment:
```bash
conda create -n techno-pipeline python=3.8
conda activate techno-pipeline
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Jupyter kernel:
```bash
python -m ipykernel install --user --name techno-pipeline --display-name "Python (techno-pipeline)"
```

## Usage

### Running the Pipeline

1. Execute the notebooks in sequence:
```bash
jupyter lab notebooks/
```

2. Or run the entire pipeline:
```bash
# On Linux/Mac
bash scripts/refresh.sh

# On Windows
scripts\refresh.bat
```

### Viewing Results

1. Access the web dashboard:
```bash
python src/dashboard.py
```
Then open http://localhost:8050 in your browser.

2. View individual candidate reports in the `outputs/` directory.

## Scheduling

### Windows
1. Open Task Scheduler
2. Create a new task
3. Set the trigger to weekly
4. Set the action to run `scripts\refresh.bat`

### Linux/Mac
Add to crontab:
```bash
0 0 * * 0 /path/to/techno-pipeline/scripts/refresh.sh >> /path/to/techno-pipeline/logs/cron.log 2>&1
```

## Data Sources

- NEOWISE: AWS S3
- Kepler/K2 & TESS: MAST (via Astroquery)
- Gaia: DR3 TAP service
- Pan-STARRS & SDSS: Astroquery
- Exoplanets: NASA Exoplanet Archive
- Radio: Breakthrough Listen
- Spectra: HARPS (via ESO)

## Features Computed

1. Transit power from light curves
2. IR excess (W1-W2 color)
3. Blackbody SED fit
4. Radio hits near 1420 MHz
5. Gaia RUWE and astrometric excess noise
6. Unexplained spectral lines

## Anomaly Detection

The pipeline uses Isolation Forest for anomaly detection, with the following parameters:
- Number of estimators: 100
- Contamination: 0.01
- Random state: 42

## License

This project is licensed under the MIT License - see the LICENSE file for details.