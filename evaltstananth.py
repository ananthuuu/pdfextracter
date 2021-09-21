from json import encoder
from operator import itemgetter
import fitz
import json

import argparse
parser = argparse.ArgumentParser()                                               

parser.add_argument("--input", "-input", type=str, required=True)
parser.add_argument("--output", "-output", type=str, required=True)
args = parser.parse_args()
  

  
args = parser.parse_args()
inpfilename=args.input
opfilename=args.output






def fonts(doc, granularity=False):
    
    styles = {}
    font_counts = {}

    for page in doc:
        blocks = page.getText("dict")["blocks"]
        for b in blocks:  # iterate through the text blocks
            if b['type'] == 0:  # block contains text
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if granularity:
                            identifier = "{0}_{1}_{2}_{3}".format(s['size'], s['flags'], s['font'], s['color'])
                            styles[identifier] = {'size': s['size'], 'flags': s['flags'], 'font': s['font'],
                                                  'color': s['color']}
                        else:
                            identifier = "{0}".format(s['size'])
                            styles[identifier] = {'size': s['size'], 'font': s['font']}

                        font_counts[identifier] = font_counts.get(identifier, 0) + 1  # count the fonts usage

    font_counts = sorted(font_counts.items(), key=itemgetter(1), reverse=True)

    if len(font_counts) < 1:
        raise ValueError("Zero discriminating fonts found!")

    return font_counts, styles


def font_tags(font_counts, styles):
    
    p_style = styles[font_counts[0][0]]  # get style for most used font by count (paragraph)
    p_size = p_style['size']  # get the paragraph's size

    # sorting the font sizes high to low, so that we can append the right integer to each tag
    font_sizes = []
    for (font_size, count) in font_counts:
        font_sizes.append(float(font_size))
    font_sizes.sort(reverse=True)

    # aggregating the tags for each font size
    idx = 0
    size_tag = {}
    for size in font_sizes:
        idx += 1
        if size == p_size:
            idx = 0
            size_tag[size] = '<p>'
        if size > p_size:
            size_tag[size] = '<h{0}>'.format(idx)
        elif size < p_size:
            size_tag[size] = '<s{0}>'.format(idx)

    return size_tag


def headers_para(doc, size_tag):
    
    header_para = []  # list with headers and paragraphs
    first = True  # boolean operator for first header
    previous_s = {}  # previous span

    for page in doc:
        blocks = page.getText("dict")["blocks"]
        for b in blocks:  # iterate through the text blocks
            if b['type'] == 0:  # this block contains text

                # REMEMBER: multiple fonts and sizes are possible IN one block

                block_string = ""  # text found in block
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if s['text'].strip():  # removing whitespaces:
                            if first:
                                previous_s = s
                                first = False
                                block_string = size_tag[s['size']] + s['text']
                            else:
                                if s['size'] == previous_s['size']:

                                    if block_string and all((c == "|") for c in block_string):
                                        # block_string only contains pipes
                                        block_string = size_tag[s['size']] + s['text']
                                    if block_string == "":
                                        # new block has started, so append size tag
                                        block_string = size_tag[s['size']] + s['text']
                                    else:  # in the same block, so concatenate strings
                                        block_string += " " + s['text']

                                else:
                                    header_para.append(block_string)
                                    block_string = size_tag[s['size']] + s['text']

                                previous_s = s

                    # new block started, indicating with a pipe
                    block_string += "|"

                header_para.append(block_string)

    return header_para




def main():
    
    document = inpfilename
    doc = fitz.open(document)
    title=[]
    headings=["Name","PersonalDetails"]
    contents=[]

    font_counts, styles = fonts(doc, granularity=False)

    size_tag = font_tags(font_counts, styles)

    elements = headers_para(doc, size_tag)

    with open("doc.json", 'w') as json_out:
        json.dump(elements, json_out)

    x=elements
    i=0
    sec=0
    tdarr=[]


    for y in elements :
        if "<h2>" in y :
            tdarr.append(contents)
            contents=[]
            
            #print(y)
            z=y.replace("<h2>","")
            z=z.replace("|","")
            headings.append(z)
        
    

    
        


    
        
    

    tdarray1 = {key:[] for key in headings}


    h2=0
    p2=0
    temp=0

    #print(elements)
    
        
            



    
    for y in elements :



        if "<h1>" in y :
            
            #print(y)
            z=y.replace("<h1>","")
            z=z.replace("|","")
            tdarray1["Name"].append(z)

            h3="PersonalDetails"

            
            
            
            
            
            #print("onouterloop1 "+str(i))
        
    

    
        


    
        if "<h2>" in y :
            
            #print(y)
            z=y.replace("<h2>","")
            z=z.replace("|","")
            

            headings.append(z)
            
            h3=z
            
            
            #print("onouterloop1 "+str(i))
            
        elif "<p>" in y :
            #print(y)
            z=y.replace("<p>","")
            z=z.replace("|","")
            z=z.replace("●","")
            z=z.replace("  ​ ","").replace(" ​  ","").replace("- ","")


            
            h2=0
            p2=1
            temp=temp+1
            
            
            try :
                 
                 tdarray1[h3].append(z)
            except:
                justforfun="0" 

        
             

           
           

    with open(opfilename, 'w') as json_out:
        json.dump(tdarray1, json_out,indent=4)

        

    
    

        


                    

        
            






        


if __name__ == '__main__':
    main()

