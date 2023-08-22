#name: JIVAJ BRAR
#assignment pa3 cryptography
#date : FEB 20, 2023

# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
     
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None
        
    
    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
        binary = self.codec.encode(message+self.delimiter)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message
            self.binary = binary
            # your code goes here
            # you may create an additional method that modifies the image array
            j = 0
            k = 0
            l = 0
            #start func
            lenbin = len(binary)
            for m in range(lenbin):
                cval = image[j,k,l] #value ###
                bval = int(binary[m]) #binary value
                
                if bval == 0:
                    
                    if (cval%2) == 0: #checks to see if it is even
                        l = l + 1
                    else:
                        cval = cval - 1
                        image[j,k,l] = cval
                        l = l + 1
                
                else: #ELSE FOR bianry value not being 0
                    
                    if (cval%2) != 0: #if not even
                        l = l + 1
                    else:
                        cval = cval - 1
                        image[j,k,l] = cval
                        l = l + 1
                imgshape = image.shape[1]
                if l == 3:
                    l = 0 # resets value for next iteration
                    k = k + 1
                elif k == imgshape:
                    k = 0 # resets value for next iteration
                    j = j + 1
                else:
                    pass 
                   
            cv2.imwrite(fileout, image)
                
    def decode(self, filein, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging      
        flag = True
        
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag:
            # your code goes here
            # you may create an additional method that extract bits from the image array
            binary_data = ""
            for col in image: # color in image
                for p in col: # pix
                    for colorval in p: # array
                        cval = format(colorval, "08b")
                        cval = cval[-1]
                        binary_data = binary_data + cval # updates bindata
                            
            # update the data attributes:
            self.text = self.codec.decode(binary_data) #self.text gives you the same value as self.codec.decode(binary_data)
            message = self.text # techincally self.text is the same as the original self.text and
            binary_data = self.codec.encode(message+"#") # same from encode function to run the codec
            self.binary = binary_data   
            #print(binary_data)   #debugging   
        
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()
        
if __name__ == '__main__':
    
    s = Steganography()

    s.encode('fractal.jpg', 'fractal.png', 'hello', 'binary')
    # NOTE: binary should have a delimiter and text should not have a delimiter
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'

    s.decode('fractal.png', 'binary')
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    print('Everything works!!!')
