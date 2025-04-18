#!/bin/bash

# Activate conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate techno-pipeline

# Set up logging
LOG_DIR="../logs"
mkdir -p $LOG_DIR
LOG_FILE="$LOG_DIR/refresh.log"
echo "Starting pipeline refresh at $(date)" >> $LOG_FILE

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
}

# Function to check if a command succeeded
check_status() {
    if [ $? -eq 0 ]; then
        log "Success: $1"
    else
        log "Error: $1 failed"
        exit 1
    fi
}

# Execute notebooks in sequence
log "Executing 1_data_access.ipynb"
jupyter nbconvert --to notebook --execute ../notebooks/1_data_access.ipynb --output-dir $LOG_DIR
check_status "1_data_access.ipynb"

log "Executing 2_preprocessing.ipynb"
jupyter nbconvert --to notebook --execute ../notebooks/2_preprocessing.ipynb --output-dir $LOG_DIR
check_status "2_preprocessing.ipynb"

log "Executing 3_feature_engineering.ipynb"
jupyter nbconvert --to notebook --execute ../notebooks/3_feature_engineering.ipynb --output-dir $LOG_DIR
check_status "3_feature_engineering.ipynb"

log "Executing 4_modeling.ipynb"
jupyter nbconvert --to notebook --execute ../notebooks/4_modeling.ipynb --output-dir $LOG_DIR
check_status "4_modeling.ipynb"

# Generate reports
log "Generating reports"
python ../src/report.py
check_status "report.py"

log "Pipeline refresh completed successfully" 