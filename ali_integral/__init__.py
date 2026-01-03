"""
Ali Integral - A library for calculating Information Flux at the Cauchy Horizon.
"""

from .physics import calculate_ali_integral
from .visualizer import plot_information_horizon

PRESETS = {
    "SgrA*": 4.1e6,
    "M87*": 6.5e9,
    "TON618": 6.6e10,
    "CygnusX-1": 14.8,
    "Sun": 1.0
}

def run(target="SgrA*", save=False):
    mass = 0.0
    name = "Custom Black Hole"
    
    if isinstance(target, str):
        if target in PRESETS:
            mass = PRESETS[target]
            name = target
        else:
            print(f"Error: Unknown preset '{target}'. Available: {list(PRESETS.keys())}")
            return
    else:
        mass = float(target)
    
    print("\n🚀 INITIALIZING VISION THEORY SIMULATION...")
    print(f"Target: {name}")
    print(f"Mass: {mass:.2e} Solar Masses")
    print("-" * 30)

    # 2. Colculates
    try:
        ofi_bits = calculate_ali_integral(mass) 
        
        print("✅ CALCULATION COMPLETE")
        print(f"Ali Integral (OFI): {ofi_bits:.2e} bits")
        
        gb = ofi_bits / (8 * 10**9)
        print(f"Human readable: ~{gb:.2f} Gigabytes (before thermal crash)")
        
    except Exception as e:
        print(f"❌ Physics Error: {e}")
        return

    # 3. Visualization
    print("-" * 30)
    print("🎨 GENERATING VISUALIZATION...")
    try:
        plot_information_horizon(mass)
        if save:
            print("Image saved.")
    except Exception as e:
        print(f"❌ Plotting Error: {e}")

    print("Done.\n")