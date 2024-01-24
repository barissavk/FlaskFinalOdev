from flask import render_template, redirect, url_for, request, flash
from app import app, db
from flask_login import current_user, login_required
from app.models import Product, Comments, AboutFooter, Cart,CartItem,Contact
from app.forms import ContactForm, NewsletterForm

@app.route('/')
def index():
    products = Product.query.all()
    product_len = len(products)
    clients = Comments.query.all()
    about = AboutFooter.query.all()
    return render_template('index.html', products=products, clients = clients,product_len=product_len, about=about)

@app.route('/about')
def about():
    about = AboutFooter.query.all()
    return render_template('about.html', about=about)

@app.route('/contact', methods=["GET", "POST"])
def contact():
    about = AboutFooter.query.all()
    contact_form = ContactForm()  # Form nesnesini doğru şekilde oluşturun

    if contact_form.validate_on_submit():
        # Form verilerini al
        name = contact_form.name.data
        email = contact_form.email.data
        message = contact_form.message.data

        # Veritabanına yeni bir ileti ekle
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        flash('Message sent successfully!', 'success')  # İsteğe bağlı: Flash mesaj ekleme

        return redirect(url_for('contact'))

    # Diğer kodlar burada...

    return render_template('contact.html', about=about, contact=contact_form, newsletter=NewsletterForm())

@app.route('/client')
def client():
    clients = Comments.query.all()
    about = AboutFooter.query.all()
    return render_template('client.html', clients = clients, about=about)

@app.route('/products')
def products():
    products = Product.query.all()
    product_len = len(products)
    about = AboutFooter.query.all()
    return render_template('products.html', products=products,product_len=product_len, about=about)

@app.route("/purchase/<int:id>", methods=['POST'])
@login_required
def purchase_product(id):
    # Kullanıcı girişi kontrolü
    user_id = current_user.get_id()
    username = current_user.username

    # Sepet işlemleri burada gerçekleşecek
    # Örneğin: ürün stokta var mı gibi kontrol etmeler yapılabilir
    # Bu örnekte sadece basit bir ekleme yapılacak

    # Kullanıcının sepetini kontrol et
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        # Kullanıcının sepeti henüz boşsa, yeni bir sepet oluştur
        new_cart = Cart(user_id=user_id,username=username)
        db.session.add(new_cart)
        db.session.commit()

    # Önce ürünü veritabanından al
    product = Product.query.get_or_404(id)

    # Kullanıcının sepetinde bu ürün var mı kontrol et
    cart_item = CartItem.query.filter_by(cart_id=user_id, product_id=product.id).first()

    if cart_item:
        # Kullanıcının sepetinde varsa, miktarı artır
        cart_item.quantity += 1
    else:
        # Yoksa yeni bir sepet öğesi oluştur
        new_cart_item = CartItem(cart_id=user_id, product_id=product.id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()

    return redirect(url_for('cart'))  # sepete götür

@app.route("/remove_from_cart/<int:id>", methods=['POST'])
@login_required
def remove_from_cart(id):
    # Kullanıcı girişi kontrolü yapılıyor
    user_id = current_user.get_id()

    # Kullanıcının sepetini al
    cart = Cart.query.filter_by(user_id=user_id).first()

    # Sepet öğesini bul
    cart_item = CartItem.query.filter_by(cart_id=user_id, product_id=id).first()

    if cart_item:
        # Sepet öğesini veritabanından kaldır
        db.session.delete(cart_item)
        db.session.commit()

    return redirect(url_for('cart'))


@app.route("/cart")
@login_required
def cart():
    about = AboutFooter.query.all()
    # Kullanıcı girişi kontrolü yapılıyor
    user_id = current_user.get_id()

    # Kullanıcının sepet içeriğini al
    cart_items = CartItem.query.filter_by(cart_id=user_id).all()

    return render_template('cart.html', cart_items=cart_items,about=about)

@app.route('/search')
def search():
    about = AboutFooter.query.all()
    query = request.args.get('query', '')
    # Burada arama işlemlerini gerçekleştirin ve sonuçları döndürün
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    
    product_len = len(products)
    # Daha sonra bu sonuçları şablonunuza geçirerek render_template kullanabilirsiniz
    return render_template('products_search.html', query=query, products=products,about=about,product_len=product_len)