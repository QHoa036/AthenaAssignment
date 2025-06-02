#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from typing import Dict, Optional, List
import cv2
import numpy as np
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader

class ValidationReporter:
    """
    Handles the generation of validation reports for game asset comparisons
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the validation reporter
        
        Args:
            template_dir: Optional directory containing report templates
        """
        # Set up Jinja2 templating
        self.template_dir = template_dir or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "..", "templates"
        )
        
        # Create template directory if it doesn't exist
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Create default template if not exists
        self._create_default_template()
        
        # Initialize Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
    
    def _create_default_template(self):
        """Create default HTML template if it doesn't exist"""
        default_template_path = os.path.join(self.template_dir, "validation_report.html")
        
        if not os.path.exists(default_template_path):
            default_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asset Validation Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .report-header {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
            border-left: 5px solid #007bff;
        }
        .status-excellent {
            color: #28a745;
            font-weight: bold;
        }
        .status-acceptable {
            color: #ffc107;
            font-weight: bold;
        }
        .status-reject {
            color: #dc3545;
            font-weight: bold;
        }
        .metrics-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .metrics-table th, .metrics-table td {
            padding: 12px 15px;
            border: 1px solid #ddd;
            text-align: left;
        }
        .metrics-table th {
            background-color: #f8f9fa;
            color: #333;
        }
        .metrics-table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .comparison-images {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin: 30px 0;
        }
        .comparison-image {
            width: 48%;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .comparison-image img {
            max-width: 100%;
            display: block;
        }
        .comparison-image h3 {
            background-color: #f8f9fa;
            margin: 0;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        .full-width-image {
            width: 100%;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .full-width-image img {
            max-width: 100%;
            display: block;
        }
        .full-width-image h3 {
            background-color: #f8f9fa;
            margin: 0;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            font-size: 14px;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="report-header">
        <h1>Game Asset Validation Report</h1>
        <p><strong>Validation ID:</strong> {{ validation_results.metadata.validation_id }}</p>
        <p><strong>Generated:</strong> {{ validation_results.metadata.timestamp }}</p>
        <p><strong>Overall Status:</strong> 
            <span class="status-{{ validation_results.pass_fail.overall }}">
                {{ validation_results.pass_fail.overall | upper }}
            </span>
        </p>
    </div>

    <h2>Asset Information</h2>
    <p><strong>Generated Asset:</strong> {{ validation_results.metadata.generated_asset }}</p>
    <p><strong>Reference Asset:</strong> {{ validation_results.metadata.reference_asset }}</p>

    <h2>Validation Metrics</h2>
    <table class="metrics-table">
        <thead>
            <tr>
                <th>Metric</th>
                <th>Value</th>
                <th>Status</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>SSIM (Structural Similarity)</td>
                <td>{{ "%.3f"|format(validation_results.metrics.ssim) }}</td>
                <td class="status-{{ validation_results.pass_fail.ssim.status }}">{{ validation_results.pass_fail.ssim.status | upper }}</td>
                <td>Measures structural similarity between images (0-1, higher is better)</td>
            </tr>
            <tr>
                <td>Color Match</td>
                <td>{{ "%.3f"|format(validation_results.metrics.color_match) }}</td>
                <td class="status-{{ validation_results.pass_fail.color_match.status }}">{{ validation_results.pass_fail.color_match.status | upper }}</td>
                <td>Measures color histogram similarity (0-1, higher is better)</td>
            </tr>
            <tr>
                <td>Edge Accuracy</td>
                <td>{{ "%.3f"|format(validation_results.metrics.edge_accuracy) }}</td>
                <td class="status-{{ validation_results.pass_fail.edge_accuracy.status }}">{{ validation_results.pass_fail.edge_accuracy.status | upper }}</td>
                <td>Measures similarity of edge features (0-1, higher is better)</td>
            </tr>
        </tbody>
    </table>

    <h2>Side by Side Comparison</h2>
    <div class="full-width-image">
        <h3>Generated vs. Reference</h3>
        <img src="side_by_side_comparison.png" alt="Side by Side Comparison">
    </div>

    <h2>Edge Detection</h2>
    <div class="full-width-image">
        <h3>Edge Comparison</h3>
        <img src="edge_comparison.png" alt="Edge Detection Comparison">
    </div>

    <h2>Color Distribution</h2>
    <div class="full-width-image">
        <h3>Color Histogram Comparison</h3>
        <img src="histogram_comparison.png" alt="Color Histogram Comparison">
    </div>

    <h2>Difference Visualization</h2>
    <div class="full-width-image">
        <h3>Pixel Differences</h3>
        <img src="difference_visualization.png" alt="Difference Visualization">
    </div>

    <footer>
        <p>Game Asset Validation System | Generated on {{ validation_results.metadata.timestamp }}</p>
    </footer>
</body>
</html>"""
            
            os.makedirs(self.template_dir, exist_ok=True)
            with open(default_template_path, "w") as f:
                f.write(default_template)
    
    def generate_report(self,
                      validation_results: Dict,
                      generated_image_path: str,
                      reference_image_path: str,
                      output_dir: str) -> str:
        """
        Generate a validation report based on comparison results
        
        Args:
            validation_results: Dictionary of validation results
            generated_image_path: Path to generated image
            reference_image_path: Path to reference image
            output_dir: Directory to save the report
            
        Returns:
            Path to generated report
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Load template
        template = self.env.get_template("validation_report.html")
        
        # Render HTML report
        html_content = template.render(validation_results=validation_results)
        
        # Save report
        report_path = os.path.join(output_dir, "validation_report.html")
        with open(report_path, "w") as f:
            f.write(html_content)
        
        # Generate summary chart
        self._generate_summary_chart(validation_results, output_dir)
        
        return report_path
    
    def _generate_summary_chart(self, validation_results: Dict, output_dir: str) -> str:
        """
        Generate a summary chart for validation metrics
        
        Args:
            validation_results: Dictionary of validation results
            output_dir: Directory to save the chart
            
        Returns:
            Path to the generated chart
        """
        metrics = validation_results["metrics"]
        
        # Extract metric values
        metric_names = list(metrics.keys())
        metric_values = [metrics[name] for name in metric_names]
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(metric_names, metric_values, color=['#3498db', '#2ecc71', '#e74c3c'])
        
        # Add threshold lines
        reject_threshold = 0.6
        acceptable_threshold = 0.8
        plt.axhline(y=reject_threshold, color='r', linestyle='-', alpha=0.3, label='Reject Threshold')
        plt.axhline(y=acceptable_threshold, color='g', linestyle='-', alpha=0.3, label='Acceptable Threshold')
        
        # Customize chart
        plt.title('Validation Metrics Summary')
        plt.ylabel('Score (0-1)')
        plt.ylim(0, 1.05)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.3f}', ha='center', va='bottom')
        
        plt.legend()
        plt.tight_layout()
        
        # Save chart
        chart_path = os.path.join(output_dir, 'metrics_summary.png')
        plt.savefig(chart_path)
        plt.close()
        
        return chart_path
    
    def generate_batch_report(self, validation_results_list: List[Dict], output_dir: str) -> str:
        """
        Generate a report for multiple validations
        
        Args:
            validation_results_list: List of validation result dictionaries
            output_dir: Directory to save the report
            
        Returns:
            Path to the generated report
        """
        # This is a placeholder for batch reporting functionality
        # In a full implementation, this would generate a comparative report
        # across multiple assets
        
        # For now, just return a message
        report_path = os.path.join(output_dir, "batch_report.txt")
        with open(report_path, "w") as f:
            f.write(f"Batch report placeholder for {len(validation_results_list)} validations\n")
            f.write("In a full implementation, this would generate an HTML comparative report.\n")
        
        return report_path


if __name__ == "__main__":
    print("Validation Reporter Module")
    # This module is intended to be imported by validation.py
