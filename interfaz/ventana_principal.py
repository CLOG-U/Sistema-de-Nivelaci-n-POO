import tkinter as tk
from tkinter import messagebox, ttk

from modelos.admin import Administrador
from servicios.sistema_nivelacion import SistemaNivelacion


class VentanaLogin(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Login - Sistema de Nivelacion")
        self.geometry("400x300")
        self.minsize(400, 300)
        self.resizable(False, False)
        self.admin_autenticado = None
        self.sistema = SistemaNivelacion()
        self.sistema.cargar_datos_demo()
        self._configurar_estilos()
        self._crear_interfaz()

    def _configurar_estilos(self):
        self.configure(bg="#f4f6f8")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f4f6f8")
        self.style.configure("Form.TFrame", background="#ffffff", relief="flat", borderwidth=0)
        self.style.configure("TLabel", background="#f4f6f8", foreground="#1f2937", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", background="#f4f6f8", foreground="#111827", font=("Segoe UI", 18, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10), padding=8)

    def _crear_interfaz(self):
        contenedor = ttk.Frame(self, padding=40, style="Form.TFrame")
        contenedor.pack(fill="both", expand=True)

        titulo = ttk.Label(contenedor, text="Iniciar Sesión", style="Title.TLabel")
        titulo.pack(pady=(0, 30))

        ttk.Label(contenedor, text="Cédula", style="TLabel").pack(anchor="w", pady=(0, 5))
        self.entrada_cedula = ttk.Entry(contenedor, width=30)
        self.entrada_cedula.pack(fill="x", pady=(0, 20))

        ttk.Label(contenedor, text="Contraseña", style="TLabel").pack(anchor="w", pady=(0, 5))
        self.entrada_contraseña = ttk.Entry(contenedor, width=30, show="*")
        self.entrada_contraseña.pack(fill="x", pady=(0, 20))

        boton_frame = ttk.Frame(contenedor)
        boton_frame.pack(fill="x", pady=(0, 5))
        ttk.Button(boton_frame, text="(Iniciar sesión)", command=self._autenticar).pack(fill="x")

    def _autenticar(self):
        cedula = self.entrada_cedula.get().strip()
        contraseña = self.entrada_contraseña.get().strip()

        if not cedula or not contraseña:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        admin_encontrado = None
        for usuario in self.sistema.usuarios:
            if isinstance(usuario, Administrador) and usuario.cedula == cedula:
                admin_encontrado = usuario
                break

        if admin_encontrado is None:
            messagebox.showerror("Error", "Administrador no encontrado")
            return

        if admin_encontrado.iniciar_sesion(contraseña):
            self.admin_autenticado = admin_encontrado
            self.destroy()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta o usuario inactivo")


class VentanaPrincipal(tk.Tk):

    def __init__(self, admin):
        super().__init__()
        self.admin = admin
        self.title(f"Bienvenido admin: {admin.nombres} {admin.apellidos}")
        self.geometry("1080x680")
        self.minsize(960, 620)
        self.sistema = SistemaNivelacion()
        self.sistema.usuarios = [admin]
        self.reporte_activo_id = None
        self._configurar_estilos()
        self._crear_interfaz()
        self._actualizar_todo()

    def _configurar_estilos(self):
        self.configure(bg="#f4f6f8")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f4f6f8")
        self.style.configure("Panel.TFrame", background="#ffffff", relief="solid", borderwidth=1)
        self.style.configure("Form.TFrame", background="#ffffff", relief="flat", borderwidth=0)
        self.style.configure("TLabel", background="#f4f6f8", foreground="#1f2937", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", background="#f4f6f8", foreground="#111827", font=("Segoe UI", 18, "bold"))
        self.style.configure("Panel.TLabel", background="#ffffff", foreground="#1f2937", font=("Segoe UI", 10))
        self.style.configure("Metric.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 22, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10), padding=8)
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _crear_interfaz(self):
        contenedor = ttk.Frame(self, padding=18)
        contenedor.pack(fill="both", expand=True)

        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill="x", pady=(0, 14))
        ttk.Label(encabezado, text=f"Bienvenido admin: {self.admin.nombres} {self.admin.apellidos}", style="Title.TLabel").pack(side="left")
        ttk.Button(encabezado, text="Cargar datos demo", command=self._cargar_demo).pack(side="right")

        self.tabs = ttk.Notebook(contenedor)
        self.tabs.pack(fill="both", expand=True)

        self.tab_inicio = ttk.Frame(self.tabs, padding=14)
        self.tab_usuarios = ttk.Frame(self.tabs, padding=14)
        self.tab_procesos = ttk.Frame(self.tabs, padding=14)
        self.tab_reportes = ttk.Frame(self.tabs, padding=14)
        self.tab_configurar_parametros = ttk.Frame(self.tabs, padding=14)
        self.tab_cursos = ttk.Frame(self.tabs, padding=14)

        self.tabs.add(self.tab_inicio, text="Inicio")
        self.tabs.add(self.tab_usuarios, text="Usuarios")
        self.tabs.add(self.tab_procesos, text="Procesos")
        self.tabs.add(self.tab_reportes, text="Reportes")
        self.tabs.add(self.tab_configurar_parametros, text="Configurar parámetros")
        self.tabs.add(self.tab_cursos, text="Cursos")

        self._crear_tab_inicio()
        self._crear_tab_usuarios()
        self._crear_tab_procesos()
        self._crear_tab_reportes()
        self._crear_tab_configurar_parametros()
        self._crear_tab_cursos()

    def _crear_tab_inicio(self):
        self.metricas = {}
        grilla = ttk.Frame(self.tab_inicio)
        grilla.pack(fill="x")

        for indice, clave in enumerate(["usuarios", "docentes", "estudiantes", "cursos", "aulas", "cargas", "reportes"]):
            panel = ttk.Frame(grilla, style="Panel.TFrame", padding=14)
            panel.grid(row=indice // 4, column=indice % 4, sticky="nsew", padx=6, pady=6)
            ttk.Label(panel, text=clave.capitalize(), style="Panel.TLabel").pack(anchor="w")
            valor = ttk.Label(panel, text="0", style="Metric.TLabel")
            valor.pack(anchor="w", pady=(8, 0))
            self.metricas[clave] = valor

        for columna in range(4):
            grilla.columnconfigure(columna, weight=1)

    def _crear_tab_usuarios(self):
        acciones = ttk.LabelFrame(self.tab_usuarios, text="Gestión de usuarios", padding=12, style="Panel.TFrame")
        acciones.pack(fill="x", pady=18)

        self.combo_usuario = self._crear_combo(acciones, "Usuario")
        ttk.Label(acciones, text="Motivo (opcional)", style="Panel.TLabel").pack(anchor="w")
        self.entrada_motivo = ttk.Entry(acciones, width=30)
        self.entrada_motivo.pack(fill="x", pady=(2, 8))

        botones = ttk.Frame(acciones)
        botones.pack(fill="x", pady=(4, 0))
        ttk.Button(botones, text="Activar usuario", command=lambda: self._accion_gestionar_usuario("activar")).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ttk.Button(botones, text="Desactivar usuario", command=lambda: self._accion_gestionar_usuario("desactivar")).pack(side="left", expand=True, fill="x")

        self.salida_usuario_text = tk.StringVar(value="Seleccione un usuario y una acción.")
        ttk.Label(acciones, textvariable=self.salida_usuario_text, style="Panel.TLabel", wraplength=780).pack(fill="x", pady=(12, 0))

    def _crear_tab_procesos(self):
        proceso_panel = ttk.LabelFrame(self.tab_procesos, text="Ejecutar proceso", padding=12, style="Panel.TFrame")
        proceso_panel.pack(fill="x", pady=18)

        ttk.Label(proceso_panel, text="Nombre del proceso", style="Panel.TLabel").pack(anchor="w")
        self.entrada_proceso = ttk.Entry(proceso_panel, width=40)
        self.entrada_proceso.pack(fill="x", pady=(2, 8))

        ttk.Button(proceso_panel, text="Ejecutar proceso", command=self._accion_gestionar_proceso).pack(fill="x")

        self.salida_proceso_text = tk.StringVar(value="Ingrese un proceso y presione el botón.")
        ttk.Label(proceso_panel, textvariable=self.salida_proceso_text, style="Panel.TLabel", wraplength=780).pack(fill="x", pady=(12, 0))

    def _crear_tab_reportes(self):
        reporte_panel = ttk.LabelFrame(self.tab_reportes, text="Generar reportes", padding=12, style="Panel.TFrame")
        reporte_panel.pack(fill="x", pady=18)

        ttk.Label(reporte_panel, text="Generar reporte administrativo", style="Panel.TLabel").pack(anchor="w")
        ttk.Button(reporte_panel, text="Generar reporte", command=self._accion_gestionar_reportes).pack(fill="x", pady=(8, 0))

        self.salida_reporte_text = tk.StringVar(value="Presione el botón para generar el reporte del administrador.")
        ttk.Label(reporte_panel, textvariable=self.salida_reporte_text, style="Panel.TLabel", wraplength=780).pack(fill="x", pady=(12, 0))

    def _crear_tab_configurar_parametros(self):
        parametro_panel = ttk.LabelFrame(self.tab_configurar_parametros, text="Configurar parámetros", padding=12, style="Panel.TFrame")
        parametro_panel.pack(fill="x", pady=18)

        ttk.Label(parametro_panel, text="Clave", style="Panel.TLabel").pack(anchor="w")
        self.entrada_param_clave = ttk.Entry(parametro_panel, width=40)
        self.entrada_param_clave.pack(fill="x", pady=(2, 8))

        ttk.Label(parametro_panel, text="Valor", style="Panel.TLabel").pack(anchor="w")
        self.entrada_param_valor = ttk.Entry(parametro_panel, width=40)
        self.entrada_param_valor.pack(fill="x", pady=(2, 8))

        ttk.Button(parametro_panel, text="Configurar parámetro", command=self._accion_configurar_parametros).pack(fill="x", pady=(8, 0))

        self.salida_param_text = tk.StringVar(value="Ingrese clave y valor, luego presione configurar.")
        ttk.Label(parametro_panel, textvariable=self.salida_param_text, style="Panel.TLabel", wraplength=780).pack(fill="x", pady=(12, 0))

    def _crear_tab_cursos(self):
        curso_panel = ttk.LabelFrame(self.tab_cursos, text="Gestión de cursos", padding=12, style="Panel.TFrame")
        curso_panel.pack(fill="x", pady=18)

        self.combo_curso = self._crear_combo(curso_panel, "Curso")
        botones = ttk.Frame(curso_panel)
        botones.pack(fill="x", pady=(4, 0))
        ttk.Button(botones, text="Abrir curso", command=lambda: self._accion_gestionar_curso("abrir")).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ttk.Button(botones, text="Cerrar curso", command=lambda: self._accion_gestionar_curso("cerrar")).pack(side="left", expand=True, fill="x")

        self.salida_curso_text = tk.StringVar(value="Seleccione un curso y una acción.")
        ttk.Label(curso_panel, textvariable=self.salida_curso_text, style="Panel.TLabel", wraplength=780).pack(fill="x", pady=(12, 0))

    def _cargar_demo(self):
        self.sistema.cargar_datos_demo()
        self._actualizar_todo()

    def _actualizar_todo(self):
        self._actualizar_metricas()
        self._actualizar_combos()

    def _actualizar_metricas(self):
        for clave, valor in self.sistema.resumen().items():
            self.metricas[clave].configure(text=str(valor))

    def _actualizar_combos(self):
        if hasattr(self, "combo_usuario"):
            self._llenar_combo(self.combo_usuario, self.sistema.usuarios)
        if hasattr(self, "combo_curso"):
            self._llenar_combo(self.combo_curso, self.sistema.cursos)

    def _accion_gestionar_usuario(self, accion):
        try:
            usuario = self._objeto_seleccionado(self.combo_usuario, self.sistema.usuarios)
            motivo = self.entrada_motivo.get().strip()
            resultado = self.admin.gestionar_usuario(accion, usuario, motivo=motivo or None)
            self.salida_usuario_text.set(resultado)
            self.entrada_motivo.delete(0, "end")
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Gestionar usuario", str(error))

    def _accion_gestionar_proceso(self):
        try:
            proceso = self.entrada_proceso.get().strip()
            if not proceso:
                raise ValueError("Complete el nombre del proceso")
            resultado = self.admin.gestionar_procesos(proceso)
            self.salida_proceso_text.set(resultado)
            self.entrada_proceso.delete(0, "end")
        except Exception as error:
            messagebox.showerror("Gestionar proceso", str(error))

    def _accion_configurar_parametros(self):
        try:
            clave = self.entrada_param_clave.get().strip()
            valor = self.entrada_param_valor.get().strip()
            if not clave or not valor:
                raise ValueError("Complete clave y valor")
            resultado = self.admin.configurar_parametros((clave, valor))
            self.salida_param_text.set(resultado)
            self.entrada_param_clave.delete(0, "end")
            self.entrada_param_valor.delete(0, "end")
        except Exception as error:
            messagebox.showerror("Configurar parámetros", str(error))

    def _accion_gestionar_curso(self, accion):
        try:
            curso = self._objeto_seleccionado(self.combo_curso, self.sistema.cursos)
            resultado = self.admin.gestionar_cursos(accion, curso)
            self.salida_curso_text.set(resultado)
        except Exception as error:
            messagebox.showerror("Gestionar curso", str(error))

    def _accion_gestionar_reportes(self):
        try:
            resultado = self.admin.gestionar_reportes()
            self.salida_reporte_text.set(resultado)
        except Exception as error:
            messagebox.showerror("Gestionar reportes", str(error))

    def _crear_combo(self, padre, etiqueta):
        ttk.Label(padre, text=etiqueta, style="Panel.TLabel").pack(anchor="w")
        variable = tk.StringVar()
        combo = ttk.Combobox(padre, textvariable=variable, state="readonly", width=28)
        combo.pack(fill="x", pady=(2, 8))
        combo.variable = variable
        return combo

    def _llenar_combo(self, combo, objetos):
        combo.objetos = objetos
        combo["values"] = [self._texto_objeto(objeto) for objeto in objetos]
        if objetos:
            combo.current(0)
        else:
            combo.set("")

    def _objeto_seleccionado(self, combo, objetos):
        indice = combo.current()
        if indice < 0 or indice >= len(objetos):
            raise ValueError("Seleccione una opcion valida")
        return objetos[indice]

    def _texto_objeto(self, objeto):
        if hasattr(objeto, "id_usuario") and hasattr(objeto, "nombres") and hasattr(objeto, "apellidos"):
            return f"{objeto.cedula} - {objeto.nombres} {objeto.apellidos}"
        if hasattr(objeto, "codigo") and hasattr(objeto, "nombre"):
            return f"{objeto.codigo} - {objeto.nombre}"
        if hasattr(objeto, "nombre"):
            return objeto.nombre
        return str(objeto)



def iniciar_interfaz():
    login = VentanaLogin()
    login.mainloop()
    
    if login.admin_autenticado:
        # Copiar los datos del sistema del login a la ventana principal
        app = VentanaPrincipal(login.admin_autenticado)
        # Copiar todos los datos cargados en el demo al nuevo sistema
        app.sistema.usuarios = login.sistema.usuarios
        app.sistema.aulas = login.sistema.aulas
        app.sistema.horarios = login.sistema.horarios
        app.sistema.cursos = login.sistema.cursos
        app.sistema.reportes = login.sistema.reportes
        app._actualizar_todo()
        app.mainloop()


        app.mainloop()

