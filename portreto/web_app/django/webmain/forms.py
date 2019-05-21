from django import forms


from .models import Gallery,Photo


class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ['AlbumCover', 'Name', 'Description']


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['Photo', 'Location', 'Description']

