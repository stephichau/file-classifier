# File Classifier

## Description

Project for Computer Science Department of the Pontificial Catholic University of Chile (PUC).

## Requirements

Developed in Python 3.7, dependency modules in `requirements.txt`

### Answer Sheet Maker

```md
[within upper level of project]
file_data.txt

{
    "course": "nameOfCourse",
    "evaluation": "nameOfEvaluation",
    "upper_bound": "upperBoundNumber",
    "lower_bound": "lowerBoundNumber",
    "template": "templateNameOfAnswerSheet",
    "semester": semesterNumber.oneOf([1, 2]),
    "year": yearOfCourse,
    "section": courseSection.oneOf([1, 2, ...nSections]),
    "instructor": "instructor'sLastName",
    "ocr": ocrToUse.oneOf(["qr", "text"]),
    "copies": numberOfCopiesOfEachAnswerSheet -- default to 1
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

### Classify Data

```md
[within upper level of project]
scanned_data.txt

{
    "year": "yyyy",
    "semester": oneOf(["1", "2"]),
    "course": "nameOfCourse",
    "evaluation": "nameOfEvaluation",
    "files": [
        {
            "nameOfQuestion": "pathToScannedQuestionFile"
        },
        {
            "nameOfQuestion": "pathToScannedQuestionFile"
        },
        .
        .
        .
    ],
    "ocr": oneOf(["qr", "text"]),
    "evaluation_sheet_id": "google_sheet_id"
}
```
