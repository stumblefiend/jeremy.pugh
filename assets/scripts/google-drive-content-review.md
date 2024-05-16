---
title: "Reviewing content in a Google Drive"
permalink: "/google-drive.html"
---

*Learn how to run a Google Apps Script in a Google Sheet to assess Google Documents in a Google Drive.*

- [Overview](#overview)
- [Step 1 - Create a Google Apps Script](#step-1---create-a-google-apps-script)
- [Step 2 - Analyze data](#step-2---analyze-data)
- [Related resources](#related-resources)

---

### Overview

Need to see what duplicate and outdated content is in your Google Drive? Assess your Google Drive content via a [Google Apps Script](https://developers.google.com/apps-script/reference). Google Apps Script is JavaScript that lets you make applications that integrate with Gmail, Calendar, Drive, and other Google Workspace apps via built-in libraries. 

For instance, Google Apps Script can run in a Google Sheet to add data about each Google Doc in your Google Drive. Data for each document can include the last modified date, the created date, data from Google Analytics, or even the number of broken links in each doc. This guide provides a sample Google Apps Script you can run to retrieve details about the Google Docs in your Google Drive.

<div class="alert-cyan">
  <p><span style="font-size:larger;">✎</span>
  Google Apps Script can't show the number of open comments on a document.</p>
</div>
 
After the script runs, determine which content to archive, consolidate, or review. This guide shows both steps of this process:

- [Step 1 - Create a Google Apps Script](#step-1---create-a-google-apps-script)
- [Step 2 - Analyze data](#step-2---analyze-data)

---

### Step 1 - Create a Google Apps Script

<div class="alert-cyan">
  <p><span style="font-size:larger;">✎</span>
  When you first use a Google Apps Script, a pop-up window asks for access to your Google Drive.</p>
</div>

Create and run a Google Apps Script using the following steps:

1. Open a new Google Sheet.
2. Click **Extensions**, and select **Apps Script**.
3. In the Apps Script window that appears, remove the default function code.

    <figure>
        <img src="/assets/images/delete-default-code.png" class="image-border-medium" alt="Location of the default function code to delete.">
        <figcaption>Figure 1 - Default function code.</figcaption>
    </figure>

4. Copy and paste the following code into the Apps Script:

    ```javascript
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
      var folderId = "0AKSQM_w_oOoAUk9PVB"; // Replace with the ID of the root folder
      var folder = DriveApp.getFolderById(folderId);
      var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
      sheet.clear(); // Clear existing data
      sheet.appendRow(["Document Name", "Folder Name", "Created Date", "Last Modified Date", "Document URL"]); // Add URL column
  
      listGoogleDocsInFolder(folder);
    }
    ```
   
    <div class="alert-cyan">
      <p><span style="font-size:larger;">✎</span>
      This example Google Apps Script provides the document name, created date, last modified date, URL, and folder name only for Google Doc files.</p>
    </div>

6. To find the starting folder ID where you want to search for documents in each subfolder, click the Google Drive and note the ID after **folders/** in your browser's URL.

    <figure>
      <img src="/assets/images/find-folder-id.png" class="image-border-medium" alt="Location of the folder ID.">
      <figcaption>Figure 2 - Folder ID.</figcaption>
    </figure>

7. Replace the default folder ID `0AKSQM_w_oOoAUk9PVB` in the Apps Script with your starting folder ID.

8. Click the **Save project** icon.

    <figure>
      <img src="/assets/images/save-project-icon.png" class="image-border-medium" alt="Location of the Save project icon.">
      <figcaption>Figure 3 - Save project icon.</figcaption>
    </figure>

9. Ensure *listGoogleDocs* is selected for **Select function to run**.

    <figure>
      <img src="/assets/images/function-to-run.png" class="image-border-medium" alt="Location of the Select function to run icon.">
      <figcaption>Figure 4 - Select function to run icon.</figcaption>
    </figure>

10. Click **Run**.

    <figure>
      <img src="/assets/images/run-icon.png" class="image-border-medium" alt="Location of the Run icon.">
      <figcaption>Figure 5 - Run icon.</figcaption>
    </figure>

11. The **Execution log** appears and shows the Google Apps Script is running. Wait until the **Execution log** shows **Execution completed**.

    <figure>
      <img src="/assets/images/execution-complete.png" class="image-border-medium" alt="Location of the Execution complete message.">
      <figcaption>Figure 6 - Execution complete.</figcaption>
    </figure>

    <div class="alert-cyan">
      <p><span style="font-size:larger;">✎</span>
      It can take several minutes for the Google Apps Script to complete depending on the amount of content in the Google Drive.</p>
    </div>

12. [Analyze your data](#step-2---analyze-data).

---

### Step 2 - Analyze Data

When the Google sheet has data, seek answers to these questions:

- What documents need archival?
- Which content needs review and update?
- Which documents look duplicated?
- What content is in the wrong folder?
- What is the average time these documents were last modified?

#### Content to archive

Sort the Google Sheet by the oldest created date to identify outdated content. Also, review documents with **Copy of** at the beginning of the name.

For archival permission, identify the content owners by looking at the document details or version history. When you contact someone responsible for the content, ensure you are clear on whether you plan to delete the content or move it to an archive location. If you can't find an owner or the owner no longer works for your company, you can look at the document analytics to see when it was last viewed.

#### Outdated content

Create a formula in the cells of a new column of the Google Sheet that shows the number of days since a document was last modified. For instance, if the date you want to analyze is in cell D2 of the Google Sheet and the dates are in a format like *4/12/2024 16:11:38*, use this formula to find the number of days old the content is from the current date:

```
=DATEDIF(DATEVALUE(MID(D2, 1, FIND(" ", D2) - 1)), TODAY(), "D")
```

Drag the formula down to calculate the number of days old for the rest of your last modified dates. Then, sort by this new "days since last modified" data to find content over a year old(or whatever date you prefer) and make a plan to review the content further. Share your data with stakeholders to find the priority content to update.

Another useful way to use the "days since last modified" data is to average the days. The "average days since last modified" is a metric to measure and report on the health of the content in your Google Drive. 

#### Duplicate content

Check document names to ensure any naming standards are followed and to identify any duplicate content. Review any documents that cover similar topics or have similar names to see if content can be combined or archived.

#### Other uses

Use the folder name column to check if content is in the correct folders or to find duplicate folder structures.

---

### Troubleshooting the Google Apps Script

The example Google Apps Script in this guide has error detection for common errors such as *Unexpected error while getting the method or property openById on object DocumentApp.* This means script execution continues if certain common errors occur. However, you may encounter errors in other areas of code that need error handling. All errors appear in the **Execution log**.

When running the Google Apps Script, a common error is *TypeError: Cannot read properties of undefined*. This error means the wrong function to run is selected. Use the **Select function to run** dropdown to select *listGoogleDocs*.

If Google Apps script doesn't appear as an option in the *Extensions* of your Google Sheet, or you see errors not mentioned in this guide, [consult Google's Apps Script troubleshooting docs](https://developers.google.com/apps-script/guides/support/troubleshooting).

---

<!---
<details>
<summary>Click to open</summary>
<p>If your browser supports this element, it should allow you to expand and collapse these details.</p></details>

<div class="alert-orange">
  <p><span style="font-size:larger;">⚠</span>
If you french fry when you’re supposed to pizza, you’re gonna have a bad time.</p>
</div>
-->

### Related resources

- [Google Apps Script reference documentation]()
