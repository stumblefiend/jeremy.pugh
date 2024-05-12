---
title: "Reviewing content in a Google Drive"
permalink: "/google-drive.html"
---

*Learn how to run a Google Apps Script in a Google Spreadsheet to analyze content in a Google Drive.*

- [Overview](#overview)
- [Step 1 - Create a Google Apps Script](#step-1---create-a-google-apps-script)
- [Step 2 - Analyze Spreadsheet Data](#step-2---analyze-spreadsheet-data)

---

## Overview

Sometimes you need to assess content in a Google Drive to identify duplicate content, outdated content for archival, and content that is overdue for re-review and approval. 

Use this as a Google Apps Script in a Google Spreadsheet to find the file name, last modified date, created date, and URL of all documents inside a folder or Google drive. Just use the Google Drive ID. Find the Google drive ID by doing X. Add the script as an Apps Script by doing Y. It has some error detection in case you hit "Exception: Unexpected error while getting the method or property openById on object DocumentApp."

Here are examples of how you can use the data from the script.

```
function listGoogleDocsInFolder(folder) {
  var files = folder.getFilesByType(MimeType.GOOGLE_DOCS);
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  while (files.hasNext()) {
    var file = files.next();
    try {
      var doc = DocumentApp.openById(file.getId());
      var creationDate = file.getDateCreated();
      var lastModified = file.getLastUpdated();
      var docUrl = doc.getUrl(); // Get the document URL

      sheet.appendRow([file.getName(), folder.getName(), creationDate, lastModified, docUrl]); // Append URL to the row
    } catch (e) {
      Logger.log("Error processing file: " + file.getName() + ", Error: " + e.toString());
    }
  }

  var subfolders = folder.getFolders();
  while (subfolders.hasNext()) {
    var subfolder = subfolders.next();
    listGoogleDocsInFolder(subfolder); // Recursively call the function for subfolders
  }
}

function listGoogleDocs() {
  var folderId = "0AKSQM_w_oOoAUk9PVA"; // Replace with the ID of the root folder
  var folder = DriveApp.getFolderById(folderId);
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  sheet.clear(); // Clear existing data
  sheet.appendRow(["Document Name", "Folder Name", "Created Date", "Last Modified Date", "Document URL"]); // Add URL column
  
  listGoogleDocsInFolder(folder);
}
```

---

## Step 1 - Create a Google Apps Script

---

## Step 2 - Analyze Spreadsheet Data
