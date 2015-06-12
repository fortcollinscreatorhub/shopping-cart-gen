#!/usr/bin/python

# Copyright (c) 2015, Stephen Warren.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# Neither the name Stephen Warren, the name Fort Collins Creator Hub, nor the
# names of this software's contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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

        print '<td><form style="line-height: 0px;" action="https://secure.paylinedatagateway.com/cart/cart.php" method="POST">'
        for (param_name, param_value) in params:
            print '<input type="hidden" name="%s" value="%s" />' % (param_name, param_value)
        print '<input type="hidden" name="hash" value="%s" />' % gen_hash(params)
        print '<input type="image" src="/wp-content/uploads/%s/shopping-%s.png" alt="%s"/>' % (
            media_upload_month, sku, desc)
        print '</form>' + explain_text + '</td>'

print '''\
<table>	
<tbody>
<tr><td colspan="2"><h3>Cart</h3></td></tr>
<tr>
<td><form style="line-height: 0px;" action="https://secure.paylinedatagateway.com/cart/cart.php" method="post">
<input name="key_id" type="hidden" value="5571335" />
<input name="action" type="hidden" value="show_cart" />
<input name="language" type="hidden" value="en" />
<input name="url_continue" type="hidden" value="http://www.fortcollinscreatorhub.org/?page_id=219" />
<input name="url_cancel" type="hidden" value="http://www.fortcollinscreatorhub.org/?page_id=219" />
<input name="url_finish" type="hidden" value="http://www.fortcollinscreatorhub.org/?page_id=263" />
<input name="customer_receipt" type="hidden" value="true" />
<input name="merchant_receipt_email" type="hidden" value="billing@fortcollinscreatorhub.org" />
<input alt="View Cart" src="/wp-content/uploads/2015/05/shopping-view-cart.png" type="image" /></form></td>
</tr>'''

for (sku, desc, value) in skus:
    print '<tr><td colspan="2"><h3>Add %s membership to cart</h3></td></tr>' % desc

    idx = 0
    for (sku_prefix, desc_prefix, value_scale, value_add, media_upload_month, monthly_plan) in sku_mods:
        if idx % 2 == 0:
            print '<tr>'
        sku_ex = sku_prefix + sku
        desc_ex = 'FCCH Membership: ' + desc_prefix + ': ' + desc
        value_ex = (value_scale * value) + value_add
        if monthly_plan:
            plan_text = ', $%0.2f every month' % value
        else:
            plan_text = ''
        explain_text = '$%0.2f one-time charge' % value_ex + plan_text
        gen_form('process_cart', sku_ex, desc_ex, value_ex, media_upload_month, explain_text)
        if idx % 2 == 1:
            print '</tr>'
        idx += 1

print '<tr><td colspan="2"><h3>Make a donation (doesn\'t use cart)</h3></td></tr>'
print '<tr>'
gen_form('process_variable', 'donate-now', 'FCCH: Donation', None, '2015/05', 'You choose the amount during checkout')
print '''\
<td></td>
</tr>
</tbody>
</table>'''
