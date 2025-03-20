from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from .models import StaticPage
from .admin import StaticPageAdmin


class StaticPageDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.page = StaticPage.objects.create(
            title="Test Page",
            slug="test-page",
            content="Test Content",
            is_hidden=False,
            created_by=self.user.id,
            updated_by=self.user.id
        )
        self.hidden_page = StaticPage.objects.create(
            title="Hidden Page",
            slug="hidden-page",
            content="Hidden Content",
            is_hidden=True,
            created_by=self.user.id,
            updated_by=self.user.id
        )

    def test_static_page_detail_view(self):
        """Проверка отображения статической страницы."""
        response = self.client.get(reverse('static_page_detail', kwargs={'slug': self.page.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'static_pages/static_page_detail.html')
        self.assertEqual(response.context['page'], self.page)

    def test_hidden_static_page_detail_view(self):
        """Проверка, что скрытая страница не отображается."""
        response = self.client.get(reverse('static_page_detail', kwargs={'slug': self.hidden_page.slug}))
        self.assertEqual(response.status_code, 404)


class StaticPageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_create_static_page(self):
        """Проверка создания статической страницы."""
        page = StaticPage.objects.create(
            title="Test Page",
            slug="test-page",
            content="Test Content",
            is_hidden=False,
            created_by=self.user.id,
            updated_by=self.user.id
        )
        self.assertEqual(page.title, "Test Page")
        self.assertEqual(page.slug, "test-page")
        self.assertEqual(page.content, "Test Content")
        self.assertFalse(page.is_hidden)

    def test_hidden_static_page(self):
        """Проверка, что скрытая страница не отображается."""
        page = StaticPage.objects.create(
            title="Hidden Page",
            slug="hidden-page",
            content="Hidden Content",
            is_hidden=True,
            created_by=self.user.id,
            updated_by=self.user.id
        )
        self.assertTrue(page.is_hidden)


class StaticPageAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = StaticPageAdmin(StaticPage, self.site)
        self.user = User.objects.create_user(username="testuser", password="testpass123", is_staff=True)
        self.factory = RequestFactory()

    def test_save_model(self):
        """Проверка, что created_by и updated_by заполняются автоматически."""
        request = self.factory.get('/admin/')
        request.user = self.user

        # Создаем страницу
        page = StaticPage(title="Test Page", slug="test-page", content="Test Content")
        self.admin.save_model(request, page, None, False)

        # Проверяем, что created_by и updated_by заполнены
        self.assertEqual(page.created_by, self.user.id)
        self.assertEqual(page.updated_by, self.user.id)

        # Обновляем страницу
        page.title = "Updated Page"
        self.admin.save_model(request, page, None, True)

        # Проверяем, что updated_by обновлён
        self.assertEqual(page.updated_by, self.user.id)

    def test_get_readonly_fields(self):
        """Проверка, что created_by и updated_by доступны только для чтения."""
        request = self.factory.get('/admin/')
        request.user = self.user

        # Проверяем, что поля доступны только для чтения
        readonly_fields = self.admin.get_readonly_fields(request)
        self.assertIn('created_by', readonly_fields)
        self.assertIn('updated_by', readonly_fields)
