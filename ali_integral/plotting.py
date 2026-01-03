import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "output"

def generate_plots(results):
    """Generates graphs and equation renders."""
    print("[INFO] Generating Plots and Equations...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Shannon Capacity Plot (Sgr A*)
    data = results["Sgr A*"]
    plt.style.use('grayscale')
    fig, ax = plt.subplots(figsize=(8, 4.5))
    
    ax.plot(data["tau"], data["Cin"], 'k-', lw=1.5, label=r'Input Capacity $C_{in}(\tau)$')
    ax.axhline(data["limit"], color='red', linestyle='--', lw=1.5, label=r'Lloyd Limit ($C_{limit}$)')
    
    # OFI Area
    ax.fill_between(data["tau"], data["limit"], 0, where=(data["Cin"] > data["limit"]), 
                    color='gray', alpha=0.3, label='Processed Information (OFI)')
    ax.fill_between(data["tau"], data["Cin"], 0, where=(data["Cin"] <= data["limit"]), 
                    color='gray', alpha=0.3)
    
    ax.set_yscale('log')
    ax.set_title(r'Fig 1: Information Inflow vs Physical Limits (Sgr A*)')
    ax.set_xlabel('Proper Time (Arbitrary Units)')
    ax.set_ylabel('Bitrate (bits/s)')
    ax.legend(loc='upper left')
    
    # Crash Label
    if len(data["tau"]) > 0:
        ax.text(data["tau"][-1], data["limit"]*0.05, ' THERMAL CRASH \n $F_E > F_{crit}$ ', 
                color='red', ha='right', fontsize=9, bbox=dict(facecolor='white', edgecolor='red'))
            
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/fig1_capacity.png", dpi=300)
    plt.close()

    # 2. Comparison Bar Chart
    names = list(results.keys())
    ofis = [results[n]["I_Ali"] for n in names]
    norm_ofis = [x/ofis[0] if ofis[0] != 0 else 0 for x in ofis]
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(names, norm_ofis, color='#444444', edgecolor='black')
    
    ax.set_yscale('log')
    ax.set_ylabel(r'Relative Total OFI ($I_{Ali}$)')
    ax.set_title('Fig 2: Scaling of Observable Information by BH Mass')
    
    for bar, val in zip(bars, norm_ofis):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height*1.1, f'x{val:.1e}', ha='center', fontsize=10)
        
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/fig2_scaling.png", dpi=300)
    plt.close()
    
    # 3. Render Equations (LaTeX style)
    _render_eq(r"$SNR(\tau) = SNR_0 \cdot g(\tau)$", "eq_snr.png")
    _render_eq(r"$C_{Lloyd} = \frac{2E}{\pi \hbar}$", "eq_lloyd.png")
    _render_eq(r"$F_E \propto E_{\gamma} \cdot Rate \propto g(\tau)^2$", "eq_flux.png")

def _render_eq(latex, filename):
    plt.figure(figsize=(6, 1.5))
    plt.text(0.5, 0.5, latex, ha='center', fontsize=18)
    plt.axis('off')
    plt.savefig(f"{OUTPUT_DIR}/{filename}", dpi=300, bbox_inches='tight')
    plt.close()