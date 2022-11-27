# from django.contrib.auth import mixins as auth_mixins
# from django.contrib.auth import views as auth_views

# UserModel = auth_views.get_user_model()


class ChoiceEnumMixin:
    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for name, _ in cls.choices())


# class SuperuserRequiredMixin(auth_mixins.UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_superuser
