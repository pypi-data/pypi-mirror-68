
# Changelog

Here we list the history of changes in remo across the various releases.


## Coming up in the next release

Improvements to data upload:

  - allow to see upload progress
  - summary of upload results, including breakdown of any error

---
## v0.3.41 - 8 May 20

**Main Changes**

Switched to PostgresSQL for database management, instead of SQLlite. This makes the whole app more responsive and reliable.
For the rest, we implemented a number of small fixes aimed at making making remo more robust

**Breakdown**

Bug fixes:

* Fixed annotation statistics inconsistencies for image classification
* Fixed sending feedback form
* Fixed autologin in browser, and in electron after user changes password
* Fixed rename annotation set
* Fixed export annotation form - missing annotation set name
* Fixed Windows installation in conda env - pip failed to install package
* Fixed duplicate annotation objects

Changes:

* Added support for PostgresSQL as main database
* Improved duplicate annotation set flow
* After annotations uploaded - images marked as annotated
* Improved create annotation set flow
* Improved save annotations behaviour
* Improved data uploading and parsing - moved it to a separate process, which allows to use remo while long uploads are in progress
* Added ability to bulk delete annotations for an image in annotation tool
* Added ability to mark image as TODO in annotation tool
* Improved description of installation steps. Also we are now asking user for explicit permission to install PostgresSQL and additional packages
