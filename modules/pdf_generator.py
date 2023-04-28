from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Flowable, KeepTogether, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm


def create_pdf(cotizaciones):
 # Datos de la empresa
    nombre_empresa = "INDUSTRIAL SHOP METALIC"
    rfc_empresa = "RFC: ISM210913-PS5"
    direccion_empresa = "RIO ATOYAC #2477, GONZALEZ ORTEGA, MEXICALI BAJA CALIFORNIA"
    telefono_empresa = "TELS. (686) 562-6369, 561-24-36, CEL. (686) 223-21-70"


    doc = SimpleDocTemplate("cotizacion.pdf", 
                            pagesize=letter,
                            leftMargin=10 * mm,  # Margen izquierdo de 20 mm
                            rightMargin=10 * mm,  # Margen derecho de 20 mm
                            topMargin=10 * mm,  # Margen superior de 20 mm
                            bottomMargin=20 * mm,  # Margen inferior de 20 mm
                            )
    
    logo_path = "./static/img/logoEmpresa.png"
    logo = Image(logo_path, width=100, height=92)  # Ajusta width y height según las dimensiones deseadas

    styles = getSampleStyleSheet() 
    header_style = styles['Heading1'] # Estilo de encabezado
    header_style.alignment = 1 # Center

    # Define un estilo personalizado para el párrafo con un espacio entre líneas mínimo
    minimal_leading_style = ParagraphStyle(
        name="MinimalLeading",
        fontSize=10,
        leading=11,  # Este valor define el espacio entre líneas, ajústalo según tus necesidades
        alignment=1,  # Alineación centrada
    )



    nombre_empresa = Paragraph(nombre_empresa, style=minimal_leading_style)
    rfc_empresa = Paragraph(rfc_empresa, style=minimal_leading_style)
    direccion_empresa = Paragraph(direccion_empresa, style=minimal_leading_style)
    telefono_empresa = Paragraph(telefono_empresa, style=minimal_leading_style)

        # Crea una tabla para organizar el logo y los datos de la empresa
    company_info_table = Table([
    [logo, '', [[nombre_empresa], [rfc_empresa], [direccion_empresa], [telefono_empresa]], '', logo]
    ], colWidths=[100, 5, 360, 5, 100])  # Ajusta el tamaño de las columnas de espacio si es necesario

    # Establece el estilo de la tabla
    company_info_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alineación vertical en la parte superior
    ('VALIGN', (1, 0), (1, 0), 'TOP'),  # Alineación vertical en la parte superior de la tabla anidada
    # ('GRID', (0, 0), (-1, -1), 1, colors.black) # Agrega bordes a la tabla
        ]))


    id_cliente = cotizaciones[0]['id_cliente']
    nombre_cliente = cotizaciones[0]['nombre_cliente']
    direccion_cliente = cotizaciones[0]['direccion_cliente']
    fecha = cotizaciones[0]['fecha']
    id_presupuesto = cotizaciones[0]['id_presupuesto']
    materiales = cotizaciones[0]['materiales']
    mano_obra = cotizaciones[0]['mano_obra']
    subtotal = cotizaciones[0]['subtotal']
    iva = cotizaciones[0]['iva']
    total = cotizaciones[0]['total'] 


    data_header = [
        ["Cliente:", nombre_cliente,"", "Presupuesto #:"],
        ["Fecha:", fecha.strftime('%d-%m-%Y'), "", str(id_presupuesto)],
        ["Direccion:", direccion_cliente, "", ""],
        ["Atencion:", "", "", ""],
    ]
    header_table = Table(data_header, colWidths=[60, 280,130, 100]) # Ajusta el tamaño de las columnas de espacio si es necesario

    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'), # Alineación a la izquierda
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), # Fuente negrita
        ('FONTSIZE', (0, 0), (-1, -1), 10), # Tamaño de fuente
        # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # ('ALIGN', (0, 0), (-1, -1), 'LEFT'), # Alineación a la izquierda
    ]))

    data = [["Part", "Descripcion", "Cant", "Precio", "Importe"]] # Encabezados de la tabla

    for cotizacion in cotizaciones:
        if 'partida' in cotizacion and cotizacion['partida'] is not None and 'descripcion' in cotizacion and cotizacion['descripcion'] is not None and cotizacion['descripcion'].strip() != "":
            descripcion = Paragraph(
            cotizacion['descripcion'], styles['Normal'])
            data.append([cotizacion['partida'], descripcion, # type: ignore
            cotizacion['cantidad'], 
            "$ {:,.2f}".format(cotizacion["precio"]), "$ {:,.2f}".format(cotizacion["importe"])])

    table = Table(data, colWidths=[30, 380, 40, 60, 60]) # Ajusta el tamaño de las columnas de espacio si es necesario

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.red),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    data_totals = [
                ["MATERIALES","$ {:,.2f}".format(materiales),"","","", "SUBTOTAL", "$ {:,.2f}".format(subtotal)],
                ["MANO DE OBRA","$ {:,.2f}".format(mano_obra),"","","", "IVA", "$ {:,.2f}".format(iva)],
                ["","","","","", "TOTAL", "$ {:,.2f}".format(total)]
            ]
    cols_data_totals = Table(data_totals, colWidths=[100,30,100, 50, 100]) # Ajusta el tamaño de las columnas de espacio si es necesario

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

    flowables = [company_info_table, spacer] # Agregar la tabla de información de la empresa
    flowables.append(header_table) # Agregar la tabla de encabezado
    flowables.append(spacer) # Agregar un espacio
    flowables.append(KeepTogether(table)) # Agregar la tabla de cotizaciones

    # Calcular la altura de las tablas
    header_table_width, header_table_height = header_table.wrap(doc.width, doc.height)
    table_width, table_height = table.wrap(doc.width, doc.height)
    table_totals_width, table_totals_height = table_totals.wrap(doc.width, doc.height)

    # Calcular espacio disponible en la página actual
    remaining_space = doc.height - (header_table_height + spacer.height + table_height) - 75
    spacer_height = remaining_space - table_totals_height - 60 
    totals_spacer = Spacer(-1, spacer_height) 

    flowables.append(totals_spacer) 
    # flowables.append(table_totals)
    flowables.append(cols_data_totals)


    doc.build(flowables) # Construir el documento

    with open("cotizacion.pdf", "rb") as f:
        pdf_data = f.read()

    return pdf_data