import os
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
from astropy.io import fits
import lightkurve as lk
from astropy import units as u
from astropy.modeling.blackbody import blackbody_lambda

# Set up paths
OUTPUT_DIR = '../outputs'
TEMPLATE_DIR = 'templates'
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# Create template
template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Technosignature Candidate Report - {{ source_id }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .section { margin-bottom: 30px; }
        .plot { width: 100%; max-width: 800px; margin: 20px auto; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Technosignature Candidate Report</h1>
            <h2>Source ID: {{ source_id }}</h2>
        </div>

        <div class="section">
            <h3>Anomaly Summary</h3>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Technosignature Score</td>
                    <td>{{ "%.3f"|format(techno_score) }}</td>
                </tr>
                <tr>
                    <td>Anomaly Score</td>
                    <td>{{ "%.3f"|format(anomaly_score) }}</td>
                </tr>
                <tr>
                    <td>Transit Power</td>
                    <td>{{ "%.3f"|format(transit_power) }}</td>
                </tr>
                <tr>
                    <td>IR Excess</td>
                    <td>{{ "%.3f"|format(ir_excess) }}</td>
                </tr>
                <tr>
                    <td>HI Line Hit Count</td>
                    <td>{{ hi_hit_count }}</td>
                </tr>
            </table>
        </div>

        <div class="section">
            <h3>Light Curve</h3>
            <img src="{{ light_curve_plot }}" class="plot" alt="Light Curve">
        </div>

        <div class="section">
            <h3>SED and Blackbody Fit</h3>
            <img src="{{ sed_plot }}" class="plot" alt="SED">
        </div>

        <div class="section">
            <h3>Radio Spectrogram</h3>
            <img src="{{ radio_plot }}" class="plot" alt="Radio Spectrogram">
        </div>
    </div>
</body>
</html>
"""

# Save template
with open(os.path.join(TEMPLATE_DIR, 'report_template.html'), 'w') as f:
    f.write(template_str)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template('report_template.html')

def generate_light_curve_plot(source_id, mission):
    """Generate light curve plot for a candidate"""
    # Load light curve data
    lc_path = os.path.join(OUTPUT_DIR, mission, f'processed_{source_id}.csv')
    if os.path.exists(lc_path):
        lc_data = pd.read_csv(lc_path)
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.scatter(lc_data['time'], lc_data['flux'], s=1)
        plt.xlabel('Time')
        plt.ylabel('Normalized Flux')
        plt.title(f'Light Curve - {source_id}')
        
        # Save plot
        plot_path = os.path.join(OUTPUT_DIR, f'plots/{source_id}_lc.png')
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        plt.savefig(plot_path)
        plt.close()
        
        return plot_path
    return None

def generate_sed_plot(source_id, temperature, scale):
    """Generate SED plot with blackbody fit"""
    # Wavelength range for plot
    wavelengths = np.logspace(-1, 1, 100) * u.micron
    
    # Generate blackbody spectrum
    bb_flux = blackbody_lambda(wavelengths, temperature * u.K) * scale
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.loglog(wavelengths, bb_flux)
    plt.xlabel('Wavelength (microns)')
    plt.ylabel('Flux Density (Jy)')
    plt.title(f'SED - {source_id}')
    
    # Save plot
    plot_path = os.path.join(OUTPUT_DIR, f'plots/{source_id}_sed.png')
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path

def generate_radio_plot(source_id):
    """Generate radio spectrogram for a candidate"""
    # Load radio hits
    radio_hits = pd.read_csv(os.path.join(OUTPUT_DIR, 'radio_hits_clean.csv'))
    candidate_hits = radio_hits[radio_hits['source_id'] == source_id]
    
    if not candidate_hits.empty:
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.scatter(candidate_hits['freq'], candidate_hits['snr'], s=1)
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Signal-to-Noise Ratio')
        plt.title(f'Radio Hits - {source_id}')
        
        # Save plot
        plot_path = os.path.join(OUTPUT_DIR, f'plots/{source_id}_radio.png')
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        plt.savefig(plot_path)
        plt.close()
        
        return plot_path
    return None

def generate_report(candidate):
    """Generate HTML report for a candidate"""
    # Generate plots
    light_curve_plot = generate_light_curve_plot(candidate['source_id'], candidate['mission'])
    sed_plot = generate_sed_plot(candidate['source_id'], candidate['temperature'], candidate['scale'])
    radio_plot = generate_radio_plot(candidate['source_id'])
    
    # Render template
    html = template.render(
        source_id=candidate['source_id'],
        techno_score=candidate['techno_score'],
        anomaly_score=candidate['anomaly_score'],
        transit_power=candidate['transit_power'],
        ir_excess=candidate['ir_excess'],
        hi_hit_count=candidate['hi_hit_count'],
        light_curve_plot=light_curve_plot,
        sed_plot=sed_plot,
        radio_plot=radio_plot
    )
    
    # Save report
    report_path = os.path.join(OUTPUT_DIR, f'report_{candidate.name + 1}.html')
    with open(report_path, 'w') as f:
        f.write(html)
    
    return report_path

def main():
    # Load top candidates
    candidates = pd.read_csv(os.path.join(OUTPUT_DIR, 'top_candidates.csv'))
    
    # Generate reports
    for _, candidate in candidates.iterrows():
        report_path = generate_report(candidate)
        print(f"Generated report: {report_path}")

if __name__ == '__main__':
    main() 