from django.db import models

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="наименование категории")
    description = models.TextField(**NULLABLE, verbose_name="описание")
    photo = models.ImageField(upload_to="catalog_photo/%Y/%m/%d/", **NULLABLE, verbose_name="фото")
    slug = models.CharField(max_length=150, **NULLABLE, verbose_name="URL")

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name="название продукта")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    photo = models.ImageField(upload_to="products_photo/%Y/%m/%d/", **NULLABLE, verbose_name="фото")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="категория",
    )
    price = models.PositiveIntegerField(verbose_name="цена за товар")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата изменения")
    slug = models.CharField(max_length=150, **NULLABLE, verbose_name="URL")

    def __str__(self):
        return (
            f"{self.name} {self.photo}"
            f"{self.description} {self.price} Руб."
            f"{self.created_at} {self.updated_at}"
        )

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
