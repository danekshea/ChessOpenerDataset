import json
import chess
import chess.svg
from contextlib import redirect_stdout
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

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
        FEN = str(subprocess.check_output("./pgn-extract --nomovenumbers --noresults --notags -C -F pgn.txt | grep '{.*}'", shell=True))
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

# #write the entire token dictionary to a file in JSON
# with open('test.txt', 'w') as outfile:
#     data =json.dump(tokens, outfile, indent=4)