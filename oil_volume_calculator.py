import tkinter as tk
from tkinter import messagebox


class HCPV:
    def __init__(self, density_derived_porosity, formation_matrix_density, formation_fluid_density, a, water_resistivity, formation_resistivity, n, thickness, area, m):
        # Initialize the class attributes
        self.density_derived_porosity = density_derived_porosity
        self.formation_matrix_density = formation_matrix_density
        self.formation_fluid_density = formation_fluid_density
        self.a = a
        self.water_resistivity = water_resistivity
        self.formation_resistivity = formation_resistivity
        self.n = n
        self.area = area
        self.thickness = thickness
        self.m = m

    def poro(self):
        # Calculate porosity using the given formula
        porosity = (self.formation_matrix_density - self.density_derived_porosity) / (self.formation_matrix_density - self.formation_fluid_density)
        return porosity

    def formation_volume_factor(self, molecular_weight):
        # Calculate the formation volume factor
        formation_factor = 0.02827 * molecular_weight / (10.73 * self.formation_fluid_density)
        return formation_factor

    def Water_Sat(self):
        # Calculate porosity
        porosity_1 = self.poro()
        # Calculate actual porosity raised to the power of m
        actual_porosity = porosity_1 ** self.m
        # Calculate the first part of the water saturation formula
        part_1 = (self.a * self.water_resistivity) / (actual_porosity * self.formation_resistivity)
        # Calculate water saturation using the given formula
        water_saturation = part_1 ** (1 / self.n)
        return water_saturation

    def vol(self, molecular_weight):
        # Calculate porosity
        porosity_1 = self.poro()
        # Calculate water saturation
        water_saturation = self.Water_Sat()
        # Calculate formation volume factor
        formation_factor = self.formation_volume_factor(molecular_weight)
        # Calculate the hydrocarbon pore volume using the given formula
        volume = self.area * self.thickness * porosity_1 * (1 - water_saturation) / formation_factor
        return volume


# Function to handle the calculation
def calculate():
    try:
        # Read input values from the GUI
        density_derived_porosity = float(entry_density_derived_porosity.get())
        formation_matrix_density = float(entry_formation_matrix_density.get())
        formation_fluid_density = float(entry_formation_fluid_density.get())
        a = float(entry_a.get())
        n = float(entry_n.get())
        m = float(entry_m.get())
        area = float(entry_area.get())
        thickness = float(entry_thickness.get())
        water_resistivity = float(entry_water_resistivity.get())
        formation_resistivity = float(entry_formation_resistivity.get())
        molecular_weight = float(entry_molecular_weight.get())

        # Create an instance of HCPV
        hcpv = HCPV(
            density_derived_porosity=density_derived_porosity,
            formation_matrix_density=formation_matrix_density,
            formation_fluid_density=formation_fluid_density,
            a=a,
            n=n,
            m=m,
            area=area,
            thickness=thickness,
            water_resistivity=water_resistivity,
            formation_resistivity=formation_resistivity
        )

        # Calculate results
        porosity = hcpv.poro()
        saturation_of_water = hcpv.Water_Sat()
        hydrocarbon_pore_volume = hcpv.vol(molecular_weight)

        # Display results
        messagebox.showinfo("Results", f"Calculated Porosity: {porosity:.4f}\n"
                                       f"Water Saturation: {saturation_of_water:.4f}\n"
                                       f"Hydrocarbon Pore Volume: {hydrocarbon_pore_volume:.4f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")


# Create the main window
root = tk.Tk()
root.title("Hydrocarbon Pore Volume Calculator")

# Create and place labels and entry fields for inputs
labels = ["Density Derived Porosity:", "Formation Matrix Density:", "Formation Fluid Density:",
          "Archie's Parameter a:", "Archie's Parameter n:", "Archie's Parameter m:",
          "Area of Reservoir (sq. units):", "Thickness of Reservoir (units):",
          "Water Resistivity:", "Formation Resistivity:", "Molecular Weight of Fluid:"]

entries = []

for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=5, sticky='e')

    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

(entry_density_derived_porosity, entry_formation_matrix_density, entry_formation_fluid_density,
 entry_a, entry_n, entry_m, entry_area, entry_thickness,
 entry_water_resistivity, entry_formation_resistivity, entry_molecular_weight) = entries

# Add the Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
