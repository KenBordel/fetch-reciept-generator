import math
import random
import time
import sys

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors, fonts

## Generate receipt file

filename = 'reciept.pdf'
reciept = canvas.Canvas(f'output/{filename}', pagesize = (250, 445))

##   Customize reciepts   ##
print("Fetch Reciept Generator")
print("Created by KenBordel")
print("""This program is meant to be used to generate custom reciepts as pdf files to be
scanned into the Fetch Rewards app. The purpose is to make the items reflect the 
current promotions that are going on to provide you maximium points \n \n""")

#Store

storename = input("Enter the name of the store: ")

storeImg = f'storeimg/{storename}.jpg'

try:
    reciept.drawImage(storeImg, 25, 375, anchor='c')
except:
    print('Error, store image could not be loaded. Please check your spelling and try again. Quiting program in 5 seconds...')
    time.sleep(5)
    sys.exit()



storeaddress = input("Enter the store address in this format '11111 Street Rd, City, State, Zip Code': ")

#Date/Time
date = input("Enter date in this format 'mm/dd/yyyy': ")
time = input("Enter time in this format '12:00 AM/PM': ")

#Price
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

item4name = input("Enter the name of your fourth product: ")
item4qty = input("Enter how much of this item you want to buy: ")
item4price = input("Enter the price of your fourth item in this format '11.11': ")

item5name = input("Enter the name of your fifth product: ")
item5qty = input("Enter how much of this item you want to buy: ")
item5price = input("Enter the price of your fifth item in this format '11.11': ")

item6name = input("Enter the name of your sixth product: ")
item6qty = input("Enter how much of this item you want to buy: ")
item6price = input("Enter the price of your sixth item in this format '11.11': ")

#barcode
barid = random.randrange(00000000000000, 99999999999999)

tax = (float(item1price) * float(item1qty) + float(item2price) * float(item2qty) + float(item3price) * float(item3qty) + float(item4price) * float(item4qty) + float(item5price) * float(item5qty) + float(item6price) * float(item6qty)) * float(salestax)  
roundtax = round(tax, 2)
result = float(item1price) * float(item1qty) + float(item2price) * float(item2qty) + float(item3price) * float(item3qty) + float(item4price) * float(item4qty) + float(item5price) * float(item5qty) + float(item6price) * float(item6qty) + tax
total = round(result, 2)
print(total)

extramoney = random.randrange(5, 30)

##   Pdf generation   ##
from barcode import EAN13
from barcode import writer
from PIL import Image

reciept_barcode = EAN13(str(barid), writer.ImageWriter('PNG'))
reciept_barcode.save('barcode/barcode')

barcode_old = Image.open('barcode/barcode.png')
barcode_new = barcode_old.resize((150, 50))
barcode_new.save('barcode/barcode.png')

reciept.setTitle('Reciept')

reciept.drawImage(storeImg, 25, 375, anchor='c')
reciept.drawImage('barcode/barcode.png', 50, 0)

#Set up fonts
pdfmetrics.registerFont(TTFont('MerchantCopy', 'fonts/MerchantCopy.ttf'))

reciept.setFont('MerchantCopy', 16)
reciept.drawString(20, 365, storeaddress)
reciept.drawCentredString(125, 380, storename)
reciept.drawCentredString(125, 350, f"{date} {time}")


reciept.setFont('MerchantCopy', 14)

if (float(item1price) != 0 and float(item1qty) != 0):
    reciept.drawString(20, 300, f"{item1qty}   {item1name}: ${item1price}")

if (float(item2price) != 0 and float(item2qty) != 0):
    reciept.drawString(20, 290, f"{item2qty}   {item2name}: ${item2price}")

if (float(item3price) != 0 and float(item3qty) != 0):
    reciept.drawString(20, 280, f"{item3qty}   {item3name}: ${item3price}")

if (float(item4price) != 0 and float(item4qty) != 0):
    reciept.drawString(20, 270, f"{item4qty}   {item4name}: ${item4price}")

if (float(item5price) != 0 and float(item5qty) != 0):
    reciept.drawString(20, 260, f"{item5qty}   {item5name}: ${item5price}")

if (float(item6price) != 0 and float(item6qty) != 0):
    reciept.drawString(20, 250, f"{item6qty}   {item6name}: ${item6price}")


reciept.setFont('MerchantCopy', 16)
reciept.drawRightString(125, 210, f"Subtotal: {round(float(item1price) * float(item1qty) + float(item2price) * float(item2qty) + float(item3price) * float(item3qty) + float(item4price) * float(item4qty) + float(item5price) * float(item5qty) + float(item6price) * float(item6qty), 2)}")
reciept.drawRightString(125, 190, f"Tax: {roundtax:.2f}")
reciept.drawRightString(125, 170, f"Cash: {round(total + float(extramoney), 2):.2f}")
reciept.drawRightString(125, 150, f"Change: {round((total + float(extramoney)) - total, 2):.2f}")


reciept.setFont('MerchantCopy', 20)
reciept.drawRightString(125, 100, f"Total: {total}")


reciept.setFont('MerchantCopy', 18)
reciept.drawString(10, 80, f"Thank you for shopping at {storename}!")

reciept.setFont('MerchantCopy', 14)
reciept.drawString(10, 60, f"ST# 01925 OP# 000069 TE# 09 TR# 07776 Mgr JODY")

reciept.save()
