#!/usr/bin/python
# -*- coding: utf-8 -*-


class ChessBoard:

    def __init__(self, width, height):
        """ Constructs objects of type Board.
        """
        self.width = width
        self.height = height
        self.data = [[' '] * width for row in range(height)]



    def __repr__(self):
        """ Returns a string representation for an object of type Board.
        """
        counter = 8
        s = ''   # the string to return
        for row in range(self.height):
            s += str(counter) + '|'   # add the spacer character
            counter -=1
            for col in range(self.width):
                if self.data[row][col] == ' ':
                    s += self.data[row][col] + '|'
                else:
                    s += self.data[row][col] + '|'

            s += '\n'


        s = s + ' ' + ('-' + ('-'*2*self.width) + '\n')

        result = ' '
        for x in range(self.width):
            result = result + str(chr(x+97)) + " "

        s += " " + result + '\n'

        return s


    def readPieces(self,string):
        counter = 0
        for row in range(8):
            for col in range(8):
                self.data[row][col] = string[counter]
                counter +=1






    def parseString(self, string):

        spaces = "0123456789"
        newstr = string.replace("/", "")
        for x in newstr:
            if x in spaces:
                replaceStr = int(x)*' '
                newstr = newstr.replace(x, replaceStr)
        newstr = newstr[0:64]
        return newstr

    def convertToImage(self,string):
        symbolString = ''

        PIECE_SYMBOLS = {'P': '♟', 'B': '♝','N': '♞','R': '♜','Q': '♛','K': '♚','p': '♙','b': '♗','n': '♘','r': '♖','q': '♕','k': '♔', ' ': ' '}
        for x in string:
            symbolString += PIECE_SYMBOLS[x]
        return symbolString

    def updateBoard(self,string):
 #       piecesString = self.convertToImage(self.parseString(string))
        piecesString = self.parseString(string)
        self.readPieces(piecesString)


    def lookupPiece(self,string):
        letters = ['a','b','c','d','e','f','g','h']
        index1 = 8-int(string[1])
        index2 = int(letters.index(string[0]))
        if self.data[index1][index2] == ' ':
            ##print('we are about to return a (space)!')
            return ' '
        else:
            ##print(self.data[index1][index2])
            return self.data[index1][index2]





