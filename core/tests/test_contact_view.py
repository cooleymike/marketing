from django.test import TestCase



class ContactTestCase(TestCase):
    def setUp(self):
        pass

    def test_new_contact_email_added(self):
        #prerequisites


        # execute function
        response = self.client.get('contact/')

        # check that expected outcome is correct
        self.assertEquals(response.status_code, 200)

