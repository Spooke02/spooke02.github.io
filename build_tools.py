"""Generates the free tool pages from one template (consistent look, SEO tags, product CTAs). Run: python build_tools.py"""
from pathlib import Path

BASE = "https://spooke02.github.io/"
NAV = [("", "Spooke"), ("gst-calculator.html", "GST calculator"), ("invoice-generator.html", "Invoice generator"),
       ("freelance-hourly-rate-calculator.html", "Hourly rate"), ("payment-reminder-message-generator.html", "Reminder messages"), ("resize-photo-to-kb-and-pixels.html", "Photo resizer")]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="icon" href="data:,">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<link rel="canonical" href="{{URL}}">
<style>
:root{--bg:#f7f8fa;--card:#fff;--text:#14213d;--muted:#5b6678;--line:#e3e7ee;--accent:#1f3a5f;--ok:#2e8b57}
@media (prefers-color-scheme:dark){:root{--bg:#0f1624;--card:#17213a;--text:#eef2f8;--muted:#a3b0c4;--line:#27344f;--accent:#f5c542}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:820px;margin:0 auto;padding:24px 20px 56px}h1{font-size:1.9rem;line-height:1.2;margin:8px 0 8px}p.lead{color:var(--muted);margin:0 0 20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin:16px 0}
label{display:block;font-weight:600;margin:12px 0 4px}input,select,textarea,button{width:100%;padding:10px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--text);font:inherit}
textarea{min-height:90px}button{background:var(--accent);color:#fff;font-weight:600;cursor:pointer}@media(prefers-color-scheme:dark){button{color:#0f1624}}
.row{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}.big{font-size:2rem;font-weight:700}.note{color:var(--muted);font-size:.9rem}
a{color:var(--accent)}nav a{margin-right:14px;white-space:nowrap}nav{overflow-x:auto;padding-bottom:4px}
.cta{display:inline-block;width:auto;background:var(--accent);color:#fff;text-decoration:none;font-weight:600;padding:10px 18px;border-radius:10px}@media(prefers-color-scheme:dark){.cta{color:#0f1624}}
table{width:100%;border-collapse:collapse}th,td{padding:8px;border-bottom:1px solid var(--line);text-align:left}td.r,th.r{text-align:right}
button.small{width:auto;padding:6px 12px}details{margin:8px 0}
{{CSS}}
</style>
</head>
<body><div class="wrap">
<nav aria-label="Site">{{NAV}}</nav>
<h1>{{H1}}</h1>
<p class="lead">{{LEAD}}</p>
{{BODY}}
<div class="card"><b>{{CTA_TITLE}}</b><p>{{CTA_TEXT}}</p><a class="cta" href="{{CTA_URL}}">{{CTA_LABEL}}</a></div>
<p class="note">{{DISCLAIMER}} Everything runs in your browser; nothing you type is sent anywhere.</p>
</div>
<script>
{{JS}}
</script>
</body>
</html>
"""

FREELANCE_CTA = ("Freelancer Income Tracker (India)", "Keep payments, INR conversion, GST-threshold progress and e-FIRA/FIRC checks in one Excel sheet.",
                 "https://spooke0.gumroad.com/l/freelancer-tracker-india", "Get the tracker")
KHATA_CTA = ("Shop Udhar Khata Ledger", "Track who owes you, how much, and who is overdue, in one Excel or Google Sheets file.",
             "https://spooke0.gumroad.com/l/shop-udhar-khata", "Get the ledger")

PAGES = {}

# ---------------------------------------------------------------- GST calculator
PAGES["gst-calculator.html"] = dict(
    title="GST Calculator India: Add or Remove GST, CGST/SGST/IGST Split",
    desc="Free GST calculator for India. Add GST to a price or remove it from a GST-inclusive amount, and see the CGST, SGST and IGST split. Runs in your browser.",
    h1="GST calculator (add or remove GST)", lead="Enter an amount and a GST rate to get the tax and the total, or work backwards from a GST-inclusive price.",
    css="", cta=FREELANCE_CTA,
    disclaimer="GST rates and rules change and depend on the item or service. Check the current notification or ask a Chartered Accountant. This is a calculator, not tax advice.",
    body="""<div class="card">
<div class="row">
 <div><label for="amt">Amount (Rs)</label><input id="amt" type="number" min="0" step="any" value="10000"></div>
 <div><label for="rate">GST rate (%)</label><input id="rate" type="number" min="0" step="any" value="18"></div>
 <div><label for="mode">What is this amount?</label><select id="mode"><option value="excl">Price without GST (add GST)</option><option value="incl">Price including GST (remove GST)</option></select></div>
 <div><label for="sup">Supply</label><select id="sup"><option value="intra">Same state (CGST + SGST)</option><option value="inter">Different state (IGST)</option></select></div>
</div>
<p class="note">Quick rates: <button class="small" type="button" data-r="5">5%</button> <button class="small" type="button" data-r="18">18%</button> <button class="small" type="button" data-r="40">40%</button> Check the rate that applies to your item or service.</p>
</div>
<div class="card" aria-live="polite"><div class="big" id="total">-</div><table><tbody id="rows"></tbody></table></div>""",
    js="""const $=id=>document.getElementById(id);
function gst(amount, rate, mode){ const r=rate/100; let base,tax;
 if(mode==='excl'){base=amount;tax=amount*r}else{base=amount/(1+r);tax=amount-base}
 return {base,tax,total:base+tax}}
const f=n=>n.toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2});
function render(){const a=+$('amt').value||0,r=+$('rate').value||0,x=gst(a,r,$('mode').value);
 $('total').textContent='Total: Rs '+f(x.total);
 let rows=`<tr><td>Amount without GST</td><td class="r">Rs ${f(x.base)}</td></tr><tr><td>GST (${r}%)</td><td class="r">Rs ${f(x.tax)}</td></tr>`;
 rows+= $('sup').value==='intra'?`<tr><td>CGST (${r/2}%)</td><td class="r">Rs ${f(x.tax/2)}</td></tr><tr><td>SGST (${r/2}%)</td><td class="r">Rs ${f(x.tax/2)}</td></tr>`:`<tr><td>IGST (${r}%)</td><td class="r">Rs ${f(x.tax)}</td></tr>`;
 $('rows').innerHTML=rows}
['amt','rate','mode','sup'].forEach(i=>$(i).addEventListener('input',render));
document.querySelectorAll('[data-r]').forEach(b=>b.onclick=()=>{$('rate').value=b.dataset.r;render()});render();""")

# ---------------------------------------------------------------- Hourly rate
PAGES["freelance-hourly-rate-calculator.html"] = dict(
    title="Freelance Hourly Rate Calculator (India): What Should You Charge?",
    desc="Work out the hourly rate a freelancer in India needs from a monthly income goal, business costs, a tax reserve and realistic billable hours. Free, runs in your browser.",
    h1="Freelance hourly rate calculator", lead="Start from the monthly money you need, add costs and a tax reserve, and divide by the hours you can really bill.",
    css="", cta=FREELANCE_CTA,
    disclaimer="Planning estimate only. Your tax reserve depends on your situation; ask a Chartered Accountant.",
    body="""<div class="card"><div class="row">
 <div><label for="take">Monthly take-home you want (Rs)</label><input id="take" type="number" min="0" step="any" value="60000"></div>
 <div><label for="cost">Monthly business costs (Rs)</label><input id="cost" type="number" min="0" step="any" value="5000"></div>
 <div><label for="tax">Tax reserve (% of earnings)</label><input id="tax" type="number" min="0" max="60" step="any" value="15"></div>
 <div><label for="hrs">Billable hours per week</label><input id="hrs" type="number" min="1" step="any" value="20"></div>
 <div><label for="wks">Working weeks per year</label><input id="wks" type="number" min="1" max="52" step="any" value="46"></div>
 <div><label for="cur">Show in</label><select id="cur"><option value="1">INR</option><option value="usd">USD (enter rate)</option></select></div>
 <div id="fxw" hidden><label for="fx">INR per 1 USD</label><input id="fx" type="number" min="0" step="any" value="84"></div>
</div></div>
<div class="card" aria-live="polite"><div class="big" id="hr">-</div><p id="det" class="note"></p></div>""",
    js="""const $=id=>document.getElementById(id);
function rate(take,cost,tax,hrs,wks){ const gross=(take+cost)/(1-tax/100); const hoursPerMonth=hrs*wks/12; return {gross,hoursPerMonth,hourly:gross/hoursPerMonth}}
const f=n=>n.toLocaleString('en-IN',{maximumFractionDigits:0});
function render(){ $('fxw').hidden=$('cur').value!=='usd';
 const r=rate(+$('take').value||0,+$('cost').value||0,Math.min(+$('tax').value||0,95),+$('hrs').value||1,+$('wks').value||1);
 const usd=$('cur').value==='usd', fx=+$('fx').value||1;
 $('hr').textContent=usd?('$'+(r.hourly/fx).toFixed(2)+' per hour'):('Rs '+f(r.hourly)+' per hour');
 $('det').textContent=`You need about Rs ${f(r.gross)} of billings per month across ${r.hoursPerMonth.toFixed(0)} billable hours. Unbilled time (finding clients, admin, revisions) is why billable hours are lower than hours worked.`}
['take','cost','tax','hrs','wks','cur','fx'].forEach(i=>$(i).addEventListener('input',render));render();""")

# ---------------------------------------------------------------- Reminder messages
PAGES["payment-reminder-message-generator.html"] = dict(
    title="Payment Reminder Message Generator (Polite to Firm) for Invoices and Fees",
    desc="Free payment reminder message maker: generate a polite, neutral or firm WhatsApp or email reminder for an unpaid invoice, fee or udhar. Copy and send.",
    h1="Payment reminder message generator", lead="Fill in the details and copy a ready message: polite, neutral or firm. You review and send it yourself.",
    css="", cta=KHATA_CTA,
    disclaimer="Messages are templates; check them before sending and follow any agreement you have. Not legal advice.",
    body="""<div class="card"><div class="row">
 <div><label for="nm">Their name</label><input id="nm" value="Rahul"></div>
 <div><label for="amt">Amount (Rs)</label><input id="amt" type="number" min="0" step="any" value="5000"></div>
 <div><label for="ref">For (invoice / fee / items)</label><input id="ref" value="invoice INV-012"></div>
 <div><label for="due">Due date</label><input id="due" type="date"></div>
 <div><label for="me">Your name</label><input id="me" value="Akshat"></div>
 <div><label for="pay">How to pay (UPI / bank)</label><input id="pay" placeholder="e.g. UPI: name@bank"></div>
 <div><label for="tone">Tone</label><select id="tone"><option value="soft">Polite (first reminder)</option><option value="mid">Neutral (second reminder)</option><option value="firm">Firm (overdue)</option></select></div>
</div></div>
<div class="card"><label for="out">Your message</label><textarea id="out" readonly></textarea><p><button id="copy" type="button" class="small">Copy message</button> <span id="ok" class="note"></span></p></div>""",
    js="""const $=id=>document.getElementById(id);
function msg(v){ const amt=Number(v.amt).toLocaleString('en-IN'); const due=v.due?` (due ${new Date(v.due+'T00:00:00').toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'})})`:'';
 const pay=v.pay?`\\nYou can pay here: ${v.pay}`:'';
 if(v.tone==='soft') return `Hi ${v.nm}, a gentle reminder that Rs ${amt} for ${v.ref}${due} is still pending. If you have already paid, please ignore this and share the payment details so I can update my records.${pay}\\nThank you!\\n- ${v.me}`;
 if(v.tone==='mid') return `Hello ${v.nm}, following up on my earlier message: Rs ${amt} for ${v.ref}${due} is still unpaid. Could you confirm when I can expect the payment?${pay}\\nThanks,\\n${v.me}`;
 return `Hello ${v.nm}, Rs ${amt} for ${v.ref}${due} is now overdue. Please clear it by [date] or let me know today if there is a problem so we can agree on a plan.${pay}\\nRegards,\\n${v.me}`}
function render(){ $('out').value=msg({nm:$('nm').value||'there',amt:$('amt').value||0,ref:$('ref').value||'the amount due',due:$('due').value,me:$('me').value,pay:$('pay').value,tone:$('tone').value})}
['nm','amt','ref','due','me','pay','tone'].forEach(i=>$(i).addEventListener('input',render));
$('copy').onclick=async()=>{try{await navigator.clipboard.writeText($('out').value);$('ok').textContent='Copied.'}catch(e){$('out').select();$('ok').textContent='Press Ctrl+C to copy.'}};render();""")

# ---------------------------------------------------------------- Invoice generator
PAGES["invoice-generator.html"] = dict(
    title="Free Invoice Generator India: Create and Print an Invoice (PDF)",
    desc="Free invoice generator for freelancers and small businesses in India. Add items, optional GST, and your payment details, then print or save as PDF. Runs in your browser.",
    h1="Free invoice generator", lead="Fill in the details, check the preview, then use Print and choose Save as PDF. Nothing is uploaded.",
    css="""@media print{nav,.noprint,.cta,.note,.lead,h1,.editor{display:none!important}body{background:#fff;color:#000}.wrap{padding:0}.card{border:none;padding:0}}
.inv{background:#fff;color:#111;border:1px solid var(--line);border-radius:10px;padding:24px}.inv h2{margin:0 0 8px;font-size:1.6rem}.inv td,.inv th{color:#111;border-bottom:1px solid #ddd}
.items input{padding:6px}""",
    cta=FREELANCE_CTA,
    disclaimer="Check that the invoice meets the rules that apply to you (for example GST invoices need specific details). This tool is not tax or legal advice.",
    body="""<div class="card editor"><div class="row">
 <div><label for="sn">Your name / business</label><input id="sn" value="Your Name"></div>
 <div><label for="sa">Your address / contact</label><input id="sa" placeholder="Address, email, phone"></div>
 <div><label for="sg">GSTIN (optional)</label><input id="sg" placeholder="Leave blank if not registered"></div>
 <div><label for="bn">Bill to</label><input id="bn" value="Client Name"></div>
 <div><label for="ba">Client address</label><input id="ba" placeholder="Address / country"></div>
 <div><label for="no">Invoice no.</label><input id="no" value="INV-001"></div>
 <div><label for="dt">Date</label><input id="dt" type="date"></div>
 <div><label for="cu">Currency symbol</label><input id="cu" value="Rs"></div>
 <div><label for="tx">GST % (0 if none)</label><input id="tx" type="number" min="0" step="any" value="0"></div>
</div>
<label>Items</label><div class="items" id="items"></div><button type="button" class="small" id="add">+ Add item</button>
<label for="pay">Payment details</label><textarea id="pay" placeholder="UPI, bank account, PayPal ... (do not include passwords)"></textarea>
<label for="nt">Notes / terms</label><textarea id="nt" placeholder="e.g. Payment due within 15 days"></textarea>
<p><button type="button" id="print">Print / Save as PDF</button></p></div>
<div class="inv card" id="inv"></div>""",
    js="""const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function totals(items,taxPct){const sub=items.reduce((a,i)=>a+(+i.q||0)*(+i.r||0),0);const tax=sub*(taxPct/100);return{sub,tax,total:sub+tax}}
const f=n=>n.toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2});
$('dt').value=new Date().toISOString().slice(0,10);
const items=[{d:'Service',q:1,r:5000}];
function drawItems(){ $('items').innerHTML=items.map((it,i)=>`<div class="row" style="margin:6px 0"><input data-i="${i}" data-k="d" value="${esc(it.d)}" placeholder="Description" aria-label="Description"><input data-i="${i}" data-k="q" type="number" min="0" step="any" value="${it.q}" aria-label="Quantity"><input data-i="${i}" data-k="r" type="number" min="0" step="any" value="${it.r}" aria-label="Rate"><button type="button" class="small" data-del="${i}">Remove</button></div>`).join('');
 document.querySelectorAll('[data-k]').forEach(e=>e.oninput=()=>{items[e.dataset.i][e.dataset.k]=e.value;render()});
 document.querySelectorAll('[data-del]').forEach(e=>e.onclick=()=>{items.splice(e.dataset.del,1);drawItems();render()})}
function render(){const c=esc($('cu').value),t=totals(items,+$('tx').value||0),tp=+$('tx').value||0;
 $('inv').innerHTML=`<h2>${tp>0&&$('sg').value?'Tax Invoice':'Invoice'}</h2><p><b>${esc($('sn').value)}</b><br>${esc($('sa').value)}${$('sg').value?'<br>GSTIN: '+esc($('sg').value):''}</p>
 <p>Invoice no: <b>${esc($('no').value)}</b> &nbsp; Date: <b>${esc($('dt').value)}</b></p><p>Bill to:<br><b>${esc($('bn').value)}</b><br>${esc($('ba').value)}</p>
 <table><thead><tr><th>Description</th><th class="r">Qty</th><th class="r">Rate</th><th class="r">Amount</th></tr></thead><tbody>${items.map(i=>`<tr><td>${esc(i.d)}</td><td class="r">${esc(i.q)}</td><td class="r">${c} ${f(+i.r||0)}</td><td class="r">${c} ${f((+i.q||0)*(+i.r||0))}</td></tr>`).join('')}</tbody></table>
 <table style="margin-top:10px"><tbody><tr><td class="r">Subtotal</td><td class="r" style="width:30%">${c} ${f(t.sub)}</td></tr>${tp>0?`<tr><td class="r">GST (${tp}%)</td><td class="r">${c} ${f(t.tax)}</td></tr>`:''}<tr><td class="r"><b>Total</b></td><td class="r"><b>${c} ${f(t.total)}</b></td></tr></tbody></table>
 ${$('pay').value?`<p><b>Payment details</b><br>${esc($('pay').value).replace(/\\n/g,'<br>')}</p>`:''}${$('nt').value?`<p><b>Notes</b><br>${esc($('nt').value).replace(/\\n/g,'<br>')}</p>`:''}`}
['sn','sa','sg','bn','ba','no','dt','cu','tx','pay','nt'].forEach(i=>$(i).addEventListener('input',render));
$('add').onclick=()=>{items.push({d:'',q:1,r:0});drawItems();render()};$('print').onclick=()=>window.print();drawItems();render();""")


def build():
    import pages_more
    pages_more.add_pages(PAGES, FREELANCE_CTA)
    out = Path(__file__).parent
    nav = "".join(f'<a href="{"/" if p == "" else p}">{t}</a>' for p, t in NAV)
    for fname, p in PAGES.items():
        cta_title, cta_text, cta_url, cta_label = p["cta"]
        html = (TEMPLATE.replace("{{TITLE}}", p["title"]).replace("{{DESC}}", p["desc"]).replace("{{URL}}", BASE + fname)
                .replace("{{CSS}}", p["css"]).replace("{{NAV}}", nav).replace("{{H1}}", p["h1"]).replace("{{LEAD}}", p["lead"])
                .replace("{{BODY}}", p["body"]).replace("{{CTA_TITLE}}", cta_title).replace("{{CTA_TEXT}}", cta_text)
                .replace("{{CTA_URL}}", cta_url).replace("{{CTA_LABEL}}", cta_label).replace("{{DISCLAIMER}}", p["disclaimer"]).replace("{{JS}}", p["js"]))
        (out / fname).write_text(html, encoding="utf-8")
    print("built", list(PAGES))


if __name__ == "__main__":
    build()
