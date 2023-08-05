from pathlib import Path
from autoxlsx import models
import yaml

def process(filemap: Path, update: Path, excelfile: Path):
    """Apply update parameters to excelfile"""
    #load yml to dict
    dictmap= yaml.load(filemap.read_text(),Loader=yaml.FullLoader)
    dictValues= yaml.load(update.read_text(),Loader=yaml.FullLoader)
    #apply changed using both information
    excelmap = models.ExcelMap.from_dict(dictmap)
    values = models.ExcelValue.from_dict(dictValues)
    excelmap.set_values(values)
    excelmap.write(excelfile)