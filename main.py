import sys
from ali_integral.utils import download_font
from ali_integral.physics import run_simulation
from ali_integral.plotting import generate_plots
from ali_integral.pdf_generator import build_pdf
from ali_integral.eht_imaging import generate_shadow_image
from ali_integral.visualizer_eht import generate_eht_animation
from ali_integral.visualizer import create_animation

def main():
    print("--- Vision Theory Project (V12: Thermodynamics & EHT) ---")
    
    # 1. Setup Resources
    font_path = download_font()
    if not font_path:
        sys.exit(1)

    # 2. Run Physics Simulation
    results = run_simulation()

    # 3. Generate Standard Plots
    generate_plots(results)

    # 4. Generate Visual Simulation (GIF)
    create_animation()
    generate_eht_animation()

    # --- EHT SIMULATION ---
    ifi_ton = results["TON 618"]["I_Ali"]
    ifi_stellar = results["Stellar BH"]["I_Ali"]
    
    import math
    
    if ifi_stellar > 0:
        impact_factor = math.log10(ifi_ton / ifi_stellar) / 10.0
    else:
        impact_factor = 0.5

    generate_shadow_image(impact_factor)
    build_pdf(font_path)

    print("\n--- Project Build Complete ---")

if __name__ == "__main__":
    main()