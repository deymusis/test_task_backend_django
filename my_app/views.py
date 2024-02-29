from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from rest_framework import generics
from .models import Product, Lesson, Group, User
from .serializers import ProductSerializer, LessonSerializer

class HomeView(View):
    def get(self, request):
        return HttpResponse("Welcome!")

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class LessonListByProduct(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Lesson.objects.filter(product_id=product_id)

def distribute_users(product_id):
    # Получаем объект продукта или вызываем ошибку 404, если продукт не найден
    product = get_object_or_404(Product, pk=product_id)

    # Получаем все группы, принадлежащие к данному продукту
    groups = Group.objects.filter(product=product)

    # Получаем количество пользователей, зарегистрированных на данный продукт
    total_users_count = User.objects.filter(groups__product=product).count()

    # Рассчитываем среднее количество пользователей в каждой группе
    average_users_per_group = total_users_count // groups.count()

    # Рассчитываем остаток пользователей, которые не учтены при делении
    remainder = total_users_count % groups.count()

    # Перебираем все группы и распределяем пользователей
    for group in groups:
        # Получаем количество пользователей в текущей группе
        current_users_count = group.users.count()

        # Рассчитываем количество пользователей, которые могут быть добавлены в эту группу
        users_to_add = average_users_per_group
        if remainder > 0 and current_users_count < average_users_per_group + 1:
            users_to_add += 1
            remainder -= 1

        # Получаем максимальное и минимальное количество пользователей для этой группы
        max_users = group.max_users
        min_users = group.min_users

        # Ограничиваем количество пользователей, которые могут быть добавлены
        users_to_add = min(max_users - current_users_count, users_to_add)
        users_to_add = max(min_users - current_users_count, users_to_add)

        # Добавляем пользователей в группу
        for _ in range(users_to_add):
            # Получаем пользователя, которого нужно добавить в группу
            user_to_add = User.objects.filter(groups__isnull=True).first()

            # Проверяем, что нашли пользователя
            if user_to_add is not None:
                # Добавляем пользователя в группу
                group.users.add(user_to_add)
            else:
                # Если пользователь не найден, выводим сообщение об ошибке или выполняем другие действия
                print("Нет доступных пользователей для добавления в группу")
