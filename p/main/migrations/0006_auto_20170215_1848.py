# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170214_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentjson',
            name='text',
            field=models.TextField(default='{"features": {"logo": null, "paragraphs": [{"text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "image": null, "header": "\\u041a\\u0430\\u0447\\u0435\\u0441\\u0442\\u0432\\u043e"}, {"text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "image": null, "header": "\\u041a\\u0440\\u0430\\u0441\\u043e\\u0442\\u0430"}, {"text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "image": null, "header": "\\u0423\\u0434\\u043e\\u0431\\u0441\\u0442\\u0432\\u043e"}, {"text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "image": null, "header": "\\u0414\\u043e\\u043b\\u0433\\u043e\\u0432\\u0435\\u0447\\u043d\\u043e\\u0441\\u0442\\u044c"}], "header": "\\u041f\\u043e\\u0447\\u0435\\u043c\\u0443 \\u0443 \\u043d\\u0430\\u0441?", "single-position": null}, "about-us": {"logo": null, "paragraphs": [{"text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc tortor elit, egestas quis tincidunt ac, varius quis arcu. Donec auctor felis sed nibh aliquam tempus et eu tellus. Quisque consectetur eu leo id tincidunt. Duis et urna leo. Morbi vestibulum id nunc id eleifend. Mauris neque nibh, pulvinar ut elementum eget, luctus at nisl.", "image": null}], "header": "O \\u043d\\u0430\\u0441", "single-position": null}, "main": {"logo": true, "slogan": "\\u041f\\u041e\\u0414 \\u0417\\u0410\\u041a\\u0410\\u0417 \\u041e\\u0422 4000 \\u0415\\u0412\\u0420\\u041e\\n\\u0413\\u0410\\u0420\\u0410\\u041d\\u0422\\u0418\\u042f 5 \\u041b\\u0415\\u0422\\n\\u0420\\u0410\\u0411\\u041e\\u0422\\u0410\\u0415\\u041c \\u041f\\u041e \\u0412\\u0421\\u0415\\u0419 \\u0411\\u0415\\u041b\\u0410\\u0420\\u0423\\u0421\\u0418", "header": "\\u041a\\u0443\\u0445\\u043d\\u0438 \\u0438\\u0437 \\u0413\\u0435\\u0440\\u043c\\u0430\\u043d\\u0438\\u0438"}}'),
        ),
    ]