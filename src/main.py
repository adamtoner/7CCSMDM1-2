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
addTitle( '1 - Classification' )

addSubtitle( '1.1 - Data Overview' )
addTable( prt1.section1_table, leftHeader=True )

addSubtitle( '1.2 - Label Encoding' )
addTable( prt1.section2_table, topHeader=True, leftHeader=True )

#addSpacer( 70 )
addSubtitle( '1.3 - Decision Tree With No Missing Values')
addParagraph( 'To build this decision tree I used the Scikit-learn module. The training set and test set were randomly selected from the set of all instances which contain no missing values. The initial decision tree that was created was overfitting the data and so I placed a limit on the fraction of total weights required to be at a leaf node. This imposed limit was a minimum of 0.001 which was found after some trial and error in an attempt to minimise the test error and the resubstitution error. \n The error rate for this decision tree was:' )
addTable( prt1.section3_table, leftHeader=True )
#doc.append( Image( 'output/decision-tree.png', width=180*mm, height=18.5*mm ))
#addParagraph( 'Above is one of the decision trees generated in exactly the same way. It may not be identical to the one for which the error rate is reported as the error rate is generated each time with the report whereas the depiction of the decision tree must be generated separately in the command line. The error rate for the tree above is very likely to be extrememly similar to those listed in the table above.' )
addParagraph( 'I attempted to add an image of the decision tree generated to this report but due to the size of the tree, it was hugely inflating the file size and causing issues when viewing the document with some PDF readers. It was also illegible due to its size and fitting, so I thought it best to omit it from the report. You can however find a copy of the image in the \'output\' folder of the zip file.')

addSubtitle( '1.4 - Handling Missing Values In Decision Trees')
addParagraph( 'In this section the same set of training data was used for each case to get a better comparison of the error rates which arose from the decision trees. All of the instances with missing values and an equal number of instances with no missing values were combined in a list. Another list was created with all remaining instances (I saw no point in wasting any data, so anything which wasn\'t being used for trainig was used for testing). This resulted in 7,240 instances in the training set and 41,602 in the test set. Two copies of the training and test set were made. The two training sets had their missing values dealt with in their respective ways. Each training set, along with a copy of the test set, were converted together to nominal values to ensure the encoded values of the test and training set matched within each method.' )

addSubSubtitle( '1.4.1 - Using a \'missing\' Value' )
addParagraph( 'With this method, the value \'missing\' was created inserted for any instance which had an attribute with a missing value. The error rates were: ')
addTable( prt1.method1_table, leftHeader=True )
addSpacer()
doc.append( Image( 'output/prt1-method1.png', width=180*mm, height = 49.9*mm ))

addSubSubtitle( '1.4.2 - Using the Most Popular Value' )
addParagraph( 'With this method, I checked each column for the most common value. Any missing values were then filled with the most popular value for the given attribute. The error rates were: ')
addSpacer( 15 )
addTable( prt1.method2_table, leftHeader=True )
addSpacer()
doc.append( Image( 'output/prt1-method2.png', width=180*mm, height = 63.7*mm ))

addSubSubtitle( '1.4.3 - Comparing the Methods' )
addParagraph( 'As you can see, the error rates of the two are very similar. I found that small changes to the restrictions which I placed on the weighted sums at the leaf nodes could make one or the other very slightly better, but overall I found no significant difference for this dataset (I have noticed a very slight error rate advantage on average when using the most popular value as opposed \'missing\' but I have not tested this thoroughly and so cannot confirm or deny this). In this case, either method would suffice as the both could get within 0.03 of the test error rate (and an even lower than the resubstitution error rate) of the decision tree in section 1.3 which had no missing values.' )
addParagraph( 'Please note that the decision trees depicted above will not have the exact error rates shown in the tables. The decision trees are regenerated every time the report is generated and the error rates shown above are for the most recently generated decision trees, not the ones in the images. However, the error rates are likely to be very similar. The images are included to show that method two, despite having largely the same error rate, method 2 has a visibly simpler decision tree due to having one less possible value for any attribute with missing values. Because of this, I would tend to prefer using method two, although one must bear in mind that there is more work involved in the set up of method 2 and so the pros and cons must be weighed on a case-to-case basis.')


################################################ Section 2
addTitle( '2 - Clustering' )
addSubtitle( '2.1 - Data Overview' )
addTable( prt2.section1_table, topHeader=True, add_style=[('ALIGN',(2,0),(2,-1),'CENTER')])

addSpacer( 30 )
addSubtitle( '2.2 - K-Means for K=3' )
addParagraph( 'These are the plots of the attribute pairs with the dataset split into 3 clusters according the Scikit-Learn Clusters module.' )
# Create the table of images
tab = [ None ] * 5
k = 0
for i in range( 5 ): # Add the images one row at a time
    tab[i] = (Image( 'output/prt2-' + str( k ) + '.png', width=55*mm, height=41.25*mm ), Image( 'output/prt2-' + str( k + 1 ) + '.png', width=55*mm, height=41.25*mm ), Image( 'output/prt2-' + str( k + 2 ) + '.png', width=55*mm, height=41.25*mm ))
    k += 3
doc.append( Table( tab )) # Add the table of images to the array
del k, tab # clean up any variables we no longer need
addParagraph( 'From the plots we can clearly see three distinct clusters as we would expect, but due to most \
    of the values being in the lower end of their respective ranges, the clusters are all clumped together in \
    the bottom left corner of each graph. It is easier to see proper clustering more aligned to what we would \
    expect in the first few graphs, then it gets messier moving down the page. This is obviously because in \
    any one plot we are showing only two of six variables used to define the clusters and so we are seeing \
    but a plane in the space. It is an interesting though exercise to think about how the data points \
    may be arranged in the 6-dimensional space and why it is that the clustering appears as it does on these plots. \
    I speak more about what the graphs tell us below.' )

addSubtitle( '2.3 - K-Means with varying K' )
addTable( prt2.section3_table, leftHeader=True, topHeader=True )
addParagraph( 'We can see a trend in that as the number of clusters increases, the WCSS (within cluster sum \
    of squares) decreases. We can also see that in general the BCSS (between clusters sum of squares) \
    increases. Both of these follow directly from our intuition. \n If we first consider the WCSS: with \
    more clusters there are more cluster centers and the points will be on average closer to one of the cluster centers. This will decrease \
    the WCSS. Similarly, with more clusters there are more centers between which the distance will be \
    summed. Thus the BCSS will be higher with more clusters within the same set.\n Below I have included two \
    plots of an attribute pair, namely \'Fresh vs Grocery\'. This pair was chosen as it is among the most \
    clear at displaying the distinction between the clusters when K=3 above. It has been added here as a \
    curiosity regarding how increasing the number of clusters would affect the plot of an attribute pair \
    clearly plotted in two dimensions.' )
# Add a small table to display the two images side by side
doc.append(Table([(Image( 'output/prt2-k5.png', width=82.5*mm, height=61.9*mm ), Image( 'output/prt2-k10.png', width=82.5*mm, height=61.9*mm ))]))
addParagraph( 'As with the above graphs for K=3, the graphs do not tell us a lot but show that our algorithms \
    do infact seem to have worked. Although the clusters overlap quite a lot from a 2D perspective, they seem to \
    be contained in one area of the graph which is exactly what we were looking for, thus I would call this a success.' )

addSpacer()
addCentredText('Thank you for taking the time to read my project.')

SimpleDocTemplate( 'report.pdf', pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm, title='7CCSMDM1 CW 1 - 1786775' ).build( doc )