from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask( __name__ )
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///myDatabase.db"
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy( app )



# users = {
#     "bob"   : { "name": "Bob Jones", "location": "Miami", "job": "Dentist"  },
#     "al"    : { "name": "Al Delcy", "location": "Orlando", "job": "Developer"  },
#     "tim"   : { "name": "Tim Smith", "location": "St. Pete", "job": "Mechanic"  },
#     "jack"  : { "name": "Jack Jones", "location": "Atlanta", "job": "Store Owner"  },
# }

# products = {
#     #   Build Product Inventory Dictionary Here
#     1 : { "name" : "banana", "price": 1.97, "desc": "Fresh and flavorful Yellow Banana.", "image": "https://www.kroger.com/product/images/xlarge/front/0000000004011" },
#     2 : { "name" : "milk", "price": 2.45, "desc": "Fresh and Organic Whole milk", "image": "https://www.stonyfield.com/wp-content/uploads/2017/02/stonyfield-organic-milk-half-gallon-whole-500x500-1.png" },
#     3 : { "name" : "eggs", "price": 4.39, "desc": "Fresh Cage free eggs from our farms.", "image": "https://solidstarts.com/wp-content/uploads/when-can-babies-eat-eggs-480x320.jpg" },
#     4 : { "name" : "beef", "price": 10.49, "desc": "The T-bone is a steak of beef cut from the short loin.", "image": "https://images-na.ssl-images-amazon.com/images/I/71Zdt55rIXL._SX425_.jpg" },
#     5 : { "name" : "toilet paper", "price": 6.59, "desc": "Soft and eco friendly toilet paper.", "image": "https://i.guim.co.uk/img/media/9698ea229567eb670114262459958ddc199b2cfa/0_28_4310_2586/master/4310.jpg?width=1200&quality=85&auto=format&fit=max&s=319e63ea5041283821a7a74ab68cadd2" },
#     6 : { "name" : "bread", "price": 4.99, "desc": "Gold steamy loaf of bread for the midnight cravings or a sandwich.", "image": "https://www.maangchi.com/wp-content/uploads/2021/03/pandemic-bread-scaled.jpg" },
# }

# mycart = []

class Category( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30) )
    desc = db.Column(db.Text)
    products = db.relationship('Product', backref = "category")
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

class Product( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30) )
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)
    image = db.Column(db.String( 300 ) )
    desc = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __init__(self, name, qty, price, image, desc, category):
        self.name = name
        self.qty = qty
        self.price = price
        self.image = image
        self.desc = desc
        self.category = category

@app.route( "/" )
def home():
    return render_template(  "index.html"  )
# Store CONTROLLER
# Show all products

@app.route( "/cart" )
def cart():
    return render_template( "cart.html", cart = mycart )

# T: Index ( Read All )
@app.route( "/store" )
def store():
    return render_template( "shop.html", inventory = Product.query.all() )

@app.route( "/add-to-cart", methods= ["POST"] )
def add_to_cart():
    product_id = request.form.get('product_id', None)
    qty = request.form.get('qty', 0)

    if product_id != None:
        product = products[ int(product_id) ]
        mycart.append( [product, float(qty)] )
        return redirect("/cart")

    return redirect("/store")

# C : Create
@app.route( "/add_product/", methods = ["GET","POST"] )
def add_product():
    if request.method == "POST":
        productTitle = request.form.get("product_title")
        productPrice = request.form.get("product_price")
        productDesc = request.form.get("product_desc")
        productQty = request.form.get("product_qty")
        productImage = request.form.get("product_image")

        category = Category.query.get( int( request.form.get("category_id" ) ))

        newProduct = Product( productTitle, productQty, productPrice, productImage, productDesc, {} )
        db.session.add(newProduct)
        db.session.commit()
        return redirect(f"/product/{newProduct.id}")
    else:
        categories = Category.query.all()
        return render_template("add_product.html", categories = categories)


# R : Read
@app.route( "/product/<product_id>" )
def product( product_id ):
    product = Product.query.get( int(product_id) )
    if product != None:
        return render_template("product.html", product = product)
    else:
        return render_template("notfound.html")

# U : Update
@app.route( "/update_product/<product_id>", methods = ["GET","POST"] )
def update_product(product_id):
    product = Product.query.get( int(product_id) )

    if request.method == "POST":
        if product != None:
            # Update the information of the product
            # return the "product.html" template and pass the single product
            product.name = request.form.get("product_title")
            product.qty = request.form.get("product_qty")
            product.desc = request.form.get("product_desc")
            product.price = request.form.get("product_price")
            product.image = request.form.get("product_image")

            return redirect(f"/product/{product.id}")
        else:
            return render_template("notfound.html")
    else:
        categories = Category.query.all()
        return render_template("update_product.html", product = product, categories = categories)

# D : Destroy/Delete
@app.route( "/delete_product/<product_id>" )
def delete_product( product_id ):
    product = Product.query.get( int(product_id) )
    if product != None:
        db.session.delete(product)
        db.session.commit()
        return redirect("/store")
    else:
        return render_template("notfound.html")

# CATEGORY

# I
@app.route( "/all_categories/" )
def all_categories():
    categories = Category.query.all()
    return render_template( "/category/categories.html", categories = categories )

# C
@app.route( "/add_category/", methods = ["GET","POST"])
def add_category():
    if request.method == "POST":
        categoryName = request.form.get("category_name")
        categoryDesc = request.form.get("category_desc")

        newCategory = Category( categoryName, categoryDesc )
        db.session.add(newCategory)
        db.session.commit()
        return redirect("/store")
    else:
        return render_template("/category/add_category.html")

# R
@app.route( "/category/<category_id>" )
def category( category_id ):
    category = Category.query.get( int(category_id) )
    if category != None:
        return render_template("/category/category.html", category = category)
    else:
        return render_template("notfound.html")

# U
@app.route( "/update_category/<category_id>", methods = ["GET","POST"] )
def update_category(category_id):
    category = Category.query.get( int(category_id) )

    if request.method == "POST":
        if category != None:
            # Update the information of the product
            # return the "product.html" template and pass the single product
            category.name = request.form.get("category_name")
            category.desc = request.form.get("category_desc")

            return redirect(f"/category/{category.id}")
        else:
            return render_template("notfound.html")
    else:
        return render_template("/category/update_category.html", category = category)

# D: Delete categories.
@app.route( "/delete_category/<category_id>" )
def delete_category( category_id ):
    category = Category.query.get( int(category_id) )
    if category != None:
        db.session.delete(category)
        db.session.commit()
        return redirect("/store")
    else:
        return render_template("notfound.html")


if __name__ == "__main__":
    app.run()