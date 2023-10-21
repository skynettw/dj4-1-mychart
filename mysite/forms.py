from django import forms

class TextFileUploadForm(forms.Form):
    file = forms.FileField(label="文字檔案")
    