from django.db import models


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_mail = models.CharField('Почта', unique=True, max_length=50)
    user_login = models.CharField('Логин', unique=True, max_length=50)
    user_password = models.CharField('Пароль', max_length=50)
    user_function = models.CharField('Роль', max_length=8)
    user_firstname = models.CharField('Имя', max_length=50, blank=True, null=True)
    user_lastname = models.CharField('Фамилия', max_length=50, blank=True, null=True)

    internship = models.ManyToManyField(
        "InternshipModel",
        verbose_name="Стажировки",
        blank=True
    )

    def __str__(self):
        return f"{self.user_id} - {self.user_login}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class InternshipModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    photo = models.ImageField("Фото", upload_to="internships/", blank=True, null=True)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    address = models.CharField("Адрес", max_length=255)
    contact = models.CharField("Контакт руководителя", max_length=100)
    additional_info = models.TextField("Дополнительная информация", blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.name}"

    def short_description(self):
        return self.description[:500] + "..." if len(self.description) > 500 else self.description

    class Meta:
        verbose_name = "Стажировка"
        verbose_name_plural = "Стажировки"