# (c) Niels Elgaard Larsen

# MIT License
# AND GNU AFFERO GENERAL PUBLIC LICENSE
# display electricity prices the next day or two
# for DK East excl taxes.
# Button A toggles barchart and text mode.
# prices in Øre (0.01 DKK). Barchart marks 0.25 DKK intervals, cropped at DKK 1.12 (which is too expensive anyway)
# only shows Danish prices, but similar API's probably exists in many other countries

import badger2040

print("start el prices")
b = badger2040.Badger2040()
numview=False
b.clear()
b.text("ELECTRICITY PRICES DK EAST", 10,30)
b.text("staring network", 10,70)
import urequests
b.connect()

URL="https://api.energidataservice.dk/dataset/Elspotprices?offset=0&start=now-P0DT1H&timezone=dk&filter=%7B%22PriceArea%22:[%22DK2%22]%7D&sort=HourUTC%20ASC"
def pr(s,iv=False):
   global x,y,sp
   if iv:
     b.rectangle(x, y, sp-3, 18)
     b.set_pen(15)
   b.text(s, x, y)
   b.set_pen(0)
   y+=18
   if y>110:
       y=0
       x+=sp
       sp=55

while True:
  b.text("READY "+str(numview), 10,100)
  if b.pressed(badger2040.BUTTON_A):
        numview=not numview
        print("ba","nw=",numview)
  if b.pressed(badger2040.BUTTON_C):
      print("wokenC")
      break
  r = urequests.get(URL)
  priser = r.json()
  b.set_pen(15)
  b.clear()
  b.set_pen(0)
  day=-1
  x=0
  if numview:
    y=0
    sp=55
    pr("El Ø",True)
    i=0
    for pris in priser["records"]:
      h=pris["HourDK"].split('T')[1].split(":")[0]
      d=pris["HourDK"].split('T')[0].split("-")[2]
      p=int(pris["SpotPriceDKK"]/10)
      if d!=day:
        pr("D: "+d,True)
      pr(h+":"+str(p))
      if p>99:
        sp=68
      i+=1
      if i>31:
        break
      day=d
  else:
      for pris in priser["records"]:
        h=pris["HourDK"].split('T')[1].split(":")[0]
        d=pris["HourDK"].split('T')[0].split("-")[2]
        p=int(pris["SpotPriceDKK"]/10)
        b.rectangle(x, 112-p, 8, p)
        if d!=day:
          b.set_pen(5)
          b.rectangle(x, 0, 3, 112)
          b.set_pen(0)
        if int(h)%4==0: 
          b.text(h, x, 116)
        x+=8
        day=d
      b.set_pen(5)
      b.rectangle(0, 56, 295, 2)
      b.rectangle(0, 28, 295,1)
      b.rectangle(0, 84, 295,1)
      b.set_pen(0)
  b.update()
  badger2040.sleep_for(60)
while True:
  b.keepalive()
  b.halt()

