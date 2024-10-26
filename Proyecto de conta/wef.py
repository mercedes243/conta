import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

class BreakEvenApp:
    def __init__(self, root):
        """Inicializa la interfaz de la aplicación y define variables."""
        self.root = root
        self.root.title("Cálculo del Punto de Equilibrio")
        self.root.geometry("800x400")
        self.root.configure(bg="#9cadce")

        # Fuentes y colores personalizados
        self.font = ("Helvetica", 12)
        self.bg_color = "#9cadce"
        self.fg_color = "#000000"
        self.button_color = "#7ec4cf"
        self.entry_bg = "#daeaf6"

        # Configuración de estilos
        style = ttk.Style()
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=self.font)
        style.configure("TButton", background=self.button_color, foreground=self.fg_color, font=self.font)
        style.configure("TEntry", fieldbackground=self.entry_bg, font=self.font)
        style.configure("Treeview", background=self.entry_bg, font=self.font, rowheight=30)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#79addc", fg="#000000")

        # Configuración de entradas y botones
        self.create_label("Precio por Unidad (Q):", 0, 0)
        self.price_per_unit_qtz = tk.DoubleVar()
        self.create_entry(self.price_per_unit_qtz, 0, 1)

        self.create_label("Costos Fijos (Q):", 1, 0)
        self.fixed_costs_qtz = tk.DoubleVar()
        self.create_entry(self.fixed_costs_qtz, 1, 1)

        self.create_label("Costo Variable por Unidad (Q):", 2, 0)
        self.variable_cost_per_unit_qtz = tk.DoubleVar()
        self.create_entry(self.variable_cost_per_unit_qtz, 2, 1)

        # Botones para ejecutar funciones principales
        self.create_button("Calcular", self.calculate_breakeven, 3, 0)
        self.create_button("Gráfica", self.plot_graph, 3, 1)
        self.create_button("Borrar Datos", self.clear_fields, 3, 2)

        # Crear marco para la tabla
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.grid(column=0, row=4, columnspan=3, pady=10)

    def create_label(self, text, row, col):
        """Crea una etiqueta en la interfaz."""
        label = ttk.Label(self.root, text=text, background=self.bg_color)
        label.grid(column=col, row=row, padx=10, pady=5)

    def create_entry(self, var, row, col):
        """Crea un campo de entrada en la interfaz."""
        entry = ttk.Entry(self.root, textvariable=var)
        entry.grid(column=col, row=row, padx=10, pady=5)

    def create_button(self, text, command, row, col):
        """Crea un botón en la interfaz."""
        button = ttk.Button(self.root, text=text, command=command)
        button.grid(column=col, row=row, padx=10, pady=10)

    def validate_inputs(self):
        """Valida que los campos contengan los datos mayores que cero."""
        try:
            if self.price_per_unit_qtz.get() <= 0 or self.fixed_costs_qtz.get() <= 0 or self.variable_cost_per_unit_qtz.get() < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese los datos mayores que cero.")
            return False
        return True

    def calculate_breakeven(self):
        """Calcula el punto de equilibrio y actualiza la tabla."""
        if not self.validate_inputs():
            return
        
        # Valores de entrada del usuario
        fixed_costs = self.fixed_costs_qtz.get()
        price = self.price_per_unit_qtz.get()
        variable_cost = self.variable_cost_per_unit_qtz.get()

        # Cálculo del margen de contribución por unidad y punto de equilibrio
        margin_per_unit = price - variable_cost
        self.breakeven_units = fixed_costs / margin_per_unit if margin_per_unit != 0 else 0
        self.breakeven_revenue = self.breakeven_units * price

        # Mostrar la tabla de resultados
        self.plot_table(fixed_costs, price, variable_cost, margin_per_unit)

        # Mostrar cuadro informativo
        self.show_info_box(margin_per_unit)

    def show_info_box(self, margin_per_unit):
        """Muestra un cuadro con el margen de contribución y el punto de equilibrio."""
        info_message = (f"Margen de Contribución por Unidad: Q{margin_per_unit:.2f}\n"
                        f"Punto de Equilibrio (Unidades): {self.breakeven_units:.2f}\n"
                        f"Punto de Equilibrio (Ventas): Q{self.breakeven_revenue:.2f}")
        messagebox.showinfo("Resultados", info_message)
    
    #____________pa
    def plot_table(self, fixed_costs, price, variable_cost, margin_per_unit):
        """Genera y muestra la tabla en torno al punto de equilibrio."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Crear tabla
        tree = ttk.Treeview(self.table_frame, columns=('Unidades', 'Ventas', 'Costos Variables', 'Margen de Contribución', 'Costos Fijos', 'Utilidad o Pérdida'), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        
        # Generar filas de datos
        start_units = max(0, self.breakeven_units - 2)
        end_units = self.breakeven_units + 2
        for units in np.arange(start_units, end_units + 1):
            ventas = units * price
            costos_variables = units * variable_cost
            margen_contribucion = units * margin_per_unit
            utilidad_perdida = margen_contribucion - fixed_costs
            tree.insert('', 'end', values=(f"{units:.2f}", f"{ventas:.2f}", f"{costos_variables:.2f}", f"{margen_contribucion:.2f}", f"{fixed_costs:.2f}", f"{utilidad_perdida:.2f}"))

        # Aplicar colores a las filas
        for i in range(len(tree.get_children())):
            color = '#daeaf6' if i % 2 == 0 else '#79addc'
            tree.tag_configure(f'row{i}', background=color)
            tree.item(tree.get_children()[i], tags=(f'row{i}',))

        # Configuración de la barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)

    def plot_graph(self):
        """Genera un gráfico visual del punto de equilibrio."""
        if not self.validate_inputs():  # Check if inputs are valid
            return

        if not hasattr(self, 'breakeven_units'):
            messagebox.showinfo("Error", "Primero calcula el punto de equilibrio.")
            return

        # Calcular datos de gráficos
        units = np.arange(max(0, self.breakeven_units - 5), self.breakeven_units + 6)
        ventas = units * self.price_per_unit_qtz.get()
        costos_variables = units * self.variable_cost_per_unit_qtz.get()
        costos_totales = costos_variables + self.fixed_costs_qtz.get()

        # Crear y mostrar gráfico
        plt.figure(figsize=(8, 6), facecolor='white')
        plt.plot(units, ventas, label='Ingresos Totales', color='green', marker='o')
        plt.plot(units, costos_totales, label='Costos Totales', color='red', marker='o')
        plt.plot(units, costos_variables, label='Costos Variables', color='orange', marker='o')
        plt.axhline(self.fixed_costs_qtz.get(), color='blue', linestyle='--', label='Costos Fijos')
        plt.axvline(self.breakeven_units, color='gray', linestyle='--', label=f'Punto de Equilibrio: {self.breakeven_units:.2f} unidades')
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.title("Gráfico del Punto de Equilibrio")
        plt.xlabel("Unidades")
        plt.ylabel("Quetzales (Q)")
        plt.legend()
        plt.grid(True)
        plt.show()

    def clear_fields(self):
        """Limpia todos los campos de entrada y la tabla."""
        self.price_per_unit_qtz.set(0)
        self.fixed_costs_qtz.set(0)
        self.variable_cost_per_unit_qtz.set(0)

        for widget in self.table_frame.winfo_children():
            widget.destroy()

# Inicializar la aplicación
root = tk.Tk()
app = BreakEvenApp(root)
root.mainloop()