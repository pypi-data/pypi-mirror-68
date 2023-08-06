# This project's name has been changed to Ebuilder
We have renamed Ebuilder Ultra to Ebuilder in preperation for our web framework
named Ebuilder Ultra. Don't wory thought, this repo isn't going anywhere!
# Purpose
The purpose of this is to:<br>
  A) Give me a project to work on<br>
  B) Provide a simple static site generator using python<br>
# Installation
`pip install Ebuilder`
 # Simple Usage
 This first simple example would create a .html file with a h1 tag, centered and gray.
  
 ```
 from ebuilder.ebuilder_core import *
 
 index = newpage('index')
 title = header(index, "Hello GitHub!")
 title.center()
 title.color('gray')
 index.commit()
 ```
  
```
from ebuilder.ebuilder_core import EbuilderTextComponent as etc
  
header_two = etc("h2")
```
This second simple example would create a new Text Component with the html tag h2 which for those of you unfamiliar with 
html is the second biggest size of text that is included without further styling (h1 being the first)

You can then call this like you would header, because they both use the EbuilderTextComponent class.

Note that if you only import EbuilderTextComponent you wont be able to 
access the other functions of Ebuilder Ultra, like making a new page, it is shown here
because it is the most efficient way.

# Whats New in version 0.2.5
* Fixed bug in ebuilder_decorators that was stopping it from running.
# Advice Welcome
Feel free to dig through the source code and open Pull Requests and start issues, if you dig you'll see that EbuilderTextComponent 
has a bit of a weird implementation....
