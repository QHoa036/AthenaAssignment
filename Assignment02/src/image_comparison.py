#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

class ImageComparison:
    """
    Handles image comparison operations for validating game assets
    """
    
    def compare_images(self, 
                      generated_image_path: str,
                      reference_image_path: str,
                      output_dir: Optional[str] = None) -> Dict:
        """
        Compare a generated image against a reference image using multiple metrics
        
        Args:
            generated_image_path: Path to generated image
            reference_image_path: Path to reference image
            output_dir: Optional directory to save comparison results
            
        Returns:
            Dictionary of comparison metrics
        """
        # Load images
        generated_img = cv2.imread(generated_image_path)
        reference_img = cv2.imread(reference_image_path)
        
        if generated_img is None:
            raise ValueError(f"Could not load generated image: {generated_image_path}")
        if reference_img is None:
            raise ValueError(f"Could not load reference image: {reference_image_path}")
        
        # Resize images to match if they have different dimensions
        if generated_img.shape != reference_img.shape:
            reference_img = cv2.resize(reference_img, 
                                       (generated_img.shape[1], generated_img.shape[0]), 
                                       interpolation=cv2.INTER_AREA)
        
        # Convert to RGB for visualization (OpenCV loads as BGR)
        generated_rgb = cv2.cvtColor(generated_img, cv2.COLOR_BGR2RGB)
        reference_rgb = cv2.cvtColor(reference_img, cv2.COLOR_BGR2RGB)
        
        # Calculate SSIM
        ssim_value = self._calculate_ssim(generated_img, reference_img)
        
        # Calculate color histogram similarity
        color_match = self._compare_color_histograms(generated_img, reference_img)
        
        # Calculate edge similarity
        edge_accuracy = self._compare_edges(generated_img, reference_img)
        
        # Generate comparison visualizations if output directory is provided
        if output_dir:
            self._generate_comparison_visualizations(
                generated_rgb, 
                reference_rgb,
                generated_img,
                reference_img,
                output_dir
            )
        
        # Return comparison results
        return {
            "ssim": float(ssim_value),
            "color_match": float(color_match),
            "edge_accuracy": float(edge_accuracy)
        }
    
    def _calculate_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """
        Calculate Structural Similarity Index (SSIM) between two images
        
        Args:
            img1: First image
            img2: Second image
            
        Returns:
            SSIM value (0.0 to 1.0, where 1.0 means identical)
        """
        # Convert to grayscale for SSIM calculation
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Calculate SSIM
        ssim_value, _ = ssim(img1_gray, img2_gray, full=True)
        return ssim_value
    
    def _compare_color_histograms(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """
        Compare color histograms of two images
        
        Args:
            img1: First image
            img2: Second image
            
        Returns:
            Histogram comparison value (0.0 to 1.0, where 1.0 means identical)
        """
        # Calculate histograms for each color channel
        hist_similarity = 0
        
        for i in range(3):  # BGR channels
            hist1 = cv2.calcHist([img1], [i], None, [256], [0, 256])
            hist2 = cv2.calcHist([img2], [i], None, [256], [0, 256])
            
            # Normalize histograms
            cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
            cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
            
            # Compare histograms using correlation method
            similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            hist_similarity += similarity
        
        # Average similarity across channels
        return hist_similarity / 3.0
    
    def _compare_edges(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """
        Compare edge detection results between two images
        
        Args:
            img1: First image
            img2: Second image
            
        Returns:
            Edge similarity value (0.0 to 1.0, where 1.0 means identical)
        """
        # Convert to grayscale
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges1 = cv2.Canny(img1_gray, 100, 200)
        edges2 = cv2.Canny(img2_gray, 100, 200)
        
        # Count edge pixels in each image
        total_edges1 = np.count_nonzero(edges1)
        total_edges2 = np.count_nonzero(edges2)
        
        # Calculate intersection of edges
        intersection = np.count_nonzero(np.logical_and(edges1, edges2))
        
        # Calculate union of edges
        union = np.count_nonzero(np.logical_or(edges1, edges2))
        
        # Calculate IoU (Intersection over Union)
        if union == 0:
            return 1.0  # Both images have no edges, consider them identical
        
        return intersection / union
    
    def _generate_comparison_visualizations(self,
                                          generated_rgb: np.ndarray,
                                          reference_rgb: np.ndarray,
                                          generated_bgr: np.ndarray,
                                          reference_bgr: np.ndarray,
                                          output_dir: str) -> None:
        """
        Generate visualization images for comparison
        
        Args:
            generated_rgb: Generated image in RGB format
            reference_rgb: Reference image in RGB format
            generated_bgr: Generated image in BGR format
            reference_bgr: Reference image in BGR format
            output_dir: Directory to save visualizations
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Side by side comparison
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        
        axes[0].imshow(generated_rgb)
        axes[0].set_title('Generated Asset')
        axes[0].axis('off')
        
        axes[1].imshow(reference_rgb)
        axes[1].set_title('Reference Asset')
        axes[1].axis('off')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "side_by_side_comparison.png"))
        plt.close(fig)
        
        # 2. Edge detection visualization
        generated_gray = cv2.cvtColor(generated_bgr, cv2.COLOR_BGR2GRAY)
        reference_gray = cv2.cvtColor(reference_bgr, cv2.COLOR_BGR2GRAY)
        
        generated_edges = cv2.Canny(generated_gray, 100, 200)
        reference_edges = cv2.Canny(reference_gray, 100, 200)
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        
        axes[0].imshow(generated_edges, cmap='gray')
        axes[0].set_title('Generated Asset Edges')
        axes[0].axis('off')
        
        axes[1].imshow(reference_edges, cmap='gray')
        axes[1].set_title('Reference Asset Edges')
        axes[1].axis('off')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "edge_comparison.png"))
        plt.close(fig)
        
        # 3. Color histogram visualization
        fig, axes = plt.subplots(3, 2, figsize=(12, 8))
        color_channels = ['Blue', 'Green', 'Red']
        
        for i in range(3):
            # Generated image histogram
            hist_gen = cv2.calcHist([generated_bgr], [i], None, [256], [0, 256])
            axes[i, 0].plot(hist_gen, color=color_channels[i].lower())
            axes[i, 0].set_title(f'Generated Asset - {color_channels[i]} Channel')
            axes[i, 0].set_xlim([0, 256])
            
            # Reference image histogram
            hist_ref = cv2.calcHist([reference_bgr], [i], None, [256], [0, 256])
            axes[i, 1].plot(hist_ref, color=color_channels[i].lower())
            axes[i, 1].set_title(f'Reference Asset - {color_channels[i]} Channel')
            axes[i, 1].set_xlim([0, 256])
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "histogram_comparison.png"))
        plt.close(fig)
        
        # 4. Difference visualization
        # Create difference image
        diff_img = cv2.absdiff(generated_bgr, reference_bgr)
        
        plt.figure(figsize=(8, 8))
        plt.imshow(cv2.cvtColor(diff_img, cv2.COLOR_BGR2RGB))
        plt.title('Difference Visualization')
        plt.colorbar(label='Difference Intensity')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "difference_visualization.png"))
        plt.close()


if __name__ == "__main__":
    print("Image Comparison Module")
    # This module is intended to be imported by validation.py
