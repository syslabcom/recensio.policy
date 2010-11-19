# coding=utf8
import unittest2 as unittest
from BeautifulSoup import BeautifulSoup
from recensio.policy.opacsearch import OpacSearch, getString, createResult

sampleblob = '''<td>

    <a id="coverimg"></a>

  <span class="book_title">
  
    <strong>¬Das ZOPE-Buch
    




<!-- BEGIN addHSTtoUBand.jsp -->

<!-- END addHSTtoUBand.jsp -->
    </strong><br>
    
  
  </span>

  <span class="book_subtitle">
  
  
    Einführung und Dokumentation zur Entwicklung von Webanwendungen<br><br>
  
  </span>

   
  








<!-- START jsp/bsb/aufsatzDB_teaser.jsp -->

<!-- END jsp/bsb/aufsatzDB_teaser.jsp -->
  
  
    <strong class="c2">Autor / Hrsg.:</strong>
    <a href="/InfoGuideClient/search.do?methodToCall=quickSearch&amp;Kateg=100&amp;Content=Pelletier%2C+Michel">Pelletier, Michel</a><a>Martens</a><br>
  

    
    
    
    
    <strong class="c2">Ort, Verlag, Jahr:</strong> München/Germany, Markt+Technik-Verl., 2002<br />

    

    
    
    

    

    

    
                <span class="orig_origin"></span>
    
        
          <strong class="c2">Umfang:</strong>
          437 S. : Ill., graph. Darst.<br>
        

    
        
        
    
        
        
            
                <strong class="c2">Schlagwort:</strong>
            
            <a href="/InfoGuideClient/search.do?methodToCall=quickSearch&amp;Kateg=902&amp;Content=Zope+%3CProgramm%3E">Zope &lt;Programm&gt;</a>,
             
         
            
            <a href="/InfoGuideClient/search.do?methodToCall=quickSearch&amp;Kateg=902&amp;Content=World+Wide+Web">World Wide Web</a>,
             
         
            
            <a href="/InfoGuideClient/search.do?methodToCall=quickSearch&amp;Kateg=902&amp;Content=Server">Server</a>
             <br>
         
        
        
    
        
        <strong class="c2">Sprache:</strong>
            Deutsch
            <br>
        
        
    
        
            <strong class="c2">ISBN-ISSN-ISMN:</strong>
            
                3-8272-6194-5
                
              <br>
            
        
        
    
        
        

        
        





<!-- START jsp/bsb/coins.jsp -->


    
    
        
    
    


 









<!-- START jsp/bsb/permalink.jsp -->







    
        
    
    
    

<!-- END jsp/bsb/permalink.jsp -->






<span title="ctx_ver=Z39.88-2004&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&amp;rfr_id=&amp;rft_id=http%3A%2F%2Fopacplus.bsb-muenchen.de%2Fsearch%3Fisbn%3D3-8272-6194-5&amp;rft.genre=book&amp;rft.btitle=%C2%ACDas+ZOPE-Buch%3B+Einf%C3%BChrung+und+Dokumentation+zur+Entwicklung+von+Webanwendungen&amp;rft.isbn=3-8272-6194-5++&amp;rft.issn=&amp;rft.au=Pelletier%2C+Michel+&amp;rft.place=M%C3%BCnchen%2FGermany&amp;rft.pub=Markt%2BTechnik-Verl.&amp;rft.edition=&amp;rft.subject=Zope+%26lt%3BProgramm%26gt%3B&amp;rft.subject=World+Wide+Web&amp;rft.subject=Server&amp;rft.date=2002" class="Z3988"></span>






<!-- END jsp/bsb/coins.jsp -->
        <br>
        
        

        

        
        

        
        

        
        <!-- BEGIN bibtip_easy.jsp -->




<div style="display: none;" id="bibtip_id">
    6623618
</div>



    
    
        <div style="display: none;" id="bibtip_isxn">
            3-8272-6194-5
        </div>
    
    
    
    
    






    







    



<div style="display: none;" id="bibtip_shorttitle">
    Pelletier, Michel: ¬Das ZOPE-Buch (2002)
</div>


&nbsp;<br>&nbsp;
<div id="bibtip_reclist" style="display: none;"></div>
<!-- END bibtip_easy.jsp -->

        
        <div class="weblinks_clearer"></div>

            
            

<!-- BEGIN /jsp/bsb/AJAX/bsbISBN.jsp -->






<!-- END /jsp/bsb/AJAX/bsbISBN.jsp -->

            <div class="weblinks_clearer"></div>
            
            
<!-- BEGIN /jsp/bsb/TeaserButtons/buttons.jsp-->
<script type="text/javascript">
$(document).ready(function(){
    $("#share_button").click(function(){
        $("#share_links").toggle("normal");
        $("#permalink").hide();
        $("#volltext_field").hide();
    })
    $("#close_cross_share_links").click(function(){
        $("#share_links").slideUp("fast");
    })

    $("#permalink_button").click(function(){
        $("#permalink").toggle("normal");
        $("#volltext_field").hide();
        $("#share_links").hide();
    })
    
    $("#close_cross_permalink").click(function(){
        $("#permalink").slideUp("fast");
    })

    $("#volltext_button").click(function(){
        $("#volltext_field").toggle("normal");
        $("#permalink").hide();
        $("#share_links").hide();
    })
    $("#close_cross_volltext").click(function(){
        $("#volltext_field").slideUp("fast");
    })
    
})
</script>

<div id="buttons">
    
    








<!-- START jsp/bsb/bestelllink.jsp -->






        
    
                <a href="/InfoGuideClient/singleHit.do?methodToCall=activateTab&amp;tab=showAvailabilityActive&amp;tabnavi_only=true" class="bestelllink_teaser">Bestellung/Verfügbarkeit</a>
    
    
    
        |&nbsp;
    



<!-- END jsp/bsb/bestelllink.jsp -->

    





                
                    
                        <ig:display type="010" itemid="show_memorize_link">
                            
                            <a title="in die Merkliste" href="/InfoGuideClient/memorizeHitList.do?methodToCall=addToMemorizeList&amp;curPos=1&amp;forward=singlehit&amp;identifier=-1_FT_1873483991">
                                
                        in die Merkliste
                        </a>
                        </ig:display>
                        <ig:display type="100" itemid="show_memorize_link">
                        </ig:display>
                    
                    
                   
                         |&nbsp;

                


    <span class="button_right">
        













<!-- START jsp/bsb/permalink.jsp -->







    
        
    
    
    

<!-- END jsp/bsb/permalink.jsp -->



    
    
    
        
    

    <a href="#permalink" name="permalink" id="permalink_button">
        <img width="83" height="16" title="Einen persistenten Link generieren" alt="Permalink" src="/InfoGuideClient/images/permalink.gif">
   </a>
    <noscript>http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5&lt;br/&gt;</noscript>
    <div class="bb_box" id="permalink">
        <span class="bb_header"> Persistenter Link
            <a id="close_cross_permalink" href="#" class="rechts_oben"><img width="13" height="13" src="/InfoGuideClient/images/close.gif" alt="close"></a>
        </span>
        <div class="bb_main">
            Kopieren Sie diesen Link um auf dieses Werk Bezug zu nehmen:
            <span class="bb_link" id="permalink_link">http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5</span>
            <a onclick="set_bookmark('http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5','Bayerische Staatsbibliothek: ¬Das ZOPE-Buch')" href="#">&nbsp;<img src="/InfoGuideClient/images/add_bookmark_star.png" alt="">Bookmark / Lesezeichen setzen</a>
        </div>
    </div>

        





<!-- START jsp/bsb/shareLink.jsp -->








    
    




    





<a id="share_button" name="share_link" href="#share_link"><img width="126" height="16" title="Buch in einem sozialen Netzwerk verlinken" alt="Verlinken" src="/InfoGuideClient/images/Verlinken.gif"></a>
<div class="bb_box" id="share_links">
    <span class="bb_header"> Dieses Buch bekannt geben
            <a href="#" class="rechts_oben" id="close_cross_share_links"><img width="13" height="13" src="/InfoGuideClient/images/close.gif" alt="close"></a>
    </span>
    <p>
    Sie können diese Seite in den unten genannten sozialen Netzwerken und Diensten durch Klicken verlinken:
    </p>
    <ul>
        <li>
             <a target="blank" alt="Externer Link: Buch in Twitter bekannt geben." title="Externer Link: Buch in Twitter bekannt geben." href="http://twitter.com/home?status=Lese gerade http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5 ¬Das ZOPE-Buch der bsb_muenchen">
                <img src="/InfoGuideClient/images/shareLink/twitter.gif" alt="twitter_image">
                Twitter
             </a>
        </li>
        <li>
             <a target="blank" alt="Externer Link: Buch in Facebook bekannt geben." title="Externer Link: Buch in Facebook bekannt geben." href="http://www.facebook.com/sharer.php?u=http%3A%2F%2Fopacplus.bsb-muenchen.de%2Fsearch%3Fisbn%3D3-8272-6194-5&amp;t=Bayerische+Staatsbibliothek%3A+%C2%ACDas+ZOPE-Buch">
                <img src="/InfoGuideClient/images/shareLink/facebook.gif" alt="facebook_image">
                Facebook
             </a>
        </li>
        <li>
            <a target="blank" alt="Externer Link: Buch  im Lokalisten Tagebuch bekannt geben." title="Externer Link: Buch in im Lokalisten Tagebuch bekannt geben." href="http://www.lokalisten.de/web/user/editAccountDiary.do?method=edit&amp;diaryTypeId=1&amp;teaser=Bayerische Staatsbibliothek: ¬Das ZOPE-Buch&amp;diaryDesc=Super Buch: ¬Das ZOPE-Buch  sollte man unbedingt gelesen haben! Mehr dazu unter http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5.">
                <img src="/InfoGuideClient/images/shareLink/lokalisten.gif" alt="lokalisten">
                Lokalisten
            </a>
        </li>
        <li>
            <a alt="Externer Link: Buch bei Delicious verlinken." title="Externer Link: Buch bei Delicious verlinken." target="blank" href="http://del.icio.us/post?url=http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5&amp;title=¬Das ZOPE-Buch&amp;notes=Bayerische Staatsbibliothek: ¬Das ZOPE-Buch">
               <img src="/InfoGuideClient/images/shareLink/delicious.gif" alt="delicious_image">
               Delicious
            </a>
        </li>
        <li>
            <a target="blank" alt="Externer Link: Buch bei Mister Wong verlinken." title="Externer Link: Buch bei Mister Wong verlinken." href="http://www.mister-wong.de/index.php?action=addurl&amp;bm_url=http%3A%2F%2Fopacplus.bsb-muenchen.de%2Fsearch%3Fisbn%3D3-8272-6194-5&amp;bm_description=Bayerische Staatsbibliothek: ¬Das ZOPE-Buch&amp;bm_notice=Buch im Katalog der Bayerischen Staatsbibliothek: ¬Das ZOPE-Buch">
                <img src="/InfoGuideClient/images/shareLink/misterwong.gif" alt="mister_wong_image">
                Mister Wong
            </a>
       </li>
       <li>
             <a target="blank" alt="Externer Link: Buch in My Space bekannt geben." title="Externer Link: Buch in My Space bekannt geben." href="http://www.myspace.com/Modules/PostTo/Pages/?u=http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5&amp;t=Bayerische Staatsbibliothek: ¬Das ZOPE-Buch&amp;c=Lese gerade: ¬Das ZOPE-Buch.">
                <img src="/InfoGuideClient/images/shareLink/myspace.gif" alt="my_space_image">
                MySpace
             </a>
        </li>
               <li>
                <a target="blank" alt="Externer Link: Buch in LinkedIn bekannt geben." title="Externer Link: Buch in LinkedIn bekannt geben." href="http://www.linkedin.com/shareArticle?mini=true&amp;url=http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5&amp;title=Bayerische Staatsbibliothek: ¬Das ZOPE-Buch&amp;ro=false&amp;summary=Lese gerade Bayerische Staatsbibliothek: ¬Das ZOPE-Buch&amp;source=">
                <img src="/InfoGuideClient/images/shareLink/linked_in.gif" alt="linked_in_image">
                LinkedIn
             </a>
        </li>
        <li>
            <a alt="Externer Link: Buch bei Digg verlinken." title="Externer Link: Buch bei Digg verlinken." target="blank" href="http://digg.com/submit?phase=2&amp;url=http%3A%2F%2Fopacplus.bsb-muenchen.de%2Fsearch%3Fisbn%3D3-8272-6194-5&amp;title=Bayerische Staatsbibliothek: ¬Das ZOPE-Buch">
                <img src="/InfoGuideClient/images/shareLink/digg.gif" alt="digg_image">
                Digg
            </a>
        </li>
        <li>
            <a target="blank" alt="Externer Link: Buch bei StumbleUpon verlinken." title="Externer Link: Buch bei StumbleUpon verlinken." href="http://www.stumbleupon.com/submit?url=http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5">
                <img src="/InfoGuideClient/images/shareLink/stumbleupon.gif" alt="stumbleupon_image">
                StumbleUpon
            </a>
        </li>
        <li>
            <a target="blank" alt="Externer Link: Buch bei Google verlinken." title="Externer Link: Buch bei Google verlinken." href="http://www.google.com/bookmarks/mark?op=edit&amp;output=popup&amp;bkmk=http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5&amp;title=Bayerische Staatsbibliothek: ¬Das ZOPE-Buch">
               <img src="/InfoGuideClient/images/shareLink/google.gif" alt="google_image">
               Google
            </a>
        </li>
        <li>
            <a target="blank" alt="Externer Link: Buch bei Google verlinken." title="Externer Link: Buch bei Diigo bookmarken." href="http://secure.diigo.com/post?url=http://opacplus.bsb-muenchen.de/search?isbn=3-8272-6194-5&amp;title=Bayerische Staatsbibliothek: ¬Das ZOPE-Buch">
                <img src="/InfoGuideClient/images/shareLink/diigo.gif" alt="diigo_image">
                Diigo
            </a>
        </li>
        
    </ul>
</div>
<!-- END jsp/bsb/shareLink.jsp -->
    </span>



</div>
<!-- END /jsp/bsb/TeaserButtons/buttons.jsp-->

            <div class="weblinks_clearer"></div><br>
    </td>'''

class TestOpacSearch(unittest.TestCase):
    def testSuccessfulSearch(self):
        opac = OpacSearch()
        is_ = opac.getMetadataForISBN('3-8272-6194-5')
        should_be = [{'publisher': u'Markt+Technik-Verl.',
            'subtitle': u'Einf\xfchrung und Dokumentation zur Entwicklung von Webanwendungen',
            'location': u'M\xfcnchen/Germany',
            'language': u'Deutsch',
            'title': u'\xacDas ZOPE-Buch',
            'ddc': [u'Zope &lt;Programm&gt;', u'World Wide Web', u'Server'],
            'isbn': u'3-8272-6194-5',
            'authors': [{'lastname': u'Pelletier', 'firstname': u'Michel'}],
            'year': u'2002', 'pages': '437'}]
        self.assertEquals(should_be, is_)

    def testUnsuccessfulSearch(self):
        opac = OpacSearch()
        is_ = opac.getMetadataForISBN('')
        should_be = []
        self.assertEquals(should_be, is_)

    def testSuccessfulSearchFunnyISBN(self):
        opac = OpacSearch()
        is_1 = opac.getMetadataForISBN('3-8272-6194-5')
        is_2 = opac.getMetadataForISBN('3-8272-61945')
        is_3 = opac.getMetadataForISBN('3827261945')
        should_be = [{'publisher': u'Markt+Technik-Verl.',
            'subtitle': u'Einf\xfchrung und Dokumentation zur Entwicklung von Webanwendungen',
            'location': u'M\xfcnchen/Germany',
            'language': u'Deutsch',
            'title': u'\xacDas ZOPE-Buch',
            'ddc': [u'Zope &lt;Programm&gt;', u'World Wide Web', u'Server'],
            'isbn': u'3-8272-6194-5',
            'authors': [{'lastname': u'Pelletier', 'firstname': u'Michel'}],
            'year': u'2002', 'pages': '437'}]
        self.assertEquals(should_be, is_1)
        self.assertEquals([], is_2)
        self.assertEquals(is_1, is_3)

    def testOpacDown(self):
        self.assertRaises(IOError, OpacSearch, 'http://www.syslab.com2')
        opac = OpacSearch('http://www.syslab.com')
        self.assertRaises(IOError,  opac.getMetadataForISBN, '3-8272-6194-5')

    def testCreateResultTitle(self):
        soup1 = BeautifulSoup('<span class="book_title"><strong>Test</strong></span>')
        soup2 = BeautifulSoup('')
        self.assertEquals('Test', createResult(soup1)['title'])
        self.assertEquals(None, createResult(soup2)['title'])

    def testCreateResultSubtitle(self):
        soup1 = BeautifulSoup('''<span class="book_subtitle">
  
  
    Einführung und Dokumentation zur Entwicklung von Webanwendungen<br><br>
  </span>''')
        soup2 = BeautifulSoup('')
        self.assertEquals(u'Einführung und Dokumentation zur Entwicklung von Webanwendungen', createResult(soup1)['subtitle'].strip())
        self.assertEquals(None, createResult(soup2)['subtitle'])

    def testAuthors(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('Pelletier, Michel', 'Pelletier, Michel, Maier'))
        soup3 = BeautifulSoup('')
        self.assertEquals([
            {'lastname' : u'Martens', 'firstname' : None},
            {'firstname' : u'Michel', 'lastname' : u'Pelletier'}],
          createResult(soup1)['authors'])
        self.assertEquals([
            {'lastname' : u'Martens', 'firstname' : None},
            {'firstname' : None, 'lastname' : u'Pelletier, Michel, Maier'}],
          createResult(soup2)['authors'])
        self.assertEquals([], createResult(soup3)['authors'])

    def testLocationPublisherYear(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('München/Germany, Markt+Technik-Verl., 2002', 'München/Germany, Markt+Technik-Verl.,, 2002'))
        soup3 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        soup3_res = createResult(soup3)
        self.assertEquals(u'München/Germany', soup1_res['location'])
        self.assertEquals(u'Markt+Technik-Verl.', soup1_res['publisher'])
        self.assertEquals(u'2002', soup1_res['year'])
        self.assertEquals(None, soup2_res['location'])
        self.assertEquals(u'München/Germany, Markt+Technik-Verl.,, 2002', soup2_res['publisher'])
        self.assertEquals(None, soup2_res['year'])
        self.assertEquals(None, soup3_res['location'])
        self.assertEquals(None, soup3_res['publisher'])
        self.assertEquals(None, soup3_res['year'])


    def testPages(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('437', 'XXX'))
        soup3 = BeautifulSoup(sampleblob.replace('437', '437 337'))
        soup4 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        soup3_res = createResult(soup3)
        soup4_res = createResult(soup4)
        self.assertEquals('437', soup1_res['pages'])
        self.assertEquals(None, soup2_res['pages'])
        self.assertEquals('437 337', soup3_res['pages'])
        self.assertEquals(None, soup4_res['pages'])

    def testLanguage(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('Deutsch', ''))
        soup3 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        soup3_res = createResult(soup3)
        self.assertEquals('Deutsch', soup1_res['language'])
        self.assertEquals(None, soup2_res['language'])
        self.assertEquals(None, soup3_res['language'])

    def testDDC(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        self.assertEquals([u'Zope &lt;Programm&gt;', u'World Wide Web', u'Server'], soup1_res['ddc'])
        self.assertEquals(None, soup2_res['ddc'])

    def testISBN(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('3-8272-6194-5', ''))
        soup3 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        soup3_res = createResult(soup3)
        self.assertEquals('3-8272-6194-5', soup1_res['isbn'])
        self.assertEquals(None, soup2_res['isbn'])
        self.assertEquals(None, soup3_res['isbn'])

    def testGetString(self):
        is_ = getString(BeautifulSoup('''<strong>  Text
<!-- Comment --></strong>''')).strip()
        should_be = 'Text'
        self.assertEquals(should_be,is_)
