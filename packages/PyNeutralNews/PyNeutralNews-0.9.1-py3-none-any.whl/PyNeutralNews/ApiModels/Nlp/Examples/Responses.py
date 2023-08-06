from pydantic import BaseModel


class SemanticAnalysis(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                'entities': [
                    {
                        "start": 0,
                        "end": 5,
                        "ent_type": "PERSON",
                        "text": "Trump"
                    },
                    {
                        "start": 57,
                        "end": 67,
                        "ent_type": "FAC",
                        "text": "Mar-a-Lago"
                    },
                    {
                        "start": 78,
                        "end": 85,
                        "ent_type": "GPE",
                        "text": "Florida"
                    },
                    {
                        "start": 123,
                        "end": 128,
                        "ent_type": "ORG",
                        "text": "House"
                    },
                    {
                        "start": 161,
                        "end": 171,
                        "ent_type": "DATE",
                        "text": "a week ago"
                    },
                    {
                        "start": 177,
                        "end": 187,
                        "ent_type": "NORP",
                        "text": "Democratic"
                    },
                    {
                        "start": 192,
                        "end": 197,
                        "ent_type": "ORG",
                        "text": "House"
                    },
                    {
                        "start": 198,
                        "end": 207,
                        "ent_type": "DATE",
                        "text": "last week"
                    },
                    {
                        "start": 279,
                        "end": 287,
                        "ent_type": "ORG",
                        "text": "Congress"
                    },
                    {
                        "start": 322,
                        "end": 329,
                        "ent_type": "GPE",
                        "text": "Ukraine"
                    }
                ],
                'concepts': [{'properties': None,
                              'labels': [{'mentions': [{'start': 57, 'end': 67}], 'text': 'Mar a Lago'}],
                              'weight': 0.14802610884279066, 'id': 'Q1262898'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 149, 'end': 160},
                                                       {'start': 227, 'end': 238}], 'text': 'impeachment'}],
                              'weight': 0.1254129262256732, 'id': 'Q480498'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 322, 'end': 329}], 'text': 'Ukraine'}],
                              'weight': 0.11488780170151257, 'id': 'Q212'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 78, 'end': 85}], 'text': 'Florida'}],
                              'weight': 0.08954558607148629, 'id': 'Q812'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 25, 'end': 29}], 'text': 'golf'}],
                              'weight': 0.07830946680736198, 'id': 'Q5377'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 279, 'end': 287}], 'text': 'Congress'}],
                              'weight': 0.07515613559680595, 'id': 'Q11268'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 177, 'end': 187}], 'text': 'Democratic'}],
                              'weight': 0.0734013547521301, 'id': 'Q29552'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 0, 'end': 5}], 'text': 'Trump'}],
                              'weight': 0.07132417397214992, 'id': 'Q22686'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 298, 'end': 309}], 'text': 'President s'}],
                              'weight': 0.06936923906991745, 'id': 'Q11696'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 334, 'end': 343}], 'text': 'political'}],
                              'weight': 0.059373008941530046, 'id': 'Q7163'},
                             {'properties': None,
                              'labels': [
                                  {'mentions': [{'start': 215, 'end': 238}], 'text': 'articles of impeachment'}],
                              'weight': 0.05072255562179739, 'id': 'Q1949797'},
                             {'properties': None,
                              'labels': [{'mentions': [{'start': 257, 'end': 262}], 'text': 'power'}],
                              'weight': 0.04447164239684429, 'id': 'Q25107'}
                             ],
                'lang': 'en'
            }
        }


class UrlAnalysis(BaseModel):
    class Config:
        schema_extra = {
            "example":
                {'cursor': 1585955990.395409,
                 'url': 'https://www.channelstv.com/2020/03/16/coronavirus-us-china-trade-blames-over-fear-mongering/',
                 'id': '39add5f5e4bcbec1f5f68c9009935f0961f88cf4e46ba198c0df56b01a1d4ec28aabb69f4aa8b47be2e2fa75029728'
                       '731dbc2e75dff3bbdad5de031a8055fae4',
                 'source': 'https://www.channelstv.com',
                 'category_url': 'https://www.channelstv.com/2020/03/16/coronavirus-us-china-trade-blames-over-fear'
                                 '-mongering/',
                 'lang': 'en', 'detected_lang': 'en',
                 'title': 'Coronavirus: US, China Trade Blames Over Fear-Mongering',
                 'text': 'The United States and China on Monday each demanded that the other stop smearing its '
                         'reputation over the novel coronavirus as the pandemic became the latest row between the '
                         'powers.\n\n\nThe clash came on the day that the World Health Organization said more cases '
                         'and deaths had been reported in the rest of the world than in China, where the new '
                         'coronavirus virus was first detected late last year.\n\n\nUS Secretary of State Mike '
                         'Pompeo, in a phone call he initiated with top Chinese official Yang Jiechi, voiced anger '
                         'that Beijing has used official channels “to shift blame for COVID-19 to the United States,'
                         '” the State Department said.\n\n\nPompeo “stressed that this is not the time to spread '
                         'disinformation and outlandish rumors, but rather a time for all nations to come together to '
                         'fight this common threat,” the department added.\n\n\nThe State Department on Friday '
                         'summoned the Chinese ambassador, Cui Tiankai, to denounce Beijing’s promotion of a '
                         'conspiracy theory that had gained wide attention on social media.\n\n\nForeign ministry '
                         'spokesman Zhao Lijian, in tweets last week in both Mandarin and English, suggested that '
                         '“patient zero” in the global pandemic may have come from the United States — not the '
                         'Chinese metropolis of Wuhan.\n\n\n“It might be US army who brought the epidemic to Wuhan. '
                         'Be transparent! Make public your data! US owe us an explanation,” tweeted Zhao, '
                         'who is known for his provocative statements on social media.\n\n\nScientists suspect that '
                         'the virus first came to humans at a meat market in Wuhan that butchered exotic '
                         'animals.\n\n\n‘Stern warning’ to US\n\n\nPompeo himself has sought to link China to the '
                         'global pandemic, repeatedly referring to SARS-CoV-2 as the “Wuhan virus” despite advice '
                         'from health professionals that such geographic labels can be stigmatizing.\n\n\nYang issued '
                         'a “stern warning to the United States that any scheme to smear China will be doomed to '
                         'fail,” the official Xinhua news agency said in its summary of the call with '
                         'Pompeo.\n\n\nThe key Chinese foreign policy leader “noted that some US politicians have '
                         'frequently slandered China and its anti-epidemic efforts and stigmatized the country, '
                         'which has enraged the Chinese people,” Xinhua said.\n\n\n“He urged the US side to '
                         'immediately correct its wrongful behavior and stop making groundless accusations against '
                         'China.”\n\n\nPresident Donald Trump, under fire over his handling of the pandemic, '
                         'and his allies have sought to cast the coronavirus as a disease brought by '
                         'foreigners.\n\n\nRepublican Senator Tom Cotton, a Trump ally, has spoken of the “Chinese '
                         'coronavirus” and in a recent statement vowed, “we will hold accountable those who inflicted '
                         'it on the world.”\n\n\nWhile COVID-19 — the disease caused by the virus — has largely come '
                         'under control in China, it has killed more than 7,000 people around the world and severely '
                         'disrupted daily life in Western countries.\n\n\nThe pandemic comes at a time of '
                         'wide-ranging tensions between the United States and China on issues from trade to human '
                         'rights to Beijing’s military buildup.\n\n\nAFP\n\n\\n',
                 'top_image': 'https://www.channelstv.com/wp-content/uploads/2020/03/Donald-Trump.jpg',
                 'images': ['https://www.channelstv.com/wp-content/uploads/2018/05/Map-of-ekiti-state-180x138.jpg',
                            'https://www.channelstv.com/wp-content/uploads/2020/03/Donald-Trump.jpg',
                            'https://certify.alexametrics.com/atrk.gif?account=rrH8k1a0CM00UH',
                            'https://www.channelstv.com/wp-content/uploads/2020/03/Ibrahim-Oloriegbe-180x138.jpg',
                            'https://www.channelstv.com/wp-content/themes/channels2016/ctv-logo.png',
                            'http://my.therubiqube.com/www/delivery/avw.php?zoneid=57&cb=%%CACHEBUSTER%%&n=a99082dd'
                            '&ct0=%%CLICK_URL_ESC%%',
                            'https://www.channelstv.com/wp-content/uploads/2019/12/Ondo-1-180x138.jpg'], 'movies': [],
                 'authors': ['Channels Television', 'Updated March'], 'summary': '',
                 'publish_date': '2020-04-03 23:19:51.037026+00:00',
                 'document': {'concepts': [
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 17, 'end': 22}, {'start': 79, 'end': 84},
                                               {'start': 379, 'end': 384}, {'start': 1662, 'end': 1667},
                                               {'start': 1915, 'end': 1920}, {'start': 2121, 'end': 2126},
                                               {'start': 2354, 'end': 2359}, {'start': 2792, 'end': 2797},
                                               {'start': 2995, 'end': 3000}],
                                  'text': 'China'},
                                 {'mentions': [{'start': 528, 'end': 535}, {'start': 932, 'end': 939},
                                               {'start': 1260, 'end': 1267}, {'start': 2033, 'end': 2040},
                                               {'start': 2208, 'end': 2215}, {'start': 2587, 'end': 2594}],
                                  'text': 'Chinese'}],
                      'weight': 0.09758909668387376, 'id': 'Q148'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 0, 'end': 11}],
                                  'text': 'Coronavirus'},
                                 {'mentions': [{'start': 168, 'end': 179}, {'start': 400, 'end': 411},
                                               {'start': 2473, 'end': 2484}, {'start': 2595, 'end': 2606}],
                                  'text': 'coronavirus'}],
                      'weight': 0.06491759550904587, 'id': 'Q290805'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1282, 'end': 1287}, {'start': 1340, 'end': 1345},
                                               {'start': 1565, 'end': 1570}, {'start': 1735, 'end': 1740}],
                                  'text': 'Wuhan'}],
                      'weight': 0.059506980945693955, 'id': 'Q11746'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 275, 'end': 300}],
                                  'text': 'World Health Organization'}],
                      'weight': 0.034321470012208866, 'id': 'Q7817'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 187, 'end': 195}, {'start': 1204, 'end': 1212},
                                               {'start': 1682, 'end': 1690}, {'start': 2424, 'end': 2432},
                                               {'start': 2915, 'end': 2923}],
                                  'text': 'pandemic'},
                                 {'mentions': [{'start': 1328, 'end': 1336}, {'start': 2140, 'end': 2148}],
                                  'text': 'epidemic'}],
                      'weight': 0.0335818737873143, 'id': 'Q12184'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 576, 'end': 583}, {'start': 977, 'end': 986},
                                               {'start': 3041, 'end': 3050}],
                                  'text': 'Beijing'},
                                 {'mentions': [{'start': 977, 'end': 986}, {'start': 3041, 'end': 3050}],
                                  'text': 'Beijing s'}],
                      'weight': 0.027048748011749717, 'id': 'Q956'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 545, 'end': 556}],
                                  'text': 'Yang Jiechi'}],
                      'weight': 0.025958280330804336, 'id': 'Q58211'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1716, 'end': 1720}],
                                  'text': 'SARS'}],
                      'weight': 0.02532895274336553, 'id': 'Q103177'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 477, 'end': 488}],
                                  'text': 'Mike Pompeo'},
                                 {'mentions': [{'start': 482, 'end': 488}, {'start': 692, 'end': 698},
                                               {'start': 1628, 'end': 1634}, {'start': 2015, 'end': 2021}],
                                  'text': 'Pompeo'}],
                      'weight': 0.024670061692584636, 'id': 'Q473239'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2542, 'end': 2552}],
                                  'text': 'Tom Cotton'}],
                      'weight': 0.024210042072682972, 'id': 'Q3090307'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 412, 'end': 417}, {'start': 1518, 'end': 1523},
                                               {'start': 1741, 'end': 1746}, {'start': 2750, 'end': 2755}],
                                  'text': 'virus'}],
                      'weight': 0.023704098198455897, 'id': 'Q808'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 952, 'end': 963}],
                                  'text': 'Cui Tiankai'}],
                      'weight': 0.022347653606048873, 'id': 'Q2213434'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1959, 'end': 1965}, {'start': 2225, 'end': 2231}],
                                  'text': 'Xinhua'},
                                 {'mentions': [{'start': 1959, 'end': 1977}],
                                  'text': 'Xinhua news agency'}],
                      'weight': 0.021883228067045478, 'id': 'Q204839'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1138, 'end': 1146}],
                                  'text': 'Mandarin'}],
                      'weight': 0.021811219276723855, 'id': 'Q7850'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1054, 'end': 1066}, {'start': 1474, 'end': 1486}],
                                  'text': 'social media'}],
                      'weight': 0.0196955743004893, 'id': 'Q202833'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2083, 'end': 2094}],
                                  'text': 'politicians'}],
                      'weight': 0.019247996748449826, 'id': 'Q7163'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1413, 'end': 1420}],
                                  'text': 'tweeted'},
                                 {'mentions': [{'start': 1113, 'end': 1119}],
                                  'text': 'tweets'}],
                      'weight': 0.019088551789014467, 'id': 'Q918'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 3016, 'end': 3021}],
                                  'text': 'trade'},
                                 {'mentions': [{'start': 23, 'end': 28}],
                                  'text': 'Trade'}],
                      'weight': 0.01908378199593146, 'id': 'Q601401'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 3071, 'end': 3074}],
                                  'text': 'AFP'}],
                      'weight': 0.018737624787521157, 'id': 'Q40464'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 13, 'end': 15}, {'start': 455, 'end': 457},
                                               {'start': 1304, 'end': 1306}, {'start': 1386, 'end': 1388},
                                               {'start': 1623, 'end': 1625}, {'start': 2080, 'end': 2082},
                                               {'start': 2254, 'end': 2256}],
                                  'text': 'US'}],
                      'weight': 0.018625055328554397, 'id': 'Q4917'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2374, 'end': 2386}],
                                  'text': 'Donald Trump'},
                                 {'mentions': [{'start': 2364, 'end': 2386}],
                                  'text': 'President Donald Trump'},
                                 {'mentions': [{'start': 2381, 'end': 2386}, {'start': 2556, 'end': 2561}],
                                  'text': 'Trump'}],
                      'weight': 0.01860154497690655, 'id': 'Q22686'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2523, 'end': 2533}],
                                  'text': 'Republican'}],
                      'weight': 0.018104678789379845, 'id': 'Q29468'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 745, 'end': 759}],
                                  'text': 'disinformation'}],
                      'weight': 0.017782070484647156, 'id': 'Q189656'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 3051, 'end': 3059}],
                                  'text': 'military'}],
                      'weight': 0.017390369354355055, 'id': 'Q8473'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1768, 'end': 1774}],
                                  'text': 'health'}],
                      'weight': 0.017322229779536638, 'id': 'Q12147'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1555, 'end': 1561}],
                                  'text': 'market'}],
                      'weight': 0.01664116855029257, 'id': 'Q179522'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2490, 'end': 2497}, {'start': 2728, 'end': 2735}],
                                  'text': 'disease'}],
                      'weight': 0.016392058275150286, 'id': 'Q12136'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1268, 'end': 1278}],
                                  'text': 'metropolis'}],
                      'weight': 0.015735483459701653, 'id': 'Q200250'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 495, 'end': 500}],
                                  'text': 'phone'}],
                      'weight': 0.015683438541942325, 'id': 'Q11035'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1775, 'end': 1788}],
                                  'text': 'professionals'}],
                      'weight': 0.015349511021794002, 'id': 'Q241588'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2056, 'end': 2062}],
                                  'text': 'leader'}],
                      'weight': 0.015200728028858015, 'id': 'Q183318'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2442, 'end': 2448}],
                                  'text': 'allies'}],
                      'weight': 0.014935052115091262, 'id': 'Q7184'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1151, 'end': 1158}],
                                  'text': 'English'}],
                      'weight': 0.014856108009888609, 'id': 'Q1860'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 987, 'end': 996}],
                                  'text': 'promotion'}],
                      'weight': 0.014587579068849615, 'id': 'Q37038'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1550, 'end': 1554}],
                                  'text': 'meat'}],
                      'weight': 0.014491549063569694, 'id': 'Q10990'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2394, 'end': 2398}],
                                  'text': 'fire'}],
                      'weight': 0.014128075928707334, 'id': 'Q3196'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2298, 'end': 2306}],
                                  'text': 'behavior'}],
                      'weight': 0.01407979124810326, 'id': 'Q9332'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2534, 'end': 2541}],
                                  'text': 'Senator'}],
                      'weight': 0.014003752891842244, 'id': 'Q66096'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1799, 'end': 1809}],
                                  'text': 'geographic'}],
                      'weight': 0.013951493247559716, 'id': 'Q1071'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1176, 'end': 1188}],
                                  'text': 'patient zero'}],
                      'weight': 0.013545482825209213, 'id': 'Q1639798'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 2161, 'end': 2172}],
                                  'text': 'stigmatized'},
                                 {'mentions': [{'start': 1824, 'end': 1836}],
                                  'text': 'stigmatizing'}],
                      'weight': 0.013445359613011314, 'id': 'Q1137326'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 1070, 'end': 1086}],
                                  'text': 'Foreign ministry'}],
                      'weight': 0.013386811285634518, 'id': 'Q1155502'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 940, 'end': 950}],
                                  'text': 'ambassador'}],
                      'weight': 0.01337660061862433, 'id': 'Q121998'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 41, 'end': 45}],
                                  'text': 'Fear'}],
                      'weight': 0.013262439061006345, 'id': 'Q44619'},
                     {'properties': None,
                      'labels': [{'mentions': [{'start': 700, 'end': 708}],
                                  'text': 'stressed'}],
                      'weight': 0.012388737872779658, 'id': 'Q123414'}]}}}


class DetectLang(BaseModel):
    class Config:
        schema_extra = {
            "example":
                {'sentences': [{'languages_confidence': [{'name': 'français', 'code': 'fr', 'confidence': 98.0}],
                                'text': 'Bonjour, je suis une phrase en français mais le reste est en farsi.'},
                               {'languages_confidence': [{'name': 'persan', 'code': 'fa', 'confidence': 99.0}],
                                'text': 'اخبار متناقض درباره نامه فرمانده آمریکایی در عراق در حالی که وزیر دفاع '
                                        'آمریکا و رییس ستاد مشترک نیروهای مسلح این کشور تاکید دارند که هیچ طرحی برای '
                                        'خروج نیروهای آمریکایی از عراق وجود ندارد اصالت یک نامه از سوی فرمانده '
                                        'آمریکایی نیروهای اتلاف در عراق که طی آن به وزارت دفاع عراق از جابجایی های '
                                        'اولیه برای خروج از عراق اشاره شده تایید شده است.'},
                               {'languages_confidence': [{'name': 'persan', 'code': 'fa', 'confidence': 99.0}],
                                'text': 'نفیسه کوهنورد - خبرنگار بی بی سی می گوید مقام های آمریکایی در ستاد نیروهای '
                                        'ائتلاف اصالت این نامه را تایید کرده اند و ممکن است تناقضات در گفته های مقام '
                                        'های آمریکایی نشان از اختلاف نظر میان فرماندهان پنتاگون باشد.'},
                               {'languages_confidence': [{'name': 'persan', 'code': 'fa', 'confidence': 83.0}],
                                'text': 'شد.'}],
                 'languages_confidence': [{'name': 'persan', 'code': 'fa', 'confidence': 93.0},
                                          {'name': 'français', 'code': 'fr', 'confidence': 6.0}]}}


class Summarize(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                'summary': ["Some of Australia's largest cities have also been affected, including Melbourne and "
                            "Sydney -- where fires have damaged homes in the outer suburbs and thick plumes of smoke "
                            "have blanketed the urban center."]
            }
        }


class TextsSimilarity(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                'similarity': 0.8926192789106295
            }
        }


class SyntaxAnalysis(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "sentences": [{"start": 0, "end": 16,
                               "words": [{"start": 0, "end": 5, "id": 0, "text": 'There', "pos_tag": 'PRON',
                                          "lemma": 'there', "dep": 'expl', "head": 1, "feats": {}},
                                         {"start": 6, "end": 10, "id": 1, "text": 'were', "pos_tag": 'VERB',
                                          "lemma": 'be', "dep": 'ROOT', "head": 1, "feats": {}},
                                         {"start": 11, "end": 17, "id": 2, "text": 'things', "pos_tag": 'NOUN',
                                          "lemma": 'thing', "dep": 'nsubj', "head": 1, "feats": {}},
                                         {"start": 18, "end": 20, "id": 3, "text": 'in', "pos_tag": 'ADP',
                                          "lemma": 'in', "dep": 'case', "head": 5, "feats": {}},
                                         {"start": 21, "end": 24, "id": 4, "text": 'the', "pos_tag": 'DET',
                                          "lemma": 'the', "dep": 'det', "head": 5, "feats": {}},
                                         {"start": 25, "end": 32, "id": 5, "text": 'shadows', "pos_tag": 'NOUN',
                                          "lemma": 'shadows', "dep": 'nmod', "head": 2, "feats": {}},
                                         {"start": 32, "end": 33, "id": 6, "text": ';', "pos_tag": 'PUNCT',
                                          "lemma": ';', "dep": 'punct', "head": 1, "feats": {}},
                                         {"start": 34, "end": 35, "id": 7, "text": 'a', "pos_tag": 'DET',
                                          "lemma": 'a', "dep": 'det', "head": 9, "feats": {}},
                                         {"start": 36, "end": 41, "id": 8, "text": 'metal', "pos_tag": 'NOUN',
                                          "lemma": 'metal', "dep": 'compound', "head": 9, "feats": {}},
                                         {"start": 42, "end": 46, "id": 9, "text": 'pail', "pos_tag": 'NOUN',
                                          "lemma": 'pail', "dep": 'nsubj', "head": 1, "feats": {}},
                                         {"start": 46, "end": 47, "id": 10, "text": ',', "pos_tag": 'PUNCT',
                                          "lemma": ',', "dep": 'punct', "head": 9, "feats": {}},
                                         {"start": 48, "end": 49, "id": 11, "text": 'a', "pos_tag": 'DET',
                                          "lemma": 'a', "dep": 'det', "head": 12, "feats": {}},
                                         {"start": 50, "end": 53, "id": 12, "text": 'mop', "pos_tag": 'NOUN',
                                          "lemma": 'mop', "dep": 'appos', "head": 9, "feats": {}},
                                         {"start": 53, "end": 54, "id": 13, "text": ',', "pos_tag": 'PUNCT',
                                          "lemma": ',', "dep": 'punct', "head": 12, "feats": {}},
                                         {"start": 55, "end": 59, "id": 14, "text": 'rags', "pos_tag": 'NOUN',
                                          "lemma": 'rag', "dep": 'appos', "head": 12, "feats": {}},
                                         {"start": 59, "end": 60, "id": 15, "text": '.', "pos_tag": 'PUNCT',
                                          "lemma": '.', "dep": 'punct', "head": 1, "feats": {}}]}],
                "visualization": None
            }
        }


class KeyPhrasesExtraction(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "key_phrases": [{"text": 'tomato sauce nozzle', "weigh": 0.031752697497046026},
                                {"text": 'sugary tomato sweetness', "weight": 0.02947166030985545},
                                {"text": 'oozy beefy mince', "weight": 0.028924779660601682},
                                {"text": 'savoury taste sensation', "weight": 0.02738701084630684},
                                {"text": 'humble meat pie', "weight": 0.0255610365121371},
                                {"text": 'young age', "weight": 0.018322040460932686},
                                {"text": 'hot climates', "weight": 0.017874783394024},
                                {"text": 'smallish hands', "weight": 0.017439467504265758},
                                {"text": 'shape mid-bite', "weight": 0.017103805586533544},
                                {"text": 'wintry days', "weight": 0.01667938878386825}]
            }
        }


class PhraseMatcher(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "matches": [{'dist': 0.8634273409843445, 'end': 13, 'start': 6, 'text': 'mon ami'}]
            }
        }