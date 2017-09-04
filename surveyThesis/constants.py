#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

GENDER_CHOICES = (
	("", ""),
	("male", "Male"),
	("female", "Female"),
	("other", "Other"),
	
)

ED_CHOICES = (
	("", ""),
	('none', _(u'None')),
	('primary', _(u'Elementary/Middle School')),
	('secondary', _(u'High school')),
	('undergrad', _(u'Undergraduate')),
	('master', _(u'Master')),
	('phd', _(u'PhD')),
)

UG_CHOICES = (
	("", ""),
	("fr", _(u"Freshman")),
	("sp", _(u"Sophomore")),
	("jr", _(u"Junior")),
	("sr", _(u"Senior")),
)

YES_NO_CHOICES = (
	(True, _(u"Yes")),
	(False, _(u"No")),
)

GENDER_CHOICES = (
	("",""),
	("f", _(u"Female")),
	("m", _(u"Male")),
	("o", _(u"Other")),
)

PROFICIENCY_CHOICES = (
	("", ""),
	(1, _(u"Almost none (can't use at all)")),
	(2, _(u"Low (know very basic phrases)")),
	(3, _(u"Intermediate (can hold simple conversations)")),
	(4, _(u"Advanced")),
	(5, _(u"Very advanced")),
)

LANGUAGE_CHOICES = (
	("", ""),
	("en", _(u"English")),
	("es", _(u"Spanish")),
	("ab", _(u"Abkhazian")),
	("aa", _(u"Afar")),
	("af", _(u"Afrikaans")),
	("sq", _(u"Albanian")),
	("am", _(u"Amharic")),
	("ar", _(u"Arabic")),
	("an", _(u"Aragonese")),
	("hy", _(u"Armenian")),
	("as", _(u"Assamese")),
	("ay", _(u"Aymara")),
	("az", _(u"Azerbaijani")),
	("ba", _(u"Bashkir")),
	("eu", _(u"Basque")),
	("bn", _(u"Bengali (Bangla)")),
	("dz", _(u"Bhutani")),
	("bh", _(u"Bihari")),
	("bi", _(u"Bislama")),
	("br", _(u"Breton")),
	("bg", _(u"Bulgarian")),
	("my", _(u"Burmese")),
	("be", _(u"Byelorussian (Belarusian)")),
	("km", _(u"Cambodian")),
	("ca", _(u"Catalan")),
	("cherokee", _(u"Cherokee")),
	("chewa", _(u"Chewa")),
	("zh", _(u"Chinese")),
	("zh-Hans", _(u"Chinese (Simplified)")),
	("zh-Hant", _(u"Chinese (Traditional)")),
	("co", _(u"Corsican")),
	("hr", _(u"Croatian")),
	("cs", _(u"Czech")),
	("da", _(u"Danish")),
	("divehi", _(u"Divehi")),
	("nl", _(u"Dutch")),
	("edo", _(u"Edo")),
	("en", _(u"English")),
	("eo", _(u"Esperanto")),
	("et", _(u"Estonian")),
	("fo", _(u"Faeroese")),
	("fa", _(u"Farsi")),
	("fj", _(u"Fiji")),
	("fi", _(u"Finnish")),
	("flemish", _(u"Flemish")),
	("fr", _(u"French")),
	("fy", _(u"Frisian")),
	("fulfulde", _(u"Fulfulde")),
	("gl", _(u"Galician")),
	("gd", _(u"Gaelic (Scottish)")),
	("gv", _(u"Gaelic (Manx)")),
	("ka", _(u"Georgian")),
	("de", _(u"German")),
	("el", _(u"Greek")),
	("kl", _(u"Greenlandic")),
	("gn", _(u"Guarani")),
	("gu", _(u"Gujarati")),
	("ht", _(u"Haitian Creole")),
	("ha", _(u"Hausa")),
	("hawaiian", _(u"Hawaiian")),
	("he,iw", _(u"Hebrew")),
	("hi", _(u"Hindi")),
	("hu", _(u"Hungarian")),
	("ibibio", _(u"Ibibio")),
	("is", _(u"Icelandic")),
	("io", _(u"Ido")),
	("igbo", _(u"Igbo")),
	("id,in", _(u"Indonesian")),
	("ia", _(u"Interlingua")),
	("ie", _(u"Interlingue")),
	("iu", _(u"Inuktitut")),
	("ik", _(u"Inupiak")),
	("ga", _(u"Irish")),
	("it", _(u"Italian")),
	("ja", _(u"Japanese")),
	("jv", _(u"Javanese")),
	("kn", _(u"Kannada")),
	("kanuri", _(u"Kanuri")),
	("ks", _(u"Kashmiri")),
	("kk", _(u"Kazakh")),
	("rw", _(u"Kinyarwanda (Ruanda)")),
	("ky", _(u"Kirghiz")),
	("rn", _(u"Kirundi (Rundi)")),
	("konkani", _(u"Konkani")),
	("ko", _(u"Korean")),
	("ku", _(u"Kurdish")),
	("lo", _(u"Laothian")),
	("la", _(u"Latin")),
	("lv", _(u"Latvian (Lettish)")),
	("li", _(u"Limburgish ( Limburger)")),
	("ln", _(u"Lingala")),
	("lt", _(u"Lithuanian")),
	("mk", _(u"Macedonian")),
	("mg", _(u"Malagasy")),
	("ms", _(u"Malay")),
	("ml", _(u"Malayalam")),
	("mt", _(u"Maltese")),
	("mi", _(u"Maori")),
	("mr", _(u"Marathi")),
	("mo", _(u"Moldavian")),
	("mn", _(u"Mongolian")),
	("na", _(u"Nauru")),
	("ne", _(u"Nepali")),
	("no", _(u"Norwegian")),
	("oc", _(u"Occitan")),
	("or", _(u"Oriya")),
	("om", _(u"Oromo (Afaan Oromo)")),
	("papiamentu", _(u"Papiamentu")),
	("ps", _(u"Pashto (Pushto)")),
	("pl", _(u"Polish")),
	("pt", _(u"Portuguese")),
	("pa", _(u"Punjabi")),
	("qu", _(u"Quechua")),
	("rm", _(u"Rhaeto-Romance")),
	("ro", _(u"Romanian")),
	("ru", _(u"Russian")),
	("sami", _(u"Sami (Lappish)")),
	("sm", _(u"Samoan")),
	("sg", _(u"Sangro")),
	("sa", _(u"Sanskrit")),
	("sr", _(u"Serbian")),
	("sh", _(u"Serbo-Croatian")),
	("st", _(u"Sesotho")),
	("tn", _(u"Setswana")),
	("sn", _(u"Shona")),
	("ii", _(u"Sichuan Yi")),
	("sd", _(u"Sindhi")),
	("si", _(u"Sinhalese")),
	("ss", _(u"Siswati")),
	("sk", _(u"Slovak")),
	("sl", _(u"Slovenian")),
	("so", _(u"Somali")),
	("es", _(u"Spanish")),
	("su", _(u"Sundanese")),
	("sw", _(u"Swahili (Kiswahili)")),
	("sv", _(u"Swedish")),
	("syriac", _(u"Syriac")),
	("tl", _(u"Tagalog")),
	("tg", _(u"Tajik")),
	("tamazight", _(u"Tamazight")),
	("ta", _(u"Tamil")),
	("tt", _(u"Tatar")),
	("te", _(u"Telugu")),
	("th", _(u"Thai")),
	("bo", _(u"Tibetan")),
	("ti", _(u"Tigrinya")),
	("to", _(u"Tonga")),
	("ts", _(u"Tsonga")),
	("tr", _(u"Turkish")),
	("tk", _(u"Turkmen")),
	("tw", _(u"Twi")),
	("ug", _(u"Uighur")),
	("uk", _(u"Ukrainian")),
	("ur", _(u"Urdu")),
	("uz", _(u"Uzbek")),
	("venda", _(u"Venda")),
	("vi", _(u"Vietnamese")),
	("vo", _(u"Volapük")),
	("wa", _(u"Wallon")),
	("cy", _(u"Welsh")),
	("wo", _(u"Wolof")),
	("xh", _(u"Xhosa")),
	("yi-language", _(u"Yi")),
	("yi,ji", _(u"Yiddish")),
	("yo", _(u"Yoruba")),
	("zu", _(u"Zulu")),
)
