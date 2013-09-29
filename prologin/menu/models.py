from django.db import models
from prologin.utils import get_slug

class MenuEntry(models.Model):
    """
    name: name displayed in the menu
    slug: auto-generated name-based id used in the menu template tag
    url: can be an url to resolve (eg: home, team:index, team:year|2012) or an absolute url (eg: http://example.com/, /example, #example)
    parent: parent entry id or None
    position: used to set the display order (lower numbers are displayed first)
    access: who can see this entry?
    """
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32, db_index=True)
    url = models.CharField(max_length=120) # Do not change me to an URLField, I wouldn't be able to store relative URLs!
    parent = models.ForeignKey('self', null=True, blank=True, default=None)
    position = models.IntegerField()
    access_types = (
        ('all', 'All'),
        ('guest', 'Guest only'),
        ('logged', 'Logged users'),
        ('admin', 'Admin'),
    )
    access = models.CharField(max_length=10, choices=access_types, default='all')

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = get_slug(self.name)
        super(MenuEntry, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Menu entry'
        verbose_name_plural = 'Menu entries'
