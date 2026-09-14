from main.models import Experience

Experience.objects.all().delete()

Experience.objects.create(
    title="Asisten Dosen Dasar-Dasar Arsitektur Komputer (DDAK)",
    description="Assisted students in understanding the concepts and fundamentals of computer architecture during the Odd Semester of the 2026/2027 academic year.",
    category="part-time",
    ended_at=None,
)

Experience.objects.create(
    title="Member of Digital Product Design at RISTEK 2026",
    description="Developing UI design and user experience in Ristek's Product (Bikun Tracker) through testing, feedback, and iteration.",
    category="part-time",
    ended_at=None,
)

Experience.objects.create(
    title="VPIC of UI/UX at Open House Fasilkom UI 2026",
    description="Developed and maintained a cohesive UI/UX design system, including reusable components and visual guidelines to ensure consistency across Open House Fasilkom UI 2026. Led the UI/UX team through 3 design sprints, coordinating workflows, reviewing design outputs, and ensuring timely delivery of key design assets.",
    category="volunteer",
    ended_at=None,
)

print(f"Berhasil, total experience sekarang: {Experience.objects.count()}")