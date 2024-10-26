import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

class BreakEvenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo del Punto de Equilibrio")
        self.root.geometry("800x600")

        # Entradas de usuario
        self.create_input_fields()

        # Crear botones
        self.create_buttons()

        # Crear tabla resumen
        self.create_summary_table()

    def create_input_fields(self):
        ttk.Label(self.root, text="Costos Fijos (Q):").grid(column=0, row=0, padx=10, pady=5)
        self.fixed_costs = tk.DoubleVar()
        ttk.Entry(self.root, textvariable=self.fixed_costs).grid(column=1, row=0)

        ttk.Label(self.root, text="Precio por Unidad (Q):").grid(column=0, row=1, padx=10, pady=5)
        self.sale_price = tk.DoubleVar()
        ttk.Entry(self.root, textvariable=self.sale_price).grid(column=1, row=1)

        ttk.Label(self.root, text="Costo Variable por Unidad (Q):").grid(column=0, row=2, padx=10, pady=5)
        self.variable_cost = tk.DoubleVar()
        ttk.Entry(self.root, textvariable=self.variable_cost).grid(column=1, row=2)

    def create_buttons(self):
        ttk.Button(self.root, text="Calcular", command=self.calculate_breakeven).grid(column=0, row=3, pady=10)
        ttk.Button(self.root, text="Gráfica", command=self.plot_breakeven).grid(column=1, row=3, pady=10)
        ttk.Button(self.root, text="Borrar Datos", command=self.clear_data).grid(column=2, row=3, pady=10)

    def create_summary_table(self):
        # Crear tabla tipo Excel (6x6)
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.grid(column=0, row=4, columnspan=3, pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=('Concepto', 'Valor'), show='headings', height=6)
        self.tree.heading('Concepto', text='Concepto')
        self.tree.heading('Valor', text='Valor')

        # Ajustar el tamaño de las columnas
        self.tree.column('Concepto', width=150)
        self.tree.column('Valor', width=150)

        # Insertar conceptos
        self.tree.insert('', 'end', values=("Ventas", "0"))
        self.tree.insert('', 'end', values=("Costos Variables", "0"))
        self.tree.insert('', 'end', values=("Margen de Contribución", "0"))
        self.tree.insert('', 'end', values=("Costos Fijos", "0"))
        self.tree.insert('', 'end', values=("Punto de Equilibrio", "0"))
        self.tree.insert('', 'end', values=("Utilidad o Pérdida", "0"))

        self.tree.pack()

    def calculate_breakeven(self):
        fixed_costs = self.fixed_costs.get()
        sale_price = self.sale_price.get()
        variable_cost = self.variable_cost.get()

        if sale_price <= variable_cost:
            self.update_summary_table(0, 0, 0, 0, 0, 0)
            return

        # Cálculo del margen de contribución
        margin_per_unit = sale_price - variable_cost

        # Cálculo del punto de equilibrio en unidades
        breakeven_units = fixed_costs / margin_per_unit

        # Ingresos totales en el punto de equilibrio
        total_revenue = breakeven_units * sale_price

        # Costos variables totales en el punto de equilibrio
        total_variable_costs = breakeven_units * variable_cost

        # Ganancias o pérdidas
        utility_loss = total_revenue - fixed_costs

        # Actualización de la tabla con los resultados
        self.update_summary_table(total_revenue, total_variable_costs, margin_per_unit, fixed_costs, breakeven_units, utility_loss)

    def update_summary_table(self, ventas, costos_variables, margen_contribucion, costos_fijos, punto_equilibrio, utilidad_perdida):
        # Actualizar los valores en la tabla
        self.tree.set(self.tree.get_children()[0], column='Valor', value=f"{ventas:.2f}")
        self.tree.set(self.tree.get_children()[1], column='Valor', value=f"{costos_variables:.2f}")
        self.tree.set(self.tree.get_children()[2], column='Valor', value=f"{margen_contribucion:.2f}")
        self.tree.set(self.tree.get_children()[3], column='Valor', value=f"{costos_fijos:.2f}")
        self.tree.set(self.tree.get_children()[4], column='Valor', value=f"{punto_equilibrio:.2f}")
        self.tree.set(self.tree.get_children()[5], column='Valor', value=f"{utilidad_perdida:.2f}")

    def plot_breakeven(self):
        fixed_costs = self.fixed_costs.get()
        sale_price = self.sale_price.get()
        variable_cost = self.variable_cost.get()

        if sale_price <= variable_cost:
            return

        # Cálculo del margen de contribución
        margin_per_unit = sale_price - variable_cost

        # Cálculo del punto de equilibrio en unidades
        breakeven_units = fixed_costs / margin_per_unit

        # Definir el rango de unidades (dos a la izquierda y dos a la derecha del punto de equilibrio)
        units = np.arange(breakeven_units - 2, breakeven_units + 3)

        # Ingresos totales en el rango de unidades
        revenue = units * sale_price

        # Costos variables totales en el rango de unidades
        variable_costs = units * variable_cost

        # Costos fijos
        fixed_costs_line = np.full_like(units, fixed_costs)

        # Ganancias o pérdidas en el rango de unidades
        profit_loss = revenue - (variable_costs + fixed_costs)

        # Gráfica del punto de equilibrio
        plt.figure(figsize=(10, 6))
        plt.plot(units, revenue, label='Ingresos Totales', color='green')
        plt.plot(units, variable_costs, label='Costos Variables', color='orange')
        plt.plot(units, fixed_costs_line, label='Costos Fijos', color='blue', linestyle='--')
        plt.plot(units, profit_loss, label='Utilidad o Pérdida', color='red')
        plt.axvline(x=breakeven_units, color='black', linestyle='--', label='Punto de Equilibrio')
        plt.title('Gráfica del Punto de Equilibrio')
        plt.xlabel('Unidades')
        plt.ylabel('Quetzales')
        plt.legend()
        plt.grid()
        plt.show()

    def clear_data(self):
        # Borrar entradas y restablecer tabla
        self.fixed_costs.set(0)
        self.sale_price.set(0)
        self.variable_cost.set(0)
        self.update_summary_table(0, 0, 0, 0, 0, 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = BreakEvenApp(root)
    root.mainloop()
