#--
# main.py
# Builds the report from the results generated in prt1.py and prt2.py
# @author: Adam Toner
# @created: 17 Feb 2021
#
#--

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import HRFlowable, Image, Spacer
from reportlab.platypus.tables import TableStyle, colors
from reportlab.lib.units import mm
import prt1
import prt2

doc = [] # Initialise document list

################################################ STYLES ################################################
# Define the methods and styles for quickly adding common elements
def addTitle( text ): # Section Title
    doc.append( Spacer( 1, 50 ))
    doc.append( Paragraph( text, ParagraphStyle( name='title', fontSize=18, fontName='Times-Roman' )))
    doc.append( Spacer( 1, 20 ))

def addSubtitle( text ): # Subsection Title
    doc.append( Spacer( 1, 10 ))
    doc.append( HRFlowable( width='100%', color=colors.ReportLabFidBlue ))
    doc.append( Spacer( 1, 10 ))
    doc.append( Paragraph( text, ParagraphStyle( name='subtitle', fontSize=15, fontName='Times-Roman' )))
    doc.append( Spacer( 1, 15 ))

def addSubSubtitle( text ): # Subsection Subtitle
    doc.append( Spacer( 1, 10 ))
    doc.append( Paragraph( text, ParagraphStyle( name='subsubtitle', fontSize=13, fontName='Times-Roman' )))
    doc.append( Spacer( 1, 15 ))

def addParagraph( text ): # Normal paragraph of text
    doc.append( Spacer( 1, 5 ))
    for line in text.split( '\n' ):
        doc.append( Paragraph( line, ParagraphStyle( name='paragraph', fontName='Times-Roman' )))
        doc.append( Spacer( 1, 10 ))

def addCentredText( text ): # Centred text used for document title
    doc.append( Spacer( 1, 5 ))
    doc.append( Paragraph( text, ParagraphStyle( name='centred', alignment=TA_CENTER, fontName='Times-Roman' )))
    doc.append( Spacer( 1, 5 ))

def addSpacer( size = 10 ): # Line-break type spacer
    doc.append( Spacer( 1, size ))

# Method for adding tables with options for additional formatting settings
def addTable( data, width=None, height=None, topHeader=False, leftHeader=False, add_style=None ):
    # Create table object
    t = Table ( data, colWidths = width, rowHeights = height, hAlign = TA_CENTER )
    # List default styles
    style = [('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black), ('FACE',(0,0),(-1,-1),'Courier')]
    # Add optional styles for headers at the top or left of the table
    if leftHeader:
        style.append(('BACKGROUND', (0,0), (0,-1), colors.ReportLabFidBlue)) 
        style.append(('TEXTCOLOR', (0,0), (0,-1), colors.white))
        style.append(('FACE', (0,0), (0,-1), 'Courier-Bold'))
    if topHeader:
        style.append(('BACKGROUND', (0,0), (-1,0), colors.ReportLabFidBlue))
        style.append(('TEXTCOLOR', (0,0), (-1,0), colors.white))
        style.append(('FACE', (0,0), (-1,0), 'Courier-Bold'))
    # This is for any additional styles we may want to add. Feed them in as an array and this will add them to the table style when drawn.
    if add_style != None:
        for s in add_style:
            style.append(s)
    t.setStyle( TableStyle( style ))
    # Add the table
    doc.append( t )

################################################ CONTENT ################################################
# Document header
addCentredText( '7CCSMDM1 - Coursework 1' )
addCentredText( 'Adam Toner 1786775' )

################################################ Section 1
addTitle( '1 - Text Mining' )

addSubtitle( '1.1' )

addSubtitle( '1.2' )

addSubtitle( '1.3' )

addSubtitle( '1.4' )

################################################ Section 2
addTitle( '2 - Image Processing' )
addSubtitle( '2.1' )

addSubtitle( '2.2' )


addSubtitle( '2.3' )

addSubtitle( '2.3' )

addSpacer()
addCentredText('Thank you for taking the time to read my project.')

SimpleDocTemplate( 'report.pdf', pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm, title='7CCSMDM1 CW 1 - 1786775' ).build( doc )