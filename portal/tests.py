from django.test import TestCase, Client
from django.urls import reverse
from portal.models import User, Subject, Doubt, DoubtResponse

class DoubtPortalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.subject_math = Subject.objects.create(name="Mathematics", code="MATH101")
        self.subject_cs = Subject.objects.create(name="Computer Science", code="CS101")

        # Student: Pavan Kumar
        self.student = User.objects.create_user(
            username="323136410112",
            roll_number="323136410112",
            full_name="Pavan Kumar",
            role="student",
            password="password123"
        )

        # Teacher: Prof Sharma (Maths)
        self.teacher_math = User.objects.create_user(
            username="T101",
            roll_number="T101",
            full_name="Prof Sharma",
            role="teacher",
            subject=self.subject_math,
            password="teacherpass"
        )

        # Teacher: Prof Priya (CS)
        self.teacher_cs = User.objects.create_user(
            username="T102",
            roll_number="T102",
            full_name="Prof Priya",
            role="teacher",
            subject=self.subject_cs,
            password="teacherpass"
        )

    def test_student_registration(self):
        # Register a new student without email or mobile
        response = self.client.post(reverse('student_register'), {
            'full_name': 'Rahul Sharma',
            'roll_number': '323136410199',
            'password': 'simplepass'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(roll_number='323136410199').exists())
        user = User.objects.get(roll_number='323136410199')
        self.assertEqual(user.full_name, 'Rahul Sharma')
        self.assertEqual(user.role, 'student')

    def test_teacher_registration(self):
        # Register teacher with subject
        response = self.client.post(reverse('teacher_register'), {
            'full_name': 'Dr. Alan Turing',
            'roll_number': 'T999',
            'subject': self.subject_cs.id,
            'password': 'simplepass'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(roll_number='T999').exists())
        teacher = User.objects.get(roll_number='T999')
        self.assertEqual(teacher.role, 'teacher')
        self.assertEqual(teacher.subject, self.subject_cs)

    def test_student_login_and_ask_doubt(self):
        # Login student
        login_res = self.client.post(reverse('student_login'), {
            'roll_number': '323136410112',
            'password': 'password123'
        }, follow=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertContains(login_res, 'Pavan Kumar')

        # Ask a doubt
        doubt_res = self.client.post(reverse('ask_doubt'), {
            'subject': self.subject_math.id,
            'title': 'How to calculate eigenvalue of 3x3 matrix?',
            'description': 'I have trouble finding characteristic roots for triangular matrices.'
        }, follow=True)
        self.assertEqual(doubt_res.status_code, 200)
        
        doubt = Doubt.objects.get(title='How to calculate eigenvalue of 3x3 matrix?')
        self.assertEqual(doubt.student, self.student)
        self.assertEqual(doubt.subject, self.subject_math)
        self.assertEqual(doubt.status, 'pending')

    def test_teacher_view_and_answer_doubt(self):
        # Create doubt in Mathematics
        doubt = Doubt.objects.create(
            student=self.student,
            subject=self.subject_math,
            title='Integration by parts issue',
            description='How do I choose u and v?',
            status='pending'
        )

        # Math teacher logs in
        self.client.post(reverse('teacher_login'), {
            'roll_number': 'T101',
            'password': 'teacherpass'
        })

        # Teacher views dashboard
        dash_res = self.client.get(reverse('teacher_dashboard'))
        self.assertContains(dash_res, 'Integration by parts issue')

        # Teacher answers the doubt
        ans_res = self.client.post(reverse('teacher_doubt_detail', args=[doubt.id]), {
            'response_text': 'Remember the ILATE rule: Inverse, Logarithmic, Algebraic, Trigonometric, Exponential.'
        }, follow=True)
        self.assertEqual(ans_res.status_code, 200)

        doubt.refresh_from_db()
        self.assertEqual(doubt.status, 'answered')
        self.assertEqual(doubt.responses.count(), 1)
        self.assertContains(ans_res, 'Remember the ILATE rule')

    def test_simultaneous_student_and_teacher_sessions(self):
        # 1. Student logs in
        student_res = self.client.post(reverse('student_login'), {
            'roll_number': '323136410112',
            'password': 'password123'
        })
        # Check student_sessionid cookie was set
        self.assertIn('student_sessionid', self.client.cookies)
        student_cookie = self.client.cookies['student_sessionid'].value

        # 2. Teacher logs in on the SAME client (browser)
        teacher_res = self.client.post(reverse('teacher_login'), {
            'roll_number': 'T101',
            'password': 'teacherpass'
        })
        # Check teacher_sessionid cookie was set
        self.assertIn('teacher_sessionid', self.client.cookies)

        # Both cookies exist simultaneously on the client
        self.assertEqual(self.client.cookies['student_sessionid'].value, student_cookie)

        # 3. Access student dashboard -> verifies student is still logged in
        sd_res = self.client.get(reverse('student_dashboard'))
        self.assertEqual(sd_res.status_code, 200)
        self.assertContains(sd_res, 'Pavan Kumar')

        # 4. Access teacher dashboard -> verifies teacher is also logged in
        td_res = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(td_res.status_code, 200)
        self.assertContains(td_res, 'Prof Sharma')

    def test_unregistered_user_login_messages(self):
        # 1. Unregistered student login
        res_student = self.client.post(reverse('student_login'), {
            'roll_number': '999999999999',
            'password': 'anypassword'
        }, follow=True)
        self.assertEqual(res_student.status_code, 200)
        self.assertContains(res_student, 'is not registered')
        self.assertContains(res_student, 'click here to register as a Student')

        # 2. Unregistered teacher login
        res_teacher = self.client.post(reverse('teacher_login'), {
            'roll_number': 'T_NONEXISTENT',
            'password': 'anypassword'
        }, follow=True)
        self.assertEqual(res_teacher.status_code, 200)
        self.assertContains(res_teacher, 'is not registered')
        self.assertContains(res_teacher, 'click here to register as a Teacher')

        # 3. Registered student with wrong password
        res_wrong_pw = self.client.post(reverse('student_login'), {
            'roll_number': '323136410112',
            'password': 'wrongpassword'
        }, follow=True)
        self.assertEqual(res_wrong_pw.status_code, 200)
        self.assertContains(res_wrong_pw, 'Incorrect password')
