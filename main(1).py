from flask import Flask
from flask import request
from flask import jsonify
from flask import json
import requests
from flask_sslify import SSLify


# Flask
app = Flask(__name__)
sslify = SSLify(app)

# Массисивы команд и ответов
G_COMMANDS =[["/help", "help", "/помощь", "помощь","/меню", "меню"],
                  ["/stipend", "стипендии", "/stipend", "стипендии"],
                  ["/sto", "sto", "/сто", "сто"],
                  ["/weather", "weather", "/погода", "погода" ],
                  ["/start", "start", "/старт", "старт" ]]
G_ANSWERS =  ["Ты можешь набрать команды: \n /STO \n /stipend \n /weather  ", "Какой вид стипендии тебя интересует?", "Какой раздел СТО тебя интересует?", "Доброго времени суток! \n\nТебя преветствует бот студенчегоского совета ВШИТАС. Меня создали для помощи студентам."]

STIPEND_COMAND = [["/u", "ссылка на стипендии", "размеры стипендии"],
                  ["/p", "государственная социальная стипендия", "социалка"],
                  ["/q", "именная стипендия"],
                  ["/r", "материалка", "материальная поддержка"],
                  ["/s", "повышенная государственная академическая стипендия","повышенка" ],
                  ["/t", "cтипендия 'первокурсник 5.0'"]]
STIPEND_ANSWERS = []
STIPEND_ANSWERS.append("Ccылка на стипендии")
STIPEND_ANSWERS.append("""Государственная социальная стипендия
Эта стипендия назначается детям сиротам, лицам из числа детей сирот, инвалидам I, II групп, инвалидам с детства, жертвам радиационных катастроф, людям пострадавшим в военных действиях или гражданским людям проходившим военную службу по контракту не менее 3 лет, а также студентам получившим государственную социальную помощь (Например: если ты прописан один, ты вышел замуж или женился, неполная семья).

Для назначения ГСС необходимо предоставить документы подтверждающие принадлежность к категориям имеющим право на получение ГСС.

Если ты учишься на 1 или 2 курсе, то тебе должны платить повышенную государственную стипендию, если у тебя нет троек и двоек.

Сумма, выплачиваемой стипендии не должна быть меньше прожиточного минимума.""")
STIPEND_ANSWERS.append("""Именны стипендии
Существует множество подвидов именных стипендий. У каждого подвида свои критерии. Более подробно вы можете ознакомиться с именными стипендиями на сайте САФУ""")
STIPEND_ANSWERS.append("""Материальная поддержка
Материальная поддержка выплачивается единоразово по заявлению студента. К заявлению необхожимо приложить документы, подтверждающие основания для оказания ему материальной поддержки.Размер материальной поддержки, оказываемой обучающимся определяется соответствующей стипендиальной комиссией в каждом конкретном случае исходя из принципов соразмерности и адресности. Более подробно ознакомиться условиями получения материальнной поддержке вы можете на сайте САФУ. """)
STIPEND_ANSWERS.append("""Повышенная государственная академическая стипендия
Если ты 2 курс и старше и ты закончил сессию на 5 и/или 4, а также ты был активен на протяжении учебного года, то ты можешь подать заявление на повышенную государственную академическую стипендию.
В повышенной государственной академической стипендии есть несколько направлений, по которой ты сможешь её получить – это учебная деятельность, научно-исследовательская деятельность, общественная деятельность, культурно-творческая деятельность, а также спортивная деятельность.

Более подробно ты сможешь узнать про эту стипендию на сайте САФУ.""")
STIPEND_ANSWERS.append("""Первокурсник 5.0
Это стипендия выплачивается только первокурсникам очной формы обучения. И если ты хочешь её получить, то тебе нужно знать несколько критериев, по которым она будет выплачиваться.

1) По направлениям
- Если ты участвовал во всероссийских и международных олимпиадах и у тебя замечательные результаты.
- Если ты окончил школу с золотой или серебряной медалью, имеешь аттестат с отличием.
- Если ты закончил колледж на отлично.
2) Если ты физмат, химбио или технарь то тебя заинтересуют, естественные, технические или инженерные направления. Чтобы получить эту стипендию необходимо сдать ЕГЭ на необходимое количество баллов:
ЕГЭ не менее 70 баллов по математике, информатике, биологии и географии, а также не менее 65 баллов по физике и химии или иметь в сумме не менее 220 баллов за экзамены.

3) Если гуманитарий, педагог или экономист, то тебе будут интересны – соответствующие направления, а чтобы получить стипендию Первокурсник 5.0, обучаясь на этих направлениях, тебе нужно сдать ЕГЭ не менее чем на 260 баллов за 3 экзамена.

Если ты поступаешь в ИСМАРТ, то тебе необходимо набрать не менее 180 баллов.

Хочешь продлить эту стипендию на второй семестр? Если да, то сдай сессию на пятёрки и не забудь про зачёты. (・`ω´・)

Если всё же ты не сможешь сдать сессию на отлично и у тебя будут несколько четвёрок, то не отчаивайся, стипендия будет ниже, но хотя бы она будет. (･ω<)☆
Размер стипендии определяется ректором университета:
5000 руб. – если ты сдал 1 профильный предмет на требуемое количество баллов,
7000 руб. – если ты сдал 2 профильных предмета на нужное количество баллов,
10000 руб. – если ты имеешь в сумме необходимое количество баллов""")
STO_COMMANDS = [["/a", "ссылка"],
                ["/b", "оглавление"],
                ["/c", "поля"],
                ["/d", "текст"],
                ["/e", "структурные элементы"],
                ["/f", "заголовки"],
                ["/g", "подразделы"],
                ["/h", "формулы"],
                ["/i", "листинг"],
                ["/j", "списки"],
                ["/k", "приложение"],
                ["/l", "рисунки"],
                ["/m", "таблицы"],
                ["/n", "ссылки"],
                ["/o", "библиографическая ссылка"]]
STO_ANSWERS = []
STO_ANSWERS.append("СТО 60-02.2.3-2018")
STO_ANSWERS.append("""_____
Если работа состоит из глав и разделов, объединенных общей темой - “ОГЛАВЛЕНИЕ”
Если работа состоит из глав и разделов, НЕ объединенных общей темой - “СОДЕРЖАНИЕ”

Структурный элемент «ОГЛАВЛЕНИЕ/СОДЕРЖАНИЕ» следует выполнять, используя:
* гарнитуру TimesNewRoman;
* размер шрифт (кегль) – от 12 до 14 пт (как в сновном тексте документа);
* междустрочный интервал – полуторный (1,5строки);
* выравнивание – по ширине, без полужирного шрифта.

Текст структурного элемента «ОГЛАВЛЕНИЕ/СОДЕРЖАНИЕ» следует размещать с отступом справа – 10 мм.
Заголовки структурных элементов и разделов (глав) следует размещать без отступа от границы левого поля.
Заголовки подразделов следует размещать сотступом слева – 5 мм.
Заголовки пунктов следует размещать с отступом слева – 12,5 мм.
_____""") # Оглавление
STO_ANSWERS.append("""_____
При использовании односторонней печати документа необходимо текстовый материал работы оформлять на белой бумаге формата А4, соблюдая следующие размеры полей:
* правое – не менее 10 мм;
* левое – 25-35 мм (в зависимости от переплёта);
* верхнее - 20 мм, нижнее – не менее 20 мм.

При использовании двусторонней печати документа необходимо текстовый материал работы оформлять на белой бумаге формата А4, соблюдая следующие размеры полей:
* внешнее – не менее 10 мм;
* внутреннее – 25-35 мм (взависимости отпереплёта);
* верхнее – 20 мм;
* нижнее – не менее 20 мм;
* параметр – «зеркальные поля».
_____""") # Поля
STO_ANSWERS.append("""_____
Документы выполняют способом с использованием ПК и принтера:
* гарнитура Times New Roman;
* размер шрифта (кегль) – от 12 до 14 (текст выполняется единообразно одним размером шрифта во всем документе);
* междустрочный интервал – полуторный;
* выравнивание – по ширине;
* цвет шрифта – чёрный.
* абзацы в тексте начинают абзацным отступом (12,5 мм);
* интервал между абзацами: до – 0 пунктов (далее – пт), после – 0 пт.
! Допускается применение полужирного и курсивного начертания в тексте для выделения отдельных элементов: определений, выводов и т.п. !
_____""") # Текст
STO_ANSWERS.append("""_____
Наименование структурных элементов работы «ЛИСТ ДЛЯЗАМЕЧАНИЙ», «РЕФЕРАТ», «ОГЛАВЛЕНИЕ», «НОРМАТИВНЫЕ ССЫЛКИ», «ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ», «ВВЕДЕНИЕ», «ЗАКЛЮЧЕНИЕ/ВЫВОДЫ», «СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ», «ПРИЛОЖЕНИЯ» служат заголовками структурных элементов работы.
Заголовки структурных элементов располагают:
* по центру строки;
* без абзацного отступа;
* используя интервал: после – 12 пт;
* без точки в конце;
* печатается прописными буквами, не подчеркивая.
! Пустые строки не допускаются до и после структурных элементов. !
_____""") # Структурные элементы

STO_ANSWERS.append("""_____
В заголовках разделов (глав) не допускаются переносы всловах, а также отрыв предлога или союза ототносящегося к нему слова.
Заголовки разделов (глав) следует оформлять:
* прописными буквами;
* без разрядки;
* без подчёркивания;
* шрифт – полужирный;
* выравнивание – по ширине;
* без абзацного отступа.

Максимальная длина текста в строке заголовка раздела (главы) должна быть:
* c отступом заголовка раздела (главы) слева – 12,5 мм, справа – 10 мм;
* размер шрифта (кегль) – от 12 до 14 (как в основном тексте).

Вторая ипоследующие строки заголовка раздела (главы) выполняются согласно требований, изложенных выше.
С целью отделения заголовков разделов (глав) от основного текста их следует выполнять интервалом: после –12 пт (по последней строке заголовка раздела (главы)).
Пустые строки не допускаются до и после заголовков разделов (глав). Если заголовок раздела (главы) состоит из нескольких предложений, их разделяют точкой, в конце последнего предложения точка не ставится.
Каждый раздел (главу) следует начинать с новой страницы.
_____""") # Заголовки разделов/глав

STO_ANSWERS.append("""_____
Заголовки подразделов, пунктов и подпунктов следует оформлять с использованием абзацного отступа 12,5 мм с прописной буквы без точки в конце.
Заголовки подразделов, пунктов и подпунктов следует выделять:
* интервалами: до – 12 пт, после – 12 пт;
* выравнивание – по ширине;
* размер шрифта (кегль) – от 12 до 14 (как в основном тексте);
* допускается использование полужирного шрифта.

Вторая и следующие строки заголовков подразделов, пунктов и подпунктов начинаются без абзацного отступа.
Пустые строки недопускаются до и после заголовков подразделов, пунктов и подпунктов.

Заголовки подразделов, пунктов и подпунктов не подчёркиваются.
В заголовках, вынесенных отдельной строкой, точка в конце не ставится.
Если заголовок состоит из нескольких предложений, их разделяют точкой, в конце последнего предложения точка не ставится.

В заголовках подразделов, пунктов и подпунктов недопускаются переносы в словах, а также отрыв предлога или союза от относящегося к нему слова.
Перед заголовком подраздела, если он помещён не в начале страницы, и после него должно быть не менее трёх строк текста. Если текст не помещается, то заголовок подраздела, пункта, подпункта рекомендуется перенести на другую страницу.
_____""") #подразделы
STO_ANSWERS.append("""_____
Уравнения и формулы (математические, химические и т.п.) следует выделять из текста в отдельную строку, с использованием интервалов:
* до –12 пт;
* после –12 пт.
Допускается располагать формулы с выравниванием по центру без использования абзацного отступа или по ширине с использованием абзацного отступа.
Во всем документе соблюдается единообразный подход в расположении формул.

После формулы ставят запятую.
Разьяснение формулы следует выполнять:
* междустрочным интервалом – одинарным (1,0 строки);
* с использованием интервалов: до – 0 пт, после последнего разъяснения символа – 12 пт;
* абзацный отступ каждой строки 12,5 мм;
* выравнивание – по ширине;
* размер шрифта (кегль) в разъяснении уменьшается по сравнению с основным текстом на 1 –2 пункта.
Первую строчку разъяснения начинают сослова «где» с абзацного отступа, двоеточие после слова «где» не ставят.

При выполнении расчётов формулу пишут:
* с новой строки;
* с использованием абзацного отступа 12,5 мм;
* с использованием интервалов: до – 0 пт, после – 0 пт;
* выравнивание – по ширине;
* с подставленными значениями всех величин и коэффициентов, с конечным результатом и единицами измерения, без нумерации.
При оформлении расчетов между объектами, заключающими формулы, следует использовать интервалы: до – 0пт, после – 0 пт.
_____""") # Формулы
STO_ANSWERS.append("""_____
При оформлении листингов программ рекомендуется использовать:
* гарнитуру Courier New;
* размер шрифта (кегль) – 11;
* междустрочный интервал – одинарный;
* выравнивание – по левому краю;
* цвет шрифта – черный;
* без абзацного отступа.

При написании исходного кода на языке программирования необходимо соблюдать требования стандарта оформления данного кода.
При оформлении программного кода следует использовать структурный отступ в два или четыре пробела. Другие размеры отступа использовать не рекомендуется.

Для возможности явного отделения текста листинга от основного текста документа, листинг рекомендуется помещать в рамку. Листинги, размещенные в приложениях, помещать в рамку не обязательно.

Если листинг объемный, то его необходимо размещать в приложении, используя альбомную ориентацию страницы, листинг выполняется в два столбца.
Либо в приложении размещаются основные функциональные элементы, а полный листинг размещается на диске в виде исходного проекта и скомпилированного программного файла. Диск прикладывается к работе.
_____""") # Листинг

STO_ANSWERS.append("""_____
Внутри документа могут быть приведены перечисления. Перед каждой позицией перечисления следует ставить дефис, а текст начинать со строчной буквы после пробела.

При необходимости ссылки в тексте документа на одно из перечислений, перед каждой позицией перечисления следует ставить строчную букву (за исключением ё, з, о, ч, ь, й, ы, ъ) со скобкой, а текст начинать со строчной буквы после пробела.
Для дальнейшей детализации перечислений необходимо использовать арабские цифры со скобкой, а запись производить с двойного абзацного отступа. Не допускается использовать арабские цифры с точкой.
_____""") # список

STO_ANSWERS.append("""_____
Приложение следует начинать с новой страницы с указанием наверху посередине страницы слова «ПРИЛОЖЕНИЕ» и его обозначения, а под ним в скобках для обязательного приложения пишут слово «обязательное», а для информационного – «рекомендуемое» или «справочное».

Приложение должно иметь заголовок, который приводят с прописной буквы отдельной строкой.
Приложение и его заголовок выполняют:
* междустрочным интервалом – одинарный (1,0 строки);
* выравнивание – по центру;
* без абзацного отступа;
* отделяют интервалом: после – 12 пт.

Приложения обозначают заглавными буквами русского алфавита, начиная с А, за исключением букв Ё, З, Й, О, Ч, Ь, Ы, Ъ. После слова «ПРИЛОЖЕНИЕ» следует буква, обозначающая его последовательность. Допускается обозначение приложений буквами латинского алфавита, за исключением букв I и О.
_____""") #приложения

STO_ANSWERS.append("""_____
На рисунок в тексте:
* должна быть ссылка;
* от текста отделяется интервалом до - 12 пт;
* выравнивание - по центру;
* без абзацного отступа
* рамки либо есть у всех рисунков в документе, либо нет ни у одного;
* крупные можно размещать на отдельной странице и даже вдоль, либо в приложение.

Подпись рисунка:
* без точки в конце;
* без абзацного отступа;
* выравнивание по центру;
* отделять интервалами до - 6 пт, после - 12 пт
_____""") # Рисунок

STO_ANSWERS.append("""_____
Название таблицы - без абзацного отступа, без точки, выравнивание по ширине.
Если таблица большая, то допускается поворот по часовой стрелке.
Должна быть ссылка в тексте на таблицу, допускается в конце предложения в скобках.

В конце заголовков и подзаголовков не ставится точка, указываются в единственном числе
Текст в таблице с одинарным междустрочным интервалом, можно уменьшить текст на 1-2 пункта, но не менее 8

Выравнивание текста в таблице:
* В заголовках и подзаголовках граф - выравнивание по центру сверху
* Боковик (текстовый) выравнивание по левому краю
* Боковик (числовой) выравнивание по центру
* Графы (текстовые) выравнивание по левому краю
* Графы (числовые) выравнивание по центру
* Таблицы ограничивают линиями, боковые по ширине основного текста
* Текст в заголовках граф можно параллельно или перпендикулярно
* После таблицы интервал до - 12 пт
_____""") #Таблицы

STO_ANSWERS.append("""_____
Допускаются ссылки в тексте на данный документ, нормативные документы и использованные источники. Ссылаться следует на литературный источник в целом или его разделы (главы), приложения. Допускаются ссылки на подразделы, пункты, таблицы и иллюстрации данного текстового документа.

При ссылках на нормативные документы указывают только их обозначение, допускается не указывать год их утверждения при условии полного описания документа в структурных элементах «НОРМАТИВНЫЕ ССЫЛКИ» или «СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ».

Ссылку на источник следует указывать порядковым номером по списку источников в квадратных скобках. Если объектов ссылки несколько, то их объединяют в одну комплексную ссылку, отделяя порядковые номера друг от друга точкой с запятой. Если объектов ссылки несколько и в списки использованных источников они расположены по порядку, то их объединяют в одну комплексную ссылку отделяя порядковые номера друг от друга знаком тире. Если по тексту приводится цитата, то в ссылке кроме номера источника указывается номер страницы, откуда взята цитата.

Ссылки на разделы (главы), подразделы, пункты и подпункты текстового документа следует давать с указанием их номеров без названия
На каждый источник информации в тексте работы должна быть дана ссылка.
_____""") #Ссылки

STO_ANSWERS.append("""_____
Используемые источники следует выполнять, используя:
* гарнитуру Times New Roman;
* размер шрифт (кегль) – от 12 до 14 пт (как в основном тексте документа);
* междустрочный интервал – полуторный (1,5 строки);
* выравнивание – по ширине;
* не допускается использование полужирного шрифта, курсива.

Схема библиографического описания источника представлена в примере:
Заголовок описания. Основное заглавие [Тип источника] : Сведения, относящиеся к заглавию / Сведения об ответственности. – Сведения об издании. – Выходные данные. – Объем.

Пример:
1) Пестовская, С. Н. Английский язык для спасателей. Технология безопасности [Текст] : учеб. пособ. / С. Н. Пестовская ; Сев. (Аркт.) федер. ун-т им. М. В. Ломоносова. – Архангельск : САФУ, 2016. – 124 с
2) Dickens, Ch. Oliver Twist [Text] / Ch. Dickens ; introd. and not. E. Westland ; ill. G. Cruikshank. – Hertfordshire : Wordsworth Editions Limited, 2000. – 373 p.
3) Научная электронная библиотека E-Library [Электронный ресурс] : [офиц. сайт] / Науч. электрон. б-ка. – Электрон. дан. – [Москва] : Научная электронная библиотека, 2000–2017. – Режим доступа : https://elibrary.ru/, свободный (дата обращения : 11.10.2017). – Загл. с экрана.
_____""")

send_url_STO = {
            "inline_keyboard":[[
                    {
                           "text": "Ссылка на СТО",
                           "url": "https://narfu.ru/upload/iblock/f8d/STO_60_02.2.3_2018_Obshchie_trebovaniya_k_oformleniyu_i_izlozheniyu_dokumentov_uchebnoy_deyatelnosti_obuchayushchikhsya.pdf"
                    }]]

    }
send_url_STIPEND = {
            "inline_keyboard":[[
                    {
                           "text": "Ссылка на стипендии",
                           "url": "https://narfu.ru/studies/stipendia/size/"
                    }]]

    }

keyboard = { "keyboard": [[{"text": "СТО"}],[{"text": "Стипендии"}],[{"text": "Погода"}]], "resize_keyboard":True }

key_STO = {
            "inline_keyboard":[[{"text": "Ссылка на СТО","callback_data": "/a"}],
                              [{"text": "Оглавление","callback_data": "/B"}],
                              [{"text": "Поля документа","callback_data": "/c"}],
                              [{"text": "Оформление текста","callback_data": "/d"}],
                              [{"text": "Структурные элементы","callback_data": "/e"}],
                              [{"text": "Заголовки разделов","callback_data": "/f"}],
                              [{"text": "Подразделы","callback_data": "/g"}],
                              [{"text": "Формулы","callback_data": "/h"}],
                              [{"text": "Листинг","callback_data": "/i"}],
                              [{"text": "Оформление списков","callback_data": "/j"}],
                              [{"text": "Приложение","callback_data": "/k"}],
                              [{"text": "Оформление рисунков","callback_data": "/l"}],
                              [{"text": "Таблицы","callback_data": "/m"}],
                              [{"text": "Ссылки","callback_data": "/n"}],
                              [{"text": "Библиографическая ссылка","callback_data": "/o"}]]
    }

key_STIPEND = {
            "inline_keyboard":[[{"text": "Ссылка на стипендии","callback_data": "/u"}],
                              [{"text": "Государственная социальная стипендия","callback_data": "/p"}],
                              [{"text": "Именные стипендии","callback_data": "/q"}],
                              [{"text": "Материальная поддержка","callback_data": "/r"}],
                              [{"text": "Повышенная государственная академическая стипендия","callback_data": "/s"}],
                              [{"text": "Стипендия 'Первокурсник 5.0'","callback_data": "/t"}]]
    }

gss = 'https://psv4.userapi.com/c856416/u237349911/docs/d17/72404b5a0e47/gss.jpg?extra=5mDiAWoFiueYMGLaBwXf4_8BV-FIn1xoYf6e0aaT9l3XbRMql-e1DWHue-D7oHbI6bDLLXf2l_hMB49M3dy6HF39RzTEG6pU6OTbcgsxKU7ytN6x-o2RGKbn0qzVz28ahA5awNPqAoL9IZ8ptNjZqy-_CMg'
im = 'https://psv4.userapi.com/c856416/u237349911/docs/d4/e40dbe486b5f/imennaya.jpg?extra=5YnohMPlQ75uAyJVF_o8fizTA_pdAYtZljqkRanw78XVL4gPOGySyG4NS7MNJRCGzRB7cr8Q1pgvcwXMtoq_e65KKfc6kNgT_IDcZblbEji8i1N-U79XL8jACqE-SzxAR977HS3UuD_i3GOgqZz5As0-YA8'
mp = 'https://psv4.userapi.com/c856416/u237349911/docs/d11/2bc6b5fc10f3/matpom.jpg?extra=lsx4_4w1aEHYjmJtdgDi1UlWNm50GzuSNiUfoMwapO7IO81u8P6RJFwTVT9pi7sIryIDxB9EpwYXDSsSOhX1Bg4p5ypRoYmwH3KpUyMoZUstg1XZUvMyXIk0abIKgjqIocMLoOQmmuTXG9zWnWG2g3kMDyM'
pgas2 = 'https://psv4.userapi.com/c856416/u237349911/docs/d4/0cf6e9fb092d/pgas1.jpg?extra=I5wcQivOqYNxhq5GNNHiic0_43hptcmPuKj3A3dBMoRDUv968OXApETU_25zdiZWrhzC-bFWOWUxIotT5Ikq8Kql9CZeS3TrmiFnCjatvlvnJ0-fyxrRGh5NT8xWy945iIXZm79HQqgT0biMM9kk4TzWku0'
pgas1 = 'https://psv4.userapi.com/c856416/u237349911/docs/d16/5ff24ff969a7/pgas2.jpg?extra=XdCrlYkzB2C8wPrwQwL4c6fDehpTHdflE3DT-3A2sB5XrKoGWtUixUusfdjIxwzCQqvSCl8p1aScPgE6EXp1c9V4IprI6GRUWisRzQy3hzPBI8KfkeEX1rqyRHdXWki5dORZbQ_Eyyhy9ceARHalSAa91P0'
p50 = 'https://psv4.userapi.com/c856416/u237349911/docs/d6/38676b43468c/perv.jpg?extra=SrwKaX2pAK6mzRx-tMk00C99iJkDVd0msLHs3lUH5uea36-0pJo2EvU_O2m3XN-NBJBH1qqG053eV-hdDpABlIc3bXNpJAkTr6ThZafoD5EuP1Ne4bCuKnuAvxucN_Zzw1j_jZSQ4kwN12W7kPZ-mrIBOk4'

# Констан
telegram_bot = " # Токен
URL = f'https://api.telegram.org/bot{telegram_bot}/' # Полная ссылка

# Метод считывания JSON от Телеграмма
def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Выкучиваем погоду
def get_weather():
    params = {"access_key": "6b4267d55e453c1a2614d6251c28e61d", "query": "Arkhangelsk"}
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    return f"""В Архангельске на {api_response['location']['localtime']}
Температура {api_response['current']['temperature']} °C
Влажность {api_response['current']['humidity']} %
Ветер {api_response['current']['wind_dir']} {api_response['current']['wind_speed']} км.ч"""

# Метод отправки сообщений
def send_message(chat_id , text, reply_markup ):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup) }
    r = requests.post(url , json=answer)
    return r.json()

def send_photo(chat_id , photo):
    url = URL + 'sendPhoto'
    answer = {'chat_id': chat_id, 'photo': photo}
    r = requests.post(url , json=answer)
    return r.json()

# Алгоритм ответов на команды
@app.route(f'/{telegram_bot}', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
              r = request.get_json()
              if 'message' in r:
                    chat_id = r['message']['chat']['id']
                    message = r['message']['text']
              if 'callback_query' in r:
                    chat_id = r['callback_query']['from']['id']
                    message = r['callback_query']['data']

              if  message.lower() in G_COMMANDS[4]:
                  send_message(chat_id=chat_id, text=G_ANSWERS[3], reply_markup=keyboard)

              # Генеральные команды
              elif message.lower() in G_COMMANDS[0]:
                  send_message(chat_id=chat_id, text=G_ANSWERS[0], reply_markup=keyboard)
              elif message.lower() in G_COMMANDS[1]:
                  send_message(chat_id=chat_id, text=G_ANSWERS[1], reply_markup=key_STIPEND)
              elif message.lower() in G_COMMANDS[2]:
                  send_message(chat_id=chat_id, text=G_ANSWERS[2], reply_markup=key_STO)
              elif message.lower() in G_COMMANDS[3]:
                  weather = get_weather()
                  send_message(chat_id=chat_id, text=weather, reply_markup=keyboard)

              # СТО команды
              elif message.lower() in STO_COMMANDS[0]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[0], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[1]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[1], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[2]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[2], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[3]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[3], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[4]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[4], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[5]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[5], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[6]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[6], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[7]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[7], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[8]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[8], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[9]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[9], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[10]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[10], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[11]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[11], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[12]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[12], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[13]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[13], reply_markup=send_url_STO)
              elif message.lower() in STO_COMMANDS[14]:
                  send_message(chat_id=chat_id, text=STO_ANSWERS[14], reply_markup=send_url_STO)

                  # Стипении команды
              elif message.lower() in STIPEND_COMAND[0]:
                  send_message(chat_id=chat_id, text=STIPEND_ANSWERS[0], reply_markup=send_url_STIPEND)
              elif message.lower() in STIPEND_COMAND[1]:
                  send_message(chat_id=chat_id, text=STIPEND_ANSWERS[1], reply_markup=send_url_STIPEND)
                  send_photo(chat_id=chat_id, photo=gss)
              elif message.lower() in STIPEND_COMAND[2]:
                  send_message(chat_id=chat_id, text=STIPEND_ANSWERS[2], reply_markup=send_url_STIPEND)
                  send_photo(chat_id=chat_id, photo=im)
              elif message.lower() in STIPEND_COMAND[3]:
                  send_message(chat_id=chat_id, text=STIPEND_ANSWERS[3], reply_markup=send_url_STIPEND)
                  send_photo(chat_id=chat_id, photo=mp)
              elif message.lower() in STIPEND_COMAND[4]:
                  send_message(chat_id=chat_id, text=STIPEND_ANSWERS[4], reply_markup=send_url_STIPEND)
                  send_photo(chat_id=chat_id, photo=pgas1)
                  send_photo(chat_id=chat_id, photo=pgas2)
              elif message.lower() in STIPEND_COMAND[5]:
                  send_message(chat_id=chat_id, text=STIPEND_ANSWERS[5], reply_markup=send_url_STIPEND)
                  send_photo(chat_id=chat_id, photo=p50)


              return jsonify(r)

    return '<h1>Hello my friend!</h1>'

# Основная функция
if __name__ == '__main__':
    app.run()
