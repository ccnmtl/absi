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
        }


PlayBlock.form = PlayBlockForm
