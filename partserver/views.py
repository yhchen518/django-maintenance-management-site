from django.shortcuts import render
from .models import Part, Section, Line, PartImages, Schematic, Manual
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import qrcode
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.db.models import Q

def index(request):
	"""View function for home page of site."""

	# Generate counts of some of the main objects
	part_list = Part.objects.all()
	num_parts = part_list.count()
	line_list = Line.objects.all()
	section_list = Section.objects.all()
	context = {
		'num_parts': num_parts,
		'line_list': line_list,
		'section_list': section_list,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)

class LineDetailView(generic.DetailView):
	model = Line
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(LineDetailView, self).get_context_data(**kwargs)
		context['part_list'] = Part.objects.all()
		return context

class PartListView(generic.ListView):
	model = Part
	paginate_by = 30
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(PartListView, self).get_context_data(**kwargs)
		context['line_list'] = Line.objects.all()
		context['section_list'] = Section.objects.all()
		context['num_parts'] = self.get_queryset().count()
		return context
	def get_queryset(self):
		querydetail = self.request.GET.get('detail')
		querysection = self.request.GET.get('section')
		queryline = self.request.GET.get('line')
		FilteredParts = Part.objects.all()
		if queryline:
			FilteredParts = Part.objects.filter(lines=Line.objects.get(pk=queryline))
		if querysection:	
			FilteredParts = FilteredParts.filter(section=Section.objects.get(id=querysection))
		FilteredParts = FilteredParts.filter(Q(name__icontains=querydetail) |
								   Q(number__icontains=querydetail) | 
								   Q(specs__icontains=querydetail))
		

		return FilteredParts

class PartDetailView(generic.DetailView):
	model = Part
	def part_detail_view(request, primary_key):
		try:
			part = part.objects.get(pk=primary_key)

		except Part.DoesNotExist:
			raise Http404('Part does not exist')

		return render(request, 'partserver/part_detail.html', context={'part': part})

class SchematicListView(generic.ListView):
	model = Schematic
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(SchematicListView, self).get_context_data(**kwargs)
		context['line_list'] = Line.objects.all()
		return context

class ManualListView(generic.ListView):
	model = Manual
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(ManualListView, self).get_context_data(**kwargs)
		context['line_list'] = Line.objects.all()
		return context

class PartImagesInline(InlineFormSetFactory):
	model = PartImages
	fields = '__all__'

class PartCreate(LoginRequiredMixin, CreateWithInlinesView):
	model = Part
	inlines = [PartImagesInline]
	fields = ['name', 'number', 'specs', 'lines', 'section']

class PartUpdate(LoginRequiredMixin, UpdateWithInlinesView):
	model = Part
	inlines = [PartImagesInline]
	fields = ['name', 'number', 'specs', 'lines', 'section']

class PartDelete(LoginRequiredMixin, DeleteView):
	model = Part
	success_url = reverse_lazy('index')

class SchematicCreate(LoginRequiredMixin, CreateView):
	model = Schematic
	fields = '__all__'
	success_url = reverse_lazy('partserver:schematics')

class SchematicUpdate(LoginRequiredMixin, UpdateView):
	model = Schematic
	fields = '__all__'
	success_url = reverse_lazy('partserver:schematics')

class SchematicDelete(LoginRequiredMixin, DeleteView):
	model = Schematic
	fields = '__all__'
	success_url = reverse_lazy('partserver:schematics')

class ManualCreate(LoginRequiredMixin, CreateView):
	model = Manual
	fields = '__all__'
	success_url = reverse_lazy('partserver:manuals')

class ManualUpdate(LoginRequiredMixin, UpdateView):
	model = Manual
	fields = '__all__'
	success_url = reverse_lazy('partserver:manuals')

class ManualDelete(LoginRequiredMixin, DeleteView):
	model = Manual
	fields = '__all__'
	success_url = reverse_lazy('partserver:manuals')