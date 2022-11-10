import json
import chess
import chess.svg
from contextlib import redirect_stdout
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

#function for generating metadata from P3eco.txt opener dataset
def p3ecotextgenerator():
    tokenid = 1
    tokens = {}

    #Prefixes for ECO
    prefixes = ['A', 'B', 'C', 'D', 'E']
    
    #Open file of openers
    with open('raw data/P3eco.txt') as f:
        lines = f.readlines()
    
    #Split the openers, remove the comments, merge multiple line PGNs and JSONify everything
    for i, line in enumerate(lines):
        if not line.startswith(';'):
            #identify eco lines
            if line.startswith(tuple(prefixes)):
                econame = line.split(' ', 1)
                #split comments from names and cleanup
                if ';' in econame[1]:
                    namecomment = econame[1].split(';')
                    econame[1] = namecomment[0]
                econame[1] = econame[1].replace('\r\n', '')
                econame[1] = econame[1].rstrip()
                econame[1] = econame[1].lstrip()
                pgn=lines[i+1]
                pgn=pgn.strip()
            
                #Accounts for multiple line pgns from the source file
                if not pgn.endswith('1/2'):
                    pgn = pgn + ' ' + lines[i+2]
                    if not pgn.endswith('1/2'):
                        pgn = pgn + ' ' + lines[i+3]

                #clean up the PGN and write to file for use with pgn-extract     
                pgn=pgn.replace('\r\n', '').replace('(', '').replace(')', '').strip()
                with open('pgn.txt', 'w') as outfile:
                    outfile.write(pgn)

                #create the FEN string using pgn-extract
                FEN = str(subprocess.check_output("/Users/daneshea/Projects/ChessOpenerDataset/pgn-extract --nomovenumbers --noresults --notags -C -F pgn.txt | grep '{.*}'", shell=True))
                FEN = FEN.split("\"")
                FEN = FEN[1]

                #create SVGs of board states
                board = chess.Board(FEN)
                with open('images/' + str(tokenid) + '.svg', 'w') as f:
                    with redirect_stdout(f):
                            print(chess.svg.board(board, size=350))

                #create token metadata and write to individual files
                tokens[tokenid] = {'tokenid': tokenid, 'eco': econame[0], 'name': econame[1], 'pgn': pgn, 'FEN': FEN, 'image_url': 'ipfs://' + os.getenv('IMAGE_CID') + '/' + str(tokenid) + '.svg'}

                #write metadata JSON files
                with open('metadata/' + str(tokenid), 'w') as outfile:
                    data =json.dump(tokens[tokenid], outfile, indent=4)

                tokenid += 1

#function for generating metadata from raw data/niklasfchessopenings.txt
def niklasfchessopeninggenerator():
    tokenid = 1
    tokens = {}
    
    #Open file of openers
    with open('raw data/niklasfchessopenings.txt') as f:
        lines = f.readlines()
    
    #Split the openers, remove the comments, merge multiple line PGNs and JSONify everything
    for i, line in enumerate(lines):
        eco = line[0:3]
        
        namepgn = line[3:].split('1.')

        name = namepgn[0].strip('\t')
        pgn = namepgn[1].strip('\n')
        pgn = '1.' + pgn + ' 1/2'

        with open('pgn.txt', 'w') as outfile:
                    outfile.write(pgn)

        #create the FEN string using pgn-extract
        FEN = str(subprocess.check_output("/Users/daneshea/Projects/ChessOpenerDataset/pgn-extract --nomovenumbers --noresults --notags -C -F pgn.txt | grep '{.*}'", shell=True))
        FEN = FEN.split("\"")
        FEN = FEN[1]

        #create SVGs of board states
        board = chess.Board(FEN)
        with open('images/' + str(tokenid) + '.svg', 'w') as f:
            with redirect_stdout(f):
                    print(chess.svg.board(board, size=350))

        #create token metadata and write to individual files
        tokens[tokenid] = {'tokenid': tokenid, 'eco': eco, 'name': name, 'pgn': pgn, 'FEN': FEN, 'image_url': 'ipfs://' + os.getenv('IMAGE_CID') + '/' + str(tokenid) + '.svg'}

        #write metadata JSON files
        with open('metadata/' + str(tokenid), 'w') as outfile:
           data =json.dump(tokens[tokenid], outfile, indent=4)

        tokenid += 1    

niklasfchessopeninggenerator()

#Write the entire token dictionary to a file in JSON
#with open('test.txt', 'w') as outfile:
    #data =json.dump(tokens, outfile, indent=4)