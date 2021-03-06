# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 21:55
from __future__ import unicode_literals

from django.db import migrations
import prologin.models
import team.models


def migrate_roles(apps, schema_editor):
    Role = team.models.Role
    mapping = {
        "Président": Role.president,
        "Vice-Président": Role.vice_president,
        "Trésorier": Role.treasurer,
        "Secrétaire": Role.secretary,
        "Responsable technique": Role.technical_lead,
        "Vice-Trésorier": Role.vice_treasurer,
        "Membre": Role.member,
        "Membre persistant": Role.persistent_member,
        "Mascotte": Role.mascot,
        "Responsable scientifique": Role.scientific_lead,
    }

    TeamMember = apps.get_model('team', 'TeamMember')

    for member in TeamMember._default_manager.select_related('role').all():
        try:
            member.role_code = mapping[member.role.name].name
            member.save()
        except KeyError:
            raise ValueError("CharField role not found in ChoiceEnum role: {}".format(member.role.name))


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_role_public'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teammember',
            options={'ordering': ('user__username',), 'verbose_name': 'Team member',
                     'verbose_name_plural': 'Team members'},
        ),
        migrations.AddField(
            model_name='teammember',
            name='role_code',
            field=prologin.models.TextEnumField(team.models.Role, blank=True, max_length=64, verbose_name='Role'),
        ),
        migrations.RunPython(migrate_roles)  # reverse migration is impossible (would create null values for role)
    ]
