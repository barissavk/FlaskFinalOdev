from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from app.models import Product, Category
from flask_login import current_user
from wtforms import validators
from flask import redirect, url_for, request




class MyModelView(ModelView):
    def is_accessible(self):
        # Yetkilendirme kontrolü yapılıyor
        # Örneğin, current_user.is_admin, kullanıcının yönetici olup olmadığını kontrol eden bir özellik olmalıdır
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

    def inaccessible_callback(self, name, **kwargs):
        # Erişim reddedildiğinde ne yapılacağını belirleyin
        # Örneğin, kullanıcıyı giriş sayfasına yönlendirin
        return redirect(url_for('auth.login', next=request.url))
    
class UserModelView(MyModelView):
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash"]
    column_searchable_list = ["username", "email"]

class ProductModelView(MyModelView):
    column_list = ('name', 'price', 'stock', 'category', 'brand')  # Gösterilecek sütunlar
    form_columns = ('name', 'description', 'price', 'stock', 'category', 'brand', 'image_url', 'color', 'size', 'weight', 'is_active')  # Düzenlenebilir sütunlar
    column_searchable_list = ('name', 'brand')  # Aranabilir sütunlar
    column_filters = ('category.name', 'brand')  # Filtrelenebilir sütunlar
    form_args = {
        'name': {
            'validators': [validators.DataRequired()]
        },
        'price': {
            'validators': [validators.NumberRange(min=0)]
        },
        'stock': {
            'validators': [validators.NumberRange(min=0)]
        }
    }

class CategoryModelView(MyModelView):
    column_list = ('name',)  # Gösterilecek sütunlar
    form_columns = ('name',)  # Düzenlenebilir sütunlar
    column_searchable_list = ('name',)  # Aranabilir sütunlar
    form_args = {
        'name': {
            'validators': [validators.DataRequired()]
        }
    }


