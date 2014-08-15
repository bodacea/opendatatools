import lxml.html
import scraperwiki

html = scraperwiki.scrape("http://unstats.un.org/unsd/methods/m49/m49alpha.htm")

root = lxml.html.fromstring(html)
print root
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
        'numerical_code' : tds[0].text_content(),
        'country_name' : tds[1].text_content(),
        'ISO-alpha3-code' : tds[2].text_content()
    }
    print data