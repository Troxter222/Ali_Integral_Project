import sys
from src.utils import download_font
from src.physics import run_simulation
from src.plotting import generate_plots
from src.pdf_generator import build_pdf

def main():
    print("--- Vision Theory Project (V10) ---")
    
    # 1. Setup Resources
    font_path = download_font()
    if not font_path:
        print("[CRITICAL ERROR] Font not found. Exiting.")
        sys.exit(1)

    # 2. Run Physics Simulation
    results = run_simulation()

    # 3. Generate Visual Assets
    generate_plots(results)

    # 4. Compile Final Paper
    build_pdf(font_path)

    print("\n--- Project Build Complete ---")
    print("Check the 'output/' folder for results.")

if __name__ == "__main__":
    main()