import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd

# ---  menu de Funciones
#  def matemáticas
def f1(x):
    return x**2 * np.cos(x) - 2*x

def f2(x):
    if x == 0: return float('inf')
    return (6 - 2/(x**2)) * (np.exp(2+x) / 4) + 1

def f3(x):
    return x**3 - 3 * np.sin(x**2) + 1

def f4(x):
    return x**3 + 6*x**2 + 9.4*x + 2.5

functions = {
    1: {'func': f1, 'str': "1. f(x) = x²cos(x) - 2x"},
    2: {'func': f2, 'str': "2. f(x) = (6 - 2/x²)(e²⁺ˣ/4) + 1"},
    3: {'func': f3, 'str': "3. f(x) = x³ - 3sen(x²) + 1"},
    4: {'func': f4, 'str': "4. f(x) = x³ + 6x² + 9.4x + 2.5"}
}

# --- el Método de la Secante
#retornara todos los resultados y mensajes
def secant_method_gui(f, x0, x1, tol, max_iter):#aqui especificamos los argumentos que necesita el proceso para la obtencion del metodo :)
    history = []
    i = 1
  
    #por si el valor inicial o final, ya son la raiz en si mismos :)  
    if abs(f(x0)) < tol:
        return x0, 0, 0, pd.DataFrame(), "El punto inicial x0 ya es una raíz."
    if abs(f(x1)) < tol:
        return x1, 0, 0, pd.DataFrame(), "El punto inicial x1 ya es una raíz."
  
        
    while i <= max_iter:
        fx0, fx1 = f(x0), f(x1)
        denominator = fx1 - fx0
        
        if abs(denominator) < 1e-15:
            msg = "Nota: División por cero (f(x1) - f(x0) es demasiado pequeño)..."
            return None, None, i, pd.DataFrame(history), msg
        
        x_next = x1 - fx1 * (x1 - x0) / denominator
        error = abs((x_next - x1) / x_next) if x_next != 0 else abs(x_next - x1)
        
        history.append({
            'Iteración': i, 'xᵢ': x_next, 'f(xᵢ)': f(x_next), 'Error Relativo': error
        })
        
        if error < tol:
            df = pd.DataFrame(history)
            msg = f"Raiz encontrada en la iteración {i}."
            return x_next, error, i, df, msg
            
        x0, x1 = x1, x_next
        i += 1
        
    df = pd.DataFrame(history)
    msg = f" No se convergió tras {max_iter} iteraciones. mostramos la mejor aproximacion."
    return x1, error, max_iter, df, msg

# ventana Tkinter en el que se despliega la interfaz

class SecantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de la Secante | Programa 1")
        self.root.geometry("700x650")

        #estilo
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 11, "bold"))
        style.configure("TRadiobutton", font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))

        # Variable para almacenar la función seleccionada para que la ejecutemos acorde a las 4 del problema...
        self.selected_function_var = tk.IntVar()

        # frames de la aplicación, estas son las ventanas que ocupamos, 2; una para seleccion y otra de calculo 
        #, la segunda tendra una apariencia acercada a la que usamos en excel para los ejercicios en clase :)
        self.selection_frame = ttk.Frame(root, padding="20")
        self.calculation_frame = ttk.Frame(root, padding="20")

        self.create_selection_widgets()
        self.create_calculation_widgets()

        # Iniciar mostrando el frame de selección
        self.selection_frame.pack(fill="both", expand=True)

    def create_selection_widgets(self):
        ttk.Label(self.selection_frame, text="Programa 01", style="Header.TLabel").pack(pady=10)
        ttk.Label(self.selection_frame, text="Método de la Secante", style="Header.TLabel").pack(pady=10)
        ttk.Label(self.selection_frame, text="Elija una función :", wraplength=400).pack(pady=10)
        
        for key, value in functions.items():
            ttk.Radiobutton(self.selection_frame, text=value['str'], variable=self.selected_function_var, value=key).pack(anchor="w", pady=5, padx=20)
        
        ttk.Button(self.selection_frame, text="Seleccionar y Continuar", command=self.show_calculation_frame).pack(pady=20)
        ttk.Label(self.selection_frame, text="Equipo", style="Header.TLabel").pack(pady=21)
        ttk.Label(self.selection_frame, text="Granados Osorio Isidoro", wraplength=400).pack(pady=2)
        ttk.Label(self.selection_frame, text="Arroyo Juarez Joseph Dylan", wraplength=400).pack(pady=2)
        ttk.Label(self.selection_frame, text="Sanchez Maldonado Kevin Antonio", wraplength=400).pack(pady=2)
        ttk.Label(self.selection_frame, text="Lopez Zamora Ingrid Yaraní", wraplength=400).pack(pady=2)


    def create_calculation_widgets(self):
        #Entradas de informacion
        input_frame = ttk.LabelFrame(self.calculation_frame, text="Parámetros de Entrada", padding="15")
        input_frame.pack(fill="x", pady=10)

        self.func_label = ttk.Label(input_frame, text="Función:", font=("Helvetica", 12, "bold"))
        self.func_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        ttk.Label(input_frame, text="Punto Inicial x₀:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.x0_entry = ttk.Entry(input_frame, width=15)
        self.x0_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Punto Inicial x₁:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.x1_entry = ttk.Entry(input_frame, width=15)
        self.x1_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Tolerancia:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.tol_entry = ttk.Entry(input_frame, width=15)
        self.tol_entry.grid(row=2, column=1, padx=5, pady=5)
        self.tol_entry.insert(0, "0.0005") #valor por defecto

        ttk.Label(input_frame, text="Max. Iteraciones:").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.iter_entry = ttk.Entry(input_frame, width=15)
        self.iter_entry.grid(row=2, column=3, padx=5, pady=5)
        self.iter_entry.insert(0, "100") #valor por defecto

        #Botones
        button_frame = ttk.Frame(self.calculation_frame)
        button_frame.pack(fill="x", pady=10)
        ttk.Button(button_frame, text="Calcular Raíz", command=self.perform_calculation).pack(side="left", expand=True, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_results).pack(side="left", expand=True, padx=5)
        ttk.Button(button_frame, text="« Volver al Menú Principal", command=self.show_selection_frame).pack(side="left", expand=True, padx=5)

        #resultados
        results_frame = ttk.LabelFrame(self.calculation_frame, text="Resultados", padding="15")
        results_frame.pack(fill="both", expand=True)

        self.result_status_label = ttk.Label(results_frame, text="Ingrese los parámetros y haga clic en 'Calcular'.", font=("Helvetica", 11, "italic"))
        self.result_status_label.pack(pady=5, anchor="w")
        
        self.result_final_label = ttk.Label(results_frame, text="", font=("Helvetica", 12, "bold"))
        self.result_final_label.pack(pady=5, anchor="w")

        # tabla que muestra iteraciones
        cols = ('Iteración', 'xᵢ', 'f(xᵢ)', 'Error Relativo')# aqui defino las colimnas, no olvidar .-.
        self.tree = ttk.Treeview(results_frame, columns=cols, show='headings', height=10)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def show_calculation_frame(self):
        choice = self.selected_function_var.get()
        if choice == 0:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione una función antes de continuar.")
            return
        
        self.func_label.config(text=f"Función: {functions[choice]['str']}")
        self.clear_results() #limpia los campos al cambiar de pantalla
        self.selection_frame.pack_forget()
        self.calculation_frame.pack(fill="both", expand=True)

    def show_selection_frame(self):
        #Oculta la pantalla de cálculo y vuelve al menú principal
        self.calculation_frame.pack_forget()
        self.selection_frame.pack(fill="both", expand=True)

    def perform_calculation(self):
        #aqui validamos las entradas :)
        self.clear_results(clear_inputs=False)
        try:
            x0 = float(self.x0_entry.get())
            x1 = float(self.x1_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.iter_entry.get())
            func_choice = self.selected_function_var.get()
            selected_func = functions[func_choice]['func']
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos en todos los campos.")
            return

        # Ejecuta el método
        root_val, final_err, iters, df, message = secant_method_gui(selected_func, x0, x1, tol, max_iter)

        # Actualiza la intefaz grafica con los resultados...
        self.result_status_label.config(text=message)
        
        if root_val is not None:
            self.result_final_label.config(text=f"Raíz obtenida ≈ {root_val:.8f}")

        # se llena la tabla aqui...
        if not df.empty:
            for i, row in df.iterrows():
                self.tree.insert("", "end", values=[
                    row['Iteración'],
                    f"{row['xᵢ']:.8f}",
                    f"{row['f(xᵢ)']:.8f}",
                    f"{row['Error Relativo']:.8f}"
                ])

    def clear_results(self, clear_inputs=True):
        self.tree.delete(*self.tree.get_children()) # Limpia la tabla
        self.result_status_label.config(text="Ingrese los parámetros y haga clic en 'Calcular'.")
        self.result_final_label.config(text="")
        if clear_inputs:
            self.x0_entry.delete(0, 'end')
            self.x1_entry.delete(0, 'end')

if __name__ == "__main__":
    root = tk.Tk()
    app = SecantApp(root)
    root.mainloop()