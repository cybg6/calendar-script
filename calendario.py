from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from calendar import TextCalendar
from datetime import datetime

def create_calendar_pdf(year):
    # Create a PDF canvas
    filename = f"calendar_{year}.pdf"

    day_names_full = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Define page dimensions and margins
    page_width, page_height = landscape(A4)
    x_margin = 12
    y_margin = 13
    calendar_width = page_width - x_margin * 2
    calendar_height = page_height - y_margin * 2
    column_width = calendar_width / 7

    # Define colors
    text_days_names_color = colors.HexColor('#00000080', hasAlpha=True)
    text_days_numbers_color = colors.HexColor('#00000030', hasAlpha=True)
    grid_color = colors.HexColor('#00000060', hasAlpha=True)
    red_60 = colors.HexColor('#ec270d80', hasAlpha=True)
    blue_80 = colors.HexColor('#0d6eece8', hasAlpha=True)

    c = canvas.Canvas(filename, pagesize=landscape(A4))

    # Create a TextCalendar instance for the specified year
    cal = TextCalendar(firstweekday=0)

    # Generate a calendar for each month and add it to the PDF
    for month_n in range(1, 13):
        # Generate the month's calendar
        month_calendar = cal.formatmonth(year, month_n, 1, 1)

        # Create a table to hold the calendar data
        month_name = datetime(year, month_n, 1).strftime('%B')
        data = [[month_name.upper()], day_names_full]

        # Split the calendar into lines
        lines = month_calendar.split('\n')

        # Split the lines into days
        for line in lines[2:]:
            if line.strip() != '':
                data.append(line.split())

        # Add empty strings for days outside the month
        first_week_length = len(data[2])
        for _ in range(7 - first_week_length):
            data[2].insert(0, '')

        # Calculate row heights
        weeks_length = len(data[2:])
        days_number_row_height = (calendar_height - 20 - 20) / weeks_length
        row_heights_list = [20, 20] + [days_number_row_height] * weeks_length

        leading = days_number_row_height + 1
        if weeks_length == 5:
            leading = days_number_row_height - 5
        
        table = Table(data, colWidths=column_width, rowHeights=row_heights_list)

        # Apply styles to the table
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            # ('FONTNAME', (0, 0), (-1, -1), 'Open_Sans'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            # Month
            ('SPAN',(0,0),(-1,0)),
            ('GRID', (0, 0), (-1, 0), 1, blue_80),
            ('BACKGROUND', (0, 0), (-1, 0), blue_80),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            # Days Names
            ('TEXTCOLOR', (0, 1), (-1, 1), text_days_names_color),
            ('FONTSIZE', (0, 0), (-1, 2), 15),
            ('LEADING', (0, 0), (-1, 2), 17),
            # Days Numbers
            ('GRID', (0, 1), (-1, -1), 1, grid_color),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 2), (-1, -1), text_days_numbers_color),
            ('TEXTCOLOR', (-1, 0), (-1, -1), red_60),
            ('FONTSIZE', (0, 2), (-1, -1), 75),
            ('LEADING', (0, 2), (-1, -1), leading ),
        ]))

        # Draw the table on the PDF canvas
        table.wrapOn(c, 10, 10)
        table.drawOn(c, x_margin, y_margin)

        # Add a new page for 20the next month
        if month_n < 12:
            c.showPage()

    # Save the PDF
    c.save()

if __name__ == "__main__":
    year = 2023
    create_calendar_pdf(year)
    print(f"Calendar PDF for {year} created successfully.")