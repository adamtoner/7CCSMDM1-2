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
addParagraph( f'There are { prt1.no_sentiments } possible sentiments that a tweet may have.' )
addParagraph( f'The second most popular tweet sentiment is { prt1.sec_sentiment }.' )
addParagraph( f'The day with the most extremely positive tweets was { prt1.mc_date }.')

addSubtitle( '1.2' )
# Print the number of words in the corpus
addParagraph( f'\nWith stop words, there are { len( prt1.corpus ) } words total, { len( prt1.corpus.unique() ) } of which are unique.' )
addParagraph( f'The ten most frequently used words are: { ", ".join(prt1.corpus.value_counts()[:10].index.tolist()) }')

# Remove the stop words from the corpus
addParagraph( f'\nWithout stop words, there are { len( prt1.nscorpus ) } words total, { len( prt1.nscorpus.unique() ) } of which are unique.' )
addParagraph( f'The ten most frequently used (non-stop) words are: { ", ".join( prt1.nscorpus.value_counts()[:10].index.tolist()) }')

addParagraph( f'It is clear that there is a large part of the corpus that consists of stop words, relatively few of which are unique.' )

addSubtitle( '1.3' )
addParagraph( 'This is a graph showing the frequency of the words in the corpus, including the stop words.' )
doc.append( Image( 'output/plot.png', width=120*mm, height=90*mm ))

addParagraph( f'It is clear that very few of the words make up a large proportion of the corpus. It is worth noting that the graph shown here do not show how many messages the words appear in, instead it shows the frequency of each word. This can be used to infer the size of the term-document matrix as it allows us to see the relative frequencies of the words, showing that a lot of the words appear a low number of times and so most of the term-document matrix will be mostly empty values. The dense term-document matrix would have one row for each tweet and one column for each non-stop word. Therefore the term-document matrix would have { len( prt1.nscorpus.unique() )} columns and { len( prt1.tdf ) }' )

addSubtitle( '1.4' )

addParagraph( f'The error rate of the classifier is { prt1.classifier_error }%.' )

addParagraph( f'\nThe total runtime for section 1 was { prt1.runtime } seconds.')

################################################ Section 2
addTitle( '2 - Image Processing' )
addSubtitle( '2.1' )
addParagraph( f'The size of avengers_imdb.jpg is { prt2.im_ave.shape[0:2] }. \n\n Here are the altered images:' )
doc.append( Image( 'output/avengers_imdb_grayscale.png', width=120*mm, height=90*mm ))
doc.append( Image( 'output/avengers_imdb_bw.png', width=120*mm, height=90*mm ))

addSubtitle( '2.2' )
addParagraph( f'bush_house_wikipedia.jpg with gaussian noise:' )
doc.append( Image( 'output/im_bhw_noise.png', width=120*mm, height=90*mm ))

addParagraph( f'bush_house_wikipedia.jpg with gaussian blue:' )
doc.append( Image( 'output/im_bhw_gfilter.png', width=120*mm, height=90*mm ))
addParagraph( f'bush_house_wikipedia.jpg with universal smoothing:' )
doc.append( Image( 'output/im_bhw_ufilter.png', width=120*mm, height=90*mm ))
addParagraph( f'bush_house_wikipedia.jpg with gaussian blur and universal smoothing:' )
doc.append( Image( 'output/im_bhw_bfilter.png', width=120*mm, height=90*mm ))

addSubtitle( '2.3' )
addParagraph( f'forestry_commission_gov_)uk.jpg split into 5 segments with k-mean segmentation:' )
doc.append( Image( 'output/im_fcg_seg.png', width=120*mm, height=90*mm ))

addSubtitle( '2.4' )
addParagraph( f'rolland_garros_tv5monde.jpg with Canny Edge Detection:' )
doc.append( Image( 'output/im_rgt_canny.png', width=120*mm, height=90*mm ))

addParagraph( f'rolland_garros_tv5monde.jpg with Hough Transform:' )
doc.append( Image( 'output/im_rgt_hough.png', width=120*mm, height=90*mm ))

addSpacer()
addCentredText('Thank you for taking the time to read my project.')

SimpleDocTemplate( 'report.pdf', pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm, title='7CCSMDM1 CW 1 - 1786775' ).build( doc )