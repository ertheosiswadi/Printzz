# Printer Client

## Overview
This is the code that will run on the Raspberry Pi to retrieve documents from the server for printing. The server will be polled at a configurable refresh time (currently 2 seconds) and checked for new files. If a file exists, it will be downloaded and sent to the wired printer.

##  Supported Features
| Feature | Support |
| ---|---|
|File Types|DOCX, PDF, TXT|
|Printer Options| # of Copies, Double-Sided, Color|
*<i>Table indicates current support. Additional features can be added.