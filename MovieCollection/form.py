from django import forms

class MovieForm(forms.Form):
    title = forms.CharField(max_length=200)
    cover = forms.ImageField()
    category = forms.CharField(max_length=100)
    actors = forms.MultipleChoiceField(choices=[])

    # 添加适当的验证规则和自定义方法
