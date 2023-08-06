# langer
Simple Flask translate tool.
Use langer_gui for edit in simple GUI

# Flask use Example
```python
#File start
import langer
langer.LANG = "en"
langer.LANGS = ["ru"]
langer.init()
#Your code...
@app.after_request # Registering middle-ware after response
def langer_translate(response): # 
	translate_lang = session.get("translate") # Checking selected language
	if langer: # If langer is imported
		try: # Trying to translate
			response = langer.translate_text(response, translate_lang) # response with translate_lang
		except:
			pass
	return response # Returning response
```
# In app use Example
```python
#File start
import langer
from langer import phrase as _
langer.LANG = "en"
langer.LANGS = ["ru"]
langer.init()
#Your code...
print(_('hello_world')) # or print(_('Hello world!'))
```
# Editing language files in app
```python
import langer
from langer import phrase as _
langer.LANGS = ["ru"]
langer.init()

l = langer.LangReader("en")
l["hello_world"] = "Hello World!"
# l.save() # Optional, default auto save enabled.
print(_('hello_world'))

```