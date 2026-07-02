from django import forms
from django.db import models
from pagetree.generic.models import BasePageBlock


class PlayBlock(BasePageBlock):
    """
    Pageblock to play a segment of Arabic text.
    """
    display_name = 'Play Block'
    template_file = 'main/pageblocks/play_block.html'
    js_template_file = 'main/pageblocks/play_block_js.html'

    text = models.TextField(help_text='Arabic text to play and evaluate')

    initial = models.CharField(null=True, blank=True)
    medial = models.CharField(null=True, blank=True)
    final = models.CharField(null=True, blank=True)
    diacritic = models.CharField(null=True, blank=True)

    @staticmethod
    def create(request):
        form = PlayBlockForm(request.POST)
        return form.save()


class PlayBlockForm(forms.ModelForm):
    class Meta:
        model = PlayBlock
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'dir': 'rtl'}),
            'initial': forms.TextInput(attrs={'dir': 'rtl'}),
            'medial': forms.TextInput(attrs={'dir': 'rtl'}),
            'final': forms.TextInput(attrs={'dir': 'rtl'}),
            'diacritic': forms.TextInput(attrs={'dir': 'rtl'}),
        }


PlayBlock.form = PlayBlockForm


class ModuleOverviewBlock(BasePageBlock):
    """
    Pageblock to display the overview for this content module.
    """
    display_name = 'Module Overview Block'
    template_file = 'main/pageblocks/module_overview_block.html'

    @staticmethod
    def create(request):
        form = ModuleOverviewBlockForm(request.POST)
        return form.save()


class ModuleOverviewBlockForm(forms.ModelForm):
    class Meta:
        model = ModuleOverviewBlock
        fields = '__all__'


ModuleOverviewBlock.form = ModuleOverviewBlockForm
