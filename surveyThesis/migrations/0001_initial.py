# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('participantNumber', models.IntegerField()),
                ('age', models.IntegerField()),
                ('education', models.CharField(max_length=50, choices=[(b'none', 'None'), (b'primary', 'Elementary/Middle School'), (b'secondary', 'High school'), (b'undergrad', 'Undergraduate'), (b'master', 'Master'), (b'phd', 'PhD')])),
                ('date', models.DateTimeField(auto_now=True)),
                ('nativeLanguage', models.CharField(max_length=50, choices=[(b'en', 'English'), (b'es', 'Spanish'), (b'ab', 'Abkhazian'), (b'aa', 'Afar'), (b'af', 'Afrikaans'), (b'sq', 'Albanian'), (b'am', 'Amharic'), (b'ar', 'Arabic'), (b'an', 'Aragonese'), (b'hy', 'Armenian'), (b'as', 'Assamese'), (b'ay', 'Aymara'), (b'az', 'Azerbaijani'), (b'ba', 'Bashkir'), (b'eu', 'Basque'), (b'bn', 'Bengali (Bangla)'), (b'dz', 'Bhutani'), (b'bh', 'Bihari'), (b'bi', 'Bislama'), (b'br', 'Breton'), (b'bg', 'Bulgarian'), (b'my', 'Burmese'), (b'be', 'Byelorussian (Belarusian)'), (b'km', 'Cambodian'), (b'ca', 'Catalan'), (b'cherokee', 'Cherokee'), (b'chewa', 'Chewa'), (b'zh', 'Chinese'), (b'zh-Hans', 'Chinese (Simplified)'), (b'zh-Hant', 'Chinese (Traditional)'), (b'co', 'Corsican'), (b'hr', 'Croatian'), (b'cs', 'Czech'), (b'da', 'Danish'), (b'divehi', 'Divehi'), (b'nl', 'Dutch'), (b'edo', 'Edo'), (b'en', 'English'), (b'eo', 'Esperanto'), (b'et', 'Estonian'), (b'fo', 'Faeroese'), (b'fa', 'Farsi'), (b'fj', 'Fiji'), (b'fi', 'Finnish'), (b'flemish', 'Flemish'), (b'fr', 'French'), (b'fy', 'Frisian'), (b'fulfulde', 'Fulfulde'), (b'gl', 'Galician'), (b'gd', 'Gaelic (Scottish)'), (b'gv', 'Gaelic (Manx)'), (b'ka', 'Georgian'), (b'de', 'German'), (b'el', 'Greek'), (b'kl', 'Greenlandic'), (b'gn', 'Guarani'), (b'gu', 'Gujarati'), (b'ht', 'Haitian Creole'), (b'ha', 'Hausa'), (b'hawaiian', 'Hawaiian'), (b'he,iw', 'Hebrew'), (b'hi', 'Hindi'), (b'hu', 'Hungarian'), (b'ibibio', 'Ibibio'), (b'is', 'Icelandic'), (b'io', 'Ido'), (b'igbo', 'Igbo'), (b'id,in', 'Indonesian'), (b'ia', 'Interlingua'), (b'ie', 'Interlingue'), (b'iu', 'Inuktitut'), (b'ik', 'Inupiak'), (b'ga', 'Irish'), (b'it', 'Italian'), (b'ja', 'Japanese'), (b'jv', 'Javanese'), (b'kn', 'Kannada'), (b'kanuri', 'Kanuri'), (b'ks', 'Kashmiri'), (b'kk', 'Kazakh'), (b'rw', 'Kinyarwanda (Ruanda)'), (b'ky', 'Kirghiz'), (b'rn', 'Kirundi (Rundi)'), (b'konkani', 'Konkani'), (b'ko', 'Korean'), (b'ku', 'Kurdish'), (b'lo', 'Laothian'), (b'la', 'Latin'), (b'lv', 'Latvian (Lettish)'), (b'li', 'Limburgish ( Limburger)'), (b'ln', 'Lingala'), (b'lt', 'Lithuanian'), (b'mk', 'Macedonian'), (b'mg', 'Malagasy'), (b'ms', 'Malay'), (b'ml', 'Malayalam'), (b'mt', 'Maltese'), (b'mi', 'Maori'), (b'mr', 'Marathi'), (b'mo', 'Moldavian'), (b'mn', 'Mongolian'), (b'na', 'Nauru'), (b'ne', 'Nepali'), (b'no', 'Norwegian'), (b'oc', 'Occitan'), (b'or', 'Oriya'), (b'om', 'Oromo (Afaan Oromo)'), (b'papiamentu', 'Papiamentu'), (b'ps', 'Pashto (Pushto)'), (b'pl', 'Polish'), (b'pt', 'Portuguese'), (b'pa', 'Punjabi'), (b'qu', 'Quechua'), (b'rm', 'Rhaeto-Romance'), (b'ro', 'Romanian'), (b'ru', 'Russian'), (b'sami', 'Sami (Lappish)'), (b'sm', 'Samoan'), (b'sg', 'Sangro'), (b'sa', 'Sanskrit'), (b'sr', 'Serbian'), (b'sh', 'Serbo-Croatian'), (b'st', 'Sesotho'), (b'tn', 'Setswana'), (b'sn', 'Shona'), (b'ii', 'Sichuan Yi'), (b'sd', 'Sindhi'), (b'si', 'Sinhalese'), (b'ss', 'Siswati'), (b'sk', 'Slovak'), (b'sl', 'Slovenian'), (b'so', 'Somali'), (b'es', 'Spanish'), (b'su', 'Sundanese'), (b'sw', 'Swahili (Kiswahili)'), (b'sv', 'Swedish'), (b'syriac', 'Syriac'), (b'tl', 'Tagalog'), (b'tg', 'Tajik'), (b'tamazight', 'Tamazight'), (b'ta', 'Tamil'), (b'tt', 'Tatar'), (b'te', 'Telugu'), (b'th', 'Thai'), (b'bo', 'Tibetan'), (b'ti', 'Tigrinya'), (b'to', 'Tonga'), (b'ts', 'Tsonga'), (b'tr', 'Turkish'), (b'tk', 'Turkmen'), (b'tw', 'Twi'), (b'ug', 'Uighur'), (b'uk', 'Ukrainian'), (b'ur', 'Urdu'), (b'uz', 'Uzbek'), (b'venda', 'Venda'), (b'vi', 'Vietnamese'), (b'vo', 'Volap\xfck'), (b'wa', 'Wallon'), (b'cy', 'Welsh'), (b'wo', 'Wolof'), (b'xh', 'Xhosa'), (b'yi-language', 'Yi'), (b'yi,ji', 'Yiddish'), (b'yo', 'Yoruba'), (b'zu', 'Zulu')])),
            ],
        ),
    ]
