from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from pagetree.generic.models import BasePageBlock
from absi.main.utils import get_word


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    voice = models.CharField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


class PlayBlock(BasePageBlock):
    """
    Pageblock to play a segment of Arabic text.
    """
    display_name = 'Play Block'
    template_file = 'main/pageblocks/play_block.html'
    js_template_file = 'main/pageblocks/play_block_js.html'

    text = models.TextField(help_text='Arabic text to play and evaluate')

    initial = models.CharField(
        null=True, blank=True,
        help_text='Word examples for initial position')
    initial_ipa = models.CharField(
        null=True, blank=True,
        help_text='IPA notation for initial examples')

    @property
    def initial_first(self) -> str:
        return get_word(self.initial, 0)

    @property
    def initial_ipa_first(self) -> str:
        return get_word(self.initial_ipa, 0)

    @property
    def initial_second(self) -> str:
        return get_word(self.initial, 1)

    @property
    def initial_ipa_second(self) -> str:
        return get_word(self.initial_ipa, 1)

    medial = models.CharField(
        null=True, blank=True,
        help_text='Word examples for medial position')
    medial_ipa = models.CharField(
        null=True, blank=True,
        help_text='IPA notation for medial examples')

    @property
    def medial_first(self) -> str:
        return get_word(self.medial, 0)

    @property
    def medial_ipa_first(self) -> str:
        return get_word(self.medial_ipa, 0)

    @property
    def medial_second(self) -> str:
        return get_word(self.medial, 1)

    @property
    def medial_ipa_second(self) -> str:
        return get_word(self.medial_ipa, 1)

    final = models.CharField(
        null=True, blank=True,
        help_text='Word examples for final position')
    final_ipa = models.CharField(
        null=True, blank=True,
        help_text='IPA notation for final examples')

    @property
    def final_first(self) -> str:
        return get_word(self.final, 0)

    @property
    def final_ipa_first(self) -> str:
        return get_word(self.final_ipa, 0)

    @property
    def final_second(self) -> str:
        return get_word(self.final, 1)

    @property
    def final_ipa_second(self) -> str:
        return get_word(self.final_ipa, 1)

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


class LetterOverviewBlock(BasePageBlock):
    """
    Pageblock to display the overview for this Arabic letter.
    """
    display_name = 'Letter Overview Block'
    template_file = 'main/pageblocks/letter_overview_block.html'

    @staticmethod
    def create(request):
        form = LetterOverviewBlockForm(request.POST)
        return form.save()


class LetterOverviewBlockForm(forms.ModelForm):
    class Meta:
        model = LetterOverviewBlock
        fields = '__all__'


LetterOverviewBlock.form = LetterOverviewBlockForm
