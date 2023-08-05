from pathlib import Path
from autoxlsx import models
from typing import List, Iterator
import yaml

def is_table(filemap:list)->bool:
    return 'columns' in filemap[0]

def is_unit(filemap:list)->bool:
    return 'parameters' in filemap[0]

def process(filemap: Path, update: Path, excelfile: Path):
    dictmap = yaml.load(filemap.read_text(), Loader=yaml.FullLoader)
    if is_table(dictmap):
        print('process table model')
        process_table(filemap, update, excelfile)
    elif is_unit(dictmap):
        print('process unit model')
        process_unit(filemap, update, excelfile)
    else:
        raise ValueError(f"{filemap} format not reconized")

def process_unit(filemap: Path, update: Path, excelfile: Path):
    """Apply update parameters to excelfile"""
    # load yml to dict
    dictmap = yaml.load(filemap.read_text(), Loader=yaml.FullLoader)
    dictValues = yaml.load(update.read_text(), Loader=yaml.FullLoader)
    # apply changed using both information
    excelmap = models.ExcelMap.from_dict(dictmap)
    values = models.ExcelValue.from_dict(dictValues)
    excelmap.set_values(values)
    excelmap.write(excelfile)


def from_range(cols: List[models.Column],
               values: list) -> Iterator[models.Loc]:
    """Generate location for table-like range"""
    def get_col(parameter):
        res = [col for col in cols if col.parameter == parameter]
        if res:
            return res[0].position
    currentrow = cols[0].start
    for elt in values:
        for key, value in elt.items():
            if get_col(key):
                yield models.Loc(key, f'{get_col(key)}{currentrow}', value)
        currentrow += 1

def sheet_fromrange(sheet:dict,values:list)->models.Sheet:
    start = sheet["rows"]["start"]
    end=sheet["rows"]["end"]
    cols = [models.Column(start,end,**col) for col in sheet["columns"]]
    locs = from_range(cols,values)
    return models.Sheet(sheet["sheetname"],list(locs))

def process_table(modelfile: Path, valuesfile: Path, excelfile: Path):
    # load yml to dict
    model_conf = yaml.load(modelfile.read_text(), Loader=yaml.FullLoader)
    values_conf = yaml.load(valuesfile.read_text(), Loader=yaml.FullLoader)
    sheets = []
    for sheet in model_conf:
        sheetname = sheet["sheetname"]
        values = [val for val in values_conf if val["sheetname"]==sheetname]
        if len(values)!=0:
            sheets.append(sheet_fromrange(sheet,values[0]["values"]))
    print(sheets) 
    model = models.ExcelMap(sheets)
    model.write(excelfile)




    model = models.ExcelMap(sheets)
    # apply `values` according to `model` to `excelfile`
    model.write(excelfile)
    pass
