from django import forms
from .models import Board, Note, Category, Tag


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter board name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your board...'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color',
                'value': '#007bff'
            }),
        }
        labels = {
            'name': 'Board Name',
            'description': 'Description',
            'color': 'Color Theme',
        }
        help_texts = {
            'name': 'Choose a descriptive name for your board',
            'description': 'Add a brief description (optional)',
            'color': 'Pick a color theme for your board',
        }


class QuickNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Quick note title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light',
                'rows': 3,
                'placeholder': 'What\'s on your mind?'
            }),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'note_type', 'category', 'priority', 'is_pinned', 'is_archived']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Note title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light',
                'rows': 8,
                'placeholder': 'Write your note content here...'
            }),
            'note_type': forms.Select(attrs={
                'class': 'form-select bg-dark text-light'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select bg-dark text-light'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select bg-dark text-light'
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_archived': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'note_type': 'Note Type',
            'category': 'Category',
            'priority': 'Priority',
            'is_pinned': 'Pin this note',
            'is_archived': 'Archive this note',
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Category name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light',
                'rows': 3,
                'placeholder': 'Describe this category...'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color',
                'value': '#007bff'
            }),
        }
        labels = {
            'name': 'Category Name',
            'description': 'Description',
            'color': 'Color',
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Tag name...'
            }),
        }
        labels = {
            'name': 'Tag Name',
        }
