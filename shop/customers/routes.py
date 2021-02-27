from itertools import product
from flask import redirect, render_template, url_for, flash,request,session,make_response
from flask_login import login_required, current_user, logout_user,login_user
from stripe.api_resources import invoice
from shop import db, app, photos,bcrypt,login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Register, AddressDelivery,Type_user,CustomerOrder
import secrets, os
import stripe
import pdfkit


Publishablekey = 'pk_test_51IPTwHK1hJnLc6TzHoomPra3ByKtDGDJL5ieN2YAGIM81XF5XjrG6dlpfmRWvGPtLwjIJNT4d5uMdni1Hhx90r8w00JQaIMr20'
stripe.api_key = 'sk_test_51IPTwHK1hJnLc6Tzkl09DkLRtCP1HaSNPFmdkYVLefDzua2FknxucKK9IeNXW4Xfj1BEEcj60wduEGGiiaMi4Vop00hTVwGgzE'

@app.route('/payment', methods=['POST'])
@login_required
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Cerv-jaria',
        amount=amount,
        currency='brl',
    )
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id,invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Pago'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/thanks')
def thanks():
    return render_template('customer/register.html')

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    usert_type = Type_user.query.all()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data,username=form.username.data,email=form.email.data,
        password=hash_password,type_id=request.form.get('type'))
        
        db.session.add(register)
        flash('Seja Ben-vindo')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html',form=form,usert_type=usert_type)

@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):            
            user_type = Type_user.query.filter_by(id=user.type_id).first_or_404()
            session['email'] = user.email
            session['user'] = user.username
            session['user_type'] = user_type.type            
            login_user(user)
            flash('Logado!')
            next = request.args.get('next')
            return redirect(next or url_for('index'))
        flash('usuario incorreto','danger')
        return redirect(url_for('customerLogin'))
                
    return render_template('customer/login.html',form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    session.clear()
    return redirect(url_for('customerLogin'))

def updateshoppingcart():    
    for _key, product in session['Shoppingcart'].items():
        session.modified = True
        del product['image']
    return updateshoppingcart
    
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()
        try:
            order = CustomerOrder(invoice=invoice,customer_id=customer_id,
                                  orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('You order has been sent ')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order')
            return redirect(url_for('getCart'))
        
@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        gradTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax,subTotal=subTotal,
                grandTotal=grandTotal,customer=customer,orders=orders,segment='homeP')
    
@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        gradTotal = 0
        subTotal = 0
        customer_id = current_user.id
        
        if request.method == "POST":                    
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = float("%.2f" % (1.06 * subTotal))

            rendered = render_template('customer/pdf.html', invoice=invoice, tax=tax,
                    grandTotal=grandTotal,customer=customer,orders=orders,segment='homeP')
            pdf = pdfkit.from_string(rendered,False)
            response = make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition']='atteched; filename='+invoice+'.pdf'
            return response        
    return request(url_for('orders'))

@app.route('/user')
def user_page():
    user = Register.query.filter_by(email = session['email']).first()
    address = AddressDelivery.query.filter_by(Address_id = user.id).first()
    return render_template('customer/user_page.html',user=user,address=address,segment='homeP')

@app.route('/addaddress',methods=['GET','POST'])
def add_addres():
    if request.method == 'POST':
        user = Register.query.filter_by(email = session['email']).first()
        address = AddressDelivery(Address_id=user.id,country=request.form.get('country'),state=request.form.get('state'),
                                  city=request.form.get('city'),contact=request.form.get('contact'),address=request.form.get('address'),
                                  zipcode=request.form.get('zipcode'))
        db.session.add(address)
        flash('Endereço cadastrado')
        db.session.commit()
        
        return redirect(url_for('user_page'))
    return redirect(url_for('user_page'))
    
    
    