import numpy as np
from scipy.integrate import simpson
from src.config import B0, SNR0, C_LIMIT, F_CRIT, HOLES, STEPS

def run_simulation():
    """
    Executes the 'Ali Integral' simulation.
    Calculates OFI (Observable Future Information) for different BH masses.
    """
    print("[INFO] Running Physics Simulation (V10 Core)...")
    
    results = {}

    for name, M in HOLES.items():
        # r normalized: 1.0 (Horizon) -> 0 (Singularity)
        r = np.linspace(1.0, 1e-5, STEPS)
        
        # Proper time tau scales with Mass M
        tau = np.linspace(0, M, STEPS)
        
        # --- PHYSICS ENGINE ---
        
        # 1. Gravitational Blueshift Factor (g)
        g_factor = 1.0 / r
        
        # 2. Bandwidth (Doppler/Gravitational shift)
        B_tau = B0 * g_factor
        
        # 3. Energy Flux (Scales as g^2 due to frequency + arrival rate)
        Flux = 1.0 * (g_factor**2)
        
        # 4. Signal-to-Noise Ratio (Dynamic)
        SNR_tau = SNR0 * g_factor
        
        # 5. Shannon-Hartley Capacity (Bits/sec)
        C_in = B_tau * np.log2(1 + SNR_tau)
        
        # --- CRASH DETECTION ---
        
        # Condition: Flux exceeds Thermal Limit
        crash_mask = Flux > F_CRIT
        
        if np.any(crash_mask):
            crash_idx = np.argmax(crash_mask)
        else:
            crash_idx = STEPS - 1
            
        # Slicing valid data (pre-crash)
        valid_tau = tau[:crash_idx]
        valid_Cin = C_in[:crash_idx]
        
        # Apply Lloyd Limit (Computational Bound)
        throughput = np.minimum(valid_Cin, C_LIMIT)
        
        # --- THE ALI INTEGRAL ---
        if len(valid_tau) > 1:
            I_Ali = simpson(throughput, x=valid_tau)
        else:
            I_Ali = 0
            
        results[name] = {
            "I_Ali": I_Ali,
            "tau": valid_tau,
            "Cin": valid_Cin,
            "limit": C_LIMIT,
            "crash_val": valid_tau[-1] if len(valid_tau) > 0 else 0
        }
        
    return results