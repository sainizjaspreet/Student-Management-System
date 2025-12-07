from django import forms


class StudentForm(forms.Form):
    _cls = "form-input border-2 border-blue-600 rounded-lg px-3 py-2 font-semibold bg-slate-50"
    rollNumber = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": _cls}))
    firstName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": _cls}))
    lastName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": _cls}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": _cls}))
    className = forms.CharField(label="Class", max_length=20, widget=forms.TextInput(attrs={"class": _cls}))


class AttendanceForm(forms.Form):
    _cls = "form-input border-2 border-blue-600 rounded-lg px-3 py-2 font-semibold bg-slate-50"
    studentId = forms.IntegerField(widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": _cls}))
    status = forms.ChoiceField(
        choices=[("Present", "Present"), ("Absent", "Absent")],
        widget=forms.RadioSelect(attrs={"class": "form-radio-group"}),
    )


class MarkForm(forms.Form):
    _cls = "form-input border-2 border-blue-600 rounded-lg px-3 py-2 font-semibold bg-slate-50"
    studentId = forms.IntegerField(widget=forms.HiddenInput())
    subjectId = forms.IntegerField(widget=forms.HiddenInput())
    examName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": _cls}))
    score = forms.IntegerField(min_value=0, max_value=100, widget=forms.NumberInput(attrs={"class": _cls}))

