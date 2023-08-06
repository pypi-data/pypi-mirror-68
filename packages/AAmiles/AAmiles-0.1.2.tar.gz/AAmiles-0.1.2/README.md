# AAmiles

*Check changes in the miles required to obtain a ticket from the AA web page.*

## **Packages required:**

- request
- bs4
- numpy

## **Installation:**

```python
pip install AAmiles
```

## **Usage:**

```python
python -m AAmiles
```

## **To run it at loading of Windows 8 and 10:**

### **a) Create a batch file in some folder with:**

```batch
@echo off
python -m AAmiles
```

### **b) Then:**

1 - Create a shortcut to the batch file.

2 - Once the shortcut is created, right-click the shortcut file and select Cut.

3 - Press Start, type Run, and press Enter.

4 - In the Run window, type shell:startup to open the Startup folder.

5 - Once the Startup folder is opened, click the Home tab at the top of the folder and select Paste to paste the shortcut file into the Startup folder.
