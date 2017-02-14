# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20161126_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentJson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='{"about-us": {"header": "O \\u043d\\u0430\\u0441", "logo": null, "paragraphs": [{"image": null, "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc tortor elit, egestas quis tincidunt ac, varius quis arcu. Donec auctor felis sed nibh aliquam tempus et eu tellus. Quisque consectetur eu leo id tincidunt. Duis et urna leo. Morbi vestibulum id nunc id eleifend. Mauris neque nibh, pulvinar ut elementum eget, luctus at nisl."}], "single-position": null}, "main": {"header": "\\u041a\\u0443\\u0445\\u043d\\u0438 \\u0438\\u0437 \\u0413\\u0435\\u0440\\u043c\\u0430\\u043d\\u0438\\u0438", "logo": true, "slogan": "\\u041f\\u041e\\u0414 \\u0417\\u0410\\u041a\\u0410\\u0417 \\u041e\\u0422 4000 \\u0415\\u0412\\u0420\\u041e\\n\\u0413\\u0410\\u0420\\u0410\\u041d\\u0422\\u0418\\u042f 5 \\u041b\\u0415\\u0422\\n\\u0420\\u0410\\u0411\\u041e\\u0422\\u0410\\u0415\\u041c \\u041f\\u041e \\u0412\\u0421\\u0415\\u0419 \\u0411\\u0415\\u041b\\u0410\\u0420\\u0423\\u0421\\u0418"}, "features": {"header": "\\u041f\\u043e\\u0447\\u0435\\u043c\\u0443 \\u0443 \\u043d\\u0430\\u0441?", "logo": null, "paragraphs": [{"header": "\\u041a\\u0430\\u0447\\u0435\\u0441\\u0442\\u0432\\u043e", "image": null, "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}, {"header": "\\u041a\\u0440\\u0430\\u0441\\u043e\\u0442\\u0430", "image": null, "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}, {"header": "\\u0423\\u0434\\u043e\\u0431\\u0441\\u0442\\u0432\\u043e", "image": null, "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}, {"header": "\\u0414\\u043e\\u043b\\u0433\\u043e\\u0432\\u0435\\u0447\\u043d\\u043e\\u0441\\u0442\\u044c", "image": null, "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}], "single-position": null}}')),
            ],
        ),
        migrations.DeleteModel(
            name='Content',
        ),
        migrations.AlterField(
            model_name='features',
            name='text',
            field=models.TextField(default="main\nattachment: scroll\npage-height: 100vh\nbackground: images/main.jpg\nlogo: images/l.png\nlogo-width: 189\nlogo-height: 136\nlogo-position: top left\nfont-size: 22px\nheader-size: 45px\nfont-family: 'Arial'\nfont-color: #dbdbdb\ninf-block-width: 75%\ninf-block-align: center\ninf-block-v-align: center\nmain-text-size: 90px\nmain-text-color: white\neffects: darken\nheader-color: white\ncolumns: none\n\nabout-us\nattachment: fixed\npage-height: 100vh\nbackground: white\neffects: none\nfont-family: 'Arial'\nheader-size: 30px\nheader-color: #121113\nmain-text-size: 90px\nmain-text-color: #121113\nfont-size: 14px\nfont-color: #8c8783\ninf-block-width: 60%\ninf-block-align: center\ninf-block-v-align: center\ncolumns: 1\nfl-bl-text-align: center\nfl-bl-header-align: center\nfl-image-position: top\nfl-block-background: none\nfl-single-image: none\nfl-image-form: square\n\nfeatures\nattachment: fixed\npage-height: 100vh\nbackground: white\neffects: none\nfont-family: 'Arial'\nheader-size: 30px\nheader-color: #121113\nmain-text-size: 90px\nmain-text-color: black\nfont-size: 14px\nfont-color: #8c8783\ninf-block-width: 60%\ninf-block-align: center\ninf-block-v-align: to-top\ncolumns: 2\nfl-bl-text-align: center\nfl-bl-header-align: center\nfl-image-position: top\nfl-block-background: none\nfl-single-image: none\nfl-image-form: square"),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
