import argparse
from pypdf import PdfWriter,PdfReader
from pathlib import Path


def validate(inputPdf:str, outputDir:str):
    msg = ""
    ok = True
    ippath = Path(inputPdf)
    if not ippath.is_file():
        ok = False
        msg = msg + f"{inputPdf} is not a file. "
    odpath = Path(outputDir)
    if not odpath.is_dir():
        ok = False
        msg = msg + f"{outputDir} is not a directory. "
    if not ok:
        print(msg)
    return ok

def padded(curVal: int, maxVal: int) -> str:
    width = len(str(maxVal))
    return str(curVal).zfill(width)

parser = argparse.ArgumentParser(description="A script that splits pdf files into separate page files.")
parser.add_argument("-i", "--input", type=str, default="", help="name of input pdf file to split.")
parser.add_argument("-d", "--directory", type=str, default=".", help="name of folder to write pdfs to.")
parser.add_argument("-p", "--prefix", type=str, default="", help="prefix for created file names.")

args = parser.parse_args()

print(f"input=[{args.input}]")
print(f"directory=[{args.directory}]")
print(f"prefix=[{args.prefix}]")

if validate(args.input,args.directory):
    path = Path(args.input)
    stem = path.stem
    reader = PdfReader(args.input)
    pcount = len(reader.pages)
    opath = Path(args.directory)
    print(f"{args.input} has {pcount} page(s)")
    for i in range(pcount):
        pn = i+1
        nfn = str(stem) + "_" + padded(pn,pcount) + ".pdf"
        ofn = opath / nfn
        print(f"writing page {pn} to {ofn}")
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        with open(ofn,"wb") as fop:
            writer.write(fop)

    

