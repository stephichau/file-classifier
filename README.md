# File Classifier

## Description

Project for Computer Science Department of the Pontificial Catholic University of Chile (PUC).

## Requirements

Developed in Python 3.7, dependency modules in `requirements.txt`

### Answer Sheet Maker

```md
[within upper level of project]
qr_data.txt

{
    "course": "nameOfCourse",
    "evaluation": "nameOfEvaluation",
    "upper_bound": "upperBoundNumber",
    "lower_bound": "lowerBoundNumber",
    "template": "templateNameOfAnswerSheet"
}

```

```md
[within upper level of project] TEMPLATES directory

[./TEMPLATES/*] store template files that are indicated in qr_data.txt

```

### Google Sheets

```md
--preliminary
[within google_sheets directory level]
sheets_data.txt

{
    "evaluation_name": "",
    "course": "courseId",
    "evaluation_sheet_id": "spreadsheetId"
}

To get spreadsheetId:
https://docs.google.com/spreadsheets/d/:spreadsheetId:/

```
