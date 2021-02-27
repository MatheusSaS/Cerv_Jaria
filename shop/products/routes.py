from flask import redirect, render_template, url_for, flash,request,session,current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os

@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if request.method=="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'branda dicionada')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',brands='brand')

@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login','danger')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash('Seua Marca foi atualizada')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html',title='update brand',
                           updatebrand=updatebrand)
    
@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash('Marca deletada')
        return redirect(url_for('brands'))
    
    return redirect(url_for('admin'))
    
    
@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if request.method=="POST":
        getCat = request.form.get('category')
        cat = Category(name=getCat)
        db.session.add(cat)
        flash(f'Categoria Adicionada')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')

@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login','danger')
    updatecat = Category.query.get_or_404(id)
    cat = request.form.get('category')
    if request.method == "POST":
        updatecat.name = cat
        flash('Seua Categoria foi atualizada')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html',title='Update categoria',
                           updatecat=updatecat)

@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    cat = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(cat)
        db.session.commit()
        flash('Categoria deletada')
        return redirect(url_for('category'))
    
    return redirect(url_for('admin'))

@app.route('/addproduct',methods = ['GET','POST'])
def addproduct():
    try:
        brands = Brand.query.all()
        categories = Category.query.all()
        form = Addproducts(request.form)
        if request.method == "POST":
            name = form.name.data
            price = form.price.data
            discount = form.discount.data
            stock = form.stock.data
            desc = form.discription.data
            brand = request.form.get('brand')
            category = request.form.get('category')
            
            image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+ ".")
            image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+ ".")
            image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+ ".")
            
            addpro = Addproduct(name=name,price=price,discount=discount,stock=stock,desc=desc,
            brand_id=brand,category_id=category,image_1=image_1,image_2=image_2,image_3=image_3)
            
            db.session.add(addpro)        
            flash('Produto adicionado!')
            db.session.commit()
            return redirect(url_for('admin'))            
    except:
        flash('Não foi possivel inserir o produto!')
        db.session.rollback        
    
    return render_template('products/addproduct.html',title='Add produto',form=form,
                           brands=brands,categories=categories)
    
@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)    
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.desc = form.discription.data
        product.brand_id = brand
        product.category_id = category
        
        if request.files.get('image_1'):
            try:                
                os.unlink(os.path.join(current_app.root_path,"static/images/"+ product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+ ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+ ".")
                
        if request.files.get('image_2'):
            try:                
                os.unlink(os.path.join(current_app.root_path,"static/images/"+ product.image_1))
                product.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+ ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+ ".")
        
        if request.files.get('image_3'):
            try:                
                os.unlink(os.path.join(current_app.root_path,"static/images/"+ product.image_1))
                product.image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+ ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+ ".")
                
        
        db.session.commit()
        flash('Seu produto foi atualizado')
        return redirect(url_for('admin')) 
                
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.discription.data = product.desc
    
    
    return render_template('products/updateproduct.html',form=form,brands=brands,categories=categories,
                           product=product)
    
@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':   
        try:           
            os.unlink(os.path.join(current_app.root_path,"static/images/"+ product.image_1))                                     
            os.unlink(os.path.join(current_app.root_path,"static/images/"+ product.image_1))                      
            os.unlink(os.path.join(current_app.root_path,"static/images/"+ product.image_1))             
        except Exception as e:
            print(e)
            
        db.session.delete(product)
        db.session.commit()
        flash('Produto deletado!')
        return redirect(url_for('admin'))
    flash('Não foi possivel deletar o item!')
        
    return redirect(url_for('admin'))
    

