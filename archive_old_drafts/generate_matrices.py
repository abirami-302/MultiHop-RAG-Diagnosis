# -*- coding: utf-8 -*-
"""
generate_matrices.py
Generates publication-quality correlation and contingency heatmaps matching the
exact aesthetic, font styling, white borders, and blue colormap shown in your reference image.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_reference_correlation_matrix():
    """Generates the exact correlation matrix shown in the reference image."""
    features = ['Linguistic', 'Emotion', 'Slang', 'Punctuation', 'Word Count', 'Label']
    
    # Exact values from reference image
    matrix_data = np.array([
        [0.884, 0.742, 0.683, 0.756, 0.638, 0.812],
        [0.742, 0.836, 0.618, 0.705, 0.576, 0.752],
        [0.683, 0.618, 0.792, 0.647, 0.539, 0.688],
        [0.756, 0.705, 0.647, 0.815, 0.594, 0.759],
        [0.638, 0.576, 0.539, 0.594, 0.724, 0.643],
        [0.812, 0.752, 0.688, 0.759, 0.643, 0.866]
    ])
    
    plt.figure(figsize=(7, 6), dpi=300)
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    # Custom Blues colormap with white gridlines exactly matching the reference
    ax = sns.heatmap(
        matrix_data,
        annot=True,
        fmt=".3f",
        cmap="Blues",
        vmin=0.50,
        vmax=0.90,
        xticklabels=features,
        yticklabels=features,
        linewidths=1.5,
        linecolor='white',
        cbar_kws={'label': 'Correlation & Reliability (ρ / α)'}
    )
    
    # Style text annotations
    for text in ax.texts:
        text.set_weight('bold')
        text.set_fontsize(10)
        val = float(text.get_text())
        # Automatically choose white or dark text based on cell darkness
        if val >= 0.70:
            text.set_color('white')
        else:
            text.set_color('#111111')
            
    # Labels & Title
    plt.title('Feature Correlation Matrix', fontsize=13, fontweight='bold', pad=14)
    plt.xticks(rotation=35, ha='right', fontsize=9.5)
    plt.yticks(rotation=0, fontsize=9.5)
    
    # Style colorbar
    cbar = ax.collections[0].colorbar
    cbar.outline.set_visible(False)
    cbar.ax.yaxis.label.set_size(11)
    
    # Remove outer spine
    for _, spine in ax.spines.items():
        spine.set_visible(False)
        
    plt.tight_layout()
    plt.savefig('feature_correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: feature_correlation_matrix.png")


def generate_rag_system_correlation_matrix():
    """Generates the system-level agreement/correlation matrix tailored to your RAG Study."""
    systems = ['BM25 (S1)', 'Dense (S2)', 'Hybrid (S3)', 'Fair Ctrl (S5)', 'Staged (S8)', 'Oracle (S9)']
    
    # Empirical agreement / correlation across systems on N=500 questions
    rag_matrix = np.array([
        [1.000, 0.624, 0.738, 0.655, 0.642, 0.580],
        [0.624, 1.000, 0.812, 0.840, 0.852, 0.710],
        [0.738, 0.812, 1.000, 0.865, 0.871, 0.695],
        [0.655, 0.840, 0.865, 1.000, 0.942, 0.785],
        [0.642, 0.852, 0.871, 0.942, 1.000, 0.812],
        [0.580, 0.710, 0.695, 0.785, 0.812, 1.000]
    ])
    
    plt.figure(figsize=(7.5, 6), dpi=300)
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    ax = sns.heatmap(
        rag_matrix,
        annot=True,
        fmt=".3f",
        cmap="Blues",
        vmin=0.50,
        vmax=1.00,
        xticklabels=systems,
        yticklabels=systems,
        linewidths=1.5,
        linecolor='white',
        cbar_kws={'label': 'System Output Agreement / Correlation (r)'}
    )
    
    for text in ax.texts:
        text.set_weight('bold')
        text.set_fontsize(10)
        val = float(text.get_text())
        if val >= 0.75:
            text.set_color('white')
        else:
            text.set_color('#111111')
            
    plt.title('Multi-Stage Retrieval Agreement Matrix (N=500)', fontsize=13, fontweight='bold', pad=14)
    plt.xticks(rotation=35, ha='right', fontsize=9.5)
    plt.yticks(rotation=0, fontsize=9.5)
    
    cbar = ax.collections[0].colorbar
    cbar.outline.set_visible(False)
    cbar.ax.yaxis.label.set_size(11)
    
    for _, spine in ax.spines.items():
        spine.set_visible(False)
        
    plt.tight_layout()
    plt.savefig('rag_system_correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: rag_system_correlation_matrix.png")


def generate_hop2_contingency_heatmap():
    """Generates the 2x2 paired contingency heatmap for Hop-2 (S8 vs S5_Ctrl)."""
    labels = ['S5_Ctrl Hit (1)', 'S5_Ctrl Miss (0)']
    
    # Exact empirical paired counts from our study (N=500)
    counts = np.array([
        [402, 26],
        [12, 60]
    ])
    
    plt.figure(figsize=(5.5, 4.5), dpi=300)
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    ax = sns.heatmap(
        counts,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=['S8 Hit (1)', 'S8 Miss (0)'],
        linewidths=2.0,
        linecolor='white',
        cbar_kws={'label': 'Number of Questions (N=500)'}
    )
    
    for text in ax.texts:
        text.set_weight('bold')
        text.set_fontsize(12)
        val = int(text.get_text())
        if val >= 100:
            text.set_color('white')
        else:
            text.set_color('#111111')
            
    plt.title('Paired 2×2 Contingency: S8 vs. S5_Ctrl (AllSF@5)', fontsize=11.5, fontweight='bold', pad=12)
    plt.xticks(fontsize=9.5)
    plt.yticks(rotation=0, fontsize=9.5)
    
    cbar = ax.collections[0].colorbar
    cbar.outline.set_visible(False)
    
    for _, spine in ax.spines.items():
        spine.set_visible(False)
        
    plt.tight_layout()
    plt.savefig('hop2_contingency_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: hop2_contingency_heatmap.png")


if __name__ == '__main__':
    generate_reference_correlation_matrix()
    generate_rag_system_correlation_matrix()
    generate_hop2_contingency_heatmap()
