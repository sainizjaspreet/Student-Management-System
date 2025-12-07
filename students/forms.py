from django import forms


class StudentForm(forms.Form):
    rollNumber = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-input"}))
    firstName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-input"}))
    lastName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-input"}))
    className = forms.CharField(label="Class", max_length=20, widget=forms.TextInput(attrs={"class": "form-input"}))


class AttendanceForm(forms.Form):
    studentId = forms.IntegerField(widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-input"}))
    status = forms.ChoiceField(
        choices=[("Present", "Present"), ("Absent", "Absent")],
        widget=forms.RadioSelect(attrs={"class": "form-radio-group"}),
    )


class MarkForm(forms.Form):
    studentId = forms.IntegerField(widget=forms.HiddenInput())
    subjectId = forms.IntegerField(widget=forms.HiddenInput())
    examName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-input"}))
    score = forms.IntegerField(min_value=0, max_value=100, widget=forms.NumberInput(attrs={"class": "form-input"}))
