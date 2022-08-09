from PIL import Image
import numpy
from random import randint
import numpy
from tkinter import *
from tkinter import filedialog, Text, Tk
import os
import tkinter as tk
from PIL import Image, ImageTk

def upshift(a, index, n):
    col = []
    for j in range(len(a)):
        col.append(a[j][index])
    shiftCol = numpy.roll(col, -n)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if j == index:
                a[i][j] = shiftCol[i]

def downshift(a, index, n):
    col = []
    for j in range(len(a)):
        col.append(a[j][index])
    shiftCol = numpy.roll(col, n)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if j == index:
                a[i][j] = shiftCol[i]

def rotate180(n):
    bits = "{0:b}".format(n)
    return int(bits[::-1], 2)

def ModInv(a):
    """
        Form equation 1 = inv(a)*a mod m. we find inv(a)
        Inverse exist only if a and m 256 Coprime
    """
    for i in range(2, 256):
        if (a * i) % 256 == 1:
            return i
    return 1

def decryption(img, pix):
    # Obtaining the RGB matrices
    r = []
    g = []
    b = []
    for i in range(img.size[0]):
        r.append([])
        g.append([])
        b.append([])
        for j in range(img.size[1]):
            rgbPerPixel = pix[i, j]
            r[i].append(rgbPerPixel[0])
            g[i].append(rgbPerPixel[1])
            b[i].append(rgbPerPixel[2])
    m = img.size[0]
    n = img.size[1]
    # print(n)
    # print(m)
    Kr = []
    Kc = []
    a = eval(input("Enter value of Kr "))
    Kr.extend(a)
    a1 = eval(input("Enter value of Kc "))
    Kc.extend(a1)
    print('Enter value of ITER_MAX')
    ITER_MAX = int(input())

    # Subkey generation
    def getKeyMatrix(key, message, keyMatrix):
        k = 0
        for i in range(len(message)):
            for j in range(len(message)):
                keyMatrix[i][j] = ord(key[k]) % 65
                k += 1

    def encrypt(messageVector, message, cipherMatrix, keyMatrix):
        for i in range(len(message)):
            for j in range(1):
                cipherMatrix[i][j] = 0
                for x in range(len(message)):
                    cipherMatrix[i][j] += (keyMatrix[i][x] * messageVector[x][j])
                cipherMatrix[i][j] = cipherMatrix[i][j] % 26

    def HillCipher(message, key):
        keyMatrix = [[0] * (len(message)) for i in range(len(message))]
        cipherMatrix = [[0] for i in range(len(message))]
        getKeyMatrix(key, message, keyMatrix)
        messageVector = [[0] for i in range(len(message))]
        for i in range(len(message)):
            messageVector[i][0] = ord(message[i]) % 65
        encrypt(messageVector, message, cipherMatrix, keyMatrix)
        CipherText = []
        for i in range(len(message)):
            CipherText.append(chr(cipherMatrix[i][0] + 65))
        temp = []
        for i in range(len(CipherText)):
            temp.append(str(ord(CipherText[i]) - 65))
        for i in range(len(temp)):
            temp.append(temp[i][::-1])
        arr = list(map(int, temp))
        return arr

    message = input("Enter the private key (3 lettered):")
    key1 = HillCipher(message, "GYBNQKURP")
    # key1=[15,14,7,51,71,7]
    for i in range(3):
        if key1[i] % 2 == 0:
            key1[i] = key1[i] + 1
        if 0 <= key1[i] <= 9:
            key1[i + 3] = key1[i] * 10
    inv1 = ModInv(key1[0])
    inv2 = ModInv(key1[1])
    inv3 = ModInv(key1[2])

    for iterations in range(ITER_MAX):
        # For each column
        for j in range(n):
            for i in range(m):
                if j % 2 == 0:
                    r[i][j] = r[i][j] ^ Kr[i]
                    g[i][j] = g[i][j] ^ Kr[i]
                    b[i][j] = b[i][j] ^ Kr[i]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kr[i])
                    g[i][j] = g[i][j] ^ rotate180(Kr[i])
                    b[i][j] = b[i][j] ^ rotate180(Kr[i])
        # For each row
        for i in range(m):
            for j in range(n):
                if i % 2 == 1:
                    r[i][j] = r[i][j] ^ Kc[j]
                    g[i][j] = g[i][j] ^ Kc[j]
                    b[i][j] = b[i][j] ^ Kc[j]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kc[j])
                    g[i][j] = g[i][j] ^ rotate180(Kc[j])
                    b[i][j] = b[i][j] ^ rotate180(Kc[j])
        # For each column
        for i in range(n):
            """
            rTotalSum = 0
            gTotalSum = 0
            bTotalSum = 0
            for j in range(m):
                rTotalSum += r[j][i]
                gTotalSum += g[j][i]
                bTotalSum += b[j][i]
            rModulus = rTotalSum % 2
            gModulus = gTotalSum % 2
            bModulus = bTotalSum % 2
            """
            # down circular shift
            downshift(r, i, key1[0])
            downshift(g, i, key1[1])
            downshift(b, i, key1[2])

        # For each row
        for i in range(m):
            """
            rTotalSum = sum(r[i])
            gTotalSum = sum(g[i])
            bTotalSum = sum(b[i])
            rModulus = rTotalSum % 2
            gModulus = gTotalSum % 2
            bModulus = bTotalSum % 2
            """
            # left circular shift
            r[i] = numpy.roll(r[i], -key1[3])
            g[i] = numpy.roll(g[i], -key1[4])
            b[i] = numpy.roll(b[i], -key1[5])
        for i in range(m):
            for j in range(n):
                r[i][j] = inv1 * (r[i][j] - key1[3]) % 256
                g[i][j] = inv2 * (g[i][j] - key1[4]) % 256
                b[i][j] = inv3 * (b[i][j] - key1[5]) % 256
        for i in range(m):
            for j in range(n):
                pix[i, j] = (r[i][j], g[i][j], b[i][j])


if __name__ == '__main__':
    def saveimg(img):
        img.save('/Users/sparshkathed/Desktop/CSProject/decrypted.png')
        print("Success")
        exit(0)


    def chooseFile():
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image',filetypes=(("JPG File", "*.jpg"), ("PNG file", "*.png"), ("All Files", "*.*")))
        img = Image.open(fln)
        pic = img.load()
        decryption(img, pic)
        saveimg(img)
        exit()


    root = Tk()
    root.resizable(False, False)
    dbg = root.cget('bg')
    frm = Frame(root)
    frm.pack(side=TOP, padx=15, pady=15)

    text = Text(root, height=13, bg=dbg)
    text.tag_configure("center", justify='center', font='Montserrat')
    text.insert('1.0', "Image Decryption using Rubik's Cube Algorithm\n\n\n")
    text.insert('3.0', 'Made by -\nSparsh Kathed\nGayathri Reddy Patlolla\n')
    text.tag_add("center", "1.0", "end")
    text.pack()

    btn = Button(frm, text="Browse Image", command=chooseFile)
    btn.configure(font='Montserrat')
    btn.pack(side=tk.LEFT)
    btn2 = Button(frm, text="Quit", command=lambda: exit())
    btn2.configure(font='Montserrat')
    btn2.pack(side=tk.LEFT, padx=10, ipadx=10)

    root.title("Rubik's Cube Algorithm")
    root.geometry("400x300")
    root.mainloop()

