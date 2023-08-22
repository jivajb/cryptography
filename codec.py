#name: JIVAJ BRAR
#assignment pa3 cryptography
#date : FEB 20, 2023
# codecs
import numpy as np

class Codec():
    
    def __init__(self):
        self.name = 'binary'
        self.delimiter = '#' 

    # convert text or numbers into binary form    
    def encode(self, text):
        if type(text) == str:
            return ''.join([format(ord(i), "08b") for i in text])
        else:
            print('Format error')

    # convert binary data into text
    def decode(self, data):
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.encode(self.delimiter): # you need to find the correct binary form for the delimiter
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr(int(byte,2))       
        return text 

class CaesarCypher(Codec):
    def __init__(self, shift=3):
        self.name = 'caesar'
        self.delimiter = '#'  
        self.shift = shift    
        self.chars = 256      # total number of characters

    # convert text into binary form
    # your code should be similar to the corresponding code used for Codec
    def encode(self, text):
        data = ''
        # your code goes here
        if type(text) == str:
            data = ''.join([format(ord(i) + self.shift, "08b") for i in text])
        else:
            print('Format error')
        return data
    
    # convert binary data into text
    # your code should be similar to the corresponding code used for Codec
    def decode(self, data):
        text = ''
        # your code goes here
        diction = []
        datalength = len(data)
        for j in range(0, datalength, 8):
            if data[j: j+8] == self.encode(self.delimiter):
                break
            else:
                diction.append(data[j:j+8])
        for m in diction:
            text = (text + (chr(int(m, 2)- self.shift)))
                
        return text

# a helper class used for class HuffmanCodes that implements a Huffman tree
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.code = ''
        
class HuffmanCodes(Codec):
    def __init__(self):
        self.delimiter = "#"
        self.nodes = None
        self.name = 'huffman'
        self.traverse = {}
        super().__init__()
        self.encodetree = 0
        self.decodetree = 0
        
    # make a Huffman Tree    
    def make_tree(self, data):
        # make nodes
        nodes = []
        for char, freq in data.items():
            nodes.append(Node(freq, char))
            
        # assemble the nodes into a tree
        while len(nodes) > 1:
            # sort the current nodes by frequency
            nodes = sorted(nodes, key=lambda x: x.freq)

            # pick two nodes with the lowest frequencies
            left = nodes[0]
            right = nodes[1]

            # assign codes
            left.code = '0'
            right.code = '1'

            # combine the nodes into a tree
            root = Node(left.freq+right.freq, left.symbol+right.symbol, left, right)

            # remove the two nodes and add their parent to the list of nodes
            nodes.remove(left)
            nodes.remove(right)
            nodes.append(root)
        
        return nodes

    # traverse a Huffman tree
    def traverse_tree(self, node, val):
        next_val = val + node.code
        if(node.left):
            self.traverse_tree(node.left, next_val)
        if(node.right):
            self.traverse_tree(node.right, next_val)
        if self.encodetree == True: #only works when encode() is run
            if(not node.left and not node.right):
                self.traverse[node.symbol] = (next_val)
        elif self.decodetree == True: #only works when decode() is run
            if(not node.left and not node.right):
                self.traverse[next_val] = (node.symbol)
            
    # convert text into binary form
    def encode(self, text):
        self.encodetree = True #turns on encode in traverse_tree
        data = text+self.delimiter
        # your code goes here
        # you need to make a tree
        # and traverse it
        exitdata = ''
        t = {}
        for j in data:
            if j not in t:
                t[j] = 0
            t[j] += 1
            
        self.nodes = self.make_tree(t)[0] # sets self.nodes used again in decode()
        self.traverse_tree(self.nodes, '') #traverses the tree after making the tree
        
        for j in range(len(data)):
            if data[j] in self.traverse:
                val = data[j]
                exitdata = exitdata + self.traverse[val]     
        #print(exitdata)
        self.encodetree = False #turns off encode in traverse_tree
        return exitdata

    # convert binary data into text
    def decode(self, data):
        self.decodetree = True #opens for decoding in traverse 
        text = ''
        t = ''
        # your code goes here
        # you need to traverse the tree
        self.traverse_tree(self.nodes, '')
        for j in range(len(data)):# loops til data can fulfil the if statement
            t = t + data[j]
            if t in self.traverse:
                if self.traverse[t] == self.delimiter:
                    break
                text += self.traverse[t]
                t = '' #resets t
        self.decodetree = False #turns of decode process in traverse tree
        return text
    
    
# driver program for codec classes
if __name__ == '__main__':
    text = 'hello' 
    #text = 'Casino Royale 10:30 Order martini' 
    print('Original:', text)
    
    c = Codec()
    binary = c.encode(text + c.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary) # should print '011010000110010101101100011011000110111100100011'
    data = c.decode(binary)  
    print('Text:', data)     # should print 'hello'
    
    cc = CaesarCypher()
    binary = cc.encode(text + cc.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary)
    data = cc.decode(binary) 
    print('Text:', data)     # should print 'hello'
     
    h = HuffmanCodes()
    binary = h.encode(text + h.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary)
    data = h.decode(binary)
    print('Text:', data)     # should print 'hello'

