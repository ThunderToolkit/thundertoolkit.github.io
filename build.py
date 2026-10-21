#!/usr/bin/env python3
"""Generate a per-investor page = shared guide (investors.html) + personal report from a JSON data file.
Usage: python build.py data/<investor>.json   ->   investors/<slug>.html
Shared guide edits: edit investors.html, then re-run for each investor. Personal data stays in data/*.json."""
import json, sys, html, os

def money(n):
    return "${:,.0f}".format(n)

def render_personal(d):
    shares = sum(a["shares"] for a in d["accounts"])
    invested = sum(a["invested"] for a in d["accounts"])
    avg = invested/shares if shares else 0
    pct = shares/d["fully_diluted_shares"]*100
    rows = ""
    for a in d["accounts"]:
        rows += f'<tr><td><strong>{html.escape(a["label"])}</strong><br><span style="color:var(--muted);font-size:13px">{html.escape(a.get("note",""))}</span></td><td>{a["shares"]:,} shares</td><td>{money(a["invested"])}</td></tr>'
    rows += f'<tr style="font-weight:700"><td>Total</td><td>{shares:,} shares</td><td>{money(invested)}</td></tr>'
    vrows = ""
    for s in d["stages"]:
        ps_lo = s["company_low"]/d["fully_diluted_shares"]
        ps_hi = s["company_high"]/d["fully_diluted_shares"]
        yv_lo = ps_lo*shares; yv_hi = ps_hi*shares
        m_lo = yv_lo/invested if invested else 0; m_hi = yv_hi/invested if invested else 0
        vrows += (f'<tr><td><strong>{html.escape(s["stage"])}</strong></td>'
                  f'<td>{money(s["company_low"])} – {money(s["company_high"])}</td>'
                  f'<td>${ps_lo:,.2f} – ${ps_hi:,.2f}</td>'
                  f'<td>{money(yv_lo)} – {money(yv_hi)}</td>'
                  f'<td>{m_lo:.1f}× – {m_hi:.1f}×</td></tr>')
    cur_val = shares * d["round_price"]
    prorata_tpl = '''
      <h3 style="margin-top:28px">Your pro-rata right in this round</h3>
      <p style="color:var(--muted)">As an existing investor, you can invest in this $PRICE per-share round to keep your ownership from being diluted. Enter the round's total raise to see your pro-rata allocation.</p>
      <div class="imodel">
        <label for="praRaise">This round's total raise</label>
        <div class="field"><span>$</span><input id="praRaise" type="text" inputmode="numeric" autocomplete="off" placeholder="e.g. 5,000,000" aria-label="Round total raise"></div>
        <div class="presets">
          <button type="button" data-raise="2000000">$2M</button><button type="button" data-raise="5000000">$5M</button><button type="button" data-raise="10000000">$10M</button><button type="button" data-raise="15000000">$15M</button>
        </div>
        <p id="praOut" class="res-note"></p>
      </div>
      <script>
      (function(){
        var SH=__SH__, FD=__FD__, PRICE=__PRICE__, own=SH/FD;
        var inp=document.getElementById('praRaise');
        function parse(){return Math.max(0,parseFloat((inp.value||'').replace(/[^0-9.]/g,''))||0);}
        function fmt(n){return '$'+Math.round(n).toLocaleString();}
        function render(){
          var raise=parse(), out=document.getElementById('praOut');
          if(!raise){out.textContent="Enter the round's total raise above to see your pro-rata.";return;}
          var newSh=raise/PRICE, proSh=own*newSh, proDol=own*raise, diluted=SH/(FD+newSh);
          out.innerHTML='To keep your <strong>'+(own*100).toFixed(2)+'%</strong> stake, you can invest about <strong>'+fmt(proDol)+'</strong> for <strong>'+Math.round(proSh).toLocaleString()+'</strong> shares at $'+PRICE.toFixed(2)+'. If you pass, your stake would dilute from '+(own*100).toFixed(2)+'% to about '+(diluted*100).toFixed(2)+'%.';
        }
        inp.addEventListener('input',render);
        document.querySelectorAll('#your-report .presets button[data-raise]').forEach(function(b){b.addEventListener('click',function(){inp.value=parseInt(b.getAttribute('data-raise'),10).toLocaleString();render();});});
        render();
      })();
      </script>'''
    prorata = (prorata_tpl.replace('__SH__', str(int(shares)))
                          .replace('__FD__', str(int(d["fully_diluted_shares"])))
                          .replace('__PRICE__', repr(float(d["round_price"])))
                          .replace('$PRICE', '$' + format(d["round_price"], '.2f')))
    return f'''
  <section id="your-report">
    <div class="wrap">
      <div class="eyebrow">Your personal report · Confidential</div>
      <h2 style="margin-top:14px">{html.escape(d["name"])}</h2>
      <p class="intro">Your Thunder Biotech position today, and what it could be worth if the company were sold at different stages. Prepared {html.escape(d["prepared"])}.</p>
      <div class="grid">
        <div class="card"><div class="stat">{money(invested)}</div><p>invested to date</p></div>
        <div class="card"><div class="stat">{shares:,}</div><p>shares held</p></div>
        <div class="card"><div class="stat">${avg:,.2f}</div><p>average cost per share</p></div>
        <div class="card"><div class="stat">{pct:.2f}%</div><p>of the company, fully diluted</p></div>
      </div>
      <h3 style="margin-top:28px">Accounts in this report</h3>
      <div class="table-wrap"><table><thead><tr><th>Account</th><th>Holdings</th><th>Cash invested</th></tr></thead><tbody>{rows}</tbody></table></div>
      <h3 style="margin-top:28px">What your shares could be worth</h3>
      <div class="table-wrap"><table><thead><tr><th>Stage at sale</th><th>Company sale value</th><th>Price per share</th><th>Your shares</th><th>Multiple of investment</th></tr></thead><tbody>{vrows}</tbody></table></div>
      <p style="color:var(--muted);font-size:14px;margin-top:10px">At this round's price of ${d["round_price"]:.2f}/share, your holdings are valued at {money(cur_val)}. Illustrative scenarios only — not a valuation, forecast or offer.</p>
      {prorata}
    </div>
  </section>
'''

def main():
    data = json.load(open(sys.argv[1]))
    tpl = open("investors.html").read()
    section = render_personal(data)
    out = tpl.replace("</header>", "</header>\n" + section, 1)
    out = out.replace("<title>Thunder Biotech Investor Guide</title>",
                      f'<title>Thunder Investor Guide · {html.escape(data["name"])}</title>', 1)
    os.makedirs("investors", exist_ok=True)
    path = f'investors/{data["slug"]}.html'
    open(path, "w").write(out)
    print("wrote", path)

if __name__ == "__main__":
    main()
