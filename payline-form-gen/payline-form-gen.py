#!/usr/bin/python

import md5

payline_key_id = "5571335"
# You need to create this file yourself. Get the ID from the payline web app
# and save it into .payline_key_text. Don't check this in since the data
# should be hidden for security reasons.
with open(".payline_key_text") as f:
    payline_key_text = f.read().strip()

skus = (
    (
        "student-senior",
        "Student/Senior",
        25
    ),
    (
        "individual",
        "Individual",
        50
    ),
    (
        "family",
        "Family",
        75
    ),
    (
        "sponsor",
        "Sponsor",
        100
    ),
)

sku_mods = (
    (
        "first-month-",
        "FCCH Membership: First Month: ",
        0.5,
        0.00
    ),
    (
        "monthly-plan-",
        "FCCH Membership: Monthly: ",
        0.0,
        0.01
    ),
)

def gen_hash(params):
    names = ""
    vals = ""
    for (name, value) in params:
        names += name + "|"
        vals += value + "|"
    vals += payline_key_text
    plhash = md5.new()
    plhash.update(vals)
    return names + plhash.hexdigest()

for (sku, desc, value) in skus:
    for (sku_prefix, desc_prefix, value_scale, value_add) in sku_mods:
        sku_ex = sku_prefix + sku
        desc_ex = desc_prefix + desc
        value_ex = (value_scale * value) + value_add
        params = [
            ("key_id", "5571335"),
            ("action", "process_cart"),
            ("language", "en"),
            ("product_sku_1", sku_ex),
            ("product_description_1", desc_ex),
            ("product_amount_1", "%0.2f" % value_ex),
            ("url_continue", "http://www.fortcollinscreatorhub.org/?page_id=219"),
            ("url_cancel", "http://www.fortcollinscreatorhub.org/?page_id=219"),
            ("url_finish", "http://www.fortcollinscreatorhub.org/?page_id=263"),
            ("customer_receipt", "true"),
            ("merchant_receipt_email", "billing@fortcollinscreatorhub.org"),
        ]

        print '<form style="line-height: 0px;" action="https://secure.paylinedatagateway.com/cart/cart.php" method="POST">'
        for (param_name, param_value) in params:
            print '<input type="hidden" name="%s" value="%s" />' % (param_name, param_value)
        print '<input type="hidden" name="hash" value="%s" />' % gen_hash(params)
        print '<input type="image" src="/wp-content/uploads/2015/05/shopping-%s.png" alt="%s"/>' % (
            sku_ex, desc_ex)
        print '</form>'
        print
