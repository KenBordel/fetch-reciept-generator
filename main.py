import math
import random
import time
import sys

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors, fonts

## Generate receipt file

filename = 'receipt.pdf'
receipt = canvas.Canvas(f'output/{filename}', pagesize = (250, 445))

##   Customize receipts   ##
print("Fetch Receipt Generator")
print("Created by BengaliTech")
print("""This program is meant to be used to generate custom receipts as PDF files to be
scanned into the Fetch Rewards app. The purpose is to make the items reflect the 
current promotions that are going on to provide you maximum points \n \n""")

# Store

storename = input("Enter the name of the store: ")

storeImg = f'storeimg/{storename}.jpg'

try:
    receipt.drawImage(storeImg, 25, 375, anchor='c')
except:
    print('Error, store image could not be loaded. Please check your spelling and try again. Quitting program in 5 seconds...')
    time.sleep(5)
    sys.exit()

storeaddress = input("Enter the store address in this format '11111 Street Rd, City, State, Zip Code': ")

# Date/Time
date = input("Enter date in this format 'mm/dd/yyyy': ")
time = input("Enter time in this format '12:00 AM/PM': ")

# Price
salestax = input("Enter your sales tax in this format '0.06': ")

item1name = input("Enter the name of your first product: ")
item1qty = input("Enter how much of this item you want to buy: ")
item1price = input("Enter the price of your first item in this format '11.11': ")

item2name = input("Enter the name of your second product: ")
item2qty = input("Enter how much of this item you want to buy: ")
item2price = input("Enter the price of your second item in this format '11.11': ")

item3name = input("Enter the name of your third product: ")
item3qty = input("Enter how much of this item you want to buy: ")
item3price = input("Enter the price of your third item in this format '11.11': ")

# Barcode
barid = random.randrange(0000000000000, 9999999999999)

tax = (float(item1price) * float(item1qty) + float(item2price) * float(item2qty) + float(item3price) * float(item3qty)) * float(salestax)
roundtax = round(tax, 2)
result = float(item1price) * float(item1qty) + float(item2price) * float(item2qty) + float(item3price) * float(item3qty) + tax
subtotal = round(result, 2)
print(subtotal)

extramoney = random.randrange(5, 30)

##   PDF generation   ##
from barcode import EAN13
from barcode import writer
from PIL import Image

receipt_barcode = EAN13(str(barid), writer.ImageWriter('PNG'))
receipt_barcode.save('barcode/barcode.png')

barcode_old = Image.open('barcode/barcode.png')
barcode_new = barcode_old.resize((150, 50))
barcode_new.save('barcode/barcode.png')

receipt.setTitle('Receipt')

receipt.drawImage(storeImg, 25, 375, anchor='c')
receipt.drawImage('barcode/barcode.png', 50, 0)

# Set up fonts
pdfmetrics.registerFont(TTFont('MerchantCopy', 'fonts/MerchantCopy.ttf'))

receipt.setFont('MerchantCopy', 16)
receipt.drawString(20, 365, storeaddress)
receipt.drawCentredString(125, 380, storename)
receipt.drawCentredString(125, 350, f"{date} {time}")

receipt.setFont('MerchantCopy', 14)

if float(item1price) != 0 and float(item1qty) != 0:
    receipt.drawString(20, 300, f"{item1qty}   {item1name}: ${item1price}")

if float(item2price) != 0 and float(item2qty) != 0:
    receipt.drawString(20, 280, f"{item2qty}   {item2name}: ${item2price}")

if float(item3price) != 0 and float(item3qty) != 0:
    receipt.drawString(20, 260, f"{item3qty}   {item3name}: ${item3price}")

receipt.setFont('MerchantCopy', 16)
receipt.drawRightString(125, 210, f"Subtotal: {subtotal:.2f}")
receipt.drawRightString(125, 190, f"Tax: {roundtax:.2f}")
cash_amount = total + float(extramoney)
receipt.drawRightString(125, 170, f"Cash: {cash_amount:.2f}")
change_amount = cash_amount - total
receipt.drawRightString(125, 150, f"Change: {change_amount:.2f}")

receipt.setFont('MerchantCopy', 20)
receipt.drawRightString(125, 100, f"Total: {total:.2f}")

receipt.setFont('MerchantCopy', 18)
receipt.drawString(10, 70, f"Thank you for shopping at {storename}!")
receipt.save()
