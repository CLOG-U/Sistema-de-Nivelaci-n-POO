# Tareas — Fase 2: SQL + Login + Branding ULEAM

Sistema de Nivelacion Academica ULEAM | POO + Streamlit

**Ultima actualizacion:** julio 2026  
**Comando local:** `streamlit run interfaz/app.py`  
**Base de datos:** SQL Server `PROYECTOPOO`

> Documento de trabajo para el equipo. Ejecutar tareas en orden de dependencias.

---

## Reglas del proyecto

1. **No modificar** `interfaz/vistas/*` ni `interfaz/navigation.py` salvo bug critico.
2. **Persistencia:** solo SQL Server; no usar `cargar_datos_demo()` en runtime.
3. **Login:** rol derivado del tipo POO (`Administrador` / `Docente` / `Estudiante`), no elegido manualmente.
4. **Contrato de sesion:** mantener `rol_actual`, `usuario_actual_id`, `obtener_usuario_actual(sistema)`.
5. **Commits:** solo cuando el responsable lo pida; mensajes en espanol, sin trailers de Cursor.

---

## Setup SQL (obligatorio antes de probar)

1. Instalar SQL Server y ODBC Driver 17.
2. Ejecutar [`POOPROYECTO.sql`](../POOPROYECTO.sql) (crea BD, tablas y datos iniciales).
3. Copiar [`.streamlit/secrets.toml.example`](../.streamlit/secrets.toml.example) a `.streamlit/secrets.toml`:

```toml
[database]
server = "localhost"
database = "PROYECTOPOO"
driver = "ODBC Driver 17 for SQL Server"
# username = "sa"
# password = "su_contrasena"
```

4. Verificar conexion en **Acerca del Sistema** dentro de la app.

### Credenciales de prueba (incluidas en POOPROYECTO.sql)

| Rol | Cedula | Correo | Contrasena |
|-----|--------|--------|------------|
| Administrador | 1300004444 | cortiz@uleam.edu.ec | adm123 |
| Docente | 1300001111 | perez123@uleam.edu.ec | doc123 |
| Estudiante | 1300002222 | mcastro@uleam.edu.ec | est123 |
| Estudiante | 1300003333 | bchiquito@uleam.edu.ec | est456 |

---

## Resumen de tareas

| ID | Titulo | Prioridad | Depende de | Estado |
|----|--------|-----------|------------|--------|
| SQL-01 | Corregir script POOPROYECTO.sql | Alta | — | Completado |
| SQL-02 | Ampliar relaciones Matricula/Calificacion/Asistencia | Alta | SQL-01 | Completado |
| SQL-03 | Estrategia de IDs (MAX+1 / seed explicito) | Media | SQL-01 | Completado |
| SQL-04 | Datos iniciales en POOPROYECTO.sql | Alta | SQL-02 | Completado |
| SQL-05 | Documentar setup SQL | Media | SQL-04 | Completado |
| BD-01 | Helpers en BaseD.py | Alta | SQL-04 | Completado |
| BD-02 | Repositorio de lectura (PersistenciaSQL.cargar) | Alta | BD-01 | Completado |
| BD-03 | cargar_desde_db() en SistemaNivelacion | Alta | BD-02 | Completado |
| BD-04 | Persistencia INSERT usuarios/aulas/horarios/cursos | Alta | BD-03 | Completado |
| BD-05 | Persistencia periodos, matriculas, calificaciones | Alta | BD-04 | Completado |
| BD-06 | Persistencia asistencias, cargas, reportes | Alta | BD-05 | Completado |
| BD-07 | Persistencia UPDATE (usuario, periodo, curso) | Alta | BD-04 | Completado |
| BD-08 | state.py carga solo desde BD | Alta | BD-03 | Completado |
| AUTH-01 | Formulario pantalla_login | Alta | BD-03 | Completado |
| AUTH-02 | autenticar_usuario + rol desde POO | Alta | AUTH-01 | Completado |
| AUTH-03 | Ajustes app.py (sin selector demo) | Alta | AUTH-02 | Completado |
| AUTH-04 | cerrar_sesion resetea nav_seleccion | Media | AUTH-02 | Completado |
| AUTH-05 | buscar_usuario_por_identificador | Media | BD-03 | Completado |
| AUTH-OPT | Hash de contrasenas (bcrypt) | Baja | AUTH-02 | Pendiente |
| BRAND-01 | Carpeta interfaz/assets/ + logos | Media | — | Completado |
| BRAND-02 | branding.py con mostrar_logo | Media | BRAND-01 | Completado |
| BRAND-03 | Logo en sidebar y login | Media | BRAND-02 | Completado |
| BRAND-04 | CSS login en styles.py | Baja | BRAND-03 | Completado |
| BRAND-05 | Verificar responsive / reemplazar SVG por PNG oficial | Baja | BRAND-03 | Pendiente |
| QA-01 | Checklist manual por rol | Alta | AUTH-03, BD-08 | Pendiente |
| QA-02 | Verificar Acerca + contadores BD | Media | BD-08 | Pendiente |
| DOC-01 | Actualizar contexto_proyecto.md | Media | QA-01 | Completado |
| DOC-02 | Setup SQL en este archivo | Media | SQL-05 | Completado |

---

## Detalle por tarea

### SQL-01 — Corregir script POOPROYECTO.sql
- **Prioridad:** Alta
- **Archivos:** `POOPROYECTO.sql`
- **Criterios:**
  - [x] Sin error `CREATE CREATE TABLE`
  - [x] `USE PROYECTOPOO` y `GO`
  - [x] Drop ordenado de tablas existentes
- **Estado:** Completado

### SQL-02 — Ampliar relaciones
- **Prioridad:** Alta
- **Depende de:** SQL-01
- **Archivos:** `POOPROYECTO.sql`
- **Criterios:**
  - [x] `Matricula` con `id_estudiante`, `id_curso`
  - [x] `Calificacion` y `Asistencia` con FK a estudiante, curso, docente
  - [x] `Estudiante.estado_nivelacion` agregado
- **Estado:** Completado

### SQL-03 — Estrategia de IDs
- **Prioridad:** Media
- **Depende de:** SQL-01
- **Criterios:**
  - [x] Seed con IDs explicitos 1..N
  - [x] Inserts nuevos usan `MAX(id)+1` via `ConexionDB.siguiente_id()`
- **Estado:** Completado

### SQL-04 — Datos iniciales
- **Prioridad:** Alta
- **Depende de:** SQL-02
- **Archivos:** `POOPROYECTO.sql`
- **Criterios:**
  - [x] 4 usuarios (admin, docente, 2 estudiantes)
  - [x] Periodos 2026-1 / 2026-2
  - [x] Curso POO-001, matriculas, notas, asistencias, carga, reporte
- **Estado:** Completado

### SQL-05 — Documentacion setup
- **Prioridad:** Media
- **Criterios:**
  - [x] Instrucciones en este archivo
  - [x] Referencia a secrets.toml.example
- **Estado:** Completado

### BD-01 — Helpers BaseD
- **Prioridad:** Alta
- **Archivos:** `servicios/BaseD.py`
- **Criterios:**
  - [x] `ejecutar()`, `consultar_uno()`, `consultar_todos()`
  - [x] `siguiente_id()`, context manager
- **Estado:** Completado

### BD-02 — Repositorio lectura
- **Prioridad:** Alta
- **Archivos:** `servicios/repositorios/persistencia.py`
- **Criterios:**
  - [x] Carga periodos, usuarios+subtipos, aulas, horarios, cursos
  - [x] Reconstruye `lista_estudiantes` desde matriculas
  - [x] Carga calificaciones, asistencias, cargas, reportes
- **Estado:** Completado

### BD-03 — cargar_desde_db()
- **Prioridad:** Alta
- **Archivos:** `servicios/sistema_nivelacion.py`
- **Criterios:**
  - [x] Retorna `(ok, mensaje)`
  - [x] Activa flag `_db_activa` para escrituras
- **Estado:** Completado

### BD-04 a BD-07 — Persistencia escritura
- **Prioridad:** Alta
- **Archivos:** `servicios/repositorios/persistencia.py`, `servicios/sistema_nivelacion.py`
- **Criterios:**
  - [x] INSERT tras cada `registrar_*`
  - [x] UPDATE tras `actualizar_usuario`, abrir/cerrar periodo, gestionar usuario/curso
- **Estado:** Completado

### BD-08 — state.py solo BD
- **Prioridad:** Alta
- **Archivos:** `interfaz/state.py`, `interfaz/app.py`
- **Criterios:**
  - [x] No invoca `cargar_datos_demo()` al iniciar
  - [x] Muestra error claro si BD no conecta
- **Estado:** Completado

### AUTH-01 — pantalla_login
- **Prioridad:** Alta
- **Archivos:** `interfaz/auth.py`
- **Criterios:**
  - [x] Campos cedula/correo + contrasena
  - [x] Mensajes de error claros
- **Estado:** Completado

### AUTH-02 — autenticar_usuario
- **Prioridad:** Alta
- **Depende de:** BD-03, AUTH-01
- **Archivos:** `interfaz/auth.py`, `servicios/sistema_nivelacion.py`
- **Criterios:**
  - [x] Usa `iniciar_sesion()` del modelo POO
  - [x] Rol derivado con `isinstance`
  - [x] Vistas sin cambios
- **Estado:** Completado

### AUTH-03 — Ajustes app.py
- **Prioridad:** Alta
- **Archivos:** `interfaz/app.py`
- **Criterios:**
  - [x] Login en lugar de selector de rol
  - [x] Eliminado selector "Usuario demo"
  - [x] Boton "Cerrar sesion"
- **Estado:** Completado

### AUTH-04 — cerrar_sesion completo
- **Prioridad:** Media
- **Criterios:**
  - [x] Resetea `nav_seleccion`
- **Estado:** Completado

### AUTH-05 — buscar_usuario_por_identificador
- **Prioridad:** Media
- **Criterios:**
  - [x] Busqueda por cedula o correo
- **Estado:** Completado

### AUTH-OPT — Hash contrasenas (opcional)
- **Prioridad:** Baja
- **Criterios:**
  - [ ] bcrypt en registro y login
  - [ ] Migracion de seed existente
- **Estado:** Pendiente

### BRAND-01 a BRAND-04 — Logos ULEAM
- **Archivos:** `interfaz/assets/`, `interfaz/branding.py`, `interfaz/styles.py`
- **Criterios:**
  - [x] Assets SVG placeholder (reemplazar por PNG oficial ULEAM)
  - [x] Logo en sidebar y pantalla login
  - [x] Colores institucionales #CE1126 / #009639
- **Estado:** Completado (BRAND-05 pendiente: PNG oficial)

### QA-01 — Checklist por rol
- **Prioridad:** Alta
- **Depende de:** AUTH-03, BD-08
- **Criterios:**
  - [ ] Admin: 7 modulos + registrar/consulta + periodos
  - [ ] Docente: notas, asistencia, mis cursos
  - [ ] Estudiante: calificaciones, asistencia, mi perfil
  - [ ] Recargar app tras registrar → datos persisten en BD
- **Estado:** Pendiente (ejecutar manualmente con SQL Server local)

### QA-02 — Acerca del sistema
- **Criterios:**
  - [ ] Estado BD "Conectada"
  - [ ] Contadores coinciden con seed
- **Estado:** Pendiente

---

## Orden de ejecucion (referencia)

```
SQL-01 → SQL-02 → SQL-04 → BD-01 → BD-02 → BD-03
                              ↓
                    BD-04..BD-07 + AUTH-01..05 (paralelo con BRAND)
                              ↓
                         QA-01 → QA-02
```

---

## Checklist cierre fase 2

- [x] POOPROYECTO.sql corregido y ampliado
- [x] POOPROYECTO.sql con schema y datos iniciales
- [x] Capa persistencia SQL (lectura + escritura)
- [x] Login real con autenticacion por rol
- [x] Logos ULEAM en sidebar y login
- [ ] QA manual completada por el equipo
- [ ] Logos PNG oficiales ULEAM (opcional)

---

## Fuera de alcance (fase 3)

- EXT-01: Pestañas en vistas secundarias docente/estudiante
- EXT-02: UI Facultad/Carrera
- EXT-03: CRUD eliminar entidades
- AUTH-OPT: Hash bcrypt
