from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
    


class Customer(models.Model):
     user=models.OneToOneField(User, on_delete=models.CASCADE)
     full_name=models.CharField(max_length=200)
     address=models.CharField(max_length=200, null=True, blank=True)
     joined_on=models.DateTimeField(auto_now_add=True)

     def __str__(self):
      return self.full_name

class Category(models.Model):
   title = models.CharField(max_length=200)
   slug = models.SlugField(unique=True)

   def __str__(self):
    return self.title

class Product(models.Model):
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    marked_price = models.IntegerField()
    selling_price = models.IntegerField()
    image = models.ImageField(upload_to='products')
    view_count = models.PositiveIntegerField(default=0)
    warranty = models.CharField(max_length=300, null=True, blank=True)
    is_new = models.BooleanField(default=True)  # New field for specifying if the product is new or used

    def get_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)
     

ORDER_STATUS=[

('Order Recieved','Order Recieved'),
('Order Processing','Order Processing'),
('on the way','on the way'),
('Order Completed','Order Completed'),

]

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
    
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200 ,blank=True)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField(null=True, blank=True)
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)
    def _str_(self):
        return "Order: " +str(self.id)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1000)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'Review for {self.product.title} by {self.user.username}'
