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
        "First Month",
        0.5,
        0.00,
        '2015/05',
        False
    ),
    (
        "single-month-",
        "Single Month",
        1.0,
        0.00,
        '2015/06',
        False,
    ),
    (
        "monthly-plan-",
        "Monthly",
        0.0,
        0.01,
        '2015/05',
        True
    ),
    (
        "one-year-",
        "One Year",
        11.0,
        0.0,
        '2015/06',
        False
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

def gen_form(action, sku, desc, value, media_upload_month, explain_text):
        params = [
            ("key_id", "5571335"),
            ("action", action),
            ("language", "en"),
            ("product_sku_1", sku),
            ("product_description_1", desc),
        ]
        if value:
            params += [
                ("product_amount_1", "%0.2f" % value),
            ]
        params += [
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
        print '<input type="image" src="/wp-content/uploads/%s/shopping-%s.png" alt="%s"/>' % (
            media_upload_month, sku, desc)
        print '</form>' + explain_text

for (sku, desc, value) in skus:
    print '<br/><h3>Add ' + desc + ' membership to cart</h3><br/>'

    for (sku_prefix, desc_prefix, value_scale, value_add, media_upload_month, monthly_plan) in sku_mods:
        sku_ex = sku_prefix + sku
        desc_ex = 'FCCH Membership: ' + desc_prefix + ': ' + desc
        value_ex = (value_scale * value) + value_add
        if monthly_plan:
            plan_text = ', $%0.2f every month' % value
        else:
            plan_text = ''
        explain_text = '$%0.2f one-time charge' % value_ex + plan_text
        gen_form('process_cart', sku_ex, desc_ex, value_ex, media_upload_month, explain_text)

print '<br/><h3>Make a donation</h3><br/>'
gen_form('process_variable', 'donate-now', 'FCCH: Donation', None, '2015/05', 'You choose the amount during checkout')
