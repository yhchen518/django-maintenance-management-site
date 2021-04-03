from django.contrib import admin
from .models import Part, Line, Section, PartImages, Schematic, Manual

class PartImagesAdmin(admin.StackedInline):
	model = PartImages

admin.site.register(Section)

@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
	list_display = ('name', 'display_section')
	fields = ['name', 'section']

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
	inlines = [PartImagesAdmin]
	list_display = ('name',  'number', 'quantity','lines', 'section')
	fields = [('name', 'number'), 'specs', 'quantity', ('lines', 'section')]

	class Meta:
		model = Part

@admin.register(PartImages)
class PartImagesAdmin(admin.ModelAdmin):
	pass

@admin.register(Schematic)
class SchematicAdmin(admin.ModelAdmin):
	list_display = ('name', 'line', 'section', 'pdfFile')
	fields = ['name', 'line', 'section', 'pdfFile']

@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
	list_display = ('name', 'line', 'section', 'pdfFile')
	fields = ['name', 'line', 'section', 'pdfFile']
