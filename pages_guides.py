"""How-to guide pages, one per spreadsheet product. Formulas shown here are the same ones used (and tested) in the templates."""

CSS = "h2{margin:28px 0 8px;font-size:1.25rem}.guide p,.guide li{max-width:68ch}pre{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;overflow-x:auto;font-size:.88rem}"
DISC = "General guidance for record-keeping. Formulas work in Excel and Google Sheets. Not tax, legal or financial advice."


def guide(fname, title, desc, h1, lead, body, cta):
    import re, html
    body = re.sub(r"<pre>(.*?)</pre>", lambda m: "<pre>" + html.escape(html.unescape(m.group(1)), quote=False) + "</pre>", body, flags=re.S)
    return fname, dict(title=title, desc=desc, h1=h1, lead=lead, css=CSS, cta=cta, disclaimer=DISC, body=f'<div class="guide">{body}</div>', js="")


def add_pages(PAGES):
    items = [
        guide("track-tuition-fees-in-excel.html",
              "How to Track Tuition and Coaching Fees in Excel (With Formulas)",
              "A simple Excel or Google Sheets method to track who has paid tuition or coaching fees, who is pending, and attendance percentage, with copy-paste formulas.",
              "How to track tuition and coaching fees in Excel",
              "A simple three-sheet setup that shows who has paid, who is pending and how regular each student is.",
              """<h2>1. Three sheets</h2>
<ul><li><b>Students</b>: ID, name, class, batch, monthly fee, months enrolled.</li><li><b>Payments</b>: date, student ID, month paid for, amount, mode (cash or UPI).</li><li><b>Attendance</b>: student ID and one column per day with P or A.</li></ul>
<h2>2. Work out what is due</h2>
<p>Students columns: A ID, B name, C class, D batch, E monthly fee, F months enrolled. Payments columns: A date, B student ID, C month paid for, D amount. Add three columns to Students (G, H, I): total due is fee times months, paid is a sum from Payments, balance is the difference. For row 2:</p>
<pre>G2 Total due:  =E2*F2
H2 Paid:       =SUMIFS(Payments!$D:$D, Payments!$B:$B, A2)
I2 Balance:    =G2-H2</pre>
<p>Apply a red font to any balance above zero with conditional formatting, so pending fees stand out.</p>
<h2>3. Attendance percentage</h2>
<pre>Present days:  =COUNTIF(C2:AG2,"P")
Marked days:   =COUNTIF(C2:AG2,"P")+COUNTIF(C2:AG2,"A")
Attendance %:  =IF(marked=0,"",present/marked)</pre>
<h2>4. Habits that keep it accurate</h2>
<ul><li>Use one student ID everywhere. Names are easy to mistype; IDs are not.</li><li>Log every payment the same day, including part payments.</li><li>Update months enrolled at the start of each month.</li><li>Keep the file private; it contains personal details.</li></ul>
<p>If you would rather not build it yourself, the ready-made version below has these sheets, the formulas and the red highlights already set up.</p>""",
              ("Coaching Centre Fee & Attendance Tracker", "The finished spreadsheet with students, payments, attendance and a summary, ready to use.", "https://spooke0.gumroad.com/l/coaching-fee-tracker", "Get the tracker")),
        guide("udhar-khata-excel-ledger-for-shops.html",
              "Udhar Khata in Excel: Track Customer Credit for Your Shop",
              "How to keep a simple udhar (customer credit) ledger in Excel or Google Sheets: who owes what, last credit date and overdue customers, with copy-paste formulas.",
              "Udhar khata in Excel: track customer credit for your shop",
              "A clean way to see who owes you, how much, and who is overdue, without a paper notebook.",
              """<h2>1. Two sheets</h2>
<ul><li><b>Customers</b>: customer ID, name, optional phone.</li><li><b>Transactions</b>: date, customer ID, type (Credit or Payment), amount, note.</li></ul>
<h2>2. Balances by formula</h2>
<p>Customers columns: A ID, B name, C phone. Transactions columns: A date, B customer ID, C type, D amount. Add D to I to Customers. For row 2:</p>
<pre>D2 Total credit:  =SUMIFS(Transactions!$D:$D, Transactions!$B:$B, A2, Transactions!$C:$C, "Credit")
E2 Total paid:    =SUMIFS(Transactions!$D:$D, Transactions!$B:$B, A2, Transactions!$C:$C, "Payment")
F2 Balance:       =D2-E2</pre>
<h2>3. Last credit date and overdue</h2>
<pre>G2 Last credit:   =MAXIFS(Transactions!$A:$A, Transactions!$B:$B, A2, Transactions!$C:$C, "Credit")
H2 Days since:    =TODAY()-G2
I2 Overdue?:      =IF(AND(F2>0, H2>30), "Overdue", IF(F2>0, "Owes", "Clear"))</pre>
<p>MAXIFS needs Excel 2019 or newer, or Google Sheets. Change 30 to the number of days you allow.</p>
<h2>4. Good habits</h2>
<ul><li>Write every credit and every payment as a separate row, never edit old rows.</li><li>Agree the credit limit and due date with the customer when you give credit.</li><li>Keep customer details private.</li></ul>
<p>The ready-made ledger below has these sheets, the formulas and a summary of the biggest dues.</p>""",
              ("Shop Udhar Khata Ledger", "Customers, transactions and a summary of overdue and biggest dues, ready to use.", "https://spooke0.gumroad.com/l/shop-udhar-khata", "Get the ledger")),
        guide("rent-collection-tracker-excel.html",
              "Rent Collection Tracker in Excel for Landlords and PGs",
              "How to track monthly rent for several flats, rooms or shops in Excel or Google Sheets: months due, rent received and pending balance, with copy-paste formulas.",
              "Rent collection tracker in Excel",
              "See at a glance which units have paid and which still owe rent.",
              """<h2>1. Two sheets</h2>
<ul><li><b>Units</b> columns: A unit ID, B tenant, C monthly rent, D first rent month, E deposit (then F to I are formulas).</li><li><b>Payments</b> columns: A date received, B unit ID, C amount.</li></ul>
<h2>2. Months due, rent due and balance</h2>
<p>For row 2 of the Units sheet:</p>
<pre>F2 Months due:     =MAX(0,(YEAR(TODAY())-YEAR(D2))*12+MONTH(TODAY())-MONTH(D2)+1)
G2 Rent due:       =C2*F2
H2 Rent received:  =SUMIFS(Payments!$C:$C, Payments!$B:$B, A2)
I2 Balance:        =G2-H2</pre>
<p>A positive balance is rent pending; a negative one means the tenant has paid in advance.</p>
<h2>3. Tips</h2>
<ul><li>Count the start month as a due month, or change the formula if you bill from the next month.</li><li>Record every payment with the date it actually arrived.</li><li>Keep the deposit in its own column and do not mix it with rent.</li><li>Keep tenant details private.</li></ul>
<p>The finished tracker below has the sheets, formulas, red highlights for pending rent and a summary.</p>""",
              ("Rent Collection Tracker", "Units, payments and a summary of rent due, received and pending, ready to use.", "https://spooke0.gumroad.com/l/rent-collection-tracker", "Get the tracker")),
        guide("track-gym-membership-renewals-excel.html",
              "How to Track Gym, Salon or Library Membership Renewals in Excel",
              "A simple Excel or Google Sheets method to track membership end dates, days left and who is expiring soon or expired, with copy-paste formulas.",
              "Track membership renewals in Excel",
              "Know who is about to expire before they do, with end dates and a status that update by themselves.",
              """<h2>1. One sheet to start</h2>
<p>Columns: A member ID, B name, C phone (optional), D plan, E start date, F months paid, G fee paid. Then three formula columns: H end date, I days left, J status.</p>
<h2>2. The formulas</h2>
<p>For row 2 (start date in E2, months paid in F2):</p>
<pre>H2 End date:   =EDATE(E2, F2)
I2 Days left:  =H2-TODAY()
J2 Status:     =IF(I2<0, "Expired", IF(I2<=7, "Expiring soon", "Active"))</pre>
<p>Change 7 to the number of days of warning you want. Add conditional formatting so Expired is red and Expiring soon is amber.</p>
<h2>3. Renewals</h2>
<ul><li>When someone renews, set a new start date (or add a new row if you want a history).</li><li>Sort by days left to see the next renewals first.</li><li>Count each status with <code>=COUNTIF(J:J,"Expiring soon")</code>.</li><li>Keep members' details private.</li></ul>
<p>The ready-made tracker below has the formulas, colour highlights and a summary already set up.</p>""",
              ("Membership Renewal Tracker", "End dates, days left and Active / Expiring soon / Expired status, ready to use.", "https://spooke0.gumroad.com/l/membership-renewal-tracker", "Get the tracker")),
        guide("small-business-sales-purchases-gst-excel.html",
              "Track Small Business Sales, Purchases and GST in Excel",
              "A simple monthly method to record sales, purchases and expenses with GST in Excel or Google Sheets and see GST collected, GST paid and a simple profit, with formulas.",
              "Track sales, purchases and GST in Excel",
              "A simple monthly view of what you sold, what you bought, the GST on each and a rough profit.",
              """<h2>1. Three sheets</h2>
<ul><li><b>Sales</b>: date, invoice no, customer, taxable value, GST rate %.</li><li><b>Purchases</b>: date, bill no, supplier, taxable value, GST rate %.</li><li><b>Expenses</b>: date, category, amount (costs without GST credit).</li></ul>
<h2>2. GST and totals per row</h2>
<p>Columns on Sales and Purchases: A date, B number, C name, D taxable value, E GST rate %, then F and G are formulas.</p>
<pre>F2 GST amount:  =D2*E2/100
G2 Total:       =D2+F2</pre>
<h2>3. A monthly summary</h2>
<p>Put the year in B3 and the month number in B4, then:</p>
<pre>Sales (taxable):  =SUMIFS(Sales!D:D, Sales!A:A, ">="&DATE(B3,B4,1), Sales!A:A, "<"&EDATE(DATE(B3,B4,1),1))
GST on sales:     =SUMIFS(Sales!F:F, ...same dates...)
GST on purchases: =SUMIFS(Purchases!F:F, ...same dates...)
Net GST estimate: = GST on sales - GST on purchases</pre>
<p><b>Important:</b> that net figure is a planning estimate. Your actual GST liability depends on your registration, the items you sell and credit rules. Confirm with a Chartered Accountant.</p>
<h2>4. Simple profit</h2>
<pre>Profit = Sales (taxable) - Purchases (taxable) - Other expenses</pre>
<p>The ready-made template below has these sheets and the monthly summary set up.</p>""",
              ("Small Business Sales, Purchases & GST Summary", "Sales, purchases, expenses and a monthly GST and profit summary, ready to use. GST figure is an estimate.", "https://spooke0.gumroad.com/l/small-business-gst-summary", "Get the template")),
    ]
    for fname, page in items:
        PAGES[fname] = page
