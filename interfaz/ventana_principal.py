import tkinter as tk
from tkinter import messagebox, ttk

from modelos.admin import Administrador
from modelos.docente import Docente
from modelos.estudiante import Estudiante
from servicios.sistema_nivelacion import SistemaNivelacion


class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Nivelacion ULEAM")
        self.geometry("1080x680")
        self.minsize(960, 620)
        self.sistema = SistemaNivelacion()
        self._configurar_estilos()
        self._crear_interfaz()
        self._actualizar_todo()

    def _configurar_estilos(self):
        self.configure(bg="#f4f6f8")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f4f6f8")
        self.style.configure("Panel.TFrame", background="#ffffff", relief="solid", borderwidth=1)
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
        ttk.Label(encabezado, text="Sistema de Nivelacion ULEAM", style="Title.TLabel").pack(side="left")
        ttk.Button(encabezado, text="Cargar datos demo", command=self._cargar_demo).pack(side="right")

        self.tabs = ttk.Notebook(contenedor)
        self.tabs.pack(fill="both", expand=True)

        self.tab_inicio = ttk.Frame(self.tabs, padding=14)
        self.tab_usuarios = ttk.Frame(self.tabs, padding=14)
        self.tab_cursos = ttk.Frame(self.tabs, padding=14)
        self.tab_carga = ttk.Frame(self.tabs, padding=14)
        self.tab_reportes = ttk.Frame(self.tabs, padding=14)

        self.tabs.add(self.tab_inicio, text="Inicio")
        self.tabs.add(self.tab_usuarios, text="Usuarios")
        self.tabs.add(self.tab_cursos, text="Cursos")
        self.tabs.add(self.tab_carga, text="Carga academica")
        self.tabs.add(self.tab_reportes, text="Reportes")

        self._crear_tab_inicio()
        self._crear_tab_usuarios()
        self._crear_tab_cursos()
        self._crear_tab_carga()
        self._crear_tab_reportes()

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

        acciones = ttk.Frame(self.tab_inicio)
        acciones.pack(fill="x", pady=18)
        ttk.Button(acciones, text="Registrar usuario", command=lambda: self.tabs.select(self.tab_usuarios)).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Crear curso", command=lambda: self.tabs.select(self.tab_cursos)).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Generar reporte", command=lambda: self.tabs.select(self.tab_reportes)).pack(side="left")

    def _crear_tab_usuarios(self):
        contenido = ttk.Frame(self.tab_usuarios)
        contenido.pack(fill="both", expand=True)
        formulario = ttk.Frame(contenido, style="Panel.TFrame", padding=14)
        formulario.pack(side="left", fill="y", padx=(0, 12))
        tabla_panel = ttk.Frame(contenido)
        tabla_panel.pack(side="left", fill="both", expand=True)

        self.tipo_usuario = tk.StringVar(value="Estudiante")
        ttk.Label(formulario, text="Tipo", style="Panel.TLabel").grid(row=0, column=0, sticky="w")
        tipo = ttk.Combobox(formulario, textvariable=self.tipo_usuario, values=["Estudiante", "Docente", "Administrador"], state="readonly", width=26)
        tipo.grid(row=1, column=0, sticky="ew", pady=(2, 8))
        tipo.bind("<<ComboboxSelected>>", lambda _event: self._actualizar_campos_usuario())

        self.campos_usuario = {}
        etiquetas = ["Cedula", "Nombres", "Apellidos", "Correo", "Contrasena", "Telefono"]
        for fila, etiqueta in enumerate(etiquetas, start=2):
            ttk.Label(formulario, text=etiqueta, style="Panel.TLabel").grid(row=fila * 2, column=0, sticky="w")
            entrada = ttk.Entry(formulario, width=30, show="*" if etiqueta == "Contrasena" else "")
            entrada.grid(row=fila * 2 + 1, column=0, sticky="ew", pady=(2, 8))
            self.campos_usuario[etiqueta] = entrada

        self.extra_usuario = ttk.Frame(formulario, style="Panel.TFrame")
        self.extra_usuario.grid(row=16, column=0, sticky="ew")
        ttk.Button(formulario, text="Guardar usuario", command=self._registrar_usuario).grid(row=17, column=0, sticky="ew", pady=(12, 0))

        columnas = ("tipo", "cedula", "nombres", "correo", "detalle")
        self.tabla_usuarios = self._crear_tabla(tabla_panel, columnas, ("Tipo", "Cedula", "Nombres", "Correo", "Detalle"))
        self._actualizar_campos_usuario()

    def _actualizar_campos_usuario(self):
        for widget in self.extra_usuario.winfo_children():
            widget.destroy()
        self.campos_extra_usuario = {}

        tipo = self.tipo_usuario.get()
        if tipo == "Docente":
            campos = ["Titulo profesional", "Especialidad"]
        elif tipo == "Administrador":
            campos = ["Cargo"]
        else:
            campos = ["Tipo documento", "Numero documento", "Fecha nacimiento"]

        for indice, etiqueta in enumerate(campos):
            ttk.Label(self.extra_usuario, text=etiqueta, style="Panel.TLabel").grid(row=indice * 2, column=0, sticky="w")
            entrada = ttk.Entry(self.extra_usuario, width=30)
            entrada.grid(row=indice * 2 + 1, column=0, sticky="ew", pady=(2, 8))
            self.campos_extra_usuario[etiqueta] = entrada

    def _crear_tab_cursos(self):
        contenido = ttk.Frame(self.tab_cursos)
        contenido.pack(fill="both", expand=True)
        formularios = ttk.Frame(contenido)
        formularios.pack(side="left", fill="y", padx=(0, 12))
        tablas = ttk.Frame(contenido)
        tablas.pack(side="left", fill="both", expand=True)

        aula_panel = ttk.LabelFrame(formularios, text="Aula", padding=12)
        aula_panel.pack(fill="x", pady=(0, 10))
        self.campos_aula = self._crear_campos(aula_panel, ["Codigo", "Nombre", "Capacidad", "Piso", "Edificio"])
        ttk.Button(aula_panel, text="Guardar aula", command=self._registrar_aula).pack(fill="x", pady=(8, 0))

        curso_panel = ttk.LabelFrame(formularios, text="Curso", padding=12)
        curso_panel.pack(fill="x", pady=(0, 10))
        self.campos_curso = self._crear_campos(curso_panel, ["Codigo", "Nombre", "Nivel", "Paralelo", "Cupo maximo"])
        self.combo_docente = self._crear_combo(curso_panel, "Docente")
        self.combo_aula = self._crear_combo(curso_panel, "Aula")
        self.campos_horario = self._crear_campos(curso_panel, ["Dia", "Hora inicio", "Hora fin", "Modalidad", "Grupo"])
        ttk.Button(curso_panel, text="Guardar curso", command=self._registrar_curso).pack(fill="x", pady=(8, 0))

        inscripcion_panel = ttk.LabelFrame(formularios, text="Inscripcion", padding=12)
        inscripcion_panel.pack(fill="x")
        self.combo_curso = self._crear_combo(inscripcion_panel, "Curso")
        self.combo_estudiante = self._crear_combo(inscripcion_panel, "Estudiante")
        ttk.Button(inscripcion_panel, text="Inscribir estudiante", command=self._inscribir_estudiante).pack(fill="x", pady=(8, 0))

        self.tabla_aulas = self._crear_tabla(tablas, ("codigo", "nombre", "capacidad", "edificio"), ("Codigo", "Nombre", "Capacidad", "Edificio"))
        self.tabla_cursos = self._crear_tabla(tablas, ("codigo", "nombre", "docente", "cupo"), ("Codigo", "Nombre", "Docente", "Cupo"))

    def _crear_tab_carga(self):
        contenido = ttk.Frame(self.tab_carga)
        contenido.pack(fill="both", expand=True)
        formulario = ttk.Frame(contenido, style="Panel.TFrame", padding=14)
        formulario.pack(side="left", fill="y", padx=(0, 12))
        self.campos_carga = self._crear_campos(formulario, ["Total asignaturas", "Total creditos"])
        ttk.Button(formulario, text="Guardar carga", command=self._registrar_carga).pack(fill="x", pady=(8, 0))
        self.tabla_cargas = self._crear_tabla(contenido, ("id", "asignaturas", "creditos", "estado"), ("ID", "Asignaturas", "Creditos", "Estado"))

    def _crear_tab_reportes(self):
        contenido = ttk.Frame(self.tab_reportes)
        contenido.pack(fill="both", expand=True)
        formulario = ttk.Frame(contenido, style="Panel.TFrame", padding=14)
        formulario.pack(side="left", fill="y", padx=(0, 12))
        self.campos_reporte = self._crear_campos(formulario, ["Tipo reporte", "Fecha generacion", "Periodo", "Descripcion"])
        self.formato_reporte = tk.StringVar(value="PDF")
        ttk.Label(formulario, text="Formato", style="Panel.TLabel").pack(anchor="w")
        ttk.Combobox(formulario, textvariable=self.formato_reporte, values=["PDF", "Excel"], state="readonly").pack(fill="x", pady=(2, 8))
        ttk.Button(formulario, text="Generar reporte", command=self._generar_reporte).pack(fill="x", pady=(8, 0))

        panel_salida = ttk.Frame(contenido)
        panel_salida.pack(side="left", fill="both", expand=True)
        self.tabla_reportes = self._crear_tabla(panel_salida, ("id", "tipo", "periodo", "formato"), ("ID", "Tipo", "Periodo", "Formato"))
        self.salida_reporte = tk.Text(panel_salida, height=8, wrap="word", font=("Segoe UI", 10))
        self.salida_reporte.pack(fill="x", pady=(10, 0))

    def _crear_campos(self, padre, etiquetas):
        campos = {}
        for etiqueta in etiquetas:
            ttk.Label(padre, text=etiqueta, style="Panel.TLabel").pack(anchor="w")
            entrada = ttk.Entry(padre, width=30)
            entrada.pack(fill="x", pady=(2, 8))
            campos[etiqueta] = entrada
        return campos

    def _crear_combo(self, padre, etiqueta):
        ttk.Label(padre, text=etiqueta, style="Panel.TLabel").pack(anchor="w")
        variable = tk.StringVar()
        combo = ttk.Combobox(padre, textvariable=variable, state="readonly", width=28)
        combo.pack(fill="x", pady=(2, 8))
        combo.variable = variable
        return combo

    def _crear_tabla(self, padre, columnas, encabezados):
        frame = ttk.Frame(padre)
        frame.pack(fill="both", expand=True, pady=(0, 8))
        tabla = ttk.Treeview(frame, columns=columnas, show="headings")
        barra = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)
        for columna, encabezado in zip(columnas, encabezados):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=130, anchor="w")
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def _registrar_usuario(self):
        try:
            tipo = self.tipo_usuario.get()
            datos = {
                "cedula": self._valor(self.campos_usuario["Cedula"]),
                "nombres": self._valor(self.campos_usuario["Nombres"]),
                "apellidos": self._valor(self.campos_usuario["Apellidos"]),
                "correo": self._valor(self.campos_usuario["Correo"]),
                "contrasena": self._valor(self.campos_usuario["Contrasena"]),
                "telefono": self._valor(self.campos_usuario["Telefono"]),
            }
            extras = {}
            if tipo == "Docente":
                extras["titulo_profesional"] = self._valor(self.campos_extra_usuario["Titulo profesional"])
                extras["especialidad"] = self._valor(self.campos_extra_usuario["Especialidad"])
            elif tipo == "Administrador":
                extras["cargo"] = self._valor(self.campos_extra_usuario["Cargo"])
            else:
                extras["tipo_documento"] = self._valor(self.campos_extra_usuario["Tipo documento"])
                extras["numero_documento"] = self._valor(self.campos_extra_usuario["Numero documento"])
                extras["fecha_nacimiento"] = self._valor(self.campos_extra_usuario["Fecha nacimiento"])

            self.sistema.registrar_usuario(tipo, **datos, **extras)
            self._limpiar_campos(self.campos_usuario)
            self._limpiar_campos(self.campos_extra_usuario)
            self._actualizar_todo()
            messagebox.showinfo("Usuario", "Usuario registrado correctamente")
        except Exception as error:
            messagebox.showerror("Usuario", str(error))

    def _registrar_aula(self):
        try:
            self.sistema.registrar_aula(
                self._valor(self.campos_aula["Codigo"]),
                self._valor(self.campos_aula["Nombre"]),
                self._valor(self.campos_aula["Capacidad"]),
                self._valor(self.campos_aula["Piso"]),
                self._valor(self.campos_aula["Edificio"]),
            )
            self._limpiar_campos(self.campos_aula)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Aula", str(error))

    def _registrar_curso(self):
        try:
            docente = self._objeto_seleccionado(self.combo_docente, self.sistema.listar_docentes())
            aula = self._objeto_seleccionado(self.combo_aula, self.sistema.aulas)
            horario = self.sistema.registrar_horario(
                self._valor(self.campos_horario["Dia"]),
                self._valor(self.campos_horario["Hora inicio"]),
                self._valor(self.campos_horario["Hora fin"]),
                self._valor(self.campos_horario["Modalidad"]),
                self._valor(self.campos_horario["Grupo"]),
                aula,
            )
            self.sistema.registrar_curso(
                self._valor(self.campos_curso["Codigo"]),
                self._valor(self.campos_curso["Nombre"]),
                self._valor(self.campos_curso["Nivel"]),
                self._valor(self.campos_curso["Paralelo"]),
                self._valor(self.campos_curso["Cupo maximo"]),
                docente,
                horario,
                aula,
            )
            self._limpiar_campos(self.campos_curso)
            self._limpiar_campos(self.campos_horario)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Curso", str(error))

    def _inscribir_estudiante(self):
        try:
            curso = self._objeto_seleccionado(self.combo_curso, self.sistema.cursos)
            estudiante = self._objeto_seleccionado(self.combo_estudiante, self.sistema.listar_estudiantes())
            self.sistema.inscribir_estudiante(curso, estudiante)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Inscripcion", str(error))

    def _registrar_carga(self):
        try:
            self.sistema.registrar_carga_academica(
                self._valor(self.campos_carga["Total asignaturas"]),
                self._valor(self.campos_carga["Total creditos"]),
            )
            self._limpiar_campos(self.campos_carga)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Carga academica", str(error))

    def _generar_reporte(self):
        try:
            reporte = self.sistema.generar_reporte(
                self._valor(self.campos_reporte["Tipo reporte"]),
                self._valor(self.campos_reporte["Fecha generacion"]),
                self._valor(self.campos_reporte["Periodo"]),
                self._valor(self.campos_reporte["Descripcion"]),
                self.formato_reporte.get(),
            )
            self.salida_reporte.delete("1.0", "end")
            self.salida_reporte.insert("end", "Reporte: " + reporte.tipo_reporte + "\n")
            self.salida_reporte.insert("end", "Periodo: " + reporte.periodo + "\n")
            self.salida_reporte.insert("end", "Descripcion: " + reporte.descripcion + "\n")
            self.salida_reporte.insert("end", "Formato: " + self.formato_reporte.get())
            self._limpiar_campos(self.campos_reporte)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Reporte", str(error))

    def _cargar_demo(self):
        self.sistema.cargar_datos_demo()
        self._actualizar_todo()

    def _actualizar_todo(self):
        self._actualizar_metricas()
        self._actualizar_usuarios()
        self._actualizar_aulas()
        self._actualizar_cursos()
        self._actualizar_cargas()
        self._actualizar_reportes()
        self._actualizar_combos()

    def _actualizar_metricas(self):
        for clave, valor in self.sistema.resumen().items():
            self.metricas[clave].configure(text=str(valor))

    def _actualizar_usuarios(self):
        self._vaciar_tabla(self.tabla_usuarios)
        for usuario in self.sistema.usuarios:
            tipo = usuario.__class__.__name__
            detalle = self._detalle_usuario(usuario)
            self.tabla_usuarios.insert("", "end", values=(tipo, usuario.cedula, usuario.nombres + " " + usuario.apellidos, usuario.correo, detalle))

    def _actualizar_aulas(self):
        self._vaciar_tabla(self.tabla_aulas)
        for aula in self.sistema.aulas:
            self.tabla_aulas.insert("", "end", values=(self._texto_objeto(aula), aula.nombre, aula.capacidad, aula.edificio))

    def _actualizar_cursos(self):
        self._vaciar_tabla(self.tabla_cursos)
        for curso in self.sistema.cursos:
            docente = curso.docente.nombres + " " + curso.docente.apellidos
            cupo = str(curso.cupo_actual) + "/" + str(curso.cupo_maximo)
            self.tabla_cursos.insert("", "end", values=(curso.codigo, curso.nombre, docente, cupo))

    def _actualizar_cargas(self):
        self._vaciar_tabla(self.tabla_cargas)
        for carga in self.sistema.cargas_academicas:
            self.tabla_cargas.insert("", "end", values=(carga.id_carga, carga.total_asignaturas, carga.total_creditos, "Activa" if carga.estado else "Inactiva"))

    def _actualizar_reportes(self):
        self._vaciar_tabla(self.tabla_reportes)
        for reporte in self.sistema.reportes:
            self.tabla_reportes.insert("", "end", values=(reporte.id_reporte, reporte.tipo_reporte, reporte.periodo, "Generado"))

    def _actualizar_combos(self):
        self._llenar_combo(self.combo_docente, self.sistema.listar_docentes())
        self._llenar_combo(self.combo_estudiante, self.sistema.listar_estudiantes())
        self._llenar_combo(self.combo_aula, self.sistema.aulas)
        self._llenar_combo(self.combo_curso, self.sistema.cursos)

    def _llenar_combo(self, combo, objetos):
        combo.objetos = objetos
        combo["values"] = [self._texto_objeto(objeto) for objeto in objetos]
        if objetos and not combo.get():
            combo.current(0)
        if not objetos:
            combo.set("")

    def _objeto_seleccionado(self, combo, objetos):
        indice = combo.current()
        if indice < 0 or indice >= len(objetos):
            raise ValueError("Seleccione una opcion valida")
        return objetos[indice]

    def _texto_objeto(self, objeto):
        if isinstance(objeto, (Docente, Estudiante, Administrador)):
            return str(objeto.id_usuario) + " - " + objeto.nombres + " " + objeto.apellidos
        if hasattr(objeto, "codigo") and hasattr(objeto, "nombre"):
            return objeto.codigo + " - " + objeto.nombre
        if hasattr(objeto, "nombre"):
            return objeto.nombre
        return str(objeto)

    def _detalle_usuario(self, usuario):
        if isinstance(usuario, Docente):
            return usuario.especialidad
        if isinstance(usuario, Estudiante):
            return usuario.estado_nivelacion
        if isinstance(usuario, Administrador):
            return usuario.cargo
        return ""

    def _valor(self, entrada):
        valor = entrada.get().strip()
        if not valor:
            raise ValueError("Complete todos los campos requeridos")
        return valor

    def _limpiar_campos(self, campos):
        for entrada in campos.values():
            entrada.delete(0, "end")

    def _vaciar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)


def iniciar_interfaz():
    app = VentanaPrincipal()
    app.mainloop()

