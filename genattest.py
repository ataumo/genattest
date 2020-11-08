#!/usr/bin/env python3

import io
import pdfrw
import sys
import getopt
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from datetime import datetime
import yaml
import os

dic_reason={
  "travail": 578,
  "achats": 533,
  "sante": 477,
  "famille": 435,
  "handicap": 396,
  "sport_animaux": 358,
  "convocation": 295,
  "missions": 255,
  "enfants": 211,
}

now = datetime.now()
date = now.strftime("%d/%m/%Y")
datefile = now.strftime("%d%m%Y")
hour = now.strftime("%H:%M")
hourh = now.strftime("%Hh%M")
hourall = now.strftime("%H%M%S")


#id infos
settgins = {}
useDefault = True
if os.path.isfile('settings.yaml'):
    with open("settings.yaml", 'r') as stream:
        try:
            settings = yaml.safe_load(stream)
            useDefault = False
        except yaml.YAMLError as exc:
            print(exc)
if useDefault:
    settings = {
        "firstname": "Emmanuel",
        "lastname": "Macron",
        "birthday": "09/02/1972",
        "placeofbirth": "Paris",
        "address": "20 rue du Caire",
        "zipcode": 75015,
        "city": "Paris",
        "ccity": "Paris"
    }

# Transforme les clés du dictionnaire en variables
locals().update(settings)
            

def usage():
    print("usage : python3 genattest.py -h -t -a -s")
    print("-h : help")
    print("-t : reason 'travail'")
    print("-a : reason 'achats'")
    print("-S : reason 'sante'")
    print("-s : reason 'sport & animaux' (to default)")


def run(argv):
    global reason
    reason="sport_animaux"
    try:
        opts, args = getopt.getopt(argv, "htaSs", ["help", "travail",\
        "achats","sante","sport"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-t", "--travail"):
            reason="travail"
        elif opt in ("-a", "--achats"):
            reason="achats"
        elif opt in ("-S", "--sante"):
            reason="sante"
        elif opt in ("-s", "--room"):
            reason="sport_animaux"

    canvas_data = get_overlay_canvas()
    form = merge(canvas_data, template_path='src/certificate.pdf')
    save(form, filename='certificate_'+datefile+''+hourall+'.pdf')


def get_overlay_canvas() -> io.BytesIO:
    global zipcode
    zipcode = str(zipcode)

    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    pdf.drawString(x=119, y=696, text=firstname+' '+lastname)
    pdf.drawString(x=119, y=674, text=birthday)
    pdf.drawString(x=297, y=674, text=placeofbirth)
    pdf.drawString(x=133, y=652, text=address+' '+zipcode+' '+city)
    pdf.drawString(x=78, y=dic_reason[reason], text='X')

    pdf.drawString(x=105, y=177, text=ccity)
    pdf.drawString(x=91, y=153, text=date)
    pdf.drawString(x=264, y=153, text=hour)

    #QRCode Zone
    text_QrCode="Cree le: "+date+" a "+hourh+";\n"\
    " Nom: "+lastname+";\n"\
    " Prenom: "+firstname+";\n"\
    " Naissance: "+birthday+" a "+placeofbirth+";\n"\
    " Adresse: "+address+" "+zipcode+" "+city+";\n"\
    " Sortie: "+date+" a "+hour+";\n"\
    " Motifs: "+reason

    qrw = QrCodeWidget(text_QrCode)
    b = qrw.getBounds()
    w=b[2]-b[0]
    h=b[3]-b[1]
    d = Drawing(92,92,transform=[100./w,0,0,100./h,0,0])
    d.add(qrw)
    renderPDF.draw(d, pdf, 435, 95)

    pdf.showPage()
    d = Drawing(300,300,transform=[340./w,0,0,340./h,0,0])
    d.add(qrw)
    renderPDF.draw(d, pdf, 50, 450)

    pdf.save()
    data.seek(0)
    return data



def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO:
    template_pdf = pdfrw.PdfReader(template_path)
    overlay_pdf = pdfrw.PdfReader(overlay_canvas)

    for page, data in zip(template_pdf.pages, overlay_pdf.pages):
        overlay = pdfrw.PageMerge().add(data)[0]
        pdfrw.PageMerge(page).add(overlay).render()

    form = io.BytesIO()
    pdfrw.PdfWriter().write(form, template_pdf)
    form.seek(0)
    return form


def save(form: io.BytesIO, filename: str):
    with open(filename, 'wb') as f:
        f.write(form.read())

if __name__ == '__main__':
    run(sys.argv[1:])
