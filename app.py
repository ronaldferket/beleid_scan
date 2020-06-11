#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go
import copy


# In[2]:


lijst_vragen = { 1: {'mdw': ['Een medewerker informeert een student+ persoonlijk over zijn rol.', 
        'De informatie geeft een student+ inzicht in de mogelijkheden (toegankelijkheid) bij een opleiding.',
        'De informatie is via één communicatiemiddel beschikbaar binnen de opleiding.',
        'Bij de digitale aanmelding wordt niet gevraagd de ondersteuningsvraag te melden.',
        'Een student+ ontvangt op aanvraag informatie over studeren met een ondersteuningsvraag.'], 
 'bld' : ['Een medewerker informeert studenten+ over het beleid m.b.t. passende ondersteuning van de opleiding op een moment dat ditrelevant is.',
         ' De informatie geeft studenten+ inzicht in de mogelijkheden (toegankelijkheid) het vakgebied.',
         'De informatie is via meerdere communicatiemiddelen beschikbaar op opleidingsniveau.',
         'Bij de digitale aanmelding en tijdens intake wordt gevraagd de ondersteuningsvraag te melden.',
         'Studenten+ ontvangen standaard na aanmelding informatie over studeren met een ondersteuningsvraag.'], 
 'org': ['De instelling informeert tijdens de voorlichting studenten structureel over de ondersteuningsmogelijkheden.',
        'De informatie geeft studenten+, studiebegeleiders en docenten inzicht in de mogelijkheden (toegankelijkheid) van de instelling.',
        'De informatie is via meerdere communicatiemiddelen beschikbaar op instellingsniveau.',
        'Bij de digitale aanmelding en tijdens de intake gevraagd de ondersteuningsvraag te melden. Wanneer nodig vindt er een warme overdracht plaats met toeleverend onderwijs.',
        'Alle studenten ontvangen standaard na aanmelding en bij de inschrijving informatie over studeren met een ondersteuningsvraag en de aanwezige ondersteuningsmogelijkheden.'], 
 'rst' : ['De instelling informeert tijdens de voorlichting studenten structureel over de ondersteuningsmogelijkheden. De instelling evalueert jaarlijks of dit toereikend is.',
         'De informatie geeft studenten+, studiebegeleiders en docenten inzicht in de mogelijkheden (toegankelijkheid) van de instelling. Deze informatie wordt jaarlijks geactualiseerd.',
         'De informatie is via meerdere communicatiemiddelen beschikbaar op instellingsniveau. De toegankelijkheid van deze informatie wordt jaarlijks geëvalueerd.',
         'Bij de digitale aanmelding, tijdens de intake en tijdens de inschrijving wordt gevraagd de ondersteuningsvraag te formuleren. Het aantal meldingen en ondersteuningsvragen wordt jaarlijks geanalyseerd.',
         'Alle studenten ontvangen standaard na aanmelding en bij de inschrijving informatie over ondersteuningsmogelijkheden. Jaarlijks wordt geëvalueerd of de informatie toereikend is.']},
         2: {'mdw': ['Voor een student+ worden op verzoek een gebouw, ruimtes en faciliteitenaangepast.',
        'Sommige medewerkers passen op eigen initiatief webrichtlijnen (WCAG) met betrekking tot toegankelijkheid toe.',
        'Studiematerialen worden incidenteel aangepast voor een student+.',
        'Digitale studiematerialen c.q. hulpmiddelen worden op verzoek verstrekt aan een student+.'], 
 'bld' : ['De opleiding zorgt structureel voor toegankelijkheid van enkele gebouwen, ruimtes, en faciliteiten',
         'Werkgroepleden werken toe naar het keurmerk drempelvrij.nl en aan een (elektronische) leeromgeving die voldoet aan de WCAG criteria.',
         'Studiematerialen worden structureel aangepast voor specifieke functiebeperkingen.',
         'Digitale studiematerialen c.q. hulpmiddelen worden vroegtijdig verstrekt aan alle studenten+. De opleiding neemt hierin het initiatief.'], 
 'org': ['Een (beleids)afdeling is verantwoordelijk voor de toegankelijkheid van alle gebouwen, ruimtes en faciliteiten, en passende BPV’s.',
        'De website heeft het keurmerk drempelvrij.nl en de (elektronische) leeromgeving voldoet aan de internationale WCAG criteria.',
        'Studiematerialen zijn gebruiksvriendelijk voor alle studenten.',
        'Digitale studiematerialen c.q. hulpmiddelen worden vroegtijdig door de instelling of opleiding verstrekt, zodat alle studenten tijdig beschikken over het (al dan niet aangepaste) lesmateriaal. '], 
 'rst' : ['Een (beleids)afdeling is verantwoordelijk voor de toegankelijkheid van alle gebouwen, ruimtes en faciliteiten, en passende BPV’s. Jaarlijks wordt dit geëvalueerd.',
         'De website heeft het keurmerk drempelvrij.nl en de (elektronische) leeromgeving voldoet aan de WCAG criteria. Jaarlijks wordt dit geëvalueerd.',
         'Studiematerialen zijn gebruiksvriendelijk voor alle studenten. Jaarlijks wordt dit geëvalueerd.',
         'Digitale studiematerialen c.q. hulpmiddelen studiematerialen worden vroegtijdig door de instelling verstrekt, zodat alle studenten tijdig beschikken over het (al dan niet aangepaste) lesmateriaal. Jaarlijks wordt dit geëvalueerd en geactualiseerd.']},
         3: {'mdw': ['Een student+ krijgt op verzoek naast deintake een verdiepend intakegesprek.',
        '(Individuele) aanpassingen worden mondeling besproken en omvatten de rechten en plichten van de student+. Afspraken over verantwoordelijkheden voor de uitvoering worden niet vastgelegd.',
        'Een student+ krijgt te maken met wisselende begeleiders.',
        'Contact tussen een student+ en studieloopbaanbegeleiders vindt incidenteel plaats.'], 
 'bld' : ['Studenten+ krijgen standaard, naast de intake een uitnodiging voor een verdiepend intakegesprek.',
         '(Individuele) aanpassingen worden schriftelijk vastgelegd en omvatten de rechten en plichten van studenten+. De instelling of opleiding wijst een verantwoordelijke voor de uitvoering aan.',
         '. De opleiding bevordert dat studenten+ vaste begeleiders krijgen.',
         'Contact tussen studenten+ en studieloopbaanbegeleiders vindt structureel plaats.'], 
 'org': ['Studenten+ krijgen standaard, als onderdeel van de intakeprocedure een verdiepend intakegesprek. Studenten+ kunnen hierin hun ondersteuningsbehoeftes kenbaar maken',
        '(Individuele) aanpassingen worden schriftelijk vastgelegd en omvatten de overeengekomen aanpassingen en rechten en plichten van de instelling en studenten+. De instelling is verantwoordelijk voor de uitvoering van de afspraken.',
        'De instelling bevordert dat studenten+ vaste begeleiders krijgen met de juiste deskundigheid.',
        'De studieloopbaanbegeleider onderhoudt het contact tussen studenten+ en anderen, gericht op het versterken van de binding tussen studenten+ en het opleidingsteam. '], 
 'rst' : ['Studenten+ krijgen standaard, als onderdeel van de intakeprocedure een verdiepend intakegesprek. Studenten+ kunnen hierin hun ondersteuningsbehoeftes kenbaar maken. Jaarlijks vindt een evaluatie plaats met de student.',
         '(Individuele) aanpassingen worden schriftelijk vastgelegd en omvatten de overeengekomen aanpassingen en de rechten en plichten van de instelling en studenten+. De instelling is verantwoordelijk voor de uitvoering van de afspraken. De gemaakte afspraken worden jaarlijks geëvalueerd en zo nodig bijgesteld.',
         'De instelling bevordert dat studenten+ vaste begeleiders krijgen met de juiste deskundigheid. De expertise van begeleiders wordt jaarlijks geëvalueerd en verder geprofessionaliseerd.',
         'De studieloopbaanbegeleider onderhoudt het contact tussen studenten+ en anderen, gericht op het versterken van de binding tussen studenten+ en de opleiding. De contacten worden gemonitord om de afstemming te optimaliseren.']},
         4: {'mdw': ['Een medewerker kan zich op eigeninitiatief (verder) professionaliseren.',
        'Voor een direct betrokken medewerker wordt zo nodig scholing georganiseerd.',
        'Een medewerker wordt incidenteel ondersteund door een intern of extern deskundige.',
        'Passend onderwijs komt niet aan de orde tijdens het inwerkprogramma van nieuwe docenten.'], 
 'bld': ['De opleiding bevordert structureel specifieke professionalisering van medewerkers.',
        'Direct betrokken medewerkers hebben een basisniveau aan kennis en kunnen studenten indien nodig doorverwijzen.',
        'Medewerkers worden op opleidingsniveau structureel ondersteund door een intern ofextern deskundige.',
        'Passend onderwijs komt facultatief aan de orde tijdens het inwerkprogramma vannieuwe docenten.'], 
 'org': ['De instelling vereist structureel specifieke professionalisering van medewerkers.',
        'Direct betrokken medewerkers hebben basiskennis passend onderwijs op functieniveau en kunnen studenten basisondersteuning bieden en indien nodig doorverwijzen.',
        'Medewerkers worden op instellingsniveau structureel ondersteund door een intern of extern deskundige.',
        'Passend onderwijs vormt een wezenlijk onderdeel van het inwerkprogramma van nieuwe docenten.'],
 'rst': ['De instelling vereist structureel specifieke professionalisering van medewerkers. Dit ligt vast in het professionaliseringsplan en wordt structureel meegenomen in POP-gesprekken van medewerkers. Jaarlijks evalueert de instelling de stand van zaken rondom de deskundigheid.',
        'Direct betrokken medewerkers hebben op functieniveau basiskennis van passend onderwijs, kunnen studenten basisondersteuning bieden en indien nodig doorverwijzen. Handelingsbekwaamheid op het vlak van ‘Studeren met een ondersteuningsvraag’ maakt onderdeel uit van het functioneringsgesprek.',
        'Medewerkers worden op instellingsniveau structureel ondersteund door een intern of extern deskundige. Jaarlijks wordt de ondersteuning en de inzet van deskundigen geëvalueerd en waar nodig aangepast.',
        'Passend onderwijs vormt een wezenlijk onderdeel van het inwerkprogramma van nieuwe docenten en wordt periodiek geëvalueerd en geactualiseerd.']},
         5: {'mdw': ['Een student+ stelt met individuele docenten een flexibele onderwijsroute op. Deze wordt mondeling besproken.',
        'Het aanpassen van onderwijsroutes vindt plaats naar bevind van zaken. Taken, bevoegdheden en verantwoordelijkheden zijn niet omschreven',
        'Beslissingen over onderwijsroute worden ad hoc en individueel genomen.',
        'd De kaders voor het opstellen van een onderwijsroute zijn afhankelijk van de betrokken medewerker.'], 
 'bld': ['Een student+ stelt met zijn begeleider een flexibele onderwijsroute route op. Deze wordt schriftelijk vastgelegd. De student+ is verantwoordelijk voor het nakomen van de afspraken.',
        'Het aanpassen van onderwijsroute gebeurt volgens vaste procedures. Taken, bevoegdheden en verantwoordelijkheden zijn niet eenduidig omschreven.',
        'Beslissingen over onderwijsroute worden genomen door medewerkers met voldoende kennis van zaken.',
        '. De opleiding formuleert kaders voor het opstellen van een onderwijsroute.'], 
 'org': ['Een student+ stelt met zijn begeleider een flexibele onderwijsroute op. Deze wordt schriftelijk vastgelegd. Het naleven ervan wordt door de opleiding gemonitord',
        'Het aanpassen van onderwijsroutes gebeurt volgens vaste procedures. Taken, bevoegdheden en verantwoordelijkheden zijn op instellingsniveau vastgelegd.',
        'Beslissingen over onderwijsroute worden genomen op basis van instellingsbeleid.',
        '. In de onderwijs- en examenregeling zijn op instellingsniveau kaders opgenomen voor het opstellen van een onderwijsroute.'],
 'rst': [' Een student+ stelt met zijn begeleider een flexibele onderwijsroute op. Deze wordt schriftelijk vastgelegd. Het naleven ervan wordt door de opleiding gemonitord. Jaarlijks worden de afspraken geëvalueerd',
        'Het aanpassen van onderwijsroutes gebeurt volgens vaste procedures. Taken, bevoegdheden en verantwoordelijkheden zijn op instellingsniveau vastgelegd. De procedures worden jaarlijks geëvalueerd.',
        'Beslissingen over onderwijsroute worden genomen op basis van instellingsbeleid door deskundigen van het examenbureau, in samenspraak met deskundigen passend onderwijs. De besluitvorming wordt jaarlijks geëvalueerd.',
        'In de onderwijs- en examenregeling zijn op instellingsniveau kaders opgenomen voor het opstellen van een onderwijsroute. De gestelde kaders worden jaarlijks geëvalueerd.']},
         6: {'mdw': ['Er ligt niet vast binnen welke termijn een verzoek moet worden behandeld.',
        '. Een medewerker beslist over aanpassingen. De gehanteerde criteria zijn persoonlijk.',
        'Besluiten over aanpassingen neemt een medewerker naar bevind van zaken.',
        'Afspraken tussen instelling en een student+ worden mondeling gemaakt'], 
 'bld': ['Verzoeken worden binnen een door de opleiding vastgestelde termijn behandeld.',
        'Examencommissies beslissen over aanpassingen. Criteria zijn op opleidingsniveau beschreven.',
        'Besluiten over aanpassingen worden naar bevind van zaken genomen op basis van voldoende kennis van belemmeringen als gevolg van een functiebeperking.',
        'Afspraken tussen instelling en studenten+ worden schriftelijk vastgelegd. De student+ is verantwoordelijk voor de naleving ervan.'], 
 'org': ['Verzoeken worden binnen een door de instelling vastgestelde termijn behandeld.',
        'Examencommissies beslissen, zonodig in samenspraak met het CvTE, over aanpassingen. Criteria zijn op instellingsniveau beschreven',
        'Besluiten over aanpassingen worden naar bevind van zaken genomen op basis van wetgeving, beleid en op basis van voldoende kennis van belemmeringen als gevolg van een functiebeperking.',
        'Afspraken tussen instelling en studenten+ worden schriftelijk vastgelegd. Het naleven ervan wordt door de opleiding gemonitord. '],
 'rst': ['Verzoeken worden binnen een door de instelling vastgestelde termijn behandeld. De haalbaarheid wordt jaarlijks geëvalueerd.',
        'Examencommissies beslissen, zonodig in samenspraak met het CvTE, over aanpassingen. Criteria zijn op instellingsniveau beschreven. De aanpassingen worden jaarlijks geëvalueerd',
        ' Besluiten over aanpassingen worden naar bevind van zaken genomen op basis van wetgeving, beleid en op basis van voldoende kennis van belemmeringen als gevolg van een functiebeperking. De procedure en de genomen besluiten worden jaarlijks geëvalueerd',
        'Afspraken tussen instelling en studenten+ worden schriftelijk vastgelegd. Het naleven ervan wordt door de opleiding gemonitord. Jaarlijks worden de afspraken geëvalueerd.']},
         7: {'mdw': ['De persoonlijke visie van een medewerker staat voorop',
        'Een student+ geeft een medewerker indien gewenst feedback op de onderwijskwaliteit.',
        'Op verzoek kan in deelaspecten uit het kwaliteitsbeleid worden voorzien.',
        '. Gemaakte afspraken worden, met toestemming van een student+, gecommuniceerd naar een specifieke medewerker.'], 
 'bld': ['De opleiding heeft een visie, beleid en  doelstellingen.',
        '. De kwaliteit van passend onderwijs wordt op opleidingsniveau geëvalueerd met in ieder geval studenten+.',
        'Op opleidingsniveau ligt vast hoe in de aspecten uit kwaliteitsbeleid is voorzien.',
        'Gemaakte afspraken worden, met toestemming van studenten+, en zo nodig geanonimiseerd, gecommuniceerd binnen de opleiding.'], 
 'org': ['De instelling heeft een visie, beleid en doelstellingen. Het kwaliteitsbeleid ligt hieraan ten grondslag.',
        'De kwaliteit van passend onderwijs wordt op instellingsniveau geëvalueerd met in ieder geval studenten+.',
        'In het studentenstatuut van de instelling ligt vast hoe in de aspecten uit het kwaliteitsbeleid en passend onderwijs is voorzien.',
        'Gemaakte afspraken worden, met toestemming van studenten+, en zo nodig geanonimiseerd, gecommuniceerd binnen de instelling.'],
 'rst': ['De instelling heeft een visie, kwaliteitsbeleid en doelstellingen. Continuïteit van beleid is gewaarborgd via de inzet van mensen en middelen.',
        'De kwaliteit van passend onderwijs wordt op instellingsniveau geëvalueerd met in ieder geval studenten+. Evaluatiegegevens worden aantoonbaar gebruikt voor verbetering van het onderwijs.',
        'In het studentenstatuut van de instelling ligt vast hoe in de aspecten uit het kwaliteitsbeleid en passend onderwijs is voorzien. Jaarlijks wordt de tevredenheid van studenten gemeten. Dit wordt als input gebruikt voor beleidsbijstelling',
        'Gemaakte afspraken worden, met toestemming van studenten+, en zo nodig geanonimiseerd, gecommuniceerd binnen de instelling. Jaarlijks worden de afspraken geëvalueerd.']},
         8: {'mdw': ['Een medewerker begeleidt een student+ op verzoek naar BPV en werk.',
        ' De kennis van de ondersteuningsbehoeften van een student+ ten aanzien van stage en werk is afhankelijk van de interesses van een medewerker',
        ' Een medewerker legt indien gewenst contacten met werkgevers voor een student+.',
        'Incidenteel wordt een medewerker met een functiebeperking aangenomen.'], 
 'bld': ['Op opleidingsniveau liggen procedures voor het toeleiden van studenten+ naar BPV en werk vast.',
        'De BPV-coördinator heeft kennis van de ondersteuningsbehoeften van studenten+ ten aanzien van stage en werk.',
        'De BPV-coördinator legt contact met werkgevers voor studenten+.',
        'Een opleiding biedt als werkgever mogelijkheden aan mensen met een functiebeperking.'], 
 'org': ['Op instellingsniveau liggen procedures voor het toeleiden van studenten+ naar BPV en werk vast.',
        'De medewerkers van het stage/BPVbureau hebben kennis van de ondersteuningsbehoeften van studenten+ ten aanzien van stage en werk.',
        'De opleiding onderhoudt structureel en actief contacten met werkgevers voor studenten+.',
        'De instelling biedt als werkgever structureel mogelijkheden aan mensen met een functiebeperking.'],
 'rst': ['Op instellingsniveau liggen procedures voor het toeleiden van studenten+ naar BPV en werk vast. De procedures worden jaarlijks geëvalueerd.',
        'De medewerkers van het stage/BPVbureau hebben kennis van de ondersteuningsbehoeften van studenten+ ten aanzien van stage en werk. Professionalisering op dit onderwerp maakt onderdeel uit van het professionaliseringsplan van de instelling.',
        'De opleiding onderhoudt structureel en actief contacten met werkgevers voor studenten+. Jaarlijks wordt het netwerk geactualiseerd.',
        'De instelling biedt als werkgever structureel mogelijkheden aan mensen met een functiebeperking. Jaarlijks wordt ditgeëvalueerd.']}}

niveau_vergelijking = {'Iedereen': [2.5, 1.5, 3.5,2.2],
                      'Student': [3,1,4,2],
                      'Uitvoerende medewerker': [1.5,2.4,2.3,2.1],
                      'Beleid/Management/Bestuur': [4,4,3,3]}
aspect_vergelijking = {'Iedereen': [3,3,3,3,3,3,3,3],
                      'Student': [2,2,2,2,2,2,2,2],
                      'Uitvoerende medewerker': [1,1,1,1,1,1,1,1],
                      'Beleid/Management/Bestuur': [4,4,4,4,4,4,4,4]}


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[3]:


def average_one(data):
    datak = np.average([data[2+4*x] for x in range(0,8) ])
    return datak
def average_two(data):
    datak = np.average([data[3+4*x] for x in range(0,8) ])
    return datak
def average_three(data):
    datak = np.average([data[4+4*x] for x in range(0,8) ])
    return datak
def average_four(data):
    datak = np.average([data[5+4*x] for x in range(0,8) ])
    return datak
position =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
opties = {'mdw': 'Medewerker georiënteerd',
         'bld': 'Beleid georiënteerd',
         'org': 'Organisatie georiënteerd',
         'rst': 'Resultaat georiënteerd'}
# WIP
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [   html.H1('Dit is de beleidsscan',style={'backgroundColor': '#b7dbbf'}),
        html.H3('U bent een:',style={'backgroundColor': 'b7dbbf'}),
        
        html.Div([
        html.Div([
        dcc.Dropdown(
            id='naam',
            options=[{'label':nametitle, 'value':name} for nametitle,name in 
                     zip(['Medewerker beleid/management/bestuur','Uitvoerende medewerker', 'Studenten'],
                         ['Beleid', 'Medewerker', 'Student']) ],style={'display': 'inline-block','width': '75%'})
        
  
        ])
        
        ,html.H3('Selecter het meest relevante antwoord', id = 'title1'),]),
        html.H4(id = 'vraag_categorie'),
        html.Div([dcc.RadioItems(id = 'vragen')]),
        html.Div(html.Thead([html.Tr([html.Th(html.Button('Volgende vraag', id='vraagknop', n_clicks_timestamp='0'))])]))
        
         
        
    
    
    ,   html.Div([dcc.Store(id='waarden',storage_type='local'),]),
        html.Div([dcc.Store(id='data_loc',storage_type='local', ),]),
     
        html.Div(html.H4( 'Vergelijk mijn resultaten met:', id = 'resss',)),
        html.Div([
        dcc.Dropdown(
            id='resultaat',
            options=[{'label':nametitle, 'value':name} for nametitle,name in 
                     zip(['Iedereen', 'Student', 'Uitvoerende medewerker', 'Beleid/Management/Bestuur'],
                         ['Iedereen', 'Student', 'Uitvoerende medewerker', 'Beleid/Management/Bestuur']) ],value = 'Iedereen', style={'display': 'inline-block','width': '75%'})
        
  
        ]),
        html.Div([dcc.Graph(id = 'Chart', style = {'display': 'inline-block', 'width': '45%','backgroundColor':'#b7dbbf' }),
                 dcc.Graph(id = 'Chart1', style = {'display': 'inline-block', 'width': '45%','backgroundColor':'#b7dbbf' })])
    ], style={'backgroundColor':'#b7dbbf'})

@app.callback([dash.dependencies.Output('data_loc', 'data'),
              dash.dependencies.Output('vragen', 'options'),
              dash.dependencies.Output('waarden', 'data'),
              dash.dependencies.Output('vraag_categorie', 'children'),
              dash.dependencies.Output('Chart', 'figure'),
              dash.dependencies.Output('Chart1', 'figure'),
              dash.dependencies.Output('title1', 'style'),
              dash.dependencies.Output('vraag_categorie', 'style')]
              ,[dash.dependencies.Input('vraagknop', 'n_clicks')],
                [dash.dependencies.State('data_loc', 'data'),
                dash.dependencies.State('waarden', 'data'),
                dash.dependencies.State('vragen', 'value'),
                dash.dependencies.State('resultaat', 'value')]
                 )
def update_data(butt, locc, waardn, infor, groep):
    if waardn is None:
        waardn = copy.deepcopy(position)
    
    if (locc is None) == False:
        if locc[1] == 'mdw':
            locc[1] = 'bld'
        elif locc[1] == 'bld':
            locc[1] = 'org'
        elif locc[1] == 'org':
            locc[1] = 'rst'
        elif locc[1] == 'rst':
            if locc[0] != 8:
                locc[0] = locc[0] +1
                locc[1] = 'mdw'
    
    if locc is None:
        locc = [1,'mdw']
    


    if waardn[33] == 0:
        displ = {'display': 'inline-block'}
      
        optionz = [{'label':nametitle, 'value':name} for nametitle,name in  
                        zip(lijst_vragen[locc[0]][locc[1]], np.arange(1,len(lijst_vragen[locc[0]][locc[1]]) +1)[::-1])]
        waardn[0] = waardn[0] + 1
        waardn[waardn[0]] = infor
        orien = opties[locc[1]]
        layout1 = go.Layout( title='Vergelijking op niveau')
        layout2 = go.Layout( title='Vergelijking op Aspect')
        bar = go.Bar(name = 'Eigen score', marker_color='#50c878',x = ['Medewerker', 'Beleid', 'Organisatie', 'Resultaat'], y = [average_one(waardn), average_two(waardn), average_three(waardn), average_four(waardn)])
        bar_avg = go.Bar(name = 'Gemiddelde score', marker_color='#6ac5fe', x = ['Medewerker', 'Beleid', 'Organisatie', 'Resultaat'], y = niveau_vergelijking[groep])
        spider = go.Scatterpolar(name = 'Eigen score', marker_color='#50c878', r=[np.average(waardn[2:6]),np.average(waardn[6:10]),np.average(waardn[10:14]),np.average(waardn[14:18]),np.average(waardn[18:22]),np.average(waardn[22:26]),np.average(waardn[26:30]),np.average(waardn[30:34])], theta=['Informatievoorziening en voorlichting', 'Fysieke en digitale toegankelijkheid','Ondersteuning', 'Deskundigheid', 'Flexibele onderwijssroutes','Toetsing en examinering', 'Waarborgen voor kwaliteit en continuiteit', 'BPV en werk'],fill='toself')
        spider_avg = go.Scatterpolar(name = 'Gemiddelde score', marker_color='#6ac5fe', r=aspect_vergelijking[groep], theta=['Informatievoorziening en voorlichting', 'Fysieke en digitale toegankelijkheid','Ondersteuning', 'Deskundigheid', 'Flexibele onderwijssroutes','Toetsing en examinering', 'Waarborgen voor kwaliteit en continuiteit', 'BPV en werk'], fill='toself')
        print(locc)
        return locc, optionz, waardn, orien, {'data': [ bar, bar_avg], 'layout' : layout1}, {'data': [ spider, spider_avg], 'layout' : layout2}, displ, displ
    if waardn[33] != 0:
        displ = {'display': 'none'}
        optionz = [{'label':'Dit was de vragenlijst, bedankt!', 'value': 0}]
        orien = opties[locc[1]]
        layout1 = go.Layout( title='Vergelijking op niveau')
        layout2 = go.Layout( title='Vergelijking op Aspect')
        bar = go.Bar(name = 'Eigen score', marker_color='#50c878',x = ['Medewerker', 'Beleid', 'Organisatie', 'Resultaat'], y = [average_one(waardn), average_two(waardn), average_three(waardn), average_four(waardn)])
        bar_avg = go.Bar(name = 'Gemiddelde score', marker_color='#6ac5fe', x = ['Medewerker', 'Beleid', 'Organisatie', 'Resultaat'], y = niveau_vergelijking[groep])
        spider = go.Scatterpolar(name = 'Eigen score', marker_color='#50c878', r=[np.average(waardn[2:6]),np.average(waardn[6:10]),np.average(waardn[10:14]),np.average(waardn[14:18]),np.average(waardn[18:22]),np.average(waardn[22:26]),np.average(waardn[26:30]),np.average(waardn[30:34])], theta=['Informatievoorziening en voorlichting', 'Fysieke en digitale toegankelijkheid','Ondersteuning', 'Deskundigheid', 'Flexibele onderwijssroutes','Toetsing en examinering', 'Waarborgen voor kwaliteit en continuiteit', 'BPV en werk'],fill='toself')
        spider_avg = go.Scatterpolar(name = 'Gemiddelde score', marker_color='#6ac5fe', r=aspect_vergelijking[groep], theta=['Informatievoorziening en voorlichting', 'Fysieke en digitale toegankelijkheid','Ondersteuning', 'Deskundigheid', 'Flexibele onderwijssroutes','Toetsing en examinering', 'Waarborgen voor kwaliteit en continuiteit', 'BPV en werk'], fill='toself')
        return locc, optionz, waardn, orien, {'data': [ bar, bar_avg], 'layout' : layout1}, {'data': [ spider, spider_avg], 'layout' : layout2}, displ, displ


# In[ ]:


if __name__ == '__main__':
    app.run_server()


# In[ ]:





# In[ ]:




