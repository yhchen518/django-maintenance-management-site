from django import template
import math

register = template.Library()

@register.filter("linefilter")
def linesectionfilter(pdffilelist, line):
	return pdffilelist.filter(line=line)

@register.filter("sectionfilter")
def sectionfilter(pdffilelist, section):
	return pdffilelist.filter(section=section)

