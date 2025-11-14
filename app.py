from flask import Flask, render_template, request, redirect, flash, session, url_for
import requests, os
from datetime import timedelta

app = Flask(__name__)
# Prefer a secret from environment; fallback to a development key
app.secret_key = os.environ.get("FLASK_SECRET", "supersecretkey")  # Needed for flash messages and session

# Session security configuration
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only (auto in production)
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Telegram config (recommend setting via environment variables in production)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8031877894:AAFqRcUIatER722OAsmYOjUjMfb1xuUmGWs")
CHAT_ID = os.environ.get("CHAT_ID", "@daraleng1234")

# --- Simple in-memory product catalog ---
PRODUCTS = [
    {"id": 1, "name": "Classic White T-Shirt", "price": 12.99, "description": "Soft cotton tee — comfortable and durable. Perfect for everyday wear.", "image": "https://www.trueclassictees.com/cdn/shop/files/TCT_4000_Short-Sleeve-Classic-Crew_WHITE_Large_Ecomm_2025_JUN_2.jpg?v=1762269520&width=750"},
    {"id": 2, "name": "Black Crew Neck Sweater", "price": 34.99, "description": "Cozy knit sweater made from premium wool blend. Ideal for layering.", "image": "https://www.trueclassictees.com/cdn/shop/files/4202_BLACK_2_498e9ba1-a813-43e9-a736-c6095cfd0288.jpg?v=1762284577&width=750"},
    {"id": 3, "name": "Denim Blue Jeans", "price": 49.99, "description": "Classic slim-fit jeans in durable denim. Timeless style for any occasion.", "image": "https://www.trueclassictees.com/cdn/shop/files/Authentic_Slim_Denim_Jeans_Light_Indigo_2_e203f3c5-ca5f-46ad-8263-251b65cc4620.jpg?v=1762281945&width=750"},
    {"id": 4, "name": "Casual Gray Hoodie", "price": 39.95, "description": "Warm and comfortable hoodie. Great for outdoor activities and relaxation.", "image": "https://www.trueclassictees.com/cdn/shop/files/TCT_4213_Waffle-Hoodie_CARBON_Large_Ecomm_2025_MAR_2.jpg?v=1762278615&width=750"},
    {"id": 5, "name": "Summer Floral Dress", "price": 44.99, "description": "Light and breathable dress perfect for warm seasons. Comfortable fit.", "image": "https://www.trueclassictees.com/cdn/shop/files/TCG_6501_Girls-LS-Fleece-Dress_Medium_Deep-Emerald_2025_OCT_JJ_3_hxttta_yr50k8.jpg?v=1760660796&width=750"},
    {"id": 6, "name": "White Button-Up Shirt", "price": 32.99, "description": "Crisp white shirt for work or casual wear. Quality cotton fabric.", "image": "https://www.trueclassictees.com/cdn/shop/files/4236_WHITE_2.jpg?v=1762279594&width=1420"},
    
]

def get_product(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


@app.context_processor
def cart_context():
    cart = session.get("cart", {})
    total_items = sum(cart.values()) if isinstance(cart, dict) else 0
    return dict(cart_item_count=total_items)


@app.context_processor
def global_context():
    # Provide small globals used by templates
    from datetime import datetime
    return {"current_year": datetime.utcnow().year}


@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        flash("Product not found", "danger")
        return redirect(url_for("index"))
    return render_template("product.html", product=product)


@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    items = []
    total = 0.0
    for pid_str, qty in cart.items():
        try:
            pid = int(pid_str)
        except ValueError:
            continue
        product = get_product(pid)
        if not product:
            continue
        subtotal = product["price"] * qty
        items.append({"product": product, "quantity": qty, "subtotal": subtotal})
        total += subtotal
    return render_template("cart.html", items=items, total=total)


@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    product_id = int(request.form.get("product_id", 0))
    qty = int(request.form.get("quantity", 1))
    product = get_product(product_id)
    if not product:
        flash("Product does not exist.", "danger")
        return redirect(url_for("index"))

    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + max(1, qty)
    session["cart"] = cart
    flash(f"Added {product['name']} to cart.", "success")
    return redirect(request.referrer or url_for("index"))


@app.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    product_id = request.form.get("product_id")
    cart = session.get("cart", {})
    if product_id and product_id in cart:
        cart.pop(product_id, None)
        session["cart"] = cart
        flash("Item removed from cart.", "success")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["POST"])
def checkout():
    # Simple checkout: summarize order, optionally send notification, then clear cart
    cart = session.get("cart", {})
    if not cart:
        flash("Your cart is empty.", "danger")
        return redirect(url_for("index"))

    # Build a summary message
    lines = ["New order received:"]
    total = 0.0
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = get_product(pid)
        if not product:
            continue
        subtotal = product["price"] * qty
        lines.append(f"- {product['name']} x{qty}: ${subtotal:.2f}")
        total += subtotal
    lines.append(f"Total: ${total:.2f}")

    text = "\n".join(lines)

    # Try to send Telegram notification (best-effort)
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text}
        requests.post(url, json=payload, timeout=5)
    except Exception:
        # non-fatal; continue
        pass

    # Clear cart and show success
    session.pop("cart", None)
    flash("✅ Your order has been placed. We will contact you shortly.", "success")
    return redirect(url_for("index"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/send", methods=["POST"])
def send():
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    subject = request.form.get("subject")
    message = request.form.get("message")

    # Create a neat Telegram message
    text = f"""
📩 <b>New Contact Message</b>
👤 <b>Name:</b> {full_name}
📧 <b>Email:</b> {email}
📞 <b>Phone:</b> {phone}
📝 <b>Subject:</b> {subject}
💬 <b>Message:</b> {message}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}

    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            flash("✅ Message sent successfully! We’ll get back to you soon.", "success")
        else:
            flash("⚠️ Failed to send message. Please try again later.", "danger")
    except Exception as e:
        flash("❌ Error: Could not connect to Telegram API.", "danger")
        print(e)

    return redirect(url_for("contact"))


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


# Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
