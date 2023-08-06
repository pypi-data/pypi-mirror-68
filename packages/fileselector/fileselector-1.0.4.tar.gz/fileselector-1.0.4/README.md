# Weather Reporter

A Python package to display all files in selected path,
Allowing the user to select what ever file they desire.

## Usage
```
#Imports FileSelector as fs.
import FileSelector as fs.

#path < folder you want to list.
#a,b < opening and closing characters, eg <1>,(1),[1]
#txt < Future versions will include keyboard controls, Txt/keyboard.
fs.PrintLocation(path, "a", "b", "txt")

#text < This will alter the visible text before Input()
#color < changes highlights colors, Pick from Colorama's Library  of colors.
#true/false < True Adds a confirmation  screen for the selected file.
fs.txt('text','color','true/false')

#returns the filepath selected by the user.
fs.filepath
```