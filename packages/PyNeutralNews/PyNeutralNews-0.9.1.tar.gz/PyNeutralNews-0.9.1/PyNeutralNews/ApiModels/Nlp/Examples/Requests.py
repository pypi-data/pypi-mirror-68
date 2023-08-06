from collections import OrderedDict

from pydantic import BaseModel


class SemanticAnalysis(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("text", "Trump, between rounds of golf and greeting guests at his Mar-a-Lago resort in Florida, "
                         "keeps returning to vent fury at the House speaker who led his impeachment a week ago. The "
                         "Democratic-led House last week passed articles of impeachment alleging abuse of power and "
                         "obstructing Congress, over the President's pressure on Ukraine for political favors. ")
            ])
        }


class UrlAnalysis(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("url", "https://www.channelstv.com/2020/03/16/coronavirus-us-china-trade-blames-over-fear-mongering/")
            ])
        }


class DetectLang(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("text", "Bonjour, je suis une phrase en français mais le reste est en farsi. اخبار متناقض درباره "
                         "نامه فرمانده آمریکایی در عراق در حالی که وزیر دفاع آمریکا و رییس ستاد مشترک نیروهای مسلح "
                         "این کشور تاکید دارند که هیچ طرحی برای خروج نیروهای آمریکایی از عراق وجود ندارد اصالت یک "
                         "نامه از سوی فرمانده آمریکایی نیروهای اتلاف در عراق که طی آن به وزارت دفاع عراق از جابجایی "
                         "های اولیه برای خروج از عراق اشاره شده تایید شده است.نفیسه کوهنورد - خبرنگار بی بی سی می "
                         "گوید مقام های آمریکایی در ستاد نیروهای ائتلاف اصالت این نامه را تایید کرده اند و ممکن است "
                         "تناقضات در گفته های مقام های آمریکایی نشان از اختلاف نظر میان فرماندهان پنتاگون باشد.شد.")
            ])
        }


class Summarize(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("text", "Australia is being ravaged by the worst wildfires seen in decades, with large swaths of the "
                         "country devastated since the fire season began in late July. At least 28 people have died "
                         "nationwide, and in the state of New South Wales (NSW) alone, more than 3,000 homes have been "
                         "destroyed or damaged. State and federal authorities are struggling to contain the massive "
                         "blazes, even with firefighting assistance from other countries, including the United States. "
                         "All this has been exacerbated by persistent heat and drought, and many point to climate "
                         "change as a factor making natural disasters go from bad to worse. There have been fires in "
                         "every Australian state, but New South Wales has been hardest hit. Blazes have torn through "
                         "bushland, wooded areas, and national parks like the Blue Mountains. Some of Australia's "
                         "largest cities have also been affected, including Melbourne and Sydney -- where fires have "
                         "damaged homes in the outer suburbs and thick plumes of smoke have blanketed the urban "
                         "center. Earlier in December, the smoke was so bad in Sydney that air quality measured 11 "
                         "times the hazardous level. The fires range in area from small blazes -- isolated buildings "
                         "or part of a neighborhood -- to massive infernos that occupy entire hectares of land. Some "
                         "start and are contained in a matter of days, but the biggest blazes have been burning for "
                         "months. In NSW alone, more than 100 fires are still burning. ")
            ])
        }


class TextsSimilarity(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("text1", "Le gouvernement a nommé douze nouveaux directeurs pour le conseil, selon l'équilibre des "
                          "pouvoirs au Parlement flamand. CD&V récite deux personnes: Luc Van den Brande et Rozane De "
                          "Cock, un nouveau visage. De Cock est affilié à la KU Leuven Institute for Media Studies. "
                          "Open Vld rappelle à nouveau l'ancien journaliste de la VRT, Dirk Sterckx, aux côtés de "
                          "l'ancien visage de VTM, Lynn Wesenbeek. Groen remplace Freya Piryns par Bart Caron, "
                          "qui faisait partie du comité des médias du Parlement flamand pendant des années pour le "
                          "parti. Sp.a remplace Jan Roegiers par Geneviève Lombaerts, le partenaire de l'ancien "
                          "président John Crombez."),
                ("text2", "De regering heeft twaalf nieuwe bestuurders benoemd voor de raad, volgens de "
                          "krachtverhoudingen in het Vlaams Parlement. CD&V draagt twee mensen voor: Luc Van den "
                          "Brande en Rozane De Cock, een nieuw gezicht. De Cock is verbonden aan het Instituut voor "
                          "Mediastudies van de KU Leuven. Open Vld draagt opnieuw voormalig VRT-journalist Dirk "
                          "Sterckx voor, naast gewezen VTM-gezicht Lynn Wesenbeek. Groen vervangt Freya Piryns door "
                          "Bart Caron, die jarenlang in de Mediacommissie van het Vlaams Parlement zat voor de partij. "
                          "Sp.a vervangt Jan Roegiers door Geneviève Lombaerts, de partner van voormalig voorzitter "
                          "John Crombez. ")
            ])
        }


class SyntaxAnalysis(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("text", "There were things in the shadows; a metal pail, a mop, rags.")
            ])
        }


class KeyPhrasesExtraction(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("text", "If you ever wondered why Australians have such an obsession with the humble meat pie, "
                         "this inculcation from a very young age is possibly at the heart of it. In heater-less "
                         "schools built for hot climates despite wintry days, there was nothing quite like the smell "
                         "and savoury taste sensation found in this warm, mince-filled bakery delight. It came in "
                         "just the right size for two smallish hands to hold, with a square casing solid enough to "
                         "retain its shape mid-bite. The pastry on top was wonderfully flaky, but flimsy too, "
                         "so the tomato sauce nozzle could be poked directly into the pie, mixing sugary tomato "
                         "sweetness with oozy beefy mince..")
            ])
        }


class PhraseMatcher(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("text", "Salut mon ami !"),
                ("phrase", "my friend")
            ])
        }

