# -*- coding: utf-8 -*-

EXPORT_MAX_ITEMS = 10

EXPORT_OUTPUT_PATH = '/tmp/recensio'  

EXPORTABLE_CONTENT_TYPES = (
    'Presentation Online Resource',
    'Presentation Article Review',
    'Presentation Collection',
    'Review Journal',
    'Presentation Monograph',
    'Review Monograph'
    )
    
vocabularies = {
    'honorifics':{
        'frau':'Frau',
        'herr':'Herr',
        'frau_dr':'Frau Dr.',
        'herr_dr':'Herr Dr.',
        'frau_prof_dr':'Frau Prof. Dr.',
        'herr_prof_dr':'Herr Prof. Dr.',
        },

    'bibliographic_source_values':{
        u'bibliographien_kataloge_verzeichnisse':u'Bibliographien, Kataloge, Verzeichnisse',
        u'bibliothekskataloge':u'Bibliothekskataloge',
        u'bibliographien':u'Bibliographien',
        u'publikationslisten':u'Publikationslisten',
        u'verzeichnisse_von_arbeitspapier_und_preprintreihen':u'Verzeichnisse von Arbeitspapier- und Preprintreihen',
        u'verzeichnisse_von_hochschulschriften':u'Verzeichnisse von Hochschulschriften',
        u'verzeichnisse_von_elektronischen_buechern':u'Verzeichnisse von elektronischen Büchern',
        u'verzeichnisse_von_vortraegen_und_tagungsbeitraegen':u'Verzeichnisse von Vorträgen und Tagungsbeiträgen',
        u'verzeichnisse_von_berichten_studien':u'Verzeichnisse von Berichten, Studien',
        u'verzeichnisse_von_geschaefts_und_jahresberichten':u'Verzeichnisse von Geschäfts- und Jahresberichten',
        u'verzeichnisse_von_karten':u'Verzeichnisse von Karten',
        u'verzeichnisse_historischer_quellen':u'Verzeichnisse historischer Quellen',
        u'verzeichnisse_von_abbildungen':u'Verzeichnisse von Abbildungen',
        u'verzeichnisse_von_videos_und_filmen':u'Verzeichnisse von Videos und Filmen',
        u'verzeichnisse_von_audioquellen':u'Verzeichnisse von Audioquellen',
        u'verzeichnisse_von_software':u'Verzeichnisse von Software',
        u'verzeichnisse_verschiedener_medientypen':u'Verzeichnisse verschiedener Medientypen',
        u'sonstige_bibliographien_und_verzeichnisse':u'Sonstige Bibliographien und Verzeichnisse',
        },

    'cooperations_and_communication_values': {
        u'portale_virtuelle_bibliotheken': u'Portale, Virtuelle Bibliotheken',
        u'suchmaschinen': u'Suchmaschinen',
        u'nachrichten': u'Nachrichten',
        u'thematische_websites': u'Thematische Websites',
        u'personenspezifische_websites_biographien': u'Personenspezifische Websites / Biographien',
        u'forscherhomepages_websites': u'Forscherhomepages / -websites',
        u'forschungsprojekte_und_projektdatenbanken': u'Forschungsprojekte und Projektdatenbanken',
        u'kongresse_tagungen_veranstaltungen': u'Kongresse, Tagungen, Veranstaltungen',
        u'mailinglisten_foren_chats': u'Mailinglisten, Foren, Chats',
        u'weblogs': u'Weblogs',
        u'newsletter_alertingdienste': u'Newsletter, Alertingdienste',
        u'ausstellungen': u'Ausstellungen',
        u'sonstige_webdienste': u'Sonstige Webdienste'
        },

    'fulltexts_public_domain': {
        u'arbeitspapiere_pre_prints':u'Arbeitspapiere, Pre-Prints',
        u'aufsaetze':u'Aufsätze',
        u'hochschulschriften':u'Hochschulschriften',
        u'e_book':u'E-Book',
        u'vortraege_und_tagungsbeitraege':u'Vorträge und Tagungsbeiträge',
        u'berichte_studien':u'Berichte, Studien',
        u'geschaefts_und_jahresberichte':u'Geschäfts- und Jahresberichte',
        u'karten':u'Karten',
        u'historische_quellen':u'Historische Quellen',
        u'bildmaterial':u'Bildmaterial',
        u'videos_und_filme':u'Videos und Filme',
        u'audioquellen':u'Audioquellen',
        u'fachspezifische_software':u'Fachspezifische Software',
        u'sonstige_volltexte_und_quellen':u'Sonstige Volltexte und Quellen',
        },

    'periodicals_journals_magazines': {
        u'fachzeitschriften_und_jahrbuecher_mit_volltext':u'Fachzeitschriften und Jahrbücher (mit Volltext)',
        u'fachzeitschriften_und_jahrbuecher_ohne_volltext':u'Fachzeitschriften und Jahrbücher (ohne Volltext)',
        u'zeitungen_digitalisiert_mit_volltext':u'Zeitungen (digitalisiert) (mit Volltext)',
        u'zeitungen_digitalisiert_ohne_volltext':u'Zeitungen (digitalisiert) (ohne Volltext)',
        },

    'institution_values': {
        u'bibliotheken': u'Bibliotheken',
        u'archive': u'Archive',
        u'museen': u'Museen',
        u'verlage_und_datenbankanbieter': u'Verlage und Datenbankanbieter',
        u'hochschulen': u'Hochschulen',
        u'forschungseinrichtungen': u'Forschungseinrichtungen',
        u'fachgesellschaften_und_berufsverbaende': u'Fachgesellschaften und Berufsverbände',
        u'amtliche_koerperschaften_und_organisationen': u'Amtliche Körperschaften und Organisationen',
        u'internationale_organisationen': u'Internationale Organisationen',
        u'nichtregierungsorganisationen': u'Nichtregierungsorganisationen',
        u'public_private_partnership': u'Public Private Partnership',
        u'parteien_und_politische_organisationen': u'Parteien und politische Organisationen',
        u'verbaende': u'Verbände',
        u'medien': u'Medien',
        u'unternehmen': u'Unternehmen',
        u'sonstige_institutionen': u'Sonstige Institutionen',
        },

    'reference_values': {
         u'allgemeine_lexika':u'Allgemeine Lexika',
         u'biographische_lexika':u'Biographische Lexika',
         u'wikis_glossare_spezielle_nachschlagewerke':u'Wikis, Glossare, spezielle Nachschlagewerke',
         u'woerterbuecher':u'Wörterbücher',
         u'personenverzeichnisse':u'Personenverzeichnisse',
         u'unternehmens_und_institutionenverzeichnisse':u'Unternehmens- und Institutionenverzeichnisse',
         u'laenderinformationen':u'Länderinformationen',
         u'datensammlungen_und_statistiken':u'Datensammlungen und Statistiken',
         u'gesetzeskommentare':u'Gesetzeskommentare',
         u'tabellenwerke':u'Tabellenwerke',
         u'abkuerzungswerke':u'Abkürzungswerke',
         u'normen_und_standards':u'Normen und Standards',
         u'anleitungen_handbuecher_lehrmaterial':u'Anleitungen, Handbücher, Lehrmaterial',
         u'sonstige_nachschlagewerke':u'Sonstige Nachschlagewerke',
         }
    }


languages = [u'sq',
             u'hy',
             u'az',
             u'bg',
             u'ca',
             u'hr',
             u'cs',
             u'da',
             u'nl',
             u'en',
             u'et',
             u'fi',
             u'fr',
             u'ka',
             u'de',
             u'el',
             u'hu',
             u'it',
             u'lv',
             u'lt',
             u'no',
             u'pl',
             u'pt',
             u'ro',
             u'ru',
             u'sr',
             u'sk',
             u'sl',
             u'es',
             u'sv',
             u'tr',
             u'uk']

interface_languages = [
        u'de',
        u'fr',
        u'en',
        ]

