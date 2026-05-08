import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calculate_diffraction_intensity(wavelength_nm, slit_width_um, num_points=1000):
    wavelength_m = wavelength_nm * 1e-9
    slit_width_m = slit_width_um * 1e-6
    theta = np.linspace(-0.1, 0.1, num_points)
    
    # Intensity formula: I(theta) = I_0 * (sin(beta)/beta)^2
    epsilon = 1e-15
    beta = (np.pi * slit_width_m * np.sin(theta)) / wavelength_m
    beta = np.where(beta == 0, epsilon, beta)
    intensity = (np.sin(beta) / beta)**2
    
    return theta, intensity

def calculate_central_width(wavelength_m, slit_width_m, distance_m):
    """
    Formula: W = (2 * lambda * d) / D
    """
    width_m = (2 * wavelength_m * distance_m) / slit_width_m
    return width_m

def show_dashboard_data(wavelength_nm, slit_width_um, current_distance_m):
    """
    Calculates and prints the tables, then plots the graphs matching the web dashboard.
    """
    wavelength_m = wavelength_nm * 1e-9
    slit_width_m = slit_width_um * 1e-6
    central_width_m = calculate_central_width(wavelength_m, slit_width_m, current_distance_m)
    
    computed_data = {
        "Quantity": ["Central Width (m)", "Distance (m)", "Wavelength (m)", 
                     "Slit Width (m)", "Slit Width (mm)", "Slit Width (\u03bcm)"],
        "Computed Value": [f"{central_width_m:.6e}", f"{current_distance_m:.6e}", f"{wavelength_m:.6e}", 
                           f"{slit_width_m:.6e}", f"{slit_width_m * 1e3:.6e}", f"{slit_width_m * 1e6:.6e}"]
    }
    df_computed = pd.DataFrame(computed_data)
    
    print("\n" + "=" * 50)
    print(" 🔢 COMPUTED VALUE")
    print("=" * 50)
    print(df_computed.to_string(index=False))
    distances_array_m = np.arange(0.3, 3.1, 0.3) 
    widths_array_m = calculate_central_width(wavelength_m, slit_width_m, distances_array_m)
    widths_array_mm = widths_array_m * 1000
    
    dispersion_data = {
        "Distance (m)": [round(d, 1) for d in distances_array_m],
        "Central Fringe Width (mm)": [round(w, 1) for w in widths_array_mm]
    }
    df_dispersion = pd.DataFrame(dispersion_data)
    
    print("\n" + "=" * 50)
    print(" 📊 DISTANCE VS CENTRAL WIDTH DATA")
    print("=" * 50)
    print(df_dispersion.to_string(index=False))
        
    print("\n" + "=" * 50 + "\n")
    print("Opening Plot Viewer...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.canvas.manager.set_window_title('Slit Width Calculator - Visualizer')
    
    # --- Subplot 1: Diffraction Intensity Curve ---
    theta, intensity = calculate_diffraction_intensity(wavelength_nm, slit_width_um)
    theta_deg = np.degrees(theta)
    
    # Match color to wavelength approximately
    if wavelength_nm < 450: color = '#8A2BE2'
    elif wavelength_nm < 550: color = '#00FF00' 
    elif wavelength_nm < 600: color = '#FFFF00'
    else: color = '#FF0000'
    
    ax1.plot(theta_deg, intensity, color=color, linewidth=2)
    ax1.fill_between(theta_deg, intensity, alpha=0.3, color=color)
    ax1.set_title(f'Real-Time 1D Intensity\n($\lambda$ = {wavelength_nm} nm, a = {slit_width_um} $\mu$m)', fontsize=12)
    ax1.set_xlabel('Screen Angle $\\theta$ (Degrees)')
    ax1.set_ylabel('Normalized Intensity $I/I_0$')
    ax1.grid(True, alpha=0.2)
    ax2.plot(distances_array_m, widths_array_mm, marker='o', markersize=10, color='#4A90E2', linewidth=2)
    ax2.set_title('Predicted Dispersion\nCentral Fringe Width vs Distance', fontsize=12)
    ax2.set_xlabel('Distance (m)', fontsize=11)
    ax2.set_ylabel('Central Fringe Width (mm)', fontsize=11)
    ax2.grid(True, alpha=0.2)
    ax2.set_xticks(np.arange(0.3, 3.1, 0.3))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    WAVELENGTH_NM = float(input("Enter Wavelength (nm): "))        # 5.32e-07 m
    SLIT_WIDTH_UM = float(input("Enter Slit Width (μm): "))        # 1.3832e-04 m
    CURRENT_DISTANCE_M = float(input("Enter Distance (m): "))     # 3.9e-01 m 
    
    show_dashboard_data(WAVELENGTH_NM, SLIT_WIDTH_UM, CURRENT_DISTANCE_M)
