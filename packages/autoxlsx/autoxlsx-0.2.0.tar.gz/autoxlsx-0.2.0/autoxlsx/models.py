from typing import List, Union
from openpyxl import load_workbook
from pathlib import Path
from dataclasses import dataclass
import logging


@dataclass
class Value:
    sheetname: str
    parameter: str
    value: Union[str, int, float]
    @classmethod
    def from_dict(cls, key, value):
        """make a CellUpdate from a dict
           using dot notation for key
           e.g. : `mysheet.name: "something"`
           """
        sheetname, parameter = key.split('.')
        return cls(sheetname=sheetname,
                   parameter=parameter,
                   value=value)


@dataclass
class ExcelValue:
    values: List[Value]
    @classmethod
    def from_dict(cls, data: dict):
        return cls([Value.from_dict(key, val) for key, val in data.items()])


@dataclass
class Column:
    start: int
    end: int
    # header name
    parameter: str
    # excel like columns A,B...
    position: str
            



@dataclass
class Loc:
    parameter: str
    position: str
    value: Union[str, int, float] = ''


@dataclass
class Sheet:
    sheetname: str
    parameters: List[Loc]
    @classmethod
    def from_dict(cls, data: dict):
        sheetname = data['sheetname']
        params = [Loc(**elt) for elt in data['parameters']]
        return cls(sheetname=sheetname, parameters=params)

    def set_value(self, parameter, value):
        for param in self.parameters:
            if param.parameter == parameter:
                param.value = value
                return
        raise ValueError(f'The parameter {parameter} does not exist')


@dataclass
class ExcelMap:
    sheets: List[Sheet]
    @classmethod
    def from_dict(cls, data: list):
        return cls(sheets=[Sheet.from_dict(elt) for elt in data])

    def set_values(self, params: ExcelValue):
        """assign values to Location"""
        for val in params.values:
            curr = self.get_sheet(val.sheetname)
            curr.set_value(val.parameter, val.value)

    def get_sheet(self, sheetname: str) -> Sheet:
        print(type(self.sheets[0]))
        for sheet in self.sheets:
            print(type(sheet))
            if sheet.sheetname == sheetname:
                return sheet
        raise ValueError(f'{sheetname} does not exist')

    def write(self, path: Path):
        wb = load_workbook(filename=path)
        for sheet in self.sheets:
            xlsx_sheet = wb[sheet.sheetname]
            for loc in sheet.parameters:
                xlsx_sheet[loc.position] = loc.value
        logging.info(f'writing to {path} updated values')
        wb.save(path)
