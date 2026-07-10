"""Generacion de archivos PDF y Excel para reportes academicos."""

import re
from dataclasses import dataclass
from io import BytesIO

from interfaz.components.tables import (
    asistencia_registro_to_dict,
    calificacion_registro_to_dict,
    carga_to_dict,
)


@dataclass
class ArchivoExportado:
    contenido: bytes
    nombre: str
    mime: str


def _slug(texto: str) -> str:
    limpio = re.sub(r"[^\w\s-]", "", texto, flags=re.UNICODE)
    limpio = re.sub(r"[\s_-]+", "_", limpio.strip())
    return limpio.lower() or "reporte"


def nombre_archivo_reporte(tipo: str, periodo: str, extension: str) -> str:
    return f"reporte_{_slug(tipo)}_{_slug(periodo)}.{extension}"


def obtener_filas_reporte(sistema, tipo_reporte: str, periodo: str) -> list[dict]:
    if tipo_reporte == "Asistencia":
        return [
            asistencia_registro_to_dict(registro)
            for registro in sistema.asistencias.values()
            if registro["periodo"] == periodo
        ]

    if tipo_reporte == "Calificaciones":
        return [
            calificacion_registro_to_dict(registro)
            for registro in sistema.calificaciones.values()
            if registro["periodo"] == periodo
        ]

    if tipo_reporte == "Inscripciones":
        filas = []
        for curso in sistema.cursos.values():
            for estudiante in curso.lista_estudiantes:
                matricula = estudiante.matricula
                if not matricula or matricula.periodo != periodo:
                    continue
                filas.append(
                    {
                        "Estudiante": f"{estudiante.nombres} {estudiante.apellidos}",
                        "Cedula": estudiante.cedula,
                        "Curso": curso.codigo,
                        "Nombre curso": curso.nombre,
                        "Periodo": matricula.periodo,
                        "Tipo matricula": matricula.tipo_matricula,
                        "Fecha": matricula.fecha_matricula,
                        "Estado": matricula.estado,
                    }
                )
        return filas

    if tipo_reporte == "Carga academica":
        return [
            carga_to_dict(carga)
            for carga in sistema.cargas_academicas.values()
            if carga.periodo == periodo
        ]

    if tipo_reporte == "General":
        resumen = sistema.resumen()
        return [
            {"Indicador": "Usuarios", "Valor": resumen.get("usuarios", 0)},
            {"Indicador": "Docentes", "Valor": resumen.get("docentes", 0)},
            {"Indicador": "Estudiantes", "Valor": resumen.get("estudiantes", 0)},
            {"Indicador": "Cursos", "Valor": resumen.get("cursos", 0)},
            {"Indicador": "Aulas", "Valor": resumen.get("aulas", 0)},
            {"Indicador": "Inscripciones", "Valor": sistema.total_inscripciones()},
            {"Indicador": "Calificaciones", "Valor": resumen.get("calificaciones", 0)},
            {"Indicador": "Asistencias", "Valor": resumen.get("asistencias", 0)},
            {"Indicador": "Cargas academicas", "Valor": resumen.get("cargas", 0)},
            {"Indicador": "Matriculas", "Valor": resumen.get("matriculas", 0)},
            {"Indicador": "Periodo", "Valor": periodo},
        ]

    return []


def generar_excel(datos: dict) -> bytes:
    from openpyxl import Workbook
    from openpyxl.styles import Font

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"

    titulo = Font(bold=True, size=12)
    ws["A1"] = "Sistema de Nivelacion Academica - ULEAM"
    ws["A1"].font = titulo
    ws["A2"] = f"Tipo: {datos.get('tipo', '')}"
    ws["A3"] = f"Periodo: {datos.get('periodo', '')}"
    ws["A4"] = f"Fecha: {datos.get('fecha', '')}"
    ws["A5"] = f"Descripcion: {datos.get('descripcion', '')}"

    filas = datos.get("filas") or []
    inicio = 7
    if not filas:
        ws[f"A{inicio}"] = "Sin registros para el periodo seleccionado."
    else:
        encabezados = list(filas[0].keys())
        for col, encabezado in enumerate(encabezados, start=1):
            celda = ws.cell(row=inicio, column=col, value=encabezado)
            celda.font = Font(bold=True)
        for offset, fila in enumerate(filas, start=1):
            for col, encabezado in enumerate(encabezados, start=1):
                ws.cell(row=inicio + offset, column=col, value=fila.get(encabezado, ""))

    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


def _html_tabla(filas: list[dict]) -> str:
    if not filas:
        return "<p>Sin registros para el periodo seleccionado.</p>"

    encabezados = list(filas[0].keys())
    thead = "".join(f"<th>{encabezado}</th>" for encabezado in encabezados)
    cuerpo = []
    for fila in filas:
        celdas = "".join(f"<td>{fila.get(encabezado, '')}</td>" for encabezado in encabezados)
        cuerpo.append(f"<tr>{celdas}</tr>")
    return f"<table border='1'><thead><tr>{thead}</tr></thead><tbody>{''.join(cuerpo)}</tbody></table>"


def generar_pdf(datos: dict) -> bytes:
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Sistema de Nivelacion Academica - ULEAM", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, f"Tipo de reporte: {datos.get('tipo', '')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Periodo: {datos.get('periodo', '')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Fecha: {datos.get('fecha', '')}", new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(0, 8, f"Descripcion: {datos.get('descripcion', '')}")
    pdf.ln(4)

    html = _html_tabla(datos.get("filas") or [])
    pdf.write_html(html)

    # FPDF.output() devuelve bytes cuando dest='S' (string/bytes mode)
    salida = pdf.output()
    if isinstance(salida, str):
        return salida.encode("latin-1", errors="replace")
    return bytes(salida)


def exportar_reporte(datos: dict, formato: str) -> ArchivoExportado:
    if formato == "Excel":
        contenido = generar_excel(datos)
        return ArchivoExportado(
            contenido=contenido,
            nombre=nombre_archivo_reporte(datos.get("tipo", "reporte"), datos.get("periodo", ""), "xlsx"),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    contenido = generar_pdf(datos)
    return ArchivoExportado(
        contenido=contenido,
        nombre=nombre_archivo_reporte(datos.get("tipo", "reporte"), datos.get("periodo", ""), "pdf"),
        mime="application/pdf",
    )


def construir_datos_exportacion(reporte, filas: list[dict]) -> dict:
    return {
        "tipo": reporte.tipo_reporte,
        "periodo": reporte.periodo,
        "descripcion": reporte.descripcion,
        "fecha": reporte.fecha_generacion,
        "filas": filas,
    }
