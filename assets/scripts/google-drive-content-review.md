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

      sheet.appendRow([file.getName(), creationDate, lastModified, docUrl]); // Append URL to the row
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
  sheet.appendRow(["Document Name", "Created Date", "Last Modified Date", "Document URL"]); // Add URL column
  
  listGoogleDocsInFolder(folder);
}
```