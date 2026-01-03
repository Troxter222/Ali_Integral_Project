import numpy as np
from scipy.integrate import simpson
try:
    from ali_integral.config import B0, SNR0, C_LIMIT, F_CRIT, STEPS
except ImportError:
    B0 = 1.0e9
    SNR0 = 10.0
    C_LIMIT = 1e17
    F_CRIT = 1e12
    STEPS = 1000

BLACK_HOLES = {
    "SgrA*": 4.1e6,
    "M87*": 6.5e9,
    "TON618": 6.6e10,
    "CygnusX-1": 14.8,
    "Sun": 1.0
}

def get_mass(mass_input):
    if isinstance(mass_input, str):
        if mass_input in BLACK_HOLES:
            return BLACK_HOLES[mass_input]
        else:
            raise ValueError(f"Unknown Black Hole. Available: {list(BLACK_HOLES.keys())}")
    return float(mass_input)

def calculate_ali_integral(mass):
    M = float(mass)
    
    # r normalized: 1.0 (Horizon) -> 0 (Singularity)
    r = np.linspace(1.0, 1e-5, STEPS)
    # Proper time tau scales with Mass M
    tau = np.linspace(0, M, STEPS)
    
    g_factor = 1.0 / r
    B_tau = B0 * g_factor
    Flux = 1.0 * (g_factor**2)
    SNR_tau = SNR0 * g_factor
    
    C_in = B_tau * np.log2(1 + SNR_tau)
    
    crash_mask = Flux > F_CRIT
    
    if np.any(crash_mask):
        crash_idx = np.argmax(crash_mask)
    else:
        crash_idx = STEPS - 1
        
    valid_tau = tau[:crash_idx]
    valid_Cin = C_in[:crash_idx]
    
    if len(valid_tau) < 2:
        return 0.0
    
    throughput = np.minimum(valid_Cin, C_LIMIT)
    
    I_Ali = simpson(throughput, x=valid_tau)
    
    return I_Ali