import os
from django.contrib.auth.models import User
from django.test import TestCase, Client
from unittest.mock import patch
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime

class FileUploadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('upload_file')

    @patch('wastewatch.views.boto3.client')
    def test_upload_file(self, mock_s3_client):
        mock_upload_fileobj = mock_s3_client.return_value.upload_fileobj
        mock_upload_fileobj.return_value = 'Upload successful'

        with open('test_text.txt', 'w') as f:
            f.write('This is a test file.')

        with open('test_text.txt', 'rb') as f:
            response = self.client.post(self.upload_url, {'text_file': f}, format='multipart')

        self.assertEqual(response.status_code, 200)

        os.remove('test_text.txt')

    @patch('wastewatch.views.boto3.client')
    def test_upload_png_file(self, mock_s3_client):
        mock_upload_fileobj = mock_s3_client.return_value.upload_fileobj
        mock_upload_fileobj.return_value = 'Upload successful'

        with open('test_image.png', 'wb') as f:
            f.write(os.urandom(1024))

        with open('test_image.png', 'rb') as f:
            response = self.client.post(self.upload_url, {'image_file': f}, format='multipart')

        self.assertEqual(response.status_code, 200)

        os.remove('test_image.png')

    @patch('wastewatch.views.boto3.client')
    def test_upload_pdf_file(self, mock_s3_client):
        mock_upload_fileobj = mock_s3_client.return_value.upload_fileobj
        mock_upload_fileobj.return_value = 'Upload successful'

        with open('test_document.pdf', 'wb') as f:
            f.write(
                b'%PDF-1.4\n%\xe2\xe3\xd7\xd3\n1 0 obj\n<</Type/Catalog/Pages 2 0 R/Lang(en-US)>>\nendobj\n')

            with open('test_document.pdf', 'rb') as f:
                response = self.client.post(self.upload_url, {'pdf_file': f}, format='multipart')

        self.assertEqual(response.status_code, 200)

        os.remove('test_document.pdf')



class LoginTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_user_notadmin (self):
        response = self.client.get(reverse('admin_page'))
        self.assertEqual(response.status_code, 403)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_submit_report(self):
        self.client.login(username='testuser', password='12345')
        data = {
            'title': 'Test Report',
            'description': 'This is a test report',
            'date': datetime.now(),
            'file': SimpleUploadedFile('test_file.pdf', b'PDF content here', content_type='application/pdf'),
            'latitude': '38.035192',
            'longitude': '-78.503805',
        }
        response = self.client.post(reverse('upload_file'), data)
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.user.delete()


from django.test import TestCase
from django.contrib.auth.models import User

class AdminTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.client.login(username='admin', password='adminpassword')

    def test_admin_access(self):
        response = self.client.get(reverse('admin_page'))
        self.assertEqual(response.status_code, 200)

    def test_admin_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_admin_submit_report(self):
        data = {
            'title': 'Test Report',
            'description': 'This is a test report',
            'date': datetime.now(),
            'file': SimpleUploadedFile('test_file.pdf', b'PDF content here', content_type='application/pdf'),
            'latitude': '38.035192',
            'longitude': '-78.503805',
        }
        response = self.client.post(reverse('upload_file'), data)
        self.assertEqual(response.status_code, 302)

    def test_admin_report_resolved_success(self):
        response = self.client.get(reverse('report_resolved_success'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()




