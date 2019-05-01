from PIL import Image
im = Image.open('IMG_0283.jpg')

orig_data = im.getdata()
new_data = [ ]

for p in orig_data:
    new_data.append((255-p[0], 255-p[1], 255-p[2]))

im.putdata(new_data)
im.save('IMG_0283.jpg')