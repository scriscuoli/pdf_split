import argparse
from pypdf import PdfWriter,PdfReader
from pathlib import Path


def validate(inputPdfFile:str, inputPdfDir:str, outputDir:str):
    msg = ""
    ok = True
    intypes = 0
    if inputPdfFile != "":
        intypes = intypes + 1
        ifpath = Path(inputPdfFile)
        if not ifpath.is_file():
            ok = False
            msg = msg + f"{inputPdfFile} is not a file. "

    if inputPdfDir != "":
        intypes = intypes + 1
        idpath = Path(inputPdfDir)
        if not idpath.is_dir():
            ok = False
            msg = msg + f"{inputPdfDir} is not a directory. "  
          
    odpath = Path(outputDir)
    if not odpath.is_dir():
        ok = False
        msg = msg + f"{outputDir} is not a directory. "

    if intypes != 1:
        ok = False
        msg = msg + "You must specify one and only one input. "

    if not ok:
        print(msg)
    return ok

def padded(curVal: int, maxVal: int) -> str:
    width = len(str(maxVal))
    return str(curVal).zfill(width)

def split_file(inPdfFile:str, outDir:str, prefix:str):
    ipath = Path(inPdfFile)
    stem = ipath.stem
    reader = PdfReader(inPdfFile)
    pcount = len(reader.pages)
    opath = Path(outDir)
    print(f"{inPdfFile} has {pcount} page(s)...")
    for i in range(pcount):
        pn = i+1
        nfn = str(stem) + "_" + padded(pn,pcount) + ".pdf"
        ofn = opath / nfn
        print(f"writing page {pn} to {ofn}")
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        with open(ofn,"wb") as fop:
            writer.write(fop)

parser = argparse.ArgumentParser(description="A script that splits pdf files into separate page files.")
parser.add_argument("-i", "--input-dir", type=str, default="", help="name of input pdf file directory.")
parser.add_argument("-f", "--file", type=str, default="", help="name of single input pdf file.")
parser.add_argument("-o", "--output-dir", type=str, default=".", help="name of folder to write pdfs to.")
parser.add_argument("-p", "--prefix", type=str, default="", help="prefix for created file names.")

args = parser.parse_args()



if validate(args.file,args.input_dir,args.output_dir):

    if args.file != "":
        print(f"Processing: {args.file}")
        split_file(args.file, args.output_dir, args.prefix)

    if args.input_dir != "":
        directory = Path(args.input_dir)
        for  pdf_path in directory.glob('*.pdf'):
           fps = directory / pdf_path
           print(f"Processing: {fps}")
           split_file(fps,args.output_dir, args.prefix)

    

