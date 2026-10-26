"""Extra pages for build_tools.py: in-browser photo resizer and two guides."""

TOOLKIT_CTA = ("Need to do many files, or work offline?",
               "The Offline Form Toolkit (Windows) resizes photos and signatures in bulk to exact pixels and KB, and merges, splits and compresses PDFs. Your files stay on your PC.",
               "https://spooke0.gumroad.com/l/offline-form-toolkit", "Get the Offline Form Toolkit")

GUIDE_CSS = "h2{margin:28px 0 8px;font-size:1.25rem}.guide p,.guide li{max-width:68ch}"

PHOTO_JS = r"""const $=id=>document.getElementById(id);
$('preset').onchange=()=>{const v=$('preset').value; if(v){const [w,h]=v.split('x');$('w').value=w;$('h').value=h}};
function drawTo(bmp,w,h,crop){const c=document.createElement('canvas');let cw=w,ch=h;
 if(!w&&!h){cw=bmp.width;ch=bmp.height}else if(!w){ch=h;cw=Math.round(bmp.width*h/bmp.height)}else if(!h){cw=w;ch=Math.round(bmp.height*w/bmp.width)}
 c.width=cw;c.height=ch;const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,cw,ch);
 if(w&&h&&crop){const s=Math.max(cw/bmp.width,ch/bmp.height),dw=bmp.width*s,dh=bmp.height*s;x.drawImage(bmp,(cw-dw)/2,(ch-dh)/2,dw,dh)}else x.drawImage(bmp,0,0,cw,ch);return c}
const toBlob=(c,q)=>new Promise(r=>c.toBlob(r,'image/jpeg',q));
async function underKb(canvas,kb){const limit=kb*1024;let cur=canvas;
 for(let i=0;i<8;i++){const lowest=await toBlob(cur,0.05);
  if(lowest.size>limit){const f=Math.max(0.3,Math.sqrt(limit/lowest.size)*0.92);
   const n=document.createElement('canvas');n.width=Math.max(8,Math.round(cur.width*f));n.height=Math.max(8,Math.round(cur.height*f));n.getContext('2d').drawImage(cur,0,0,n.width,n.height);cur=n;continue}
  let lo=0.05,hi=0.95,best=lowest;
  for(let k=0;k<7;k++){const q=(lo+hi)/2,bl=await toBlob(cur,q);if(bl.size<=limit){best=bl;lo=q}else hi=q}
  return {blob:best,canvas:cur}}
 return null}
$('go').onclick=async()=>{const f=$('file').files[0];if(!f){$('msg').textContent='Choose an image first.';return}
 $('go').disabled=true;$('msg').textContent='Working...';
 try{const bmp=await createImageBitmap(f,{imageOrientation:'from-image'});
  const w=+$('w').value||0,h=+$('h').value||0,kb=+$('kb').value||0;
  const c=drawTo(bmp,w,h,$('crop').checked);
  let res=kb?await underKb(c,kb):{blob:await toBlob(c,0.92),canvas:c};
  if(!res){$('msg').textContent='Could not reach that size. Try a larger KB limit.';return}
  const url=URL.createObjectURL(res.blob);$('prev').src=url;$('prev').hidden=false;$('dl').href=url;$('dl').hidden=false;
  let note=`Result: ${res.canvas.width} x ${res.canvas.height} px, ${(res.blob.size/1024).toFixed(1)} KB.`;
  if(w&&h&&(res.canvas.width!==w||res.canvas.height!==h))note+=` The size had to shrink from ${w} x ${h} to fit ${kb} KB.`;
  $('msg').textContent=note}catch(e){$('msg').textContent='Could not read that image. Try a JPG or PNG.'}finally{$('go').disabled=false}};"""


def add_pages(PAGES, FREELANCE_CTA):
    PAGES["resize-photo-to-kb-and-pixels.html"] = dict(
        title="Resize Photo to Exact Pixels and KB Online (Private, in Your Browser)",
        desc="Free tool to resize a photo or signature to exact width and height and under a maximum size in KB, for forms and exams. Runs in your browser; your image is never uploaded.",
        h1="Resize a photo to exact pixels and KB",
        lead="Choose an image, set the size and the maximum KB, and download the result. Your picture stays in your browser and is never uploaded.",
        css=".prev{max-width:100%;border:1px solid var(--line);border-radius:8px;margin-top:10px}", cta=TOOLKIT_CTA,
        disclaimer="Always check the exact size and KB limits on your own form or notice. There is no guarantee that any website or office accepts the output.",
        body="""<div class="card">
<label for="file">1. Choose an image</label><input id="file" type="file" accept="image/*">
<div class="row">
 <div><label for="preset">2. Size preset</label><select id="preset"><option value="">Custom</option><option value="413x531">Passport photo 3.5 x 4.5 cm (413 x 531 px)</option><option value="200x230">ID-style photo 200 x 230 px</option><option value="200x200">Square 200 x 200 px</option><option value="140x60">Signature 140 x 60 px</option><option value="200x80">Signature 200 x 80 px</option></select></div>
 <div><label for="w">Width (px)</label><input id="w" type="number" min="1" step="1"></div>
 <div><label for="h">Height (px)</label><input id="h" type="number" min="1" step="1"></div>
 <div><label for="kb">Max size (KB)</label><input id="kb" type="number" min="1" step="any" value="50"></div>
</div>
<label><input id="crop" type="checkbox" checked style="width:auto"> Crop to fit (keeps faces from stretching)</label>
<p><button id="go" type="button">3. Resize</button></p></div>
<div class="card" aria-live="polite"><div id="msg" class="note">Choose an image to start.</div><img id="prev" class="prev" alt="Result preview" hidden><p><a id="dl" class="cta" hidden download="resized.jpg">Download resized image</a></p></div>""",
        js=PHOTO_JS)

    PAGES["do-freelancers-need-gst-registration-india.html"] = dict(
        title="Do Freelancers in India Need GST Registration? A Plain Guide",
        desc="A plain-language guide for Indian freelancers: the usual turnover threshold, how foreign clients and export of services fit in, and what to check with a Chartered Accountant.",
        h1="Do freelancers in India need GST registration?",
        lead="Short answer: it depends on your turnover and your situation. Here is how to think about it, without the jargon.",
        css=GUIDE_CSS, cta=FREELANCE_CTA,
        disclaimer="General information, not tax or legal advice. GST rules, thresholds and notifications change and depend on your facts. Confirm with a Chartered Accountant.",
        body="""<div class="guide">
<h2>The usual starting point: the threshold</h2>
<p>GST registration is generally required once your aggregate turnover in a financial year crosses a threshold. For suppliers of services, sources commonly cite <b>Rs 20 lakh</b> for most states and <b>Rs 10 lakh</b> for special-category states. Check the current notification, because limits and conditions can change. You can test your numbers with the <a href="gst-threshold-calculator.html">GST threshold calculator</a>.</p>
<h2>Do payments from clients abroad count?</h2>
<p>Income from foreign clients is generally part of your turnover. Export of services is usually treated as zero-rated, often supported by an annual Letter of Undertaking (LUT), but the conditions matter (for example, how and in what currency you receive the money). Keep the paperwork for each foreign payment; see the <a href="efira-firc-guide.html">e-FIRA/FIRC guide</a>.</p>
<h2>Can you register even if you are below the threshold?</h2>
<p>Voluntary registration is possible in many cases, but it brings filing duties. Some clients also ask for a GSTIN. Whether it is worth it depends on your clients and costs, so ask a CA before you decide.</p>
<h2>What to do in practice</h2>
<ul><li>Track every payment with date, client, currency, amount and the rupee amount credited.</li><li>Watch your running total against the threshold each month.</li><li>Keep each foreign payment's e-FIRA or FIRC.</li><li>Talk to a Chartered Accountant before you cross about 80% of the limit.</li></ul>
<h2>Questions to ask your CA</h2>
<ul><li>Does my kind of work qualify as export of services?</li><li>Do I need a LUT, and when do I file it?</li><li>How should my platform withdrawals and fees be recorded?</li><li>Should I register voluntarily?</li></ul>
</div>""", js="")

    PAGES["how-to-invoice-foreign-clients-from-india.html"] = dict(
        title="How to Invoice Foreign Clients from India: A Practical Checklist",
        desc="A practical checklist for Indian freelancers invoicing clients abroad: what to put on the invoice, currency and payment details, and record-keeping for foreign payments.",
        h1="How to invoice foreign clients from India",
        lead="A practical checklist for a clean, professional invoice and the records you should keep afterwards.",
        css=GUIDE_CSS,
        cta=("Make an invoice now", "Use the free invoice generator to add items, optional GST and payment details, then print or save as PDF.", "invoice-generator.html", "Open the invoice generator"),
        disclaimer="General information, not tax or legal advice. Invoice requirements depend on whether you are GST-registered, your client's country and your agreement. Confirm with a Chartered Accountant.",
        body="""<div class="guide">
<h2>What to put on the invoice</h2>
<ul><li>Your name or business name, address and contact details.</li><li>The client's name and address (and their tax ID if they ask for it).</li><li>A unique invoice number and the invoice date.</li><li>A clear description of the work, the quantity or hours, and the rate.</li><li>The currency and the total, stated clearly.</li><li>Payment terms (for example, due in 15 days) and how to pay.</li></ul>
<h2>Currency and payment details</h2>
<p>Invoice in the currency you agreed with the client. Put in only the payment details the client needs (for example, a PayPal email, or bank details if you use a transfer service). Never put passwords or card numbers on an invoice. Platform and bank fees come out of what you receive, so note the amount that actually reaches you.</p>
<h2>GST and export of services</h2>
<p>If you are GST-registered, an invoice for an export of services may need special wording and may be linked to a Letter of Undertaking. If you are not registered, you generally do not charge GST. Which case applies to you is something to confirm with a Chartered Accountant. See also: <a href="do-freelancers-need-gst-registration-india.html">do freelancers need GST registration?</a></p>
<h2>After you are paid</h2>
<ul><li>Record the date, the currency amount, the fee and the rupees credited. The <a href="usd-to-inr-freelance-income.html">USD to INR converter</a> gives an ECB reference estimate for planning.</li><li>Ask your bank or platform for the e-FIRA or FIRC and file it with the payment; see the <a href="efira-firc-guide.html">guide</a>.</li><li>Follow up politely if payment is late; the <a href="payment-reminder-message-generator.html">reminder message generator</a> can help.</li></ul>
<h2>Tip</h2>
<p>Agree scope, price, payment dates and a part-payment up front in writing. Most late-payment problems start with an unclear agreement.</p>
</div>""", js="")
