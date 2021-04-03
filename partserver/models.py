from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.template.defaultfilters import slugify
import uuid
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .validators import validate_file_extension
import os

def get_image_filename(instance, filename):
    name = instance.part.name
    slug = slugify(name)
    return "part_images/%s-%s" % (slug, filename)  

def get_schematic_filename(instance, filename):
	name = instance.name
	line = instance.line.name
	section = instance.section.name
	slug = slugify(name)
	ext = os.path.splitext(filename)[1]
	return "schematics/%s/%s/%s%s" % (line, section, slug, ext)

def get_manual_filename(instance, filename):
	name = instance.name
	line = instance.line.name
	section = instance.section.name
	slug = slugify(name)
	ext = os.path.splitext(filename)[1]
	return "manual/%s/%s/%s%s" % (line, section, slug, ext)

class Section(models.Model):
	"""Model representing the section of line."""
	name = models.CharField(max_length=30, help_text='Enter the section for the line')

	def __str__(self):
		"""String for representing the Model object."""
		return self.name

class Part(models.Model):
	#module representing the part
	name = models.CharField(max_length=100, help_text='Enter the part\'s name')
	number = models.CharField(max_length=20, help_text='Enter the part\'s number')
	quantity = models.PositiveIntegerField(blank=True, null=True, help_text='Part\'s in stock quantity')
	specs = models.TextField(max_length=1000, help_text='Enter the specification of the part')
	lines = models.ForeignKey('Line', on_delete=models.SET_NULL, null=True, help_text='Select the applied lines for the part')
	section = models.ForeignKey(Section, on_delete=models.CASCADE, null=False, help_text='Select the section(s) for this part')

	class Meta:
		ordering = ['name']

	def __str__(self):
		"""String for representing the Model object."""
		return self.name + " - " + self.number
    
	def get_absolute_url(self):
		"""Returns the url to access a detail record for this book."""
		return reverse('partserver:part-detail', args=[str(self.id)])

	def get_images(request):
		images = PartImages.objects.filter(part=request).values_list('images', flat=True)
		return images

	def get_specs(self):
		return self.specs.split("\n")

class Schematic(models.Model):
	name = models.CharField(max_length=100, help_text='Enter the schematic\'s name')
	line = models.ForeignKey('Line', on_delete=models.SET_NULL, null=True, help_text='Select the applied line for the schematic')
	section = models.ForeignKey(Section, on_delete=models.CASCADE, null=False, help_text='Select the section for the schematic')
	pdfFile = models.FileField(upload_to=get_schematic_filename, validators=[validate_file_extension])

class Manual(models.Model):
	name = models.CharField(max_length=100, help_text='Enter the manual\'s name')
	line = models.ForeignKey('Line', on_delete=models.SET_NULL, null=True, help_text='Select the applied line for the manual')
	section = models.ForeignKey(Section, on_delete=models.CASCADE, null=False, help_text='Select the section for the manual')
	pdfFile = models.FileField(upload_to=get_manual_filename, validators=[validate_file_extension])


class Line(models.Model):
	#name for the line(s)
	name = models.CharField(max_length=50, help_text='Enter the line(s)')
	section = models.ManyToManyField(Section, help_text='Select the section(s) for this line')

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('partserver:line-detail', args=[str(self.id)])

	def display_section(self):
		"""Create a string for the Section in Admin."""
		return ', '.join(section.name for section in self.section.all())

class PartImages(models.Model):
    """Images for a model"""
    part = models.ForeignKey(
        Part,
        null=False,
        on_delete=models.CASCADE,
        related_name='images',
        )

    images = models.ImageField(
        verbose_name='images',
        upload_to=get_image_filename,
    )

@receiver(post_delete, sender=PartImages)
def submission_delete(sender, instance, **kwargs):
    instance.images.delete(False) 

@receiver(post_delete, sender=Schematic)
def submission_delete(sender, instance, **kwargs):
    instance.pdfFile.delete(False) 

@receiver(post_delete, sender=Manual)
def submission_delete(sender, instance, **kwargs):
    instance.pdfFile.delete(False) 