import os
import csv
import sys

# Define transactions for mock data
TRANSACTIONS_JAN = [
    {"Date": "2026-01-01", "Description": "TechCorp Salary", "Category": "Income", "Amount": 5000.00},
    {"Date": "2026-01-02", "Description": "Apex Properties Rent", "Category": "Rent", "Amount": -1500.00},
    {"Date": "2026-01-03", "Description": "Whole Foods Market", "Category": "Groceries", "Amount": -120.50},
    {"Date": "2026-01-05", "Description": "Netflix Subscription", "Category": "Entertainment", "Amount": -15.49},
    {"Date": "2026-01-08", "Description": "City Power & Light", "Category": "Utilities", "Amount": -110.20},
    {"Date": "2026-01-10", "Description": "Starbucks Coffee", "Category": "Dining", "Amount": -6.75},
    {"Date": "2026-01-12", "Description": "Amazon.com Purchase", "Category": "Shopping", "Amount": -45.99},
    {"Date": "2026-01-15", "Description": "Freelance Design Client", "Category": "Income", "Amount": 600.00},
    {"Date": "2026-01-18", "Description": "Chipotle Mexican Grill", "Category": "Dining", "Amount": -14.30},
    {"Date": "2026-01-20", "Description": "Trader Joe's", "Category": "Groceries", "Amount": -85.40},
    {"Date": "2026-01-22", "Description": "Spotify Premium", "Category": "Entertainment", "Amount": -10.99},
    {"Date": "2026-01-25", "Description": "Target Stores", "Category": "Shopping", "Amount": -98.50},
    {"Date": "2026-01-28", "Description": "Shell Gas Station", "Category": "Transportation", "Amount": -42.00},
    {"Date": "2026-01-30", "Description": "Olive Garden", "Category": "Dining", "Amount": -75.60}
]

TRANSACTIONS_FEB = [
    {"Date": "2026-02-01", "Description": "TechCorp Salary", "Category": "Income", "Amount": 5000.00},
    {"Date": "2026-02-02", "Description": "Apex Properties Rent", "Category": "Rent", "Amount": -1500.00},
    {"Date": "2026-02-04", "Description": "Whole Foods Market", "Category": "Groceries", "Amount": -135.20},
    {"Date": "2026-02-05", "Description": "Netflix Subscription", "Category": "Entertainment", "Amount": -15.49},
    {"Date": "2026-02-07", "Description": "City Water Utility", "Category": "Utilities", "Amount": -45.50},
    {"Date": "2026-02-09", "Description": "Starbucks Coffee", "Category": "Dining", "Amount": -5.50},
    {"Date": "2026-02-12", "Description": "Best Buy Electronics", "Category": "Shopping", "Amount": -250.00},
    {"Date": "2026-02-14", "Description": "McDonald's", "Category": "Dining", "Amount": -12.80},
    {"Date": "2026-02-18", "Description": "Kroger Grocery", "Category": "Groceries", "Amount": -70.10},
    {"Date": "2026-02-20", "Description": "eBay Sale Payout", "Category": "Income", "Amount": 120.00},
    {"Date": "2026-02-22", "Description": "Spotify Premium", "Category": "Entertainment", "Amount": -10.99},
    {"Date": "2026-02-24", "Description": "Amazon.com Purchase", "Category": "Shopping", "Amount": -89.99},
    {"Date": "2026-02-26", "Description": "Shell Gas Station", "Category": "Transportation", "Amount": -45.50},
    {"Date": "2026-02-28", "Description": "Subway Sandwiches", "Category": "Dining", "Amount": -9.50}
]

TRANSACTIONS_MAR = [
    {"Date": "2026-03-01", "Description": "TechCorp Salary", "Category": "Income", "Amount": 5000.00},
    {"Date": "2026-03-02", "Description": "Apex Properties Rent", "Category": "Rent", "Amount": -1500.00},
    {"Date": "2026-03-03", "Description": "Whole Foods Market", "Category": "Groceries", "Amount": -112.40},
    {"Date": "2026-03-05", "Description": "Netflix Subscription", "Category": "Entertainment", "Amount": -15.49},
    {"Date": "2026-03-08", "Description": "City Power & Light", "Category": "Utilities", "Amount": -95.80},
    {"Date": "2026-03-10", "Description": "Starbucks Coffee", "Category": "Dining", "Amount": -7.25},
    {"Date": "2026-03-12", "Description": "Amazon.com Purchase", "Category": "Shopping", "Amount": -120.50},
    {"Date": "2026-03-15", "Description": "Freelance Design Client", "Category": "Income", "Amount": 850.00},
    {"Date": "2026-03-17", "Description": "Chipotle Mexican Grill", "Category": "Dining", "Amount": -15.80},
    {"Date": "2026-03-19", "Description": "Trader Joe's", "Category": "Groceries", "Amount": -92.10},
    {"Date": "2026-03-22", "Description": "Spotify Premium", "Category": "Entertainment", "Amount": -10.99},
    {"Date": "2026-03-25", "Description": "Target Stores", "Category": "Shopping", "Amount": -145.00},
    {"Date": "2026-03-27", "Description": "Shell Gas Station", "Category": "Transportation", "Amount": -40.00},
    {"Date": "2026-03-29", "Description": "The Cheesecake Factory", "Category": "Dining", "Amount": -88.50}
]

TRANSACTIONS_APR = [
    {"Date": "2026-04-01", "Description": "TechCorp Salary", "Category": "Income", "Amount": 5000.00},
    {"Date": "2026-04-02", "Description": "Apex Properties Rent", "Category": "Rent", "Amount": -1500.00},
    {"Date": "2026-04-04", "Description": "Whole Foods Market", "Category": "Groceries", "Amount": -142.10},
    {"Date": "2026-04-05", "Description": "Netflix Subscription", "Category": "Entertainment", "Amount": -15.49},
    {"Date": "2026-04-07", "Description": "City Comcast Internet", "Category": "Utilities", "Amount": -80.00},
    {"Date": "2026-04-09", "Description": "Starbucks Coffee", "Category": "Dining", "Amount": -6.50},
    {"Date": "2026-04-12", "Description": "Apple Store Purchase", "Category": "Shopping", "Amount": -999.00},
    {"Date": "2026-04-15", "Description": "IRS Tax Refund", "Category": "Income", "Amount": 1200.00},
    {"Date": "2026-04-18", "Description": "Chick-fil-A", "Category": "Dining", "Amount": -13.20},
    {"Date": "2026-04-20", "Description": "Kroger Grocery", "Category": "Groceries", "Amount": -65.30},
    {"Date": "2026-04-22", "Description": "Spotify Premium", "Category": "Entertainment", "Amount": -10.99},
    {"Date": "2026-04-25", "Description": "Amazon.com Purchase", "Category": "Shopping", "Amount": -35.40},
    {"Date": "2026-04-27", "Description": "Shell Gas Station", "Category": "Transportation", "Amount": -48.00},
    {"Date": "2026-04-30", "Description": "Domino's Pizza", "Category": "Dining", "Amount": -24.50}
]

def generate_csv(filepath, transactions):
    """Generate a CSV bank statement."""
    print(f"Generating CSV: {filepath}")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Date", "Description", "Category", "Amount"])
        writer.writeheader()
        for tx in transactions:
            writer.writerow(tx)

def generate_pdf(filepath, transactions, month_name, starting_balance=3500.00):
    """Generate a beautiful PDF bank statement using ReportLab."""
    print(f"Generating PDF: {filepath}")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
    except ImportError:
        print("Error: reportlab is not installed. Please run pip install reportlab first.")
        sys.exit(1)
        
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom colors and styles
    navy = colors.HexColor("#1A365D")
    dark_gray = colors.HexColor("#2D3748")
    light_gray = colors.HexColor("#F7FAFC")
    border_gray = colors.HexColor("#E2E8F0")
    
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        textColor=navy,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=dark_gray,
        spaceAfter=5
    )
    
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=navy,
        spaceBefore=15,
        spaceAfter=10
    )
    
    cell_style = ParagraphStyle(
        "Cell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=dark_gray
    )
    
    cell_style_bold = ParagraphStyle(
        "CellBold",
        parent=cell_style,
        fontName="Helvetica-Bold"
    )

    # Document Header
    story.append(Paragraph("Apex Horizon Bank", title_style))
    story.append(Paragraph("Account Statement", ParagraphStyle("Sub", parent=title_style, fontSize=14, spaceAfter=20)))
    
    # Account Summary Block
    summary_data = [
        [Paragraph("<b>Customer Name:</b> Jane Doe", subtitle_style), Paragraph(f"<b>Statement Period:</b> {month_name} 2026", subtitle_style)],
        [Paragraph("<b>Account Number:</b> 1234-5678-9012", subtitle_style), Paragraph("<b>Account Type:</b> Primary Checking", subtitle_style)]
    ]
    summary_table = Table(summary_data, colWidths=[250, 250])
    summary_table.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Financial Overview Calculation
    deposits = sum(tx["Amount"] for tx in transactions if tx["Amount"] > 0)
    withdrawals = sum(tx["Amount"] for tx in transactions if tx["Amount"] < 0)
    ending_balance = starting_balance + deposits + withdrawals
    
    overview_data = [
        ["Starting Balance", "Total Deposits", "Total Withdrawals", "Ending Balance"],
        [f"${starting_balance:,.2f}", f"${deposits:,.2f}", f"${abs(withdrawals):,.2f}", f"${ending_balance:,.2f}"]
    ]
    overview_table = Table(overview_data, colWidths=[130, 130, 130, 130])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,1), light_gray),
        ('GRID', (0,0), (-1,-1), 0.5, border_gray),
    ]))
    story.append(Paragraph("Account Summary", h2_style))
    story.append(overview_table)
    story.append(Spacer(1, 25))
    
    # Transaction Details Block
    story.append(Paragraph("Transaction History", h2_style))
    
    tx_table_data = [["Date", "Description", "Category", "Amount"]]
    for tx in transactions:
        amt_str = f"${tx['Amount']:,.2f}" if tx['Amount'] >= 0 else f"-${abs(tx['Amount']):,.2f}"
        tx_table_data.append([
            Paragraph(tx["Date"], cell_style),
            Paragraph(tx["Description"], cell_style),
            Paragraph(tx["Category"], cell_style),
            Paragraph(f"<b>{amt_str}</b>" if tx['Amount'] >= 0 else amt_str, cell_style)
        ])
        
    tx_table = Table(tx_table_data, colWidths=[80, 200, 120, 110])
    
    # Set Table Styles (with zebra striping)
    t_style = [
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, border_gray),
    ]
    for i in range(1, len(transactions) + 1):
        bg = colors.white if i % 2 != 0 else light_gray
        t_style.append(('BACKGROUND', (0, i), (-1, i), bg))
        
    tx_table.setStyle(TableStyle(t_style))
    story.append(tx_table)
    
    doc.build(story)
    print(f"Generated PDF successfully at {filepath}")

def main():
    # Store files in data/
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate CSVs
    generate_csv(os.path.join(data_dir, "statement_2026_01.csv"), TRANSACTIONS_JAN)
    generate_csv(os.path.join(data_dir, "statement_2026_02.csv"), TRANSACTIONS_FEB)
    
    # Generate PDFs
    generate_pdf(os.path.join(data_dir, "statement_2026_03.pdf"), TRANSACTIONS_MAR, "March")
    # April starts with the ending balance of March.
    # January ending balance: 3500 + 5600 - 2105.23 = 6994.77
    # Let's just use 5000 as a reasonable starting point
    generate_pdf(os.path.join(data_dir, "statement_2026_04.pdf"), TRANSACTIONS_APR, "April", starting_balance=6000.00)
    
    print("\nAll mock statements generated in the 'data/' folder:")
    for f in os.listdir(data_dir):
        print(f"  - {f}")

if __name__ == "__main__":
    main()
