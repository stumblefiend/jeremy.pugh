---
title: "Reviewing content in a Google Drive"
permalink: "/google-drive.html"
---

*Learn how to run a Google Apps Script in a Google Spreadsheet to analyze documents in a Google Drive.*

- [Overview](#overview)
- [Step 1 - Create a Google Apps Script](#step-1---create-a-google-apps-script)
- [Step 2 - Analyze data](#step-2---analyze-data)
- [Related resources](#related-resources)

---

## Overview

Sometimes you need to assess content in a Google Drive to identify duplicate content, outdated content for archival, and content that is due for re-review and approval. One way to analyze your Google Drive is via a [Google Apps Script](). A Google Apps Script is......This guide provdes a sample script you can run.

For instance, if you run a Google Apps Script in a Google Sheet, you can have each the rows of the Sheet show data about each Google Doc in your Google Drive. Data for each document can include the last modified date, created date, and even, with a little ingenuity, the number of broken links in each doc. One piece of data you can't find via this method is the number of open comments on a document (can I add HTML to style this in blue as a tip?). 

After the script runs, you can determine which content to archive, consolidate, re-review, or flag for further audit. This guide shows both steps of this process:

- [Step 1 - Create a Google Apps Script](#step-1---create-a-google-apps-script)
- [Step 2 - Analyze data](#step-2---analyze-data)

---

## Step 1 - Create a Google Apps Script

Create and run a Google Apps Script using the following steps:

1. Open a new Google Sheet.
1. Click **Extensions**, and select **Apps Script**.
1. In the Apps Script window that appears, remove the default function code.

  ![Location of the default function code to delete](/assets/images/delete-default-code.png)

1. Copy and paste the following code into the Apps Script:

```
function listGoogleDocsInFolder(folder) {
  var files = folder.getFilesByType(MimeType.GOOGLE_DOCS); // Only looking at Documents, not spreadsheets, presentations, etc
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

Just use the Google Drive ID. Find the Google Drive ID by doing X. Add the script as an Apps Script by doing Y. It has some error detection in case you hit "Exception: Unexpected error while getting the method or property openById on object DocumentApp."

Here are examples of how you can use the data from the script.

Tell them to click the right space or whatever to run the script in. What if Google App script doesn't appear as an option? How do they install?

---



---

## Step 2 - Analyze Data

---

## Related resources

- [Google Apps Script reference documentation]()
