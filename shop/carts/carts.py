
from flask import redirect, render_template, url_for, flash,request,session,current_app
from shop import db, app
from shop.products.models import Addproduct
from shop.admin.routes import brands,categories
from shop.products.models import  Brand, Category

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1 + dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart',methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == 'POST':
            DictItem = {product_id:{'name':product.name, 
                                    'price':str(product.price),
                                    'discount':product.discount,
                                    'quantity':int(quantity),
                                    'image':product.image_1}}
            
            if 'Shoppingcart' in session:
                if product_id in session['Shoppingcart']:                    
                    for key, item in session['Shoppingcart'].items():
                        print(session['Shoppingcart'].items())   
                        if int(key) == int(product_id): 
                            session.modified = True  
                            sumQtd = int(item['quantity']) + 1                          
                            item['quantity'] = sumQtd                       
                                                                                            
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItem)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItem
                return redirect(request.referrer)
        
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()    
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all() 
    
    if 'Shoppingcart' not in session :
        return redirect(request.referrer)
    
    subtotal = 0
    grandtotal = 0
    tax = 0
    for key, product in session['Shoppingcart'].items():        
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
        
    return render_template('products/carts.html',segment='homeP',tax=tax,grandtotal=grandtotal,
                           brands=brands,categories=categories)

@app.route('/updatecart/<int:code>',methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        try:
            session.modifield = True            
            for key,item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item alterado!')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
    
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('index'))
    try:
        for key,item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key,None)   
                session.medified = True                    
                if session['Shoppingcart']:
                    return redirect(url_for('getCart'))
                else:
                    return redirect(url_for('index'))                    
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart',None)
        return redirect(url_for('index'))
    except Exception as e:
        print(e)