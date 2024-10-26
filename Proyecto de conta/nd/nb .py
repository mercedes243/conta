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

        # Fuentes
        self.font = ("Helvetica", 12)
        
        # Colores
        self.bg_color = "#E5CEDC"
        self.fg_color = "#8F9491"
        self.button_color = "#BCA3AC"
        self.entry_bg = "#F3EAF4"

        # Estilo personalizado
        style = ttk.Style()
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=self.font)
        style.configure("TButton", background=self.button_color, foreground=self.fg_color, font=self.font)
        style.configure("TEntry", fieldbackground=self.entry_bg, font=self.font)
        style.configure("Treeview", background=self.entry_bg, font=self.font)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

        # Entradas de usuario
        self.create_label("Precio por Unidad (Quetzales):", 0, 0)
        self.price_per_unit = tk.DoubleVar()
        self.create_entry(self.price_per_unit, 0, 1)

        self.create_label("Costos Fijos (Quetzales):", 1, 0)
        self.fixed_costs = tk.DoubleVar()
        self.create_entry(self.fixed_costs, 1, 1)

        self.create_label("Costo Variable por Unidad (Quetzales):", 2, 0)
        self.variable_cost_per_unit = tk.DoubleVar()
        self.create_entry(self.variable_cost_per_unit, 2, 1)

        # Botones
        self.create_button("Calcular", self.calculate_breakeven, 3, 0)
        self.create_button("Gráfica", self.plot_graph, 3, 1)
        self.create_button("Borrar Datos", self.clear_fields, 3, 2)

        # Crear espacio para la tabla
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.grid(column=0, row=4, columnspan=3, pady=10)

    def create_label(self, text, row, col):
        label = ttk.Label(self.root, text=text, background=self.bg_color)
        label.grid(column=col, row=row, padx=10, pady=5)

    def create_entry(self, var, row, col):
        entry = ttk.Entry(self.root, textvariable=var)
        entry.grid(column=col, row=row, padx=10, pady=5)

    def create_button(self, text, command, row, col):
        button = ttk.Button(self.root, text=text, command=command)
        button.grid(column=col, row=row, padx=10, pady=10)

    def validate_inputs(self):
        """Valida que los campos no estén vacíos ni sean valores no válidos."""
        try:
            if self.price_per_unit.get() <= 0 or self.fixed_costs.get() <= 0 or self.variable_cost_per_unit.get() < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores válidos y mayores que cero.")
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
        if self.margin_per_unit != 0:
            self.breakeven_units = self.fixed_costs_value / self.margin_per_unit
        else:
            self.breakeven_units = 0

        # Punto de Equilibrio en Ventas
        self.breakeven_revenue = self.breakeven_units * self.price_value

        self.plot_table()

    def plot_table(self):
        """Genera una tabla con los datos ajustados en torno al punto de equilibrio"""
        for widget in self.table_frame.winfo_children():
            widget.destroy()  # Limpiar tabla previa si existe

        tree = ttk.Treeview(self.table_frame, columns=( 'Unidades', 'Ventas', 'Costos Variables', 'Margen de Contribución', 'Costos Fijos', 'Utilidad o Pérdida'), show='headings')
        tree.heading('Unidades', text='Unidades')
        tree.heading('Ventas', text='Ventas (Q)')
        tree.heading('Costos Variables', text='Costos Variables (Q)')
        tree.heading('Margen de Contribución', text='Margen de Contribución (Q)')
        tree.heading('Costos Fijos', text='Costos Fijos (Q)')
        tree.heading('Utilidad o Pérdida', text='Utilidad o Pérdida (Q)')
        
        # Ajustes de columnas
        columns_widths = [100, 80, 120, 150, 150, 100, 150]
        for col, width in zip(tree["columns"], columns_widths):
            tree.column(col, width=width)

        # Agregar filas ajustadas alrededor del punto de equilibrio
        start_units = max(0, self.breakeven_units - 2)  # No permitir unidades negativas
        end_units = self.breakeven_units + 2

        for i, units in enumerate(np.arange(start_units, end_units + 1)):
            ventas = units * self.price_value
            costos_variables = units * self.variable_cost_value
            margen_contribucion = units * self.margin_per_unit
            utilidad_perdida = margen_contribucion - self.fixed_costs_value

            tree.insert('', 'end', values=(f"Fila {i+1}", f"{units:.2f}", f"{ventas:.2f}", f"{costos_variables:.2f}", f"{margen_contribucion:.2f}", f"{self.fixed_costs_value:.2f}", f"{utilidad_perdida:.2f}"))

        # Agregar Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)

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

        plt.figure(figsize=(8, 6), facecolor='white')
        plt.plot(units, ventas, label='Ventas', color='green', marker='o')
        plt.plot(units, costos_variables, label='Costos Variables', color='red', marker='o')
        plt.plot(units, utilidad_perdida, label='Utilidad/Pérdida', color='blue', marker='o')
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(self.breakeven_units, color='gray', linestyle='--', label=f'Punto de Equilibrio: {self.breakeven_units:.2f} unidades')

        plt.title("Gráfico del Punto de Equilibrio")
        plt.xlabel("Unidades")
        plt.ylabel("Quetzales")
        plt.legend()
        plt.grid(True)
        plt.show()

    def clear_fields(self):
        """Borrar todos los campos de entrada y eliminar tabla"""
        self.price_per_unit.set(0)
        self.fixed_costs.set(0)
        self.variable_cost_per_unit.set(0)

        for widget in self.table_frame.winfo_children():
            widget.destroy()  # Eliminar la tabla

if __name__ == "__main__":
    root = tk.Tk()
    app = BreakEvenApp(root)
    root.mainloop()
