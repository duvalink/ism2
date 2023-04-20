from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Flowable, KeepTogether, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm


def create_pdf(cotizaciones):
 # Datos de la empresa
    nombre_empresa = "INDUSTRIAL SHOP METALIC"
    rfc_empresa = "ISM210913-PS5"
    direccion_empresa = "RIO ATOYAC #2477, GONZALEZ ORTEGA, MEXICALI BAJA CALIFORNIA"
    telefono_empresa = "TELS. (686) 562-6369, 561-24-36, CEL. (686) 223-21-70"


    doc = SimpleDocTemplate("cotizacion.pdf", 
                            pagesize=letter,
                            leftMargin=20 * mm,  # Margen izquierdo de 20 mm
                            rightMargin=20 * mm,  # Margen derecho de 20 mm
                            topMargin=10 * mm,  # Margen superior de 20 mm
                            bottomMargin=20 * mm,  # Margen inferior de 20 mm
                            )
    styles = getSampleStyleSheet()
    header_style = styles['Heading1']
    header_style.alignment = 1 # Center

    # Define un estilo personalizado para el párrafo con un espacio entre líneas mínimo
    minimal_leading_style = ParagraphStyle(
        name="MinimalLeading",
        fontSize=10,
        leading=1,  # Este valor define el espacio entre líneas, ajústalo según tus necesidades
        alignment=1,  # Alineación centrada
    )

    nombre_empresa = Paragraph(nombre_empresa, style=minimal_leading_style)
    rfc_empresa = Paragraph(rfc_empresa, style=minimal_leading_style)
    direccion_empresa = Paragraph(direccion_empresa, style=minimal_leading_style)
    telefono_empresa = Paragraph(telefono_empresa, style=minimal_leading_style)
    id_cliente = cotizaciones[0]['id_cliente']
    nombre_cliente = cotizaciones[0]['nombre_cliente']
    fecha = cotizaciones[0]['fecha']
    id_presupuesto = cotizaciones[0]['id_presupuesto']
    materiales = cotizaciones[0]['materiales']
    mano_obra = cotizaciones[0]['mano_obra']
    subtotal = cotizaciones[0]['subtotal']
    iva = cotizaciones[0]['iva']
    total = cotizaciones[0]['total']

    data_header = [
        ["Cliente:", nombre_cliente, "Presupuesto #:",
         str(id_presupuesto)],
        ["Fecha:", fecha.strftime('%d-%m-%Y'), "", ""],
    ]
    header_table = Table(data_header, colWidths=[100, 150, 200, 50])

    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'), # Alineación a la izquierda
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), # Fuente negrita
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    data = [["Partida", "Descripcion", "Cantidad", "Precio", "Importe"]]

    for cotizacion in cotizaciones:
        if 'partida' in cotizacion and cotizacion['partida'] is not None and 'descripcion' in cotizacion and cotizacion['descripcion'] is not None and cotizacion['descripcion'].strip() != "":
            descripcion = Paragraph(
                cotizacion['descripcion'], styles['Normal'])
            data.append([cotizacion['partida'], descripcion, cotizacion['cantidad'],
                        "$ {:,.2f}".format(cotizacion["precio"]), "$ {:,.2f}".format(cotizacion["importe"])])

    table = Table(data, colWidths=[50, 200, 100, 80, 60])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 13),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.red),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # data_totals = [["Materiales", "Mano de Obra", "Subtotal", "IVA", "Total"],
    #                [materiales, mano_obra, subtotal, iva, total]]
    data_totals = [
                ["Materiales", "Mano de Obra", "Subtotal", "IVA", "Total"],
                [
                    "$ {:,.2f}".format(materiales),
                    "$ {:,.2f}".format(mano_obra),
                    "$ {:,.2f}".format(subtotal),
                    "$ {:,.2f}".format(iva),
                    "$ {:,.2f}".format(total),
                ],
            ]

    table_totals = Table(data_totals)

    table_totals.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    spacer = Spacer(0, 20)

    flowables = [
        nombre_empresa,
        Spacer(1, 10),
        rfc_empresa,
        Spacer(1, 10),
        direccion_empresa,
        Spacer(1, 10),
        telefono_empresa,
        Spacer(1, 20),
    ]
    flowables.append(header_table)
    flowables.append(spacer)
    flowables.append(KeepTogether(table))

    # Calcular la altura de las tablas
    header_table_width, header_table_height = header_table.wrap(doc.width, doc.height)
    table_width, table_height = table.wrap(doc.width, doc.height)
    table_totals_width, table_totals_height = table_totals.wrap(doc.width, doc.height)

    # Calcular espacio disponible en la página actual
    remaining_space = doc.height - (header_table_height + spacer.height + table_height) - 30  # 20 es el padding
    # Verificar si hay espacio suficiente para la tabla de totales
    # if remaining_space < table_totals_height + 20:
    #     flowables.append(PageBreak())
    #     remaining_space = doc.height

    # Calcular la altura del spacer para mover la tabla de totales a la parte inferior de la página
    spacer_height = remaining_space - table_totals_height - 40  # 20 es el padding
    totals_spacer = Spacer(-1, spacer_height) 

    flowables.append(totals_spacer)
    flowables.append(table_totals)

    doc.build(flowables)

    with open("cotizacion.pdf", "rb") as f:
        pdf_data = f.read()

    return pdf_data