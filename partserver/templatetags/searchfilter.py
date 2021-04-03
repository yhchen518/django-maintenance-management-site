from django import template
import math

register = template.Library()

@register.filter("idcompare")
def idcompare(id, requestid):
	if requestid:
		return int(id)==int(requestid)
	return False

@register.filter("idtoname")
def idtoname(id, itemlist):
	if id:
		return itemlist.get(id=int(id))
	else:
		return ""

@register.filter("pagerange")
def pagerange(curpage, numpage):
	if numpage > 10:
		numdig = (curpage-1)//10
		if numdig*10 + 11 > numpage:
			return range(numdig*10+1, numpage+1)
		return range(numdig*10+1, numdig*10+11)
	return range(curpage, numpage+1)
