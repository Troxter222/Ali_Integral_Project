from fpdf import FPDF
from src.config import B0, SNR0

OUTPUT_DIR = "output"

class ScientificPaper(FPDF):
    def footer(self):
        self.set_y(-15)
        try:
            self.set_font('SciFont', '', 8)
        except Exception:
            self.set_font('Arial', '', 8)
            
        self.cell(0, 10, f'Page {self.page_no()} | Vision Theory V10 (Final)', 0, 0, 'C')

    def chapter_header(self, txt):
        self.ln(8)
        try:
            self.set_font('SciFont', '', 12)
        except Exception:
            self.set_font('Arial', 'B', 12)

        self.cell(0, 8, txt, 0, 1, 'L')
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

    def body_text(self, txt):
        try:
            self.set_font('SciFont', '', 10)
        except Exception:
            self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, txt)
        self.ln(2)

    def draw_param_table(self):
        self.ln(5)
        self.set_fill_color(240, 240, 240)
        self.set_font('SciFont', '', 10)
        self.cell(0, 8, "Table 1: Model Parameters", 0, 1, 'L', fill=True)
        
        data = [
            ("B0", f"{B0/1e9} GHz", "Base Detector Bandwidth"),
            ("SNR0", f"{SNR0}", "Initial Signal-to-Noise Ratio"),
            ("C_limit", "~10^17 ops/s", "Lloyd Bound (Thermal Limit)"),
            ("F_crit", "10^14 W/m^2", "Structural Crash Threshold"),
            ("Metric", "Kerr (Ideal)", "Spacetime Geometry")
        ]
        
        self.set_font('SciFont', '', 9)
        for name, val, desc in data:
            self.cell(25, 6, name, 1)
            self.cell(35, 6, val, 1)
            self.cell(130, 6, desc, 1)
            self.ln()
        self.ln(5)

def build_pdf(font_path):
    print("[INFO] Compiling PDF Paper...")
    
    pdf = ScientificPaper()
    pdf.add_page()
    pdf.add_font('SciFont', '', font_path, uni=True)

    # Title
    pdf.set_font('SciFont', '', 16)
    pdf.cell(0, 10, 'THE ALI INTEGRAL: OBSERVABLE FUTURE INFORMATION', 0, 1, 'C')
    pdf.set_font('SciFont', '', 12)
    pdf.cell(0, 8, 'Quantum-Information Analysis of the Cauchy Horizon', 0, 1, 'C')
    pdf.set_font('SciFont', '', 10)
    pdf.cell(0, 8, 'Author: Ali | Version: 10.0 (Final Release)', 0, 1, 'C')
    pdf.ln(5)

    # Abstract
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 6, 'ABSTRACT', 0, 1, 'L')
    abs_txt = (
        "This paper presents the final formulation of 'Vision Theory', unifying General Relativity "
        "and Information Theory. We introduce the metric I_Ali (Total OFI), calculated via the "
        "Shannon-Hartley theorem, accounting for dynamic SNR and quadratic energy flux growth. "
        "We demonstrate that the Lloyd limit and thermal destruction of the probe render the "
        "amount of receivable information finite, yet vast for supermassive black holes."
    )
    pdf.set_font('SciFont', '', 10)
    pdf.multi_cell(0, 5, abs_txt, fill=True)

    pdf.draw_param_table()

    # Sections
    pdf.chapter_header('1. Physical Model (Physics & Info)')
    pdf.body_text(
        "We consider a communication channel where capacity is defined by the Shannon equation. "
        "A key feature is the dependence of SNR on the gravitational shift g(tau):"
    )
    pdf.image(f"{OUTPUT_DIR}/eq_snr.png", x=60, w=80)
    pdf.body_text(
        "Energy Flux scales as the square of g(tau), since both photon energy and arrival frequency increase:"
    )
    pdf.image(f"{OUTPUT_DIR}/eq_flux.png", x=60, w=80)

    pdf.chapter_header('2. Fundamental Limits')
    pdf.body_text(
        "Maximum processing speed is bounded by the Lloyd limit, dependent on system energy E:"
    )
    pdf.image(f"{OUTPUT_DIR}/eq_lloyd.png", x=70, w=60)
    pdf.body_text(
        "The simulation employs C_limit corresponding to the processor's effective energy, "
        "or the Thermal Crash threshold, whichever occurs first."
    )

    pdf.chapter_header('3. Simulation Results')
    pdf.body_text(
        "Fig. 1 illustrates the 'Information Horizon'. The OFI zone (gray) represents data "
        "the probe successfully decodes before thermal destruction."
    )
    pdf.image(f"{OUTPUT_DIR}/fig1_capacity.png", x=25, w=160)
    pdf.ln(5)
    pdf.body_text(
        "Comparative analysis (Fig. 2) confirms that TON 618 is the most efficient instrument "
        "for hypothetical observation of the future (OFI is orders of magnitude higher)."
    )
    pdf.image(f"{OUTPUT_DIR}/fig2_scaling.png", x=25, w=160)

    pdf.chapter_header('4. Conclusion')
    pdf.body_text(
        "The developed I_Ali model successfully resolves the infinite energy paradox through "
        "information and thermodynamic limits. This work provides a rigorous mathematical "
        "framework for estimating the observability of 'Universe History' inside the event horizon."
    )

    pdf.chapter_header('References')
    pdf.set_font('SciFont', '', 9)
    refs = [
        "1. Shannon, C. E. (1948). A Mathematical Theory of Communication.",
        "2. Lloyd, S. (2000). Ultimate physical limits to computation. Nature.",
        "3. Poisson, E. & Israel, W. (1990). Mass Inflation.",
        "4. Hamilton, A. J. S. (2012). Inside Black Holes."
    ]
    for r in refs:
        pdf.cell(0, 5, r, 0, 1)

    pdf_path = f"{OUTPUT_DIR}/Vision_Theory_Ali_V10_Final.pdf"
    pdf.output(pdf_path)
    print(f"[SUCCESS] PDF generated: {pdf_path}")