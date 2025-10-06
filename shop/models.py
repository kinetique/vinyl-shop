from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='albums')
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField()

    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password_hash = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')


class CartItem(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, related_name='cart_items')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
