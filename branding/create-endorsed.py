#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import csv
import random
import sys

import sys
import os.path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# We use the Arimo font
pdfmetrics.registerFont(TTFont('Arimo-Bold', 'Arimo-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Arimo', 'Arimo-Regular.ttf'))

class PDFDoc():
  def __init__(self, name, width, height):
    self.dim = (width*cm, height*cm)
    self.c = canvas.Canvas(name, pagesize=self.dim)

  def newpage(self):
    self.c.showPage()

  def save(self):
    self.c.showPage()
    self.c.save()

  def findImg(self, fileimg):
    fileimg = fileimg.replace(" ", "-").lower()
    for typ in ["png", "jpg"]:
      fname = fileimg + "." + typ
      if os.path.isfile(fname):
        return fname
    return None

  def addKeyVal(self, value, posx, posy, size=0.1, font= "Arimo", color=(0,0,0)):
    if value == None or len(value) == 0:
      return
    #relative font size
    self.c.setFont(font, self.dim[1] * size)
    self.c.setStrokeColorRGB(*color)
    self.c.setFillColorRGB(*color)
    value = value.strip().split("\n")
    for l in value:
      self.c.drawCentredString(self.dim[0] * posx, self.dim[1] * posy, l)

def adjSize(name, size, maxlen):
  if len(name) > maxlen:
    return size * maxlen / len(name)
  return size

def createSeal(outputFile, version):
  tempfile = "tmp-%d-foreground.pdf" % random.randrange(10000000)

  dim = (8.5, 9.6)
  doc = PDFDoc(tempfile, dim[0], dim[1])

  doc.addKeyVal(version, 0.795, 0.28, 0.05, font="Arimo-Bold", color=(0,0,0))
  doc.save()

  from PyPDF2 import PdfFileWriter, PdfFileReader
  import io
  background = PdfFileReader(open("endorsed-raw.pdf", "rb"))
  foreground = PdfFileReader(open(tempfile, "rb"))
  page = background.getPage(0)
  page.mergeRotatedScaledTranslatedPage(foreground.getPage(0), 0.0, 1.0, 0, 0, expand=True)
  output = PdfFileWriter()
  output.addPage(page)
  outputStream = open(outputFile, "wb")
  output.write(outputStream)
  outputStream.close()
  os.remove(tempfile)

if __name__ == "__main__":
  version = sys.argv[1]
  file = "endorsement-%s" % version
  createSeal(file + ".pdf", version)
  print("To receive a PNG, run: convert -density 300 %s.pdf %s.png" % (file, file))
