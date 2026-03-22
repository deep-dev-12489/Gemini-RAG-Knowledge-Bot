from reportlab.pdfgen import canvas
import os

def create_sample_pdf(filename="sample_knowledge.pdf"):
    # Create the PDF object, using the filename as the path.
    c = canvas.Canvas(filename)
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 750, "Project Zero: Confidential Knowledge Base")
    
    # Body
    c.setFont("Helvetica", 12)
    text = c.beginText(72, 720)
    text.textLines([
        "1. Project Zero was initiated in 2024 to revolutionize data processing.",
        "",
        "2. The core algorithm is called 'Quantum Weave', which speeds up ",
        "   computations by 300% compared to traditional methods.",
        "",
        "3. The project is led by Dr. Aris Thorne and Dr. Elena Rostova.",
        "",
        "4. The secret password to access the mainframe is 'Alpha-Tango-99'.",
        "",
        "5. The project headquarters is located secretly beneath the Swiss Alps.",
        "",
        "This document contains strictly confidential data."
    ])
    c.drawText(text)
    
    # Save the PDF file
    c.save()
    print(f"Successfully created {filename}!")

if __name__ == "__main__":
    create_sample_pdf()
