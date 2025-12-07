from django.shortcuts import render, redirect
from datetime import date as _date, datetime, timedelta, timezone
from .forms import StudentForm, AttendanceForm, MarkForm
from .prisma_client import prisma_session


async def home(request):
    return render(request, "students/dashboard.html")


async def student_list(request):
    # Optional date filter (YYYY-MM-DD)
    selected_date_str = request.GET.get("date")
    selected_date = None
    if selected_date_str:
        try:
            selected_date = _date.fromisoformat(selected_date_str)
        except ValueError:
            selected_date = None

    # Fetch students
    async with prisma_session() as pdb:
        students = await pdb.student.find_many(order={"id": "asc"})

    # Build attendance status mapping for the selected date (or today by default)
    att_status = {}
    if selected_date is None:
        selected_date = _date.today()

    # Create UTC day range [start, next day)
    start_dt = datetime.combine(selected_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_dt = start_dt + timedelta(days=1)

    async with prisma_session() as pdb:
        attendances = await pdb.attendance.find_many(
        where={"date": {"gte": start_dt, "lt": end_dt}},
        include={"student": True},
    )
    for a in attendances:
        att_status[a.studentId] = a.status

    context = {
        "students": students,
        "att_status": att_status,
        "selected_date": selected_date.isoformat(),
        "today": _date.today().isoformat(),
    }
    return render(request, "students/student_list.html", context)


async def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            async with prisma_session() as pdb:
                await pdb.student.create(
                data={
                    "rollNumber": data["rollNumber"],
                    "firstName": data["firstName"],
                    "lastName": data["lastName"],
                    "email": data["email"],
                    "className": data["className"],
                }
            )
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "students/student_form.html", {"form": form})


async def attendance_list(request):
    async with prisma_session() as pdb:
        attendances = await pdb.attendance.find_many(
        include={"student": True}, order={"date": "desc"}
    )
    return render(
        request, "students/attendance_list.html", {"attendances": attendances}
    )


async def attendance_mark(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Prisma expects DateTime; convert date -> aware datetime (UTC midnight)
            dt = datetime.combine(data["date"], datetime.min.time()).replace(tzinfo=timezone.utc)
            async with prisma_session() as pdb:
                await pdb.attendance.create(
                data={
                    "studentId": data["studentId"],
                    "date": dt,
                    "status": data["status"],
                }
            )
            return redirect("attendance_list")
    else:
        student_id = request.GET.get("student_id")
        form = AttendanceForm(initial={"studentId": student_id})
    return render(request, "students/attendance_form.html", {"form": form})


async def marks_list(request):
    async with prisma_session() as pdb:
        marks = await pdb.mark.find_many(
        include={"student": True, "subject": True}, order={"id": "desc"}
    )
    return render(request, "students/marks_list.html", {"marks": marks})


async def _ensure_default_subjects(pdb):
    # Ensure common subjects exist
    subjects = [
        ("English", "ENG"),
        ("Math", "MAT"),
        ("Physics", "PHY"),
        ("Chemistry", "CHE"),
        ("ComputerScience", "CS"),
    ]
    for name, code in subjects:
        existing = await pdb.subject.find_unique(where={"name": name})
        if existing is None:
            try:
                await pdb.subject.create(data={"name": name, "code": code})
            except Exception:
                # Ignore races if created in between
                pass


async def marks_add(request):
    async with prisma_session() as pdb:
        await _ensure_default_subjects(pdb)
    if request.method == "POST":
        form = MarkForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            async with prisma_session() as pdb:
                await pdb.mark.create(
                data={
                    "studentId": data["studentId"],
                    "subjectId": data["subjectId"],
                    "examName": data["examName"],
                    "score": data["score"],
                }
            )
            return redirect("marks_list")
    else:
        # Pre-fill student if provided
        student_id = request.GET.get("student_id")
        initial = {"studentId": int(student_id)} if student_id else None
        form = MarkForm(initial=initial)

    async with prisma_session() as pdb:
        subjects = await pdb.subject.find_many(order={"name": "asc"})
    return render(request, "students/marks_form.html", {"form": form, "subjects": subjects})
