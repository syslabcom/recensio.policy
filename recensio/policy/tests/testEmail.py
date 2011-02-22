# -*- coding: utf-8 -*-

import unittest2 as unittest
from doctest import OutputChecker, ELLIPSIS

compare = lambda x, y:OutputChecker().check_output(x, y, ELLIPSIS)

from zope.component import getMultiAdapter
from zope.interface import directlyProvides

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer

class TestEmailFormat(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def texstFormat(self):
        expected_mail = u'''(English version see below)

**Liebe Abonnenten,**


wie jeden Monat freuen wir uns, Sie über Neuigkeiten auf recensio.net informieren zu können.

Angenehmes Stöbern und Entdecken wünscht Ihnen


*Ihre recensio.net-Redaktion.*


--------------------
Neue Rezensionen ...
--------------------

Zeitschrift 1
-------------
Tadeusz Kotłowski: Test ReviewMonograph No 0. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph935683199)


Fürchtegott Hubermüller: Test ReviewMonograph No 1. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph45869486)


François Lamère: Test ReviewMonograph No 2. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph45869487)


Fürchtegott Hubermüller: Test ReviewMonograph No 3. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph398373824)


Tadeusz Kotłowski: Test ReviewMonograph No 4. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph330877621)


Tadeusz Kotłowski: Test ReviewMonograph No 5. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph139418921)


Harald Schmidt: Test ReviewMonograph No 6. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph34443312)


François Lamère: Test ReviewMonograph No 7. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph984202830)


Fürchtegott Hubermüller: Test ReviewMonograph No 8. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph55508766)


Стоичков: Test ReviewMonograph No 9. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph75075260)


Test ReviewJournal No 0 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal816654554)


Test ReviewJournal No 1 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal749451901)


Test ReviewJournal No 2 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal271984688)


Test ReviewJournal No 3 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal658378399)


Test ReviewJournal No 4 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal745079423)


Test ReviewJournal No 5 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal736243531)


Test ReviewJournal No 6 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal75788844)


Test ReviewJournal No 7 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal761590244)


Test ReviewJournal No 8 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal521399713)


Test ReviewJournal No 9 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal479502338)

Zeitschrift 2
-------------
Стоичков: test title. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspaperb/summer/issue-2/ReviewMonograph736312157)



-----------------------
Neue Präsentationen ...
-----------------------

Präsentationen von Aufsätzen
----------------------------
Tadeusz Kotłowski: Test PresentationArticleReview No 0. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653150)


François Lamère: Test PresentationArticleReview No 1. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653151)


Стоичков: Test PresentationArticleReview No 2. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653152)


Tadeusz Kotłowski: Test PresentationArticleReview No 3. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653153)


Стоичков: Test PresentationArticleReview No 4. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653154)


François Lamère: Test PresentationArticleReview No 5. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653155)


Tadeusz Kotłowski: Test PresentationArticleReview No 6. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653156)


Fürchtegott Hubermüller: Test PresentationArticleReview No 7. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653157)


François Lamère: Test PresentationArticleReview No 8. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653158)


Стоичков: Test PresentationArticleReview No 9. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653159)


Стоичков: Test PresentationCollection No 0. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection40497463)


Fürchtegott Hubermüller: Test PresentationCollection No 1. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection914231235)


Fürchtegott Hubermüller: Test PresentationCollection No 2. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection66473592)


Fürchtegott Hubermüller: Test PresentationCollection No 3. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection672807398)


François Lamère: Test PresentationCollection No 4. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection662265084)


François Lamère: Test PresentationCollection No 5. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection144286261)


Стоичков: Test PresentationCollection No 6. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection496142500)


Tadeusz Kotłowski: Test PresentationCollection No 7. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection329622936)


François Lamère: Test PresentationCollection No 8. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection508653711)


Fürchtegott Hubermüller: Test PresentationCollection No 9. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection62282448)

Präsentationen von Internetressourcen
-------------------------------------
Test PresentationOnlineResource No 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource856653160)


Test PresentationOnlineResource No 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource856653161)


Test PresentationOnlineResource No 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource842650602)


Test PresentationOnlineResource No 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource765602758)


Test PresentationOnlineResource No 4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource8823777)


Test PresentationOnlineResource No 5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource888248672)


Test PresentationOnlineResource No 6
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource902751501)


Test PresentationOnlineResource No 7
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource565101041)


Test PresentationOnlineResource No 8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource276372135)


Test PresentationOnlineResource No 9
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource474931893)

Präsentationen von Monographien
-------------------------------
Tadeusz Kotłowski: Test PresentationMonograph No 0. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph798183973)


Harald Schmidt: Test PresentationMonograph No 1. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph798183974)


Fürchtegott Hubermüller: Test PresentationMonograph No 2. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph468219967)


Tadeusz Kotłowski: Test PresentationMonograph No 3. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph560568698)


Harald Schmidt: Test PresentationMonograph No 4. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph303462882)


Harald Schmidt: Test PresentationMonograph No 5. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph487988438)


Fürchtegott Hubermüller: Test PresentationMonograph No 6. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph754449079)


Стоичков: Test PresentationMonograph No 7. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph389229328)


François Lamère: Test PresentationMonograph No 8. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph759542674)


François Lamère: Test PresentationMonograph No 9. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph142652439)



-------------------------------------
Verfolgen Sie die Diskussion über ...
-------------------------------------

... die meistkommentierten Präsentationen des vergangenen Monats:
-----------------------------------------------------------------

test title (1 Comment)
~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspaperb/summer/issue-2/ReviewMonograph736312157)




*********************************************


**Dear subscribers,**


It’s time again for your monthly digest of news from recensio.net.

We hope you will enjoy browsing our platform and discovering its content.


*Your recensio.net editorial team*


---------------
New reviews ...
---------------

Zeitschrift 1
-------------
Tadeusz Kotłowski: Test ReviewMonograph No 0. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph935683199)


Fürchtegott Hubermüller: Test ReviewMonograph No 1. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph45869486)


François Lamère: Test ReviewMonograph No 2. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph45869487)


Fürchtegott Hubermüller: Test ReviewMonograph No 3. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph398373824)


Tadeusz Kotłowski: Test ReviewMonograph No 4. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph330877621)


Tadeusz Kotłowski: Test ReviewMonograph No 5. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph139418921)


Harald Schmidt: Test ReviewMonograph No 6. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph34443312)


François Lamère: Test ReviewMonograph No 7. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph984202830)


Fürchtegott Hubermüller: Test ReviewMonograph No 8. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph55508766)


Стоичков: Test ReviewMonograph No 9. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph75075260)


Test ReviewJournal No 0 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal816654554)


Test ReviewJournal No 1 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal749451901)


Test ReviewJournal No 2 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal271984688)


Test ReviewJournal No 3 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal658378399)


Test ReviewJournal No 4 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal745079423)


Test ReviewJournal No 5 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal736243531)


Test ReviewJournal No 6 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal75788844)


Test ReviewJournal No 7 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal761590244)


Test ReviewJournal No 8 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal521399713)


Test ReviewJournal No 9 (2008/2008) (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewJournal479502338)

Zeitschrift 2
-------------
Стоичков: test title. Dzieje państwa i społeczeństwa 1890–1945 (reviewed by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspaperb/summer/issue-2/ReviewMonograph736312157)



---------------------
New presentations ...
---------------------

Präsentationen von Aufsätzen
----------------------------
Tadeusz Kotłowski: Test PresentationArticleReview No 0. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653150)


François Lamère: Test PresentationArticleReview No 1. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653151)


Стоичков: Test PresentationArticleReview No 2. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653152)


Tadeusz Kotłowski: Test PresentationArticleReview No 3. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653153)


Стоичков: Test PresentationArticleReview No 4. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653154)


François Lamère: Test PresentationArticleReview No 5. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653155)


Tadeusz Kotłowski: Test PresentationArticleReview No 6. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653156)


Fürchtegott Hubermüller: Test PresentationArticleReview No 7. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653157)


François Lamère: Test PresentationArticleReview No 8. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653158)


Стоичков: Test PresentationArticleReview No 9. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview856653159)


Стоичков: Test PresentationCollection No 0. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection40497463)


Fürchtegott Hubermüller: Test PresentationCollection No 1. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection914231235)


Fürchtegott Hubermüller: Test PresentationCollection No 2. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection66473592)


Fürchtegott Hubermüller: Test PresentationCollection No 3. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection672807398)


François Lamère: Test PresentationCollection No 4. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection662265084)


François Lamère: Test PresentationCollection No 5. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection144286261)


Стоичков: Test PresentationCollection No 6. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection496142500)


Tadeusz Kotłowski: Test PresentationCollection No 7. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection329622936)


François Lamère: Test PresentationCollection No 8. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection508653711)


Fürchtegott Hubermüller: Test PresentationCollection No 9. Dzieje państwa i społeczeństwa 1890–1945
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationCollection62282448)

Präsentationen von Internetressourcen
-------------------------------------
Test PresentationOnlineResource No 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource856653160)


Test PresentationOnlineResource No 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource856653161)


Test PresentationOnlineResource No 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource842650602)


Test PresentationOnlineResource No 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource765602758)


Test PresentationOnlineResource No 4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource8823777)


Test PresentationOnlineResource No 5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource888248672)


Test PresentationOnlineResource No 6
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource902751501)


Test PresentationOnlineResource No 7
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource565101041)


Test PresentationOnlineResource No 8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource276372135)


Test PresentationOnlineResource No 9
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource474931893)

Präsentationen von Monographien
-------------------------------
Tadeusz Kotłowski: Test PresentationMonograph No 0. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph798183973)


Harald Schmidt: Test PresentationMonograph No 1. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph798183974)


Fürchtegott Hubermüller: Test PresentationMonograph No 2. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph468219967)


Tadeusz Kotłowski: Test PresentationMonograph No 3. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph560568698)


Harald Schmidt: Test PresentationMonograph No 4. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph303462882)


Harald Schmidt: Test PresentationMonograph No 5. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph487988438)


Fürchtegott Hubermüller: Test PresentationMonograph No 6. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph754449079)


Стоичков: Test PresentationMonograph No 7. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph389229328)


François Lamère: Test PresentationMonograph No 8. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph759542674)


François Lamère: Test PresentationMonograph No 9. Dzieje państwa i społeczeństwa 1890–1945 (presented by Христо Стоичков)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph142652439)



----------------------------
Follow the discussion on ...
----------------------------

... the presentations most commented on over the course of the past months:
---------------------------------------------------------------------------
test title (1 Comment)
~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspaperb/summer/issue-2/ReviewMonograph736312157)
'''
        portal = self.layer['portal']
        feeds = portal['RSS-feeds']
        request = self.layer['request']
        directlyProvides(request, IRecensioLayer)

        setRoles(portal, TEST_USER_ID, ['Manager'])

        mail_schema = IMailSchema(portal)
        mail_schema.email_from_address = 'fake@syslab.com'
        membership_tool = getToolByName(portal, 'portal_membership')
        user = membership_tool.getAuthenticatedMember()
        user.setProperties({'email': 'fake2@syslab.com'})

        view = getMultiAdapter((feeds, request), name='mail_results')

        class MockMailHost(object):
            sentMail = ''
            def send(self, messageText, mto, mfrom, subject, charset):
                self.sentMail = messageText
                self.mto = mto
                self.mfrom = mfrom
        view.mailhost = MockMailHost()

        view()
        self.assertEquals('Recensio.net <fake@syslab.com>', view.mailhost.mto)
        self.assertEquals('Recensio.net <fake@syslab.com>', view.mailhost.mfrom)
        for lineno, (expected, real) in enumerate(
                                  zip(expected_mail.split('\n'),
                                      view.mailhost.sentMail.split('\n'))):
            self.assertTrue(compare(expected, real), ("Error in Line %i:\nExp:\n%s\nGot:\n%s" % (lineno, '\n'.join(expected_mail.split('\n')[lineno-2:lineno+3]), '\n'.join(view.mailhost.sentMail.split('\n')[lineno-2:lineno+3]))).encode('ascii', 'ignore'))
