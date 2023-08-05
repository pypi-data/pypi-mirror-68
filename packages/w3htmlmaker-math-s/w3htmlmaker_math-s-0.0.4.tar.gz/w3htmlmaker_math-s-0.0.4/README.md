
# This is a HTML maker for articles. 
If you have a text and need to publish it you can use this pkg.
You install with:
```
 pip install -i https://test.pypi.org/simple/ w3htmlmaker-math-s==0.0.3
```
And then, if **a** is the Object, you can define:
```
a_html = HtmlArticle(a.content, a.title).get_html()
```
a_html now contains a valid HTML, using w3.css library. 
Now you just have to send **a_html** to your template, or write it down in a HTML file.
