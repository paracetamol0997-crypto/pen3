from django.core.management.base import BaseCommand
from portal.models import Subject, User, Doubt, DoubtResponse

class Command(BaseCommand):
    help = "Seed initial subjects and demo users for testing"

    def handle(self, *args, **options):
        # 1. Seed Subjects
        subjects_data = [
            ("Mathematics", "MATH101", "Calculus, Linear Algebra, Probability and Discrete Math"),
            ("Physics", "PHY101", "Mechanics, Thermodynamics, Optics, and Electromagnetism"),
            ("Chemistry", "CHEM101", "Organic, Inorganic, and Physical Chemistry"),
            ("Computer Science", "CS101", "Programming, Algorithms, Data Structures and Systems"),
            ("Data Structures & Algorithms", "DSA102", "Arrays, Trees, Graphs, Sorting and Dynamic Programming"),
            ("English Communication", "ENG101", "Grammar, Technical Writing, and Professional Communication"),
        ]

        created_subjects = {}
        for name, code, desc in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=name,
                defaults={'code': code, 'description': desc}
            )
            created_subjects[name] = subject
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Subject: {name}"))

        # 2. Seed a sample Teacher if not exists
        math_subject = created_subjects.get("Mathematics")
        cs_subject = created_subjects.get("Computer Science")

        if not User.objects.filter(roll_number="T101").exists():
            teacher_math = User.objects.create(
                username="T101",
                roll_number="T101",
                full_name="Prof. Sharma (Maths)",
                role="teacher",
                subject=math_subject,
            )
            teacher_math.set_password("teacher123")
            teacher_math.save()
            self.stdout.write(self.style.SUCCESS("Created Demo Teacher: T101 (pass: teacher123) for Mathematics"))

        if not User.objects.filter(roll_number="T102").exists():
            teacher_cs = User.objects.create(
                username="T102",
                roll_number="T102",
                full_name="Dr. Priya Rao (CS)",
                role="teacher",
                subject=cs_subject,
            )
            teacher_cs.set_password("teacher123")
            teacher_cs.save()
            self.stdout.write(self.style.SUCCESS("Created Demo Teacher: T102 (pass: teacher123) for Computer Science"))

        # 3. Seed demo student as mentioned by user (pavan kumar - 323136410112)
        if not User.objects.filter(roll_number="323136410112").exists():
            student = User.objects.create(
                username="323136410112",
                roll_number="323136410112",
                full_name="Pavan Kumar",
                role="student",
            )
            student.set_password("123456")
            student.save()
            self.stdout.write(self.style.SUCCESS("Created Demo Student: 323136410112 (pass: 123456) for Pavan Kumar"))

            # Create a sample doubt for Pavan Kumar
            d1 = Doubt.objects.create(
                student=student,
                subject=cs_subject,
                title="What is the difference between BFS and DFS?",
                description="I am confused about when to use Breadth First Search vs Depth First Search in graph traversals. Can you please explain with a simple example?",
                status="pending"
            )

            d2 = Doubt.objects.create(
                student=student,
                subject=math_subject,
                title="How to solve non-homogeneous second-order differential equations?",
                description="I understand how to find the complementary function, but finding the particular integral for e^(ax) * sin(bx) is tricky. Please guide me.",
                status="answered"
            )

            teacher_math_user = User.objects.get(roll_number="T101")
            DoubtResponse.objects.create(
                doubt=d2,
                teacher=teacher_math_user,
                response_text="Hello Pavan,\nFor non-homogeneous equations, first find the roots of the auxiliary equation for CF. For PI with e^(ax)*v, use the shift theorem: (1 / f(D)) [e^(ax) * v] = e^(ax) * (1 / f(D+a)) [v]. We will also solve two practice problems in tomorrow's lecture!"
            )
            self.stdout.write(self.style.SUCCESS("Created sample doubts and answers for Pavan Kumar"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
