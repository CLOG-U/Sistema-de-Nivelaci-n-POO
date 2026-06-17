import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from modelos.admin import Administrador
from modelos.aula import Aula
from modelos.curso_nivelacion import CursoNivelacion
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

        self.tipo_documento = tk.StringVar(value="Cedula")
        ttk.Label(formulario, text="Tipo documento", style="Panel.TLabel").grid(row=2, column=0, sticky="w")
        combo_documento = ttk.Combobox(
            formulario,
            textvariable=self.tipo_documento,
            values=["Cedula", "Pasaporte"],
            state="readonly",
            width=26,
        )
        combo_documento.grid(row=3, column=0, sticky="ew", pady=(2, 8))

        self.campos_usuario = {}
        etiquetas = ["Cedula", "Nombres", "Apellidos", "Correo", "Contrasena", "Telefono"]
        for fila, etiqueta in enumerate(etiquetas, start=2):
            ttk.Label(formulario, text=etiqueta, style="Panel.TLabel").grid(row=fila * 2, column=0, sticky="w")
            entrada = ttk.Entry(formulario, width=30, show="*" if etiqueta == "Contrasena" else "")
            entrada.grid(row=fila * 2 + 1, column=0, sticky="ew", pady=(2, 8))
            self.campos_usuario[etiqueta] = entrada

        self.extra_usuario = ttk.Frame(formulario, style="Form.TFrame")
        self.extra_usuario.grid(row=16, column=0, sticky="ew", pady=(0, 2))
        self.extra_usuario.columnconfigure(0, weight=1)
        ttk.Button(formulario, text="Guardar usuario", command=self._registrar_usuario).grid(row=17, column=0, sticky="ew", pady=(12, 0))

        columnas = ("tipo", "cedula", "nombres", "correo", "detalle")
        self.tabla_usuarios = self._crear_tabla(tabla_panel, columnas, ("Tipo", "Cedula", "Nombres", "Correo", "Detalle"))
        self.tabla_usuarios.bind("<Double-1>", self._mostrar_detalle_usuario_seleccionado)
        ttk.Button(tabla_panel, text="Ver detalle", command=self._mostrar_detalle_usuario_seleccionado).pack(anchor="e")
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
            campos = ["Fecha nacimiento"]

        for indice, etiqueta in enumerate(campos):
            ttk.Label(self.extra_usuario, text=etiqueta, style="Panel.TLabel").grid(row=indice * 2, column=0, sticky="w")
            entrada = ttk.Entry(self.extra_usuario, width=30)
            entrada.grid(row=indice * 2 + 1, column=0, sticky="ew", pady=(2, 8))
            self.campos_extra_usuario[etiqueta] = entrada

    def _crear_tab_cursos(self):
        contenido = ttk.Frame(self.tab_cursos)
        contenido.pack(fill="both", expand=True)
        formularios = ttk.Frame(contenido, width=280)
        formularios.pack(side="left", fill="y", padx=(0, 12))
        formularios.pack_propagate(False)
        registros = ttk.LabelFrame(contenido, text="Registros", padding=10)
        registros.pack(side="left", fill="both", expand=True)

        gestor_formularios = ttk.Notebook(formularios)
        gestor_formularios.pack(fill="both", expand=True)

        aula_panel = ttk.Frame(gestor_formularios, padding=12, style="Form.TFrame")
        curso_panel = ttk.Frame(gestor_formularios, padding=12, style="Form.TFrame")
        horario_panel = ttk.Frame(gestor_formularios, padding=12, style="Form.TFrame")
        inscripcion_panel = ttk.Frame(gestor_formularios, padding=12, style="Form.TFrame")

        gestor_formularios.add(aula_panel, text="Aula")
        gestor_formularios.add(curso_panel, text="Curso")
        gestor_formularios.add(horario_panel, text="Horario")
        gestor_formularios.add(inscripcion_panel, text="Inscripcion")

        self.campos_aula = self._crear_campos(aula_panel, ["Codigo", "Nombre", "Capacidad", "Piso", "Edificio"])
        ttk.Button(aula_panel, text="Guardar aula", command=self._registrar_aula).pack(fill="x", pady=(8, 0))

        self.campos_curso = self._crear_campos(curso_panel, ["Codigo", "Nombre", "Nivel", "Paralelo", "Cupo maximo"])
        self.combo_docente = self._crear_combo(curso_panel, "Docente")
        self.combo_aula = self._crear_combo(curso_panel, "Aula")

        self.campos_horario = self._crear_campos(horario_panel, ["Dia", "Hora inicio", "Hora fin", "Modalidad", "Grupo"])
        ttk.Button(horario_panel, text="Guardar curso", command=self._registrar_curso).pack(fill="x", pady=(8, 0))

        self.combo_curso = self._crear_combo(inscripcion_panel, "Curso")
        self.combo_estudiante = self._crear_combo(inscripcion_panel, "Estudiante")
        ttk.Button(inscripcion_panel, text="Inscribir estudiante", command=self._inscribir_estudiante).pack(fill="x", pady=(8, 0))

        registros_tabs = ttk.Notebook(registros)
        registros_tabs.pack(fill="both", expand=True)
        panel_aulas = ttk.Frame(registros_tabs, padding=8)
        panel_cursos = ttk.Frame(registros_tabs, padding=8)
        registros_tabs.add(panel_aulas, text="Aulas")
        registros_tabs.add(panel_cursos, text="Cursos")

        self.tabla_aulas = self._crear_tabla(
            panel_aulas,
            ("codigo", "nombre", "capacidad", "edificio"),
            ("Codigo", "Nombre", "Capacidad", "Edificio"),
        )
        self.tabla_aulas.bind("<Double-1>", self._mostrar_detalle_aula_seleccionada)
        ttk.Button(panel_aulas, text="Ver detalle", command=self._mostrar_detalle_aula_seleccionada).pack(anchor="e")

        self.tabla_cursos = self._crear_tabla(
            panel_cursos,
            ("codigo", "nombre", "docente", "cupo"),
            ("Codigo", "Nombre", "Docente", "Cupo"),
        )
        self.tabla_cursos.bind("<Double-1>", self._mostrar_detalle_curso_seleccionado)
        ttk.Button(panel_cursos, text="Ver detalle", command=self._mostrar_detalle_curso_seleccionado).pack(anchor="e")

    def _crear_tab_carga(self):
        contenido = ttk.Frame(self.tab_carga)
        contenido.pack(fill="both", expand=True)
        formulario = ttk.Frame(contenido, style="Panel.TFrame", padding=14)
        formulario.pack(side="left", fill="y", padx=(0, 12))
        self.combo_estudiante_carga = self._crear_combo(formulario, "Estudiante")
        ttk.Label(formulario, text="Periodo actual", style="Panel.TLabel").pack(anchor="w")
        ttk.Label(formulario, text=self.sistema.periodo_actual, style="Panel.TLabel").pack(anchor="w", pady=(2, 12))
        ttk.Button(formulario, text="Generar carga", command=self._registrar_carga).pack(fill="x", pady=(8, 0))

        panel_cargas = ttk.Frame(contenido)
        panel_cargas.pack(side="left", fill="both", expand=True)
        self.tabla_cargas = self._crear_tabla(
            panel_cargas,
            ("id", "estudiante", "periodo", "asignaturas", "creditos", "estado"),
            ("ID", "Estudiante", "Periodo", "Asignaturas", "Creditos", "Estado"),
        )
        self.tabla_cargas.bind("<Double-1>", self._mostrar_detalle_carga_seleccionada)
        ttk.Button(panel_cargas, text="Ver detalle", command=self._mostrar_detalle_carga_seleccionada).pack(anchor="e")

    def _crear_tab_reportes(self):
        contenido = ttk.Frame(self.tab_reportes)
        contenido.pack(fill="both", expand=True)
        formulario = ttk.Frame(contenido, style="Panel.TFrame", padding=14)
        formulario.pack(side="left", fill="y", padx=(0, 12))
        ttk.Label(formulario, text="Fecha generacion", style="Panel.TLabel").pack(anchor="w")
        ttk.Label(formulario, text=date.today().isoformat(), style="Panel.TLabel").pack(anchor="w", pady=(2, 12))
        self.campos_reporte = self._crear_campos(formulario, ["Tipo reporte", "Descripcion"])
        self.combo_periodo_reporte = self._crear_combo(formulario, "Periodo")
        self.formato_reporte = tk.StringVar(value="PDF")
        ttk.Label(formulario, text="Formato", style="Panel.TLabel").pack(anchor="w")
        ttk.Combobox(formulario, textvariable=self.formato_reporte, values=["PDF", "Excel"], state="readonly").pack(fill="x", pady=(2, 8))
        ttk.Button(formulario, text="Generar reporte", command=self._generar_reporte).pack(fill="x", pady=(8, 0))

        panel_salida = ttk.Frame(contenido)
        panel_salida.pack(side="left", fill="both", expand=True)
        self.tabla_reportes = self._crear_tabla(panel_salida, ("id", "tipo", "fecha", "periodo", "formato"), ("ID", "Tipo", "Fecha", "Periodo", "Formato"))
        self.tabla_reportes.bind("<<TreeviewSelect>>", self._mostrar_reporte_seleccionado)
        self.salida_reporte = tk.Text(panel_salida, height=8, wrap="word", font=("Segoe UI", 10))
        self.salida_reporte.pack(fill="x", pady=(10, 0))
        self._renderizar_reporte(None)

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
                extras["tipo_documento"] = self.tipo_documento.get()
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
            estudiante = self._objeto_seleccionado(self.combo_estudiante_carga, self.sistema.listar_estudiantes())
            self.sistema.registrar_carga_academica(estudiante)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Carga academica", str(error))

    def _generar_reporte(self):
        try:
            reporte = self.sistema.generar_reporte(
                self._valor(self.campos_reporte["Tipo reporte"]),
                self.combo_periodo_reporte.get(),
                self._valor(self.campos_reporte["Descripcion"]),
                self.formato_reporte.get(),
            )
            self.reporte_activo_id = reporte.id_reporte
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
        self._actualizar_registros_cursos()
        self._actualizar_cargas()
        self._actualizar_reportes()
        self._actualizar_combos()

    def _actualizar_metricas(self):
        for clave, valor in self.sistema.resumen().items():
            self.metricas[clave].configure(text=str(valor))

    def _actualizar_usuarios(self):
        self._vaciar_tabla(self.tabla_usuarios)
        self.objetos_usuarios = {}
        for usuario in self.sistema.usuarios:
            tipo = usuario.__class__.__name__
            detalle = self._detalle_usuario(usuario)
            item = self.tabla_usuarios.insert("", "end", values=(tipo, usuario.cedula, usuario.nombres + " " + usuario.apellidos, usuario.correo, detalle))
            self.objetos_usuarios[item] = usuario

    def _actualizar_registros_cursos(self):
        self._vaciar_tabla(self.tabla_aulas)
        self._vaciar_tabla(self.tabla_cursos)
        self.objetos_aulas = {}
        self.objetos_cursos = {}

        for aula in self.sistema.aulas:
            item = self.tabla_aulas.insert("", "end", values=(aula.codigo, aula.nombre, aula.capacidad, aula.edificio))
            self.objetos_aulas[item] = aula

        for curso in self.sistema.cursos:
            docente = curso.docente.nombres + " " + curso.docente.apellidos
            cupo = str(curso.cupo_actual) + "/" + str(curso.cupo_maximo)
            item = self.tabla_cursos.insert("", "end", values=(curso.codigo, curso.nombre, docente, cupo))
            self.objetos_cursos[item] = curso

    def _mostrar_detalle_usuario_seleccionado(self, _event=None):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        usuario = self.objetos_usuarios.get(seleccion[0])
        if usuario is not None:
            self._mostrar_detalle_usuario(usuario)

    def _mostrar_detalle_usuario(self, usuario):
        if isinstance(usuario, Estudiante):
            self._mostrar_detalle_estudiante(usuario)
        elif isinstance(usuario, Docente):
            self._mostrar_detalle_docente(usuario)
        elif isinstance(usuario, Administrador):
            self._mostrar_detalle_administrador(usuario)

    def _mostrar_detalle_estudiante(self, estudiante):
        ventana = self._crear_ventana_detalle("Detalle del estudiante")
        cursos = self.sistema.obtener_cursos_estudiante(estudiante)
        materias = ", ".join([curso.nombre for curso in cursos])
        if not materias:
            materias = "Sin cursos inscritos"

        datos = [
            ("ID", estudiante.id_usuario),
            ("Nombres", estudiante.nombres + " " + estudiante.apellidos),
            ("Cedula", estudiante.cedula),
            ("Tipo documento", estudiante.tipo_documento),
            ("Correo", estudiante.correo),
            ("Telefono", estudiante.telefono),
            ("Nacimiento", estudiante.fecha_nacimiento),
            ("Estado nivelacion", estudiante.estado_nivelacion),
            ("Materias inscritas", materias),
        ]
        self._llenar_detalle(ventana, datos)

    def _mostrar_detalle_docente(self, docente):
        ventana = self._crear_ventana_detalle("Detalle del docente")
        cursos = [curso.nombre for curso in self.sistema.cursos if curso.docente == docente]
        materias = ", ".join(cursos) if cursos else "Sin cursos asignados"
        datos = [
            ("ID", docente.id_usuario),
            ("Nombres", docente.nombres + " " + docente.apellidos),
            ("Cedula", docente.cedula),
            ("Correo", docente.correo),
            ("Telefono", docente.telefono),
            ("Titulo", docente.titulo_profesional),
            ("Especialidad", docente.especialidad),
            ("Cursos asignados", materias),
        ]
        self._llenar_detalle(ventana, datos)

    def _mostrar_detalle_administrador(self, admin):
        ventana = self._crear_ventana_detalle("Detalle del administrador")
        datos = [
            ("ID", admin.id_usuario),
            ("Nombres", admin.nombres + " " + admin.apellidos),
            ("Cedula", admin.cedula),
            ("Correo", admin.correo),
            ("Telefono", admin.telefono),
            ("Cargo", admin.cargo),
            ("Estado", "Activo" if admin.estado else "Inactivo"),
        ]
        self._llenar_detalle(ventana, datos)

    def _mostrar_detalle_curso_seleccionado(self, _event=None):
        seleccion = self.tabla_cursos.selection()
        if not seleccion:
            return

        curso = self.objetos_cursos.get(seleccion[0])
        if curso is not None:
            self._mostrar_detalle_curso(curso)

    def _mostrar_detalle_aula_seleccionada(self, _event=None):
        seleccion = self.tabla_aulas.selection()
        if not seleccion:
            return

        aula = self.objetos_aulas.get(seleccion[0])
        if aula is not None:
            self._mostrar_detalle_aula(aula)

    def _mostrar_detalle_curso(self, curso):
        ventana = self._crear_ventana_detalle("Detalle del curso")
        horario = curso.horario
        aula = curso.aula
        docente = curso.docente.nombres + " " + curso.docente.apellidos
        estudiantes = ", ".join([est.nombres + " " + est.apellidos for est in curso.lista_estudiantes])
        if not estudiantes:
            estudiantes = "Sin estudiantes inscritos"

        datos = [
            ("Codigo", curso.codigo),
            ("Nombre", curso.nombre),
            ("Nivel", curso.nivel),
            ("Paralelo", curso.paralelo),
            ("Cupo", str(curso.cupo_actual) + "/" + str(curso.cupo_maximo)),
            ("Estado", "Abierto" if curso.estado else "Cerrado"),
            ("Docente", docente),
            ("Aula", aula.nombre + " - " + aula.edificio),
            ("Horario", horario.dia + " de " + horario.hora_inicio + " a " + horario.hora_fin),
            ("Modalidad", horario.modalidad),
            ("Grupo", horario.grupo),
            ("Estudiantes", estudiantes),
        ]
        self._llenar_detalle(ventana, datos)

    def _mostrar_detalle_aula(self, aula):
        ventana = self._crear_ventana_detalle("Detalle del aula")
        datos = [
            ("Codigo", aula.codigo),
            ("Nombre", aula.nombre),
            ("Capacidad", aula.capacidad),
            ("Piso", aula.piso),
            ("Edificio", aula.edificio),
            ("Estado", "Disponible" if aula.estado else "No disponible"),
        ]
        self._llenar_detalle(ventana, datos)

    def _mostrar_detalle_carga_seleccionada(self, _event=None):
        seleccion = self.tabla_cargas.selection()
        if not seleccion:
            return

        carga = self.objetos_cargas.get(seleccion[0])
        if carga is not None:
            self._mostrar_detalle_carga(carga)

    def _mostrar_detalle_carga(self, carga):
        ventana = self._crear_ventana_detalle("Detalle de carga academica")
        estudiante = carga.estudiante.nombres + " " + carga.estudiante.apellidos
        datos = [
            ("ID", carga.id_carga),
            ("Estudiante", estudiante),
            ("Cedula", carga.estudiante.cedula),
            ("Periodo", carga.periodo),
            ("Asignaturas", carga.total_asignaturas),
            ("Creditos", carga.total_creditos),
            ("Estado", "Activa" if carga.estado else "Inactiva"),
        ]
        self._llenar_detalle(ventana, datos)

    def _mostrar_reporte_seleccionado(self, _event=None):
        seleccion = self.tabla_reportes.selection()
        if not seleccion:
            return

        reporte = self.objetos_reportes.get(seleccion[0])
        if reporte is not None:
            self.reporte_activo_id = reporte.id_reporte
            self._renderizar_reporte(reporte)

    def _renderizar_reporte(self, reporte):
        self.salida_reporte.configure(state="normal")
        self.salida_reporte.delete("1.0", "end")

        if reporte is None:
            self.salida_reporte.insert("end", "Seleccione un reporte para ver su detalle.")
        else:
            self.salida_reporte.insert("end", "Reporte: " + reporte.tipo_reporte + "\n")
            self.salida_reporte.insert("end", "Fecha de generacion: " + reporte.fecha_generacion + "\n")
            self.salida_reporte.insert("end", "Periodo: " + reporte.periodo + "\n")
            self.salida_reporte.insert("end", "Descripcion: " + reporte.descripcion + "\n")
            self.salida_reporte.insert("end", "Formato: " + reporte.formato)

        self.salida_reporte.configure(state="disabled")

    def _crear_ventana_detalle(self, titulo):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("460x360")
        ventana.minsize(420, 300)
        ventana.configure(bg="#f4f6f8")
        return ventana

    def _llenar_detalle(self, ventana, datos):
        contenedor = ttk.Frame(ventana, padding=16, style="Form.TFrame")
        contenedor.pack(fill="both", expand=True)

        for fila, (etiqueta, valor) in enumerate(datos):
            ttk.Label(contenedor, text=etiqueta + ":", style="Panel.TLabel").grid(row=fila, column=0, sticky="nw", padx=(0, 10), pady=4)
            ttk.Label(contenedor, text=str(valor), style="Panel.TLabel", wraplength=300).grid(row=fila, column=1, sticky="nw", pady=4)

        contenedor.columnconfigure(1, weight=1)

    def _actualizar_cargas(self):
        self._vaciar_tabla(self.tabla_cargas)
        self.objetos_cargas = {}
        for carga in self.sistema.cargas_academicas:
            estudiante = carga.estudiante.nombres + " " + carga.estudiante.apellidos
            item = self.tabla_cargas.insert(
                "",
                "end",
                values=(
                    carga.id_carga,
                    estudiante,
                    carga.periodo,
                    carga.total_asignaturas,
                    carga.total_creditos,
                    "Activa" if carga.estado else "Inactiva",
                ),
            )
            self.objetos_cargas[item] = carga

    def _actualizar_reportes(self):
        self._vaciar_tabla(self.tabla_reportes)
        self.objetos_reportes = {}
        item_activo = None

        for reporte in self.sistema.reportes:
            item = self.tabla_reportes.insert("", "end", values=(reporte.id_reporte, reporte.tipo_reporte, reporte.fecha_generacion, reporte.periodo, reporte.formato))
            self.objetos_reportes[item] = reporte
            if reporte.id_reporte == self.reporte_activo_id:
                item_activo = item

        if item_activo is not None:
            self.tabla_reportes.selection_set(item_activo)
            self.tabla_reportes.focus(item_activo)
            self.tabla_reportes.see(item_activo)
            self._renderizar_reporte(self.objetos_reportes[item_activo])
        elif self.reporte_activo_id is not None:
            self.reporte_activo_id = None
            self._renderizar_reporte(None)

    def _actualizar_combos(self):
        self._llenar_combo(self.combo_docente, self.sistema.listar_docentes())
        self._llenar_combo(self.combo_estudiante, self.sistema.listar_estudiantes())
        self._llenar_combo(self.combo_estudiante_carga, self.sistema.listar_estudiantes())
        self._llenar_combo(self.combo_aula, self.sistema.aulas)
        self._llenar_combo(self.combo_curso, self.sistema.cursos)
        self._llenar_combo_texto(self.combo_periodo_reporte, self.sistema.listar_periodos())

    def _llenar_combo(self, combo, objetos):
        combo.objetos = objetos
        combo["values"] = [self._texto_objeto(objeto) for objeto in objetos]
        if objetos and not combo.get():
            combo.current(0)
        if not objetos:
            combo.set("")

    def _llenar_combo_texto(self, combo, valores):
        combo["values"] = valores
        if valores and not combo.get():
            combo.current(0)
        if not valores:
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
