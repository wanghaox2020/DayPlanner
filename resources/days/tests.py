from django.test import RequestFactory, TestCase
from resources.days.views import DayDetailView


# class ListViewTest(TestCase):
#     def test_get_queryset(self):
#         request = RequestFactory().get("/test1/")
#         view = DayListView()
#         view.setup(request)
#         view.get_queryset()


class DetailViewTest(TestCase):
    def test_set_in_context(self):
        request = RequestFactory().get("/1")
        view = DayDetailView()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn("detail", context)
