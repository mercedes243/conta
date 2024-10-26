import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

class BreakEvenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo del Punto de Equilibrio")
        self.root.geometry("850x650")
        self.root.configure(bg="#EADDE1")

        # Estilo para los widgets
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TLabel", background="#EADDE1", font=("Arial", 10))

        # Entradas de usuario
        self.create_input_fields()

        # Botones
        self.create_buttons()

        # Crear espacio para la tabla
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.grid(column=0, row=4, columnspan=3, pady=10)

    def create_input_fields(self):
        """Crea los campos de entrada para el usuario."""
        ttk.Label(self.root, text="Precio por Unidad (Quetzales):").grid(column=0, row=0, padx=10, pady=5)
        self.price_per_unit = tk.DoubleVar()
        ttk.Entry(self.root, textvariable=self.price_per_unit, width=20).grid(column=1, row=0)

        ttk.Label(self.root, text="Costos Fijos (Quetzales):").grid(column=0, row=1, padx=10, pady=5)
        self.fixed_costs = tk.DoubleVar()
        ttk.Entry(self.root, textvariable=self.fixed_costs, width=20).grid(column=1, row=1)

        ttk.Label(self.root, text="Costo Variable por Unidad (Quetzales):").grid(column=0, row=2, padx=10, pady=5)
        self.variable_cost_per_unit = tk.DoubleVar()
        ttk.Entry(self.root, textvariable=self.variable_cost_per_unit, width=20).grid(column=1, row=2)

        # Campos para la tabla
        ttk.Label(self.root, text="MagMargen:").grid(column=0, row=3, padx=10, pady=5, sticky=tk.E)
        self.entry_concepto = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.entry_concepto, width=20).grid(column=1, row=3)

    def create_buttons(self):
        """Crea los botones de la aplicación."""
        ttk.Button(self.root, text="Calcular", command=self.calculate_breakeven).grid(column=0, row=5, pady=10)
        ttk.Button(self.root, text="Gráfica", command=self.plot_graph).grid(column=1, row=5, pady=10)
        ttk.Button(self.root, text="Borrar Datos", command=self.clear_fields).grid(column=2, row=5, pady=10)

    def validate_inputs(self):
        """Valida que los campos no estén vacíos ni sean valores no válidos."""
        if self.price_per_unit.get() <= 0 or self.fixed_costs.get() < 0 or self.variable_cost_per_unit.get() < 0:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos y mayores que cero.")
            return False
        return True

    def calculate_breakeven(self):
        """Realiza el cálculo del Punto de Equilibrio"""
        if not self.validate_inputs():
            return
        
        self.fixed_costs_value = self.fixed_costs.get()
        self.price_value = self.price_per_unit.get()
        self.variable_cost_value = self.variable_cost_per_unit.get()

        # Margen de Contribución por Unidad
        self.margin_per_unit = self.price_value - self.variable_cost_value

        # Punto de Equilibrio en Unidades
        self.breakeven_units = self.fixed_costs_value / self.margin_per_unit if self.margin_per_unit > 0 else float('inf')

        # Punto de Equilibrio en Ventas
        self.breakeven_revenue = self.breakeven_units * self.price_value

        self.plot_table()

    def plot_table(self):
        """Genera una tabla con los datos ajustados en torno al punto de equilibrio"""
        for widget in self.table_frame.winfo_children():
            widget.destroy()  # Limpiar tabla previa si existe

        tree = ttk.Treeview(self.table_frame, columns=('Concepto', 'Ventas', 'Costos Variables', 'Margen de Contribución', 'Costos Fijos', 'Utilidad o Pérdida'), show='headings')
        tree.heading('Concepto', text='Concepto')
        tree.heading('Ventas', text='Ventas (Q)')
        tree.heading('Costos Variables', text='Costos Variables (Q)')
        tree.heading('Margen de Contribución', text='Margen de Contribución (Q)')
        tree.heading('Costos Fijos', text='Costos Fijos (Q)')
        tree.heading('Utilidad o Pérdida', text='Utilidad o Pérdida (Q)')
        
        tree.column('Concepto', width=100)
        tree.column('Ventas', width=120)
        tree.column('Costos Variables', width=150)
        tree.column('Margen de Contribución', width=150)
        tree.column('Costos Fijos', width=100)
        tree.column('Utilidad o Pérdida', width=150)

        # Agregar filas ajustadas alrededor del punto de equilibrio
        start_units = max(0, self.breakeven_units - 2)
        end_units = self.breakeven_units + 2

        for i, units in enumerate(np.arange(start_units, end_units + 1)):
            concpeto = units - self.price_value
            ventas = units * self.price_value
            costos_variables = units * self.variable_cost_value
            margen_contribucion = units * self.margin_per_unit
            utilidad_perdida = margen_contribucion - self.fixed_costs_value

            # Insertar fila en la tabla
            tree.insert('', 'end', values=(self.entry_concepto.get(),f"{concpeto:.2f}," f"{ventas:.2f}", f"{costos_variables:.2f}", f"{margen_contribucion:.2f}", f"{self.fixed_costs_value:.2f}", f"{utilidad_perdida:.2f}"))

        tree.pack()

    def plot_graph(self):
        """Genera una gráfica visual del punto de equilibrio"""
        if not hasattr(self, 'breakeven_units'):
            messagebox.showinfo("Error", "Primero calcula el punto de equilibrio.")
            return

        units = np.arange(self.breakeven_units - 5, self.breakeven_units + 6)
        ventas = units * self.price_value
        costos_variables = units * self.variable_cost_value
        margen_contribucion = ventas - costos_variables
        utilidad_perdida = margen_contribucion - self.fixed_costs_value

        plt.figure(figsize=(10, 6))
       
        plt.plot(units, ventas, label='Ventas', color='green', marker='o')
        plt.plot(units, costos_variables, label='Costos Variables', color='red', marker='o')
        plt.plot(units, utilidad_perdida, label='Utilidad/Pérdida', color='blue', marker='o')
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(self.breakeven_units, color='gray', linestyle='--', label=f'Punto de Equilibrio: {self.breakeven_units:.2f} unidades')

        plt.title("Gráfico del Punto de Equilibrio", fontsize=14)
        plt.xlabel("Unidades", fontsize=12)
        plt.ylabel("Quetzales", fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def clear_fields(self):
        """Borrar todos los campos de entrada y eliminar tabla"""
        self.price_per_unit.set(0)
        self.fixed_costs.set(0)
        self.variable_cost_per_unit.set(0)
        self.entry_concepto.set("")  # Limpiar el campo de concepto

        for widget in self.table_frame.winfo_children():
            widget.destroy()  # Eliminar la tabla

if __name__ == "__main__":
    root = tk.Tk()
    app = BreakEvenApp(root)
    root.mainloop()
