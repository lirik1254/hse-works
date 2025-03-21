from django.test import TestCase
from django.urls import reverse
from .models import Section, Page
from django.contrib.auth.models import User


class SectionDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.parent_section = Section.objects.create(
            title="Parent Section",
            slug="parent-section",
            is_hidden=False
        )
        self.subsection = Section.objects.create(
            title="Subsection",
            slug="subsection",
            parent=self.parent_section,
            is_hidden=False
        )
        self.hidden_subsection = Section.objects.create(
            title="Hidden Subsection",
            slug="hidden-subsection",
            parent=self.parent_section,
            is_hidden=True
        )
        self.page = Page.objects.create(
            title="Test Page",
            slug="test-page",
            content="Test Content",
            is_hidden=False,
            created_by=self.user.id,
            updated_by=self.user.id
        )
        self.page.sections.add(self.parent_section)
        self.hidden_page = Page.objects.create(
            title="Hidden Page",
            slug="hidden-page",
            content="Hidden Content",
            is_hidden=True,
            created_by=self.user.id,
            updated_by=self.user.id
        )
        self.hidden_page.sections.add(self.parent_section)

    def test_section_detail_view(self):
        """Проверка отображения раздела."""
        response = self.client.get(reverse('section_detail', kwargs={'slug': self.parent_section.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'handbook/section_detail.html')
        self.assertEqual(response.context['section'], self.parent_section)

        # Проверка контекста
        self.assertIn(self.subsection, response.context['subsections'])
        self.assertNotIn(self.hidden_subsection, response.context['subsections'])
        self.assertIn(self.page, response.context['pages'])
        self.assertNotIn(self.hidden_page, response.context['pages'])


class PageDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        self.section = Section.objects.create(
            title="Test Section",
            slug="test-section"
        )

        self.page = Page.objects.create(
            title="Test Page",
            slug="test-page",
            content="Test Content",
            is_hidden=False,
            created_by=self.user.id,
            updated_by=self.user.id
        )
        self.page.sections.add(self.section)  # Привязываем секцию к странице

        self.hidden_page = Page.objects.create(
            title="Hidden Page",
            slug="hidden-page",
            content="Hidden Content",
            is_hidden=True,
            created_by=self.user.id,
            updated_by=self.user.id
        )

    def test_page_detail_view(self):
        """Проверка отображения страницы."""
        response = self.client.get(reverse('page_detail', kwargs={'slug': self.page.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'handbook/page_detail.html')
        self.assertEqual(response.context['page'], self.page)


class SectionListViewTest(TestCase):
    def setUp(self):
        self.root_section = Section.objects.create(
            title="Root Section",
            slug="root-section",
            is_hidden=False
        )
        self.hidden_section = Section.objects.create(
            title="Hidden Section",
            slug="hidden-section",
            is_hidden=True
        )
        self.subsection = Section.objects.create(
            title="Subsection",
            slug="subsection",
            parent=self.root_section,
            is_hidden=False
        )

    def test_section_list_view(self):
        """Проверка отображения списка разделов."""
        response = self.client.get(reverse('section_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'handbook/section_list.html')

        # Проверка, что отображаются только корневые разделы
        self.assertIn(self.root_section, response.context['sections'])
        self.assertNotIn(self.hidden_section, response.context['sections'])
        self.assertNotIn(self.subsection, response.context['sections'])
