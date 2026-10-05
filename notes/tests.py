from django.test import TestCase
from django.urls import reverse
from .models import Note, Category

# Create your tests here.

class NoteCreateEditTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Тестова категорія")
        
        self.note = Note.objects.create(
            title="Стара назва",
            text="Старий текст",
            category=self.category
        )
        
        self.create_url = reverse('note_create')
        self.edit_url = reverse('note_edit', args=[self.note.pk])
        self.home_url = reverse('home_text')

    def test_note_create_saves_data(self):
        """Тестуємо збереження нової нотатки через POST-запит (функція note_create)[cite: 15]"""
        data = {
            'title': 'Нова тестова нотатка',
            'text': 'Текст нової нотатки',
            'category': self.category.pk,
        }
        
        response = self.client.post(self.create_url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        
        self.assertTrue(Note.objects.filter(title='Нова тестова нотатка').exists())

    def test_note_edit_updates_data(self):
        """Тестуємо оновлення існуючої нотатки через POST-запит (функція note_edit)[cite: 16]"""
        data = {
            'title': 'Оновлена назва',
            'text': 'Оновлений текст',
            'category': self.category.pk,
        }
        
        response = self.client.post(self.edit_url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Оновлена назва')
        self.assertEqual(self.note.text, 'Оновлений текст')