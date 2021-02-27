from flask import render_template, session, request, redirect, url_for,flash
from shop import app, db
from shop.products.models import  Brand, Category, Addproduct
from sqlalchemy import func
from shop.customers.model import Type_user

def brands():
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()    
    return list(brands)

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return list(categories)
    
@app.route('/')
def index():
    page = request.args.get('page',1,type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(
        Addproduct.id.desc()).paginate(page=page, per_page=6)  
    
    #nao consegui substituir pela função
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()    
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()      
    return render_template('products/index.html',products=products,brands=brands,
                           categories=categories,segment='homeP')

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)    
    
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()    
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all() 
    return render_template('products/single_page.html',product=product,brands=brands,
                           categories=categories,segment='homeP')

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Please Login')         
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    max_stoke = db.session.query(func.sum(Addproduct.stock)).scalar()
    count = db.session.query(func.count(Addproduct.stock)).scalar()
    return render_template('admin/index.html',title='Admin Page',products=products,
                           max_stoke=max_stoke,count=count,segment='index',local='admin')

@app.route('/brand/<int:id>')
def get_brand(id):
    get_b = Brand.query.filter_by(id=id).first_or_404()
    page =request.args.get('page',1,type=int)
    brand = Addproduct.query.filter_by(brand=get_b).paginate(page=page, per_page=6)    
    
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()    
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all() 
    return render_template('products/index.html',brand = brand, brands=brands,categories=categories,
                           segment='homeP',get_b=get_b)

@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1,type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=6)  
    
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()    
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()  
    return render_template('products/index.html',get_cat_prod = get_cat_prod, categories=categories, 
                           brands=brands,get_cat=get_cat,segment='homeP')
    

@app.route('/brands')
def brands():
    if 'email' not in session:
        flash('Please Login') 
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brands.html',title="Brand Page",brands=brands,
                           segment='brand')

@app.route('/category')
def category():
    if 'email' not in session:        
        flash('Please Login') 
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brands.html',title="Brand Page",categories=categories,
                           segment='category')

@app.route('/typeuser',methods=['GET', 'POST'])
def type_user():
    if 'email' not in session: 
        flash('Please Login') 
        return redirect(url_for('login'))
    user_type = Type_user.query.order_by(Type_user.id.desc()).all()
    return render_template('admin/type_user.html',title="Tipos de usuarios",user_type=user_type,
                           segment="typeUser")

@app.route('/addtypeuser',methods=['GET', 'POST'])
def addtype_user():
    if request.method == 'POST':
        user_type = Type_user(type=request.form.get('type'))
        db.session.add(user_type)
        flash(f'Tipo dicionada')
        db.session.commit()
        return redirect(url_for('type_user'))
    return render_template('admin/addtype_user.html')
    

