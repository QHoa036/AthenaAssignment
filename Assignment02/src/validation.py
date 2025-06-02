#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime
import uuid

import config
from image_comparison import ImageComparison
from validation_reporting import ValidationReporter

class AssetValidator:
    """
    Main validator class that orchestrates the validation process for AI-generated game assets
    """
    def __init__(self, layer_api_key: Optional[str] = None):
        """
        Initialize the asset validator

        Args:
            layer_api_key: Optional API key for Layer.ai integration
        """
        self.layer_api_key = layer_api_key or config.LAYER_API_KEY
        self.image_comparison = ImageComparison()
        self.reporter = ValidationReporter()

        # Ensure validation directory exists
        os.makedirs(config.VALIDATION_DIR, exist_ok=True)

    def validate_asset(self,
                      generated_asset_path: str,
                      reference_asset_path: str,
                      validation_name: Optional[str] = None,
                      metadata: Optional[Dict] = None) -> Dict:
        """
        Validate a generated asset against a reference asset

        Args:
            generated_asset_path: Path to the generated asset
            reference_asset_path: Path to the reference asset
            validation_name: Optional name for the validation
            metadata: Optional metadata about the validation

        Returns:
            Dictionary containing validation results
        """
        if not os.path.exists(generated_asset_path):
            raise FileNotFoundError(f"Generated asset not found: {generated_asset_path}")

        if not os.path.exists(reference_asset_path):
            raise FileNotFoundError(f"Reference asset not found: {reference_asset_path}")

        # Create validation name if not provided
        if not validation_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            validation_name = f"validation_{timestamp}_{uuid.uuid4().hex[:8]}"

        # Create validation directory
        validation_dir = os.path.join(config.VALIDATION_DIR, validation_name)
        os.makedirs(validation_dir, exist_ok=True)

        # Run image comparisons
        comparison_results = self.image_comparison.compare_images(
            generated_asset_path,
            reference_asset_path,
            output_dir=validation_dir
        )

        # Create validation metadata
        validation_metadata = metadata or {}
        validation_metadata.update({
            "validation_id": validation_name,
            "timestamp": datetime.now().isoformat(),
            "generated_asset": os.path.basename(generated_asset_path),
            "reference_asset": os.path.basename(reference_asset_path)
        })

        # Combine results
        validation_results = {
            "metadata": validation_metadata,
            "metrics": comparison_results,
            "pass_fail": self._evaluate_results(comparison_results)
        }

        # Save validation results
        results_path = os.path.join(validation_dir, "validation_results.json")
        with open(results_path, "w") as f:
            json.dump(validation_results, f, indent=2)

        # Generate validation report
        report_path = self.reporter.generate_report(
            validation_results,
            generated_asset_path,
            reference_asset_path,
            validation_dir
        )

        validation_results["report_path"] = report_path

        return validation_results

    def validate_with_layer_ai(self,
                             generated_asset_path: str,
                             reference_asset_path: str,
                             project_name: Optional[str] = None,
                             metadata: Optional[Dict] = None) -> Dict:
        """
        Use Layer.ai service to validate assets

        Args:
            generated_asset_path: Path to generated asset
            reference_asset_path: Path to reference asset
            project_name: Optional Layer.ai project name
            metadata: Optional additional metadata

        Returns:
            Dictionary containing validation results from Layer.ai
        """
        if not self.layer_api_key:
            raise ValueError("Layer.ai API key not provided")

        # This is a placeholder for Layer.ai integration
        # In a real implementation, this would make API calls to Layer.ai

        print("Warning: Layer.ai integration is a placeholder")
        print("In a real implementation, this would connect to Layer.ai API")

        # For demonstration, we'll use our local comparison instead
        validation_name = f"layer_ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        results = self.validate_asset(
            generated_asset_path,
            reference_asset_path,
            validation_name,
            metadata
        )

        # Add layer.ai specific metadata
        results["layer_ai"] = {
            "integration": "placeholder",
            "project_name": project_name or "Game Asset Evaluation",
            "note": "This is a placeholder for Layer.ai integration"
        }

        return results

    def _evaluate_results(self, comparison_results: Dict) -> Dict:
        """
        Evaluate comparison results against thresholds

        Args:
            comparison_results: Dictionary of metric results from comparison

        Returns:
            Dictionary with pass/fail status for each metric
        """
        evaluation = {}

        # Evaluate SSIM
        if "ssim" in comparison_results:
            ssim_value = comparison_results["ssim"]
            ssim_thresholds = config.VALIDATION_THRESHOLDS["ssim"]

            if ssim_value < ssim_thresholds["reject"]:
                evaluation["ssim"] = {"status": "reject", "value": ssim_value}
            elif ssim_value < ssim_thresholds["acceptable"]:
                evaluation["ssim"] = {"status": "acceptable", "value": ssim_value}
            else:
                evaluation["ssim"] = {"status": "excellent", "value": ssim_value}

        # Evaluate color match
        if "color_match" in comparison_results:
            color_value = comparison_results["color_match"]
            color_thresholds = config.VALIDATION_THRESHOLDS["color_match"]

            if color_value < color_thresholds["reject"]:
                evaluation["color_match"] = {"status": "reject", "value": color_value}
            elif color_value < color_thresholds["acceptable"]:
                evaluation["color_match"] = {"status": "acceptable", "value": color_value}
            else:
                evaluation["color_match"] = {"status": "excellent", "value": color_value}

        # Evaluate edge accuracy
        if "edge_accuracy" in comparison_results:
            edge_value = comparison_results["edge_accuracy"]
            edge_thresholds = config.VALIDATION_THRESHOLDS["edge_accuracy"]

            if edge_value < edge_thresholds["reject"]:
                evaluation["edge_accuracy"] = {"status": "reject", "value": edge_value}
            elif edge_value < edge_thresholds["acceptable"]:
                evaluation["edge_accuracy"] = {"status": "acceptable", "value": edge_value}
            else:
                evaluation["edge_accuracy"] = {"status": "excellent", "value": edge_value}

        # Overall status is the worst of any individual metric
        statuses = [item["status"] for item in evaluation.values()]
        if "reject" in statuses:
            evaluation["overall"] = "reject"
        elif "acceptable" in statuses:
            evaluation["overall"] = "acceptable"
        else:
            evaluation["overall"] = "excellent"

        return evaluation


if __name__ == "__main__":
    print("Asset Validator Tool")
    print("====================")

    if len(sys.argv) < 3:
        print("Usage: python validation.py <generated_asset_path> <reference_asset_path>")
        sys.exit(1)

    generated_asset = sys.argv[1]
    reference_asset = sys.argv[2]

    validator = AssetValidator()

    try:
        results = validator.validate_asset(generated_asset, reference_asset)
        print(f"\nValidation complete! Report saved to: {results['report_path']}")
        print(f"Overall status: {results['pass_fail']['overall'].upper()}")
    except Exception as e:
        print(f"Validation error: {str(e)}")
        sys.exit(1)
