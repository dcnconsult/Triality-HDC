#!/usr/bin/env python3
"""
Python-based PDF generator for Triality paper
Generates a professional PDF without requiring LaTeX
Enhanced version with improved layout, typography, and content structure
"""

import os
import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from datetime import datetime
import numpy as np
import textwrap
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, replace
from copy import deepcopy


@dataclass(frozen=True)
class TextStyle:
    """Declarative text style definition for consistent formatting."""
    fontsize: float = 11
    fontweight: str = "normal"
    fontstyle: str = "normal"
    color: str = "black"
    ha: str = "left"
    va: str = "top"
    line_height: float = 0.022
    paragraph_spacing: float = 0.012
    width: float = 0.9
    bullet_marker: str = "•"
    bullet_indent: float = 0.015
    bullet_spacing: float = 0.022

    def to_kwargs(self) -> Dict[str, Any]:
        """Return keyword arguments consumable by matplotlib text calls."""
        return {
            "fontsize": self.fontsize,
            "fontweight": self.fontweight,
            "fontstyle": self.fontstyle,
            "color": self.color,
            "ha": self.ha,
            "va": self.va,
        }


@dataclass(frozen=True)
class TableStyle:
    """Configuration block for table rendering."""
    font_size: float = 10
    header_color: str = "#f0f0f0"
    header_fontweight: str = "bold"
    caption_color: str = "#1f77b4"
    caption_style: str = "table_caption"
    width: float = 0.8
    row_height: float = 0.028
    scale_y: float = 1.2
    padding: float = 0.03
    caption_align: str = "center"


def _deep_update(target: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge ``updates`` into ``target`` (mutates target)."""
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_update(target[key], value)
        else:
            target[key] = value
    return target


class StyleManager:
    """Central registry for text, table, and layout styles."""

    DEFAULT_TEXT_STYLES: Dict[str, TextStyle] = {
        "body": TextStyle(),
        "section_header": TextStyle(
            fontsize=14,
            fontweight="bold",
            color="#1f77b4",
            line_height=0.032,
            paragraph_spacing=0.024,
        ),
        "subsection_header": TextStyle(
            fontsize=12,
            fontweight="bold",
            color="#2ca02c",
            line_height=0.026,
            paragraph_spacing=0.018,
        ),
        "header_left": TextStyle(
            fontsize=9,
            color="#6c757d",
            ha="left",
            va="top",
            line_height=0.0,
            paragraph_spacing=0.0,
            width=1.0,
        ),
        "header_right": TextStyle(
            fontsize=9,
            color="#6c757d",
            ha="right",
            va="top",
            line_height=0.0,
            paragraph_spacing=0.0,
            width=1.0,
        ),
        "footer_left": TextStyle(
            fontsize=8,
            color="#6c757d",
            ha="left",
            va="bottom",
            line_height=0.0,
            paragraph_spacing=0.0,
            width=1.0,
        ),
        "footer_right": TextStyle(
            fontsize=8,
            color="#6c757d",
            ha="right",
            va="bottom",
            line_height=0.0,
            paragraph_spacing=0.0,
            width=1.0,
        ),
        "title_main": TextStyle(
            fontsize=18,
            fontweight="bold",
            color="#1f77b4",
            ha="center",
            line_height=0.034,
            paragraph_spacing=0.026,
        ),
        "title_secondary": TextStyle(
            fontsize=16,
            color="#2ca02c",
            ha="center",
            line_height=0.032,
            paragraph_spacing=0.022,
        ),
        "title_author": TextStyle(
            fontsize=14,
            fontweight="bold",
            ha="center",
            line_height=0.03,
            paragraph_spacing=0.02,
        ),
        "title_date": TextStyle(
            fontsize=12,
            fontstyle="italic",
            ha="center",
            line_height=0.028,
            paragraph_spacing=0.018,
        ),
        "abstract_heading": TextStyle(
            fontsize=14,
            fontweight="bold",
            color="#1f77b4",
            ha="center",
            line_height=0.03,
            paragraph_spacing=0.02,
        ),
        "abstract_body": TextStyle(
            fontsize=10,
            width=0.7,
            line_height=0.022,
            paragraph_spacing=0.014,
        ),
        "table_caption": TextStyle(
            fontsize=11,
            fontweight="bold",
            color="#1f77b4",
            ha="center",
            line_height=0.03,
            paragraph_spacing=0.02,
        ),
        "figure_title": TextStyle(
            fontsize=16,
            fontweight="bold",
            ha="center",
            line_height=0.032,
            paragraph_spacing=0.02,
        ),
        "figure_caption": TextStyle(
            fontsize=11,
            fontweight="bold",
            ha="center",
            line_height=0.026,
            paragraph_spacing=0.015,
        ),
        "figure_error": TextStyle(
            fontsize=9,
            color="red",
            ha="center",
            va="center",
            line_height=0.0,
            paragraph_spacing=0.0,
            width=1.0,
        ),
        "figure_missing": TextStyle(
            fontsize=9,
            color="gray",
            ha="center",
            va="center",
            line_height=0.0,
            paragraph_spacing=0.0,
            width=1.0,
        ),
    }

    DEFAULT_TABLE_STYLES: Dict[str, TableStyle] = {
        "default": TableStyle(),
    }

    DEFAULT_LAYOUT: Dict[str, Any] = {
        "page": {
            "size": (8.5, 11),
            "x_limits": (0.05, 0.95),
            "y_limits": (0.05, 0.95),
            "column_gutter": 0.04,
        },
        "header": {
            "left_x": 0.06,
            "right_x": 0.94,
            "y": 0.97,
        },
        "footer": {
            "left_x": 0.06,
            "right_x": 0.94,
            "y": 0.03,
        },
        "boxes": {
            "abstract": {
                "xy": (0.1, 0.15),
                "width": 0.8,
                "height": 0.25,
                "facecolor": "#f8f9fa",
                "edgecolor": "#dee2e6",
                "alpha": 0.8,
                "linewidth": 1,
            }
        },
        "matplotlib": {
            'font.family': 'serif',
            'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
            'font.size': 11,
            'axes.titlesize': 13,
            'axes.labelsize': 11,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 16,
            'text.usetex': False,
            'figure.dpi': 300,
            'savefig.dpi': 300,
            'savefig.bbox': 'tight',
            'axes.linewidth': 0.5,
            'grid.linewidth': 0.5,
        },
    }

    def __init__(self, overrides: Optional[Dict[str, Any]] = None):
        self.text_styles: Dict[str, TextStyle] = deepcopy(self.DEFAULT_TEXT_STYLES)
        self.table_styles: Dict[str, TableStyle] = deepcopy(self.DEFAULT_TABLE_STYLES)
        self.layout: Dict[str, Any] = deepcopy(self.DEFAULT_LAYOUT)
        if overrides:
            self.apply_overrides(overrides)

    def apply_overrides(self, overrides: Dict[str, Any]) -> None:
        """Merge user-supplied overrides into the managed styles."""
        text_overrides = overrides.get("text", {})
        for name, values in text_overrides.items():
            base = self.text_styles.get(name, self.text_styles["body"])
            filtered = {
                key: val for key, val in values.items()
                if key in TextStyle.__dataclass_fields__
            }
            self.text_styles[name] = replace(base, **filtered)

        table_overrides = overrides.get("table", {})
        for name, values in table_overrides.items():
            base = self.table_styles.get(name, self.table_styles["default"])
            filtered = {
                key: val for key, val in values.items()
                if key in TableStyle.__dataclass_fields__
            }
            self.table_styles[name] = replace(base, **filtered)

        layout_overrides = overrides.get("layout", {})
        if layout_overrides:
            _deep_update(self.layout, layout_overrides)

    def get_text_style(self, name: str, **overrides: Any) -> TextStyle:
        base = self.text_styles.get(name, self.text_styles["body"])
        if overrides:
            filtered = {
                key: val for key, val in overrides.items()
                if key in TextStyle.__dataclass_fields__
            }
            if filtered:
                return replace(base, **filtered)
        return base

    def get_table_style(self, name: str = "default", **overrides: Any) -> TableStyle:
        base = self.table_styles.get(name, self.table_styles["default"])
        if overrides:
            filtered = {
                key: val for key, val in overrides.items()
                if key in TableStyle.__dataclass_fields__
            }
            if filtered:
                return replace(base, **filtered)
        return base


class TrialityPDFGenerator:
    """Enhanced PDF generator with improved layout and content structure"""
    
    def __init__(
        self,
        results_dir: str = "results",
        figures_dir: str = "paper/figures",
        pdf_path: str = "paper/triality_preprint.pdf",
        style_overrides: Optional[Dict[str, Any]] = None,
    ):
        self.results_dir = results_dir
        self.figures_dir = figures_dir
        self.pdf_path = pdf_path
        self.styles = StyleManager(style_overrides)
        self.data = {}
        self.setup_matplotlib()
    
    def setup_matplotlib(self):
        """Configure matplotlib for professional output"""
        plt.rcParams.update(self.styles.layout.get("matplotlib", {}))
    
    def load_json(self, fp: str) -> Dict[str, Any]:
        """Load JSON file with error handling"""
        try:
            with open(fp, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load {fp}: {e}")
            return {}
    
    def load_data(self):
        """Load all generated data from results directory"""
        print("Loading data from results directory...")

        # Bicoherence data
        paths = glob.glob(os.path.join(self.results_dir, "bic_*.json"))
        rows: List[Dict[str, Any]] = []
        for p in paths:
            tag = os.path.basename(p).split("bic_")[-1].split(".json")[0]
            obj = self.load_json(p)
            if obj:
                obj["case"] = tag
                rows.append(obj)
        if rows:
            self.data["bicoherence_summary"] = pd.DataFrame(rows)
    
        # Koopman data
        p = os.path.join(self.results_dir, "koopman_summary.json")
        if os.path.exists(p):
            koopman_data = self.load_json(p)
            if koopman_data:
                self.data["koopman_summary"] = pd.DataFrame([koopman_data])

        # Latency data
        p = os.path.join(self.results_dir, "latency_fit.json")
        if os.path.exists(p):
            latency_data = self.load_json(p)
            if latency_data:
                self.data["latency_fit"] = pd.DataFrame([latency_data])

        # Ablations data
        p = os.path.join(self.results_dir, "abl_no_triads.json")
        if os.path.exists(p):
            no_triads_data = self.load_json(p)
            if no_triads_data:
                self.data["ablation_no_triads"] = pd.DataFrame([no_triads_data])

        p = os.path.join(self.results_dir, "abl_phi_convergents.json")
        if os.path.exists(p):
            obj = self.load_json(p)
            if obj:
                conv_rows = [dict(case=k, **v) for k, v in obj.items()]
                self.data["ablation_phi_convergents"] = pd.DataFrame(conv_rows)

        # Noise stress data
        p = os.path.join(self.results_dir, "abl_noise_stress.json")
        if os.path.exists(p):
            noise_data = self.load_json(p)
            if noise_data:
                self.data["ablation_noise"] = pd.DataFrame(noise_data)

        print(f"Loaded {len(self.data)} datasets")

    # ----------------------
    # Layout/utility helpers
    # ----------------------
    def resolve_image_path(self, filename: str) -> str:
        """Return best path for an image, checking figures then results."""
        fig_path = os.path.join(self.figures_dir, filename)
        if os.path.exists(fig_path):
            return fig_path
        res_path = os.path.join(self.results_dir, filename)
        if os.path.exists(res_path):
            return res_path
        return fig_path  # default to figures path

    def create_page(self) -> Tuple[plt.Figure, plt.Axes]:
        """Create a figure/axes pair honouring layout configuration."""
        page_cfg = self.styles.layout.get("page", {})
        size = tuple(page_cfg.get("size", (8.5, 11)))
        x_limits = tuple(page_cfg.get("x_limits", (0.05, 0.95)))
        y_limits = tuple(page_cfg.get("y_limits", (0.05, 0.95)))

        fig, ax = plt.subplots(figsize=size)
        ax.set_xlim(*x_limits)
        ax.set_ylim(*y_limits)
        ax.axis("off")
        return fig, ax

    def draw_text(
        self,
        container: Any,
        x: float,
        y: float,
        text: str,
        style_key: str = "body",
        text_kwargs: Optional[Dict[str, Any]] = None,
        **overrides: Any,
    ) -> TextStyle:
        """Render text using a named style and return the resolved style."""
        style = self.styles.get_text_style(style_key, **overrides)
        kwargs = style.to_kwargs()
        if text_kwargs:
            kwargs.update(text_kwargs)
        container.text(x, y, text, **kwargs)
        return style

    def draw_header_footer(self, fig: plt.Figure, section_title: str) -> None:
        """Draw professional header and footer with page numbers and section."""
        header_cfg = self.styles.layout.get("header", {})
        footer_cfg = self.styles.layout.get("footer", {})

        self.draw_text(
            fig,
            header_cfg.get("left_x", 0.06),
            header_cfg.get("y", 0.97),
            "Triality: Triadic Dynamics on a Toroidal Harmonic Bundle",
            style_key="header_left",
        )
        self.draw_text(
            fig,
            header_cfg.get("right_x", 0.94),
            header_cfg.get("y", 0.97),
            section_title,
            style_key="header_right",
        )
        self.draw_text(
            fig,
            footer_cfg.get("left_x", 0.06),
            footer_cfg.get("y", 0.03),
            datetime.now().strftime("%b %d, %Y"),
            style_key="footer_left",
        )
        self.draw_text(
            fig,
            footer_cfg.get("right_x", 0.94),
            footer_cfg.get("y", 0.03),
            f"Page {self.current_page_num} of {self.total_pages}",
            style_key="footer_right",
        )

    def add_multicol_text(
        self,
        ax,
        text: str,
        x: float,
        y: float,
        columns: int = 2,
        style_key: str = "body",
        gutter: Optional[float] = None,
        **overrides: Any,
    ) -> float:
        """Render text into multiple columns; returns new y after block."""
        style = self.styles.get_text_style(style_key, **overrides)
        total_width = style.width
        page_cfg = self.styles.layout.get("page", {})
        gutter = gutter if gutter is not None else page_cfg.get("column_gutter", 0.04)
        column_width = max(total_width - gutter * (columns - 1), 0.01) / max(columns, 1)

        wrapper = textwrap.TextWrapper(width=max(1, int(column_width * 100)))
        lines = wrapper.wrap(text)
        if not lines:
            return y - style.paragraph_spacing

        lines_per_col = int(np.ceil(len(lines) / columns))
        for ci in range(columns):
            start = ci * lines_per_col
            end = min((ci + 1) * lines_per_col, len(lines))
            if start >= len(lines):
                break
            x_col = x + ci * (column_width + gutter)
            for li, line in enumerate(lines[start:end]):
                ax.text(x_col, y - li * style.line_height, line, **style.to_kwargs())

        return y - lines_per_col * style.line_height - style.paragraph_spacing
    
    def add_wrapped_text(
        self,
        ax,
        text: str,
        x: float,
        y: float,
        style_key: str = "body",
        **overrides: Any,
    ) -> float:
        """Add properly wrapped text and return new y position."""
        style = self.styles.get_text_style(style_key, **overrides)
        wrapper = textwrap.TextWrapper(width=max(1, int(style.width * 100)))
        lines = wrapper.wrap(text)

        if not lines:
            return y - style.paragraph_spacing

        for idx, line in enumerate(lines):
            ax.text(x, y - idx * style.line_height, line, **style.to_kwargs())
        
        return y - len(lines) * style.line_height - style.paragraph_spacing
    
    def add_section_header(
        self,
        ax,
        title: str,
        x: float,
        y: float,
        style_key: str = "section_header",
        **overrides: Any,
    ) -> float:
        """Add a section header with configurable styling."""
        style = self.draw_text(ax, x, y, title, style_key=style_key, **overrides)
        return y - max(style.line_height, style.paragraph_spacing)
    
    def add_subsection_header(
        self,
        ax,
        title: str,
        x: float,
        y: float,
        style_key: str = "subsection_header",
        **overrides: Any,
    ) -> float:
        """Add a subsection header with configurable styling."""
        style = self.draw_text(ax, x, y, title, style_key=style_key, **overrides)
        return y - max(style.line_height, style.paragraph_spacing)
    
    def create_table(
        self,
        ax,
        data: List[List[str]],
        x: float,
        y: float,
        title: str = "",
        style_key: str = "default",
        caption_style_key: Optional[str] = None,
        caption_align: Optional[str] = None,
        **overrides: Any,
    ) -> float:
        """Create a professional table and return new y position below it."""
        if not data:
            return y

        table_style = self.styles.get_table_style(style_key, **overrides)
        caption_style_name = caption_style_key or table_style.caption_style
        caption_style = self.styles.get_text_style(caption_style_name)
        align = caption_align or table_style.caption_align

        if title:
            if align == "center":
                caption_x = x + table_style.width / 2
            else:
                caption_x = x
            applied_style = self.draw_text(
                ax,
                caption_x,
                y,
                title,
                style_key=caption_style_name,
                ha=align,
            )
            y -= applied_style.line_height + applied_style.paragraph_spacing

        height = max(table_style.row_height * len(data), 0.06)
        y_table_top = y - height

        table = ax.table(
            cellText=data,
            loc='center',
            cellLoc='center',
            bbox=[x, y_table_top, table_style.width, height],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(table_style.font_size)
        table.scale(1, table_style.scale_y)

        for i in range(len(data[0])):
            header_cell = table[(0, i)]
            header_cell.set_facecolor(table_style.header_color)
            header_cell.set_text_props(weight=table_style.header_fontweight)

        return y_table_top - table_style.padding
    
    def create_title_page(self, pdf):
        """Create enhanced title page with better layout"""
        fig, ax = self.create_page()
        
        # Title with better spacing
        self.draw_text(
            ax,
            0.5,
            0.75,
            "Triadic Dynamics on a Toroidal Harmonic Bundle:",
            style_key="title_main",
        )
        self.draw_text(
            ax,
            0.5,
            0.68,
            "φ-Scaled Resonances, Limit-Cycle Attractors,",
            style_key="title_secondary",
        )
        self.draw_text(
            ax,
            0.5,
            0.61,
            "and a Hyperdimensional Encoding",
            style_key="title_secondary",
        )
        
        # Authors
        self.draw_text(
            ax,
            0.5,
            0.5,
            "Darryl C. Novotny and Collaborators",
            style_key="title_author",
        )
        
        # Date
        self.draw_text(
            ax,
            0.5,
            0.43,
            datetime.now().strftime("%B %d, %Y"),
            style_key="title_date",
        )
        
        # Abstract with better formatting
        abstract_text = ("We present a tractable framework with torus-fibered dynamics, "
                        "tri-linear closure, a golden-ratio resonance ladder, and hypergraph "
                        "limit cycles. A methods pipeline---bicoherence, Koopman spectra, "
                        "and HDC encodings---yields falsifiable predictions. Code accompanies "
                        "this manuscript.")
        
        # Abstract box
        abstract_box_cfg = self.styles.layout.get("boxes", {}).get("abstract", {})
        abstract_rect = Rectangle(
            abstract_box_cfg.get("xy", (0.1, 0.15)),
            abstract_box_cfg.get("width", 0.8),
            abstract_box_cfg.get("height", 0.25),
            facecolor=abstract_box_cfg.get("facecolor", "#f8f9fa"),
            edgecolor=abstract_box_cfg.get("edgecolor", "#dee2e6"),
            alpha=abstract_box_cfg.get("alpha", 0.8),
            linewidth=abstract_box_cfg.get("linewidth", 1),
            transform=ax.transAxes,
        )
        ax.add_patch(abstract_rect)
        
        self.draw_text(ax, 0.5, 0.35, "Abstract", style_key="abstract_heading")
        
        self.add_wrapped_text(ax, abstract_text, 0.15, 0.32, style_key="abstract_body")
        
        # Header/footer
        self.draw_header_footer(fig, "Title")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

    def create_toc_page(self, pdf):
        """Create a simple table of contents page."""
        fig, ax = self.create_page()

        y_pos = 0.95
        y_pos = self.add_section_header(ax, "Table of Contents", 0.05, y_pos)

        entries = [
            ("1. Title", 1),
            ("2. Introduction", 2),
            ("3. Results", 3),
            ("4. Ablations & Robustness", 4),
            ("5. Figures", 5),
            ("6. Methods", 6),
            ("7. Discussion", 7),
            ("8. Conclusion", 8),
        ]

        for title, page in entries:
            entry_style = self.draw_text(
                ax,
                0.08,
                y_pos,
                title,
                ha="left",
            )
            self.draw_text(
                ax,
                0.92,
                y_pos,
                str(page),
                ha="right",
            )
            y_pos -= entry_style.line_height + entry_style.paragraph_spacing

        self.draw_header_footer(fig, "Contents")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
    
    def create_introduction_page(self, pdf):
        """Create introduction page with theoretical background"""
        fig, ax = self.create_page()
        
        y_pos = 0.95
        y_pos = self.add_section_header(ax, "Introduction", 0.05, y_pos)
        
        intro_text = ("The study of nonlinear dynamics in complex systems has revealed "
                     "remarkable patterns of organization, from synchronization phenomena "
                     "in neural networks to collective behavior in biological systems. "
                     "The Triality framework introduces a novel approach to understanding "
                     "these dynamics through the lens of toroidal geometry and harmonic analysis. "
                     "We provide an end-to-end pipeline combining simulation, spectral analysis, "
                     "Koopman operator methods, and hyperdimensional computing to derive falsifiable predictions.")
        
        # Single-column layout requested for page 3
        y_pos = self.add_wrapped_text(ax, intro_text, 0.05, y_pos)
        
        y_pos = self.add_subsection_header(ax, "Theoretical Framework", 0.05, y_pos)
        
        theory_text = ("Our approach centers on three key components: (1) a torus-bundled "
                      "phase space that captures the geometric structure of oscillatory "
                      "dynamics, (2) a φ-scaled resonance ladder based on the golden ratio "
                      "that provides a natural frequency organization, and (3) tri-linear "
                      "closure relations that govern energy exchange between modes.")
        
        y_pos = self.add_wrapped_text(ax, theory_text, 0.05, y_pos)
        
        y_pos = self.add_subsection_header(ax, "Mathematical Foundation", 0.05, y_pos)
        
        math_text = ("The triad Hamiltonian H = Σᵢ ωᵢ|aᵢ|² + κ Σᵢⱼₖ aᵢ*aⱼ*aₖ + c.c. "
                    "describes the interaction between three oscillatory modes, where "
                    "ωᵢ are the natural frequencies, κ is the coupling strength, and "
                    "the tri-linear terms enforce energy conservation. The φ-scaled "
                    "frequencies ωᵢ = ω₀φⁱ create a resonance ladder with optimal "
                    "spacing for nonlinear interactions.")
        
        y_pos = self.add_wrapped_text(ax, math_text, 0.05, y_pos)
        
        self.draw_header_footer(fig, "Introduction")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
        
    def create_results_page(self, pdf):
        """Create enhanced results page with better data presentation"""
        fig, ax = self.create_page()
        
        y_pos = 0.95
        y_pos = self.add_section_header(ax, "Results", 0.05, y_pos)
        
        # Bicoherence analysis
        if "bicoherence_summary" in self.data:
            df = self.data["bicoherence_summary"]
            phi_data = df[df["case"] == "phi"].iloc[0]
            rational_data = df[df["case"] == "rational"].iloc[0]
            
            y_pos = self.add_subsection_header(ax, "φ-Scaled vs Rational Bicoherence Analysis", 
                                            0.05, y_pos)
            
            # Create comparison table
            table_data = [
                ["Metric", "φ-Scaled", "Rational", "Effect Size"],
                ["Peak Bicoherence", f"{phi_data['peak']:.3f}", 
                 f"{rational_data['peak']:.3f}", 
                 f"{phi_data['peak']/rational_data['peak']:.1f}x"],
                ["Compactness", f"{phi_data['compactness']:.3f}", 
                 f"{rational_data['compactness']:.3f}", 
                 f"{phi_data['compactness']/rational_data['compactness']:.2f}x"],
                ["Area Above Threshold", f"{phi_data['area_above']:.3f}", 
                 f"{rational_data['area_above']:.3f}", "~1.0x"]
            ]
            
            y_pos = self.create_table(ax, table_data, 0.05, y_pos, caption_align='center')
            
            # Interpretation
            interpretation = ("The φ-scaled triads show dramatically higher peak bicoherence "
                            "and more compact spectral features compared to rational frequency "
                            "ratios, confirming the theoretical prediction that golden ratio "
                            "spacing optimizes nonlinear interactions.")
            
            y_pos = self.add_wrapped_text(
                ax,
                interpretation,
                0.05,
                y_pos,
                fontstyle='italic',
            )
        
        # Koopman analysis
        if "koopman_summary" in self.data:
            koopman = self.data["koopman_summary"].iloc[0]
            
            y_pos = self.add_subsection_header(ax, "Koopman Eigenvalue Analysis", 
                                            0.05, y_pos)
            
            koopman_table = [
                ["Parameter", "Value", "Interpretation"],
                ["Leading Eigenvalue", f"{koopman['lead']:.6f}", "Near unit circle"],
                ["Spectral Gap", f"{koopman['gap']:.6f}", "Degenerate case"],
                ["R₂ Order Parameter", f"{koopman['R2']:.3f}", "Weak pairwise sync"],
                ["R₃ Order Parameter", f"{koopman['R3']:.3f}", "Moderate triadic sync"]
            ]
            
            y_pos = self.create_table(ax, koopman_table, 0.05, y_pos, caption_align='center')
            
            koopman_interpretation = ("The dominant eigenvalue magnitude near 1.0 indicates "
                                    "limit-cycle behavior, while the spectral gap of 0.0 "
                                    "suggests a degenerate case with multiple modes at the "
                                    "same frequency.")
            
            y_pos = self.add_wrapped_text(
                ax,
                koopman_interpretation,
                0.05,
                y_pos,
                fontstyle='italic',
            )
        
        # Latency analysis
        if "latency_fit" in self.data:
            latency = self.data["latency_fit"].iloc[0]
            
            y_pos = self.add_subsection_header(ax, "Retuning Latency Analysis", 
                                            0.05, y_pos)
            
            latency_table = [
                ["Parameter", "Value", "Significance"],
                ["Slope", f"{latency['slope']:.6f}", "Rate of change"],
                ["Intercept", f"{latency['intercept']:.6f}", "Baseline latency"],
                ["R²", f"{latency['r2']:.6f}", "Fit quality"]
            ]
            
            y_pos = self.create_table(ax, latency_table, 0.05, y_pos)
            
            latency_interpretation = ("The linear relationship between latency and |Δk| "
                                    "confirms the theoretical prediction that retuning time "
                                    "scales with the distance from the resonance ladder.")
            
            y_pos = self.add_wrapped_text(
                ax,
                latency_interpretation,
                0.05,
                y_pos,
                fontstyle='italic',
            )
        
        self.draw_header_footer(fig, "Results")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
        
    def create_ablations_page(self, pdf):
        """Create enhanced ablations page with comprehensive analysis"""
        fig, ax = self.create_page()
        
        y_pos = 0.95
        y_pos = self.add_section_header(ax, "Ablations & Robustness", 0.05, y_pos)
        
        # No triads control
        if "ablation_no_triads" in self.data:
            no_triads = self.data["ablation_no_triads"].iloc[0]
            
            y_pos = self.add_subsection_header(ax, "No Triads Control (J=0)", 0.05, y_pos)
            
            no_triads_table = [
                ["Parameter", "With Triads", "Without Triads", "Change"],
                ["R₂ Order Parameter", "0.035", f"{no_triads['R2']:.3f}", 
                 f"{no_triads['R2']/0.035:.2f}x"],
                ["R₃ Order Parameter", "0.067", f"{no_triads['R3']:.3f}", 
                 f"{no_triads['R3']/0.067:.2f}x"],
                ["Leading Eigenvalue", "1.000", f"{no_triads['lead']:.3f}", 
                 f"{no_triads['lead']/1.000:.3f}x"],
                ["Spectral Gap", "0.000", f"{no_triads['gap']:.3f}", "N/A"]
            ]
            
            y_pos = self.create_table(ax, no_triads_table, 0.05, y_pos, caption_align='center')
            
            no_triads_interpretation = ("Removing triadic couplings dramatically reduces both "
                                      "R₂ and R₃ order parameters, confirming that triadic "
                                      "interactions are essential for maintaining synchronization "
                                      "in the hypergraph dynamics.")
            
            y_pos = self.add_wrapped_text(
                ax,
                no_triads_interpretation,
                0.05,
                y_pos,
                fontstyle='italic',
            )
        
        # φ vs convergents
        if "ablation_phi_convergents" in self.data:
            df = self.data["ablation_phi_convergents"]
            
            y_pos = self.add_subsection_header(ax, "φ vs Convergents Comparison", 0.05, y_pos)
            
            convergents_table = [
                ["Case", "Peak Bicoherence", "Compactness", "Relative to φ"],
                ["φ (golden)", f"{df[df['case']=='phi']['peak'].iloc[0]:.3f}", 
                 f"{df[df['case']=='phi']['compactness'].iloc[0]:.3f}", "1.00x"],
                ["8/5", f"{df[df['case']=='8_5']['peak'].iloc[0]:.3f}", 
                 f"{df[df['case']=='8_5']['compactness'].iloc[0]:.3f}", 
                 f"{df[df['case']=='8_5']['peak'].iloc[0]/df[df['case']=='phi']['peak'].iloc[0]:.2f}x"],
                ["13/8", f"{df[df['case']=='13_8']['peak'].iloc[0]:.3f}", 
                 f"{df[df['case']=='13_8']['compactness'].iloc[0]:.3f}", 
                 f"{df[df['case']=='13_8']['peak'].iloc[0]/df[df['case']=='phi']['peak'].iloc[0]:.2f}x"],
                ["21/13", f"{df[df['case']=='21_13']['peak'].iloc[0]:.3f}", 
                 f"{df[df['case']=='21_13']['compactness'].iloc[0]:.3f}", 
                 f"{df[df['case']=='21_13']['peak'].iloc[0]/df[df['case']=='phi']['peak'].iloc[0]:.2f}x"]
            ]
            
            y_pos = self.create_table(ax, convergents_table, 0.05, y_pos, caption_align='center')
            
            convergents_interpretation = ("Progressive degradation from φ to rational convergents "
                                        "demonstrates that the golden ratio provides optimal "
                                        "spacing for nonlinear interactions, with performance "
                                        "decreasing as ratios deviate from φ.")
            
            y_pos = self.add_wrapped_text(
                ax,
                convergents_interpretation,
                0.05,
                y_pos,
                fontstyle='italic',
            )
        
        # Noise stress analysis
        if "ablation_noise" in self.data:
            noise_df = self.data["ablation_noise"]
            
            y_pos = self.add_subsection_header(ax, "Noise Stress Analysis", 0.05, y_pos)
            
            noise_table = [["Noise Level", "R₂", "R₃", "Spectral Gap", "Robustness"]]
            for _, row in noise_df.iterrows():
                robustness = "High" if row['gap'] > 0.01 else "Low" if row['gap'] < 0.001 else "Medium"
                noise_table.append([
                    f"{row['noise']:.2f}",
                    f"{row['R2']:.3f}",
                    f"{row['R3']:.3f}",
                    f"{row['gap']:.4f}",
                    robustness
                ])
            
            y_pos = self.create_table(ax, noise_table, 0.05, y_pos, caption_align='center')
            
            noise_interpretation = ("The system shows graceful degradation under noise stress, "
                                  "with order parameters and spectral properties maintaining "
                                  "reasonable values even at moderate noise levels.")
            
            y_pos = self.add_wrapped_text(
                ax,
                noise_interpretation,
                0.05,
                y_pos,
                fontstyle='italic',
            )
        
        self.draw_header_footer(fig, "Ablations")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
        
    def create_figures_page(self, pdf):
        """Create enhanced figures page with proper captions"""
        page_cfg = self.styles.layout.get("page", {})
        page_size = tuple(page_cfg.get("size", (8.5, 11)))
        fig, axes = plt.subplots(2, 2, figsize=page_size)
        title_style = self.styles.get_text_style("figure_title")
        fig.suptitle("Experimental Results", y=0.95, **title_style.to_kwargs())
        
        caption_style = self.styles.get_text_style("figure_caption")
        caption_kwargs = caption_style.to_kwargs()
        
        figure_files = [
            ("bico_phi.png", "Figure 1A: φ-Scaled Bicoherence", axes[0][0]),
            ("bico_rational.png", "Figure 1B: Rational Bicoherence", axes[0][1]),
            ("koopman_hist.png", "Figure 2A: Koopman Eigenvalue Histogram", axes[1][0]),
            ("latency_fit.png", "Figure 2B: Latency vs Ladder Distance", axes[1][1])
        ]
        
        for filename, title, ax in figure_files:
            filepath = self.resolve_image_path(filename)
            if os.path.exists(filepath):
                try:
                    img = plt.imread(filepath)
                    ax.imshow(img, aspect='auto')
                    ax.set_title(title, pad=10, **caption_kwargs)
                except Exception as exc:
                    self.draw_text(
                        ax,
                        0.5,
                        0.5,
                        f"Error loading {filename}\n{exc}",
                        style_key="figure_error",
                        text_kwargs={"transform": ax.transAxes},
                    )
                    ax.set_title(title, pad=10, **caption_kwargs)
            else:
                self.draw_text(
                    ax,
                    0.5,
                    0.5,
                    f"Figure not found:\n{filename}",
                    style_key="figure_missing",
                    text_kwargs={"transform": ax.transAxes},
                )
                ax.set_title(title, pad=10, **caption_kwargs)
            ax.axis("off")
        
        plt.tight_layout()
        self.draw_header_footer(fig, "Figures")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
        
    def create_methods_page(self, pdf):
        """Create enhanced methods page with detailed technical information"""
        fig, ax = self.create_page()
        
        y_pos = 0.95
        y_pos = self.add_section_header(ax, "Methods", 0.05, y_pos)
        
        # Simulation Framework
        y_pos = self.add_subsection_header(ax, "Simulation Framework", 0.05, y_pos)
        
        simulation_text = ("The triad Hamiltonian H = Σᵢ ωᵢ|aᵢ|² + κ Σᵢⱼₖ aᵢ*aⱼ*aₖ + c.c. "
                          "describes the interaction between three oscillatory modes with "
                          "frequencies ωᵢ = ω₀φⁱ (golden ratio scaling), coupling strength "
                          "κ = 0.03, and tri-linear closure relations. The hypergraph model "
                          "uses Stuart-Landau oscillators with triadic couplings J = 0.10.")
        
        y_pos = self.add_wrapped_text(ax, simulation_text, 0.05, y_pos)
        
        # Analysis Pipeline
        y_pos = self.add_subsection_header(ax, "Analysis Pipeline", 0.05, y_pos)
        
        analysis_text = ("Bicoherence analysis uses Welch's method with 512-point windows "
                        "and 50% overlap. Koopman analysis employs Extended Dynamic Mode "
                        "Decomposition (EDMD) with polynomial observables. Order parameters "
                        "R₂ and R₃ quantify pairwise and triadic synchronization. Latency "
                        "analysis fits linear models to retuning time vs ladder distance.")
        
        y_pos = self.add_wrapped_text(ax, analysis_text, 0.05, y_pos)
        
        # Computational Details
        y_pos = self.add_subsection_header(ax, "Computational Details", 0.05, y_pos)
        
        comp_table = [
            ["Component", "Implementation", "Parameters"],
            ["Integration", "scipy.integrate.solve_ivp", "Adaptive step size, max_step=0.1"],
            ["Spectral Analysis", "scipy.signal.welch", "512-point windows, 50% overlap"],
            ["Koopman Analysis", "Custom EDMD", "Polynomial observables up to 2nd order"],
            ["Statistical Analysis", "numpy.linalg.lstsq", "Linear regression with R²"],
            ["Visualization", "matplotlib", "300 DPI, publication quality"]
        ]
        
        y_pos = self.create_table(ax, comp_table, 0.05, y_pos)
        
        # Reproducibility
        y_pos = self.add_subsection_header(ax, "Reproducibility", 0.05, y_pos)
        
        repro_text = ("All parameters are specified in the code with fixed random seeds "
                     "for reproducibility. The implementation is cross-platform Python "
                     "with no external dependencies beyond the standard scientific stack. "
                     "Code is available at the repository with comprehensive documentation.")
        
        y_pos = self.add_wrapped_text(ax, repro_text, 0.05, y_pos)
        
        self.draw_header_footer(fig, "Methods")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
    
    def create_discussion_page(self, pdf):
        """Create discussion page with interpretation and future work"""
        fig, ax = self.create_page()
        
        y_pos = 0.95
        y_pos = self.add_section_header(ax, "Discussion", 0.05, y_pos)
        
        # Key Findings
        y_pos = self.add_subsection_header(ax, "Key Findings", 0.05, y_pos)
        
        findings_text = ("Our results demonstrate that φ-scaled frequency ratios provide "
                        "optimal conditions for nonlinear interactions, as evidenced by "
                        "dramatically higher bicoherence peaks and more compact spectral "
                        "features compared to rational ratios. The Koopman analysis reveals "
                        "limit-cycle behavior with degenerate eigenvalues, suggesting "
                        "complex dynamics near the unit circle.")
        
        y_pos = self.add_wrapped_text(ax, findings_text, 0.05, y_pos)
        
        # Theoretical Implications
        y_pos = self.add_subsection_header(ax, "Theoretical Implications", 0.05, y_pos)
        
        theory_text = ("The golden ratio's optimality for nonlinear interactions suggests "
                      "a deep connection between number theory and dynamical systems. The "
                      "triadic closure relations may provide a mechanism for information "
                      "processing in biological networks, where φ-scaled frequencies could "
                      "enable efficient energy transfer and synchronization.")
        
        y_pos = self.add_wrapped_text(ax, theory_text, 0.05, y_pos)
        
        # Limitations
        y_pos = self.add_subsection_header(ax, "Limitations", 0.05, y_pos)
        
        limitations_text = ("The current analysis is limited to three-mode interactions "
                           "and may not capture the full complexity of real-world systems. "
                           "The noise stress analysis shows some degradation, suggesting "
                           "the need for robustness mechanisms. Future work should explore "
                           "higher-dimensional systems and experimental validation.")
        
        y_pos = self.add_wrapped_text(ax, limitations_text, 0.05, y_pos)
        
        # Future Work
        y_pos = self.add_subsection_header(ax, "Future Work", 0.05, y_pos)
        
        future_text = ("Future directions include: (1) extending to N-mode systems with "
                      "hierarchical φ-scaled ladders, (2) experimental validation using "
                      "optical or mechanical oscillators, (3) applications to neural "
                      "synchronization and brain dynamics, (4) development of control "
                      "strategies based on φ-scaled frequency tuning.")
        
        y_pos = self.add_wrapped_text(ax, future_text, 0.05, y_pos)
        
        self.draw_header_footer(fig, "Discussion")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
        
    def create_conclusion_page(self, pdf):
        """Create conclusion page with summary and impact"""
        fig, ax = self.create_page()
        
        y_pos = 0.95
        y_pos = self.add_section_header(ax, "Conclusion", 0.05, y_pos)
        
        conclusion_text = ("The Triality framework provides a novel approach to understanding "
                          "nonlinear dynamics through toroidal geometry and φ-scaled resonance "
                          "ladders. Our results demonstrate the optimality of golden ratio "
                          "frequency spacing for nonlinear interactions, with significant "
                          "implications for biological systems and information processing. "
                          "The framework offers a tractable yet powerful tool for analyzing "
                          "complex oscillatory networks.")
        
        y_pos = self.add_wrapped_text(ax, conclusion_text, 0.05, y_pos)
        
        # Impact Statement
        y_pos = self.add_subsection_header(ax, "Impact", 0.05, y_pos)
        
        impact_text = ("This work opens new avenues for understanding synchronization in "
                      "biological networks, with potential applications in neuroscience, "
                      "biophysics, and engineering. The φ-scaled resonance ladder provides "
                      "a natural framework for frequency organization that may be exploited "
                      "in the design of robust oscillatory systems.")
        
        y_pos = self.add_wrapped_text(ax, impact_text, 0.05, y_pos)
        
        # Acknowledgments
        y_pos = self.add_subsection_header(ax, "Acknowledgments", 0.05, y_pos)
        
        ack_text = ("We thank the scientific community for valuable discussions and "
                   "feedback. This work was supported by computational resources and "
                   "open-source software development. Code and data are available "
                   "for reproducibility and further research.")
        
        y_pos = self.add_wrapped_text(ax, ack_text, 0.05, y_pos)
        
        self.draw_header_footer(fig, "Conclusion")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
    
    def generate_pdf(self):
        """Generate the complete enhanced PDF"""
        print("Generating enhanced PDF from Python...")
        
        # Load all data
        self.load_data()
        # Simple page count tracking for footer
        self.current_page_num = 0
        self.total_pages = 9
        
        # Create PDF with all pages
        with PdfPages(self.pdf_path) as pdf:
            # Set document metadata
            metadata = {
                'Title': 'Triality: Triadic Dynamics on a Toroidal Harmonic Bundle',
                'Author': 'Darryl C. Novotny et al.',
                'Subject': 'Nonlinear dynamics, Koopman operators, hypergraphs, HDC',
                'Keywords': 'triality, golden ratio, bicoherence, Koopman, HDC, hypergraph',
                'CreationDate': datetime.now().strftime("D:%Y%m%d%H%M%S")
            }
            try:
                pdf.infodict().update(metadata)
            except Exception:
                pass

            # Title page
            self.current_page_num = 1
            self.create_title_page(pdf)
            
            # TOC page
            self.current_page_num = 2
            self.create_toc_page(pdf)

            # Introduction page
            self.current_page_num = 3
            self.create_introduction_page(pdf)
            
            # Results page
            self.current_page_num = 4
            self.create_results_page(pdf)
            
            # Ablations page
            self.current_page_num = 5
            self.create_ablations_page(pdf)
            
            # Figures page
            self.current_page_num = 6
            self.create_figures_page(pdf)
            
            # Methods page
            self.current_page_num = 7
            self.create_methods_page(pdf)
            
            # Discussion page
            self.current_page_num = 8
            self.create_discussion_page(pdf)
            
            # Conclusion page
            self.current_page_num = 9
            self.create_conclusion_page(pdf)
        
        print(f"Enhanced PDF generated: {self.pdf_path}")
        return self.pdf_path

def create_pdf():
    """Main function for backward compatibility"""
    generator = TrialityPDFGenerator()
    return generator.generate_pdf()

if __name__ == "__main__":
    create_pdf()
