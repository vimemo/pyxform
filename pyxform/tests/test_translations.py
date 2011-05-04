from unittest import TestCase
from pyxform.builder import SurveyElementBuilder

class TranslationTest(TestCase):

    def setUp(self):
        self.builder = SurveyElementBuilder()
        self.builder.set_translator(u"nigeria")

    def test_create_question_from_dict(self):
        d = {
            u"name": u"building_type",
            u"label": u"What type of school building is this?",
            u"type": u"text"
            }
        q = self.builder._create_question_from_dict(d)
        label_dict = {
            u"English": u"What type of school building is this?",
            u"Igbo": "Olee udiri ulo akwukwo bu nka?", 
            u"Yoruba": "Iru ile ile'we wo ni eyi.?", 
            u"Hausa": "Shin wannan wanne irin ginin makaranta ne?"
            }
        self.assertEquals(self.builder._translator.translate(d[u'label']),
                          label_dict)
        self.assertEquals(d[u'label'], label_dict)
        self.builder._translate_label(d)
        self.assertEquals(d[u'label'], label_dict)
        self.assertEquals(q.to_dict()[u'label'], label_dict)
