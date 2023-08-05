# README

When you need to carrefully fill-out an Excel file, it can be tricky.

It's even worse when the sheet is so ugly that it kind of burn your soul every time you open it.

This package try to tackle optimise that: writing plain yaml and never open the damn Excel file again.

## Install

```shell
pip install autoxlsx
```

## How to use

A simple workbook

**myugly.xlsx**

![excelTable](img/eg_simple.png)

`Name`,`function` & `age` are inputs others (E) are calculated by Excel formula.

### Write model

Usually people are picky about their excel format, so I expect this part to be quite static.

**Model.yaml**

```yaml
- sheetname: mysheet
  parameters:
    #that's an employee first name
    - parameter: "name"
      position: "C4"
    #here you have a function
    #note: nobody care
    - parameter: "function"
      position: "C5"
    #same nobody care but put something
    - parameter: "age"
      position: "C6"
```
### Write values

This part that will change often.

**Values.yaml**

```yaml
mysheet.name: Bob
mysheet.function: Sword man
mysheet.age: 42
```

The key use a dot notation to point to a specific value in the whole workbook. Note that parameter are defined in the `model.yaml`

### Update excel

Use the cli utility.

It will update inplace the excel file writing to the correct cells.

```shell
autoxlsx model.yaml values.yaml myugly.xlsx
```

## Example

See `tests/data/` for more example