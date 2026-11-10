"""Offline translations for revision 7 (no translation services at runtime)."""
import json
from pathlib import Path

KEYS = '''17 characters
A clearer decision.
AI verdict + score 0–100
Basic vehicle specifications
Body class
Buy in the app — your next decoded VIN opens as a full report.
Compare two cars
Could not reach NHTSA. Check your connection and retry.
Crash rating
Data availability varies by vehicle and source.
Decode VIN
Decode basic vehicle specifications for free.
Decode your VIN for free: make, model, engine and basic specifications from NHTSA. Get a full AI report in the Vin AI app.
Decoding VIN…
Detailed data for this VIN is available in the Vin AI app
Drive type
Enter 17 letters and digits. I, O and Q are not allowed.
Enter a VIN
Free VIN Decoder | Vin AI
Free VIN decoder
Free basic VIN decode. Full AI report $3.99 for one VIN or compare two cars $5.99. One-time purchases in the Vin AI app. No subscription.
Free basic specifications · Source: NHTSA (US data). Coverage varies.
Free: basic VIN decode.
Fuel economy
Full AI report
Full AI reports for both cars
Get the full report in the Vin AI app
How it works
Market value
Model year
No subscription.
One VIN
One-time payment.
One-time payment. No subscription.
Plant country
Pricing
Report preview is locked. Data availability varies by vehicle and source.
Retry
Safety recalls & owner complaints
Source: NHTSA vPIC. Specifications only; availability varies by vehicle.
Start with the VIN.
Two cars
Two cars side by side
USD
VIN decoder
Vehicle specifications and AI insights
Vin AI Pricing | Full AI Reports & Car Comparison
cylinders'''.splitlines()

COPY = {
'ru': '''17 символов
Решение станет проще.
Вердикт ИИ + оценка 0–100
Основные характеристики автомобиля
Тип кузова
Купи в приложении — следующий расшифрованный VIN откроется как полный отчёт.
Сравнить два авто
Не удалось подключиться к NHTSA. Проверь интернет и повтори попытку.
Оценка краш-тестов
Доступность данных зависит от автомобиля и источника.
Расшифровать VIN
Узнай основные характеристики автомобиля бесплатно.
Бесплатная расшифровка VIN: марка, модель, двигатель и характеристики из NHTSA. Полный отчёт ИИ — в приложении Vin AI.
Расшифровываем VIN…
Подробные данные по этому VIN доступны в приложении Vin AI
Тип привода
Введи 17 латинских букв и цифр. Буквы I, O и Q недопустимы.
Введи VIN
Бесплатная расшифровка VIN | Vin AI
Бесплатная расшифровка VIN
Базовая расшифровка VIN бесплатно. Полный отчёт ИИ — $3.99 за один VIN, сравнение двух авто — $5.99. Разовая покупка в Vin AI, без подписки.
Основные характеристики бесплатно · Источник: NHTSA (данные США). Покрытие различается.
Бесплатно: базовая расшифровка VIN.
Расход топлива
Полный отчёт ИИ
Полные отчёты ИИ для обоих авто
Получи полный отчёт в приложении Vin AI
Как это работает
Рыночная стоимость
Модельный год
Без подписки.
Один VIN
Разовая оплата.
Разовая оплата. Без подписки.
Страна сборки
Цены
Предпросмотр отчёта закрыт. Доступность данных зависит от автомобиля и источника.
Повторить
Отзывы по безопасности и жалобы владельцев
Источник: NHTSA vPIC. Только характеристики; доступность зависит от автомобиля.
Начни с VIN.
Два автомобиля
Два автомобиля рядом
USD
Расшифровка VIN
Характеристики автомобилей и выводы ИИ
Цены Vin AI | Отчёты ИИ и сравнение авто
цил.''',
'de': '''17 Zeichen
Eine klarere Entscheidung.
KI-Urteil + Bewertung 0–100
Grundlegende Fahrzeugdaten
Karosserieklasse
In der App kaufen — die nächste VIN-Abfrage öffnet einen vollständigen Bericht.
Zwei Autos vergleichen
NHTSA ist nicht erreichbar. Verbindung prüfen und erneut versuchen.
Crashtest-Bewertung
Die Datenverfügbarkeit hängt vom Fahrzeug und der Quelle ab.
VIN entschlüsseln
Grundlegende Fahrzeugdaten kostenlos entschlüsseln.
VIN kostenlos entschlüsseln: Marke, Modell, Motor und Basisdaten von NHTSA. Vollständiger KI-Bericht in der Vin AI App.
VIN wird entschlüsselt…
Detaillierte Daten zu dieser VIN sind in der Vin AI App verfügbar
Antriebsart
17 Buchstaben und Ziffern eingeben. I, O und Q sind nicht erlaubt.
VIN eingeben
Kostenloser VIN-Decoder | Vin AI
Kostenloser VIN-Decoder
VIN-Basisdaten kostenlos. Vollständiger KI-Bericht $3.99 pro VIN oder zwei Autos vergleichen für $5.99. Einmalkauf in Vin AI, ohne Abo.
Kostenlose Basisdaten · Quelle: NHTSA (US-Daten). Abdeckung variiert.
Kostenlos: grundlegende VIN-Entschlüsselung.
Kraftstoffverbrauch
Vollständiger KI-Bericht
Vollständige KI-Berichte für beide Autos
Vollständigen Bericht in der Vin AI App erhalten
So funktioniert es
Marktwert
Modelljahr
Kein Abo.
Eine VIN
Einmalzahlung.
Einmalzahlung. Kein Abo.
Produktionsland
Preise
Berichtsvorschau gesperrt. Datenverfügbarkeit hängt vom Fahrzeug und der Quelle ab.
Erneut versuchen
Sicherheitsrückrufe und Besitzerbeschwerden
Quelle: NHTSA vPIC. Nur technische Daten; Verfügbarkeit hängt vom Fahrzeug ab.
Mit der VIN starten.
Zwei Autos
Zwei Autos nebeneinander
USD
VIN-Decoder
Fahrzeugdaten und KI-Einschätzungen
Vin AI Preise | KI-Berichte und Fahrzeugvergleich
Zylinder''',
'es': '''17 caracteres
Una decisión más clara.
Veredicto de IA + puntuación 0–100
Especificaciones básicas del vehículo
Clase de carrocería
Compra en la app: el próximo VIN que decodifiques abrirá un informe completo.
Comparar dos coches
No se pudo conectar con NHTSA. Revisa tu conexión e inténtalo de nuevo.
Calificación de choque
La disponibilidad de datos varía según el vehículo y la fuente.
Decodificar VIN
Consulta gratis las especificaciones básicas del vehículo.
Decodifica tu VIN gratis: marca, modelo, motor y datos básicos de NHTSA. Obtén un informe de IA completo en Vin AI.
Decodificando VIN…
Los datos detallados de este VIN están disponibles en la app Vin AI
Tipo de tracción
Introduce 17 letras y números. No se permiten I, O ni Q.
Introduce un VIN
Decodificador VIN gratuito | Vin AI
Decodificador VIN gratuito
Datos VIN básicos gratis. Informe de IA completo por $3.99 por VIN o compara dos coches por $5.99. Compra única en Vin AI, sin suscripción.
Datos básicos gratis · Fuente: NHTSA (datos de EE. UU.). La cobertura varía.
Gratis: decodificación VIN básica.
Consumo de combustible
Informe de IA completo
Informes de IA completos para ambos coches
Obtén el informe completo en la app Vin AI
Cómo funciona
Valor de mercado
Año del modelo
Sin suscripción.
Un VIN
Pago único.
Pago único. Sin suscripción.
País de fabricación
Precios
Vista previa bloqueada. Los datos disponibles varían según el vehículo y la fuente.
Reintentar
Llamadas a revisión y quejas de propietarios
Fuente: NHTSA vPIC. Solo especificaciones; la disponibilidad varía según el vehículo.
Empieza por el VIN.
Dos coches
Dos coches uno al lado del otro
USD
Decodificador VIN
Especificaciones del vehículo y análisis de IA
Precios Vin AI | Informes de IA y comparación de coches
cilindros''',
'fr': '''17 caractères
Une décision plus claire.
Verdict IA + note de 0 à 100
Caractéristiques de base du véhicule
Catégorie de carrosserie
Achetez dans l’app : le prochain VIN décodé ouvrira un rapport complet.
Comparer deux voitures
Connexion à NHTSA impossible. Vérifiez votre connexion et réessayez.
Note aux crash-tests
La disponibilité des données varie selon le véhicule et la source.
Décoder le VIN
Décodez gratuitement les caractéristiques de base du véhicule.
Décodage VIN gratuit : marque, modèle, moteur et données de base NHTSA. Rapport IA complet dans l’app Vin AI.
Décodage du VIN…
Les données détaillées de ce VIN sont disponibles dans l’app Vin AI
Type de transmission aux roues
Saisissez 17 lettres et chiffres. I, O et Q sont interdits.
Saisissez un VIN
Décodeur VIN gratuit | Vin AI
Décodeur VIN gratuit
Décodage VIN de base gratuit. Rapport IA complet à $3.99 par VIN ou comparaison de deux voitures à $5.99. Achat unique dans Vin AI, sans abonnement.
Données de base gratuites · Source : NHTSA (données américaines). Couverture variable.
Gratuit : décodage VIN de base.
Consommation de carburant
Rapport IA complet
Rapports IA complets pour les deux voitures
Obtenez le rapport complet dans l’app Vin AI
Comment ça marche
Valeur du marché
Année modèle
Sans abonnement.
Un VIN
Paiement unique.
Paiement unique. Sans abonnement.
Pays de fabrication
Tarifs
Aperçu du rapport verrouillé. Les données disponibles varient selon le véhicule et la source.
Réessayer
Rappels de sécurité et plaintes des propriétaires
Source : NHTSA vPIC. Caractéristiques uniquement ; disponibilité variable selon le véhicule.
Commencez par le VIN.
Deux voitures
Deux voitures côte à côte
USD
Décodeur VIN
Caractéristiques des véhicules et analyses IA
Tarifs Vin AI | Rapports IA et comparaison de voitures
cylindres''',
'it': '''17 caratteri
Una decisione più chiara.
Verdetto IA + punteggio 0–100
Specifiche di base del veicolo
Classe di carrozzeria
Acquista nell’app: il prossimo VIN decodificato aprirà un rapporto completo.
Confronta due auto
Impossibile raggiungere NHTSA. Controlla la connessione e riprova.
Valutazione crash test
La disponibilità dei dati varia in base al veicolo e alla fonte.
Decodifica VIN
Decodifica gratis le specifiche di base del veicolo.
Decodifica VIN gratuita: marca, modello, motore e dati di base NHTSA. Rapporto IA completo nell’app Vin AI.
Decodifica del VIN…
I dati dettagliati per questo VIN sono disponibili nell’app Vin AI
Tipo di trazione
Inserisci 17 lettere e cifre. I, O e Q non sono consentite.
Inserisci un VIN
Decoder VIN gratuito | Vin AI
Decoder VIN gratuito
Decodifica VIN di base gratuita. Rapporto IA completo a $3.99 per VIN o confronto di due auto a $5.99. Acquisto unico in Vin AI, senza abbonamento.
Specifiche di base gratuite · Fonte: NHTSA (dati USA). Copertura variabile.
Gratis: decodifica VIN di base.
Consumo di carburante
Rapporto IA completo
Rapporti IA completi per entrambe le auto
Ottieni il rapporto completo nell’app Vin AI
Come funziona
Valore di mercato
Anno modello
Nessun abbonamento.
Un VIN
Pagamento unico.
Pagamento unico. Nessun abbonamento.
Paese di produzione
Prezzi
Anteprima del rapporto bloccata. I dati disponibili variano in base al veicolo e alla fonte.
Riprova
Richiami di sicurezza e reclami dei proprietari
Fonte: NHTSA vPIC. Solo specifiche; la disponibilità varia in base al veicolo.
Inizia dal VIN.
Due auto
Due auto fianco a fianco
USD
Decoder VIN
Specifiche dei veicoli e analisi IA
Prezzi Vin AI | Rapporti IA e confronto auto
cilindri''',
'pt': '''17 caracteres
Uma decisão mais clara.
Veredito da IA + nota de 0 a 100
Especificações básicas do veículo
Classe da carroceria
Compre no app: o próximo VIN decodificado abrirá um relatório completo.
Comparar dois carros
Não foi possível acessar a NHTSA. Verifique sua conexão e tente novamente.
Nota em testes de colisão
A disponibilidade dos dados varia conforme o veículo e a fonte.
Decodificar VIN
Consulte grátis as especificações básicas do veículo.
Decodifique seu VIN grátis: marca, modelo, motor e dados básicos da NHTSA. Relatório completo de IA no app Vin AI.
Decodificando VIN…
Os dados detalhados deste VIN estão disponíveis no app Vin AI
Tipo de tração
Digite 17 letras e números. I, O e Q não são permitidos.
Digite um VIN
Decodificador VIN gratuito | Vin AI
Decodificador VIN gratuito
Decodificação VIN básica grátis. Relatório completo de IA por $3.99 por VIN ou comparação de dois carros por $5.99. Compra única no Vin AI, sem assinatura.
Dados básicos grátis · Fonte: NHTSA (dados dos EUA). A cobertura varia.
Grátis: decodificação VIN básica.
Consumo de combustível
Relatório completo de IA
Relatórios completos de IA para os dois carros
Obtenha o relatório completo no app Vin AI
Como funciona
Valor de mercado
Ano-modelo
Sem assinatura.
Um VIN
Pagamento único.
Pagamento único. Sem assinatura.
País de fabricação
Preços
Prévia do relatório bloqueada. Os dados disponíveis variam conforme o veículo e a fonte.
Tentar novamente
Recalls de segurança e reclamações de proprietários
Fonte: NHTSA vPIC. Apenas especificações; a disponibilidade varia conforme o veículo.
Comece pelo VIN.
Dois carros
Dois carros lado a lado
USD
Decodificador VIN
Especificações dos veículos e análises de IA
Preços Vin AI | Relatórios de IA e comparação de carros
cilindros''',
'tr': '''17 karakter
Daha net bir karar.
Yapay zekâ kararı + 0–100 puan
Temel araç özellikleri
Gövde sınıfı
Uygulamada satın al — sonraki VIN sorgun tam rapor olarak açılır.
İki aracı karşılaştır
NHTSA’ya ulaşılamadı. Bağlantını kontrol edip tekrar dene.
Çarpışma testi puanı
Veri kullanılabilirliği araca ve kaynağa göre değişir.
VIN çözümle
Temel araç özelliklerini ücretsiz öğren.
VIN kodunu ücretsiz çözümle: NHTSA’dan marka, model, motor ve temel özellikler. Tam yapay zekâ raporu Vin AI uygulamasında.
VIN çözümleniyor…
Bu VIN için ayrıntılı veriler Vin AI uygulamasında mevcut
Çekiş tipi
17 harf ve rakam gir. I, O ve Q kullanılamaz.
VIN gir
Ücretsiz VIN Çözücü | Vin AI
Ücretsiz VIN çözücü
Temel VIN çözümleme ücretsiz. Bir VIN için tam yapay zekâ raporu $3.99, iki araç karşılaştırma $5.99. Vin AI’da tek seferlik satın alma, abonelik yok.
Ücretsiz temel özellikler · Kaynak: NHTSA (ABD verileri). Kapsam değişir.
Ücretsiz: temel VIN çözümleme.
Yakıt tüketimi
Tam yapay zekâ raporu
Her iki araç için tam yapay zekâ raporları
Tam raporu Vin AI uygulamasında al
Nasıl çalışır
Piyasa değeri
Model yılı
Abonelik yok.
Bir VIN
Tek seferlik ödeme.
Tek seferlik ödeme. Abonelik yok.
Üretim ülkesi
Fiyatlar
Rapor önizlemesi kilitli. Veri kullanılabilirliği araca ve kaynağa göre değişir.
Tekrar dene
Güvenlik geri çağırmaları ve araç sahibi şikâyetleri
Kaynak: NHTSA vPIC. Yalnızca teknik özellikler; kullanılabilirlik araca göre değişir.
VIN ile başla.
İki araç
Yan yana iki araç
USD
VIN çözücü
Araç özellikleri ve yapay zekâ değerlendirmeleri
Vin AI Fiyatları | Yapay Zekâ Raporları ve Araç Karşılaştırma
silindir''',
'ko': '''17자
더 명확한 결정.
AI 판정 + 점수 0–100
기본 차량 제원
차체 분류
앱에서 구매하면 다음 VIN 조회 시 전체 보고서가 열립니다.
두 차량 비교
NHTSA에 연결할 수 없습니다. 연결을 확인하고 다시 시도하세요.
충돌 안전 등급
데이터 제공 여부는 차량과 출처에 따라 다릅니다.
VIN 해독
차량의 기본 제원을 무료로 확인하세요.
무료 VIN 해독: NHTSA의 제조사, 모델, 엔진 및 기본 제원. 전체 AI 보고서는 Vin AI 앱에서 확인하세요.
VIN 해독 중…
이 VIN의 상세 데이터는 Vin AI 앱에서 확인할 수 있습니다
구동 방식
영문과 숫자 17자를 입력하세요. I, O, Q는 사용할 수 없습니다.
VIN 입력
무료 VIN 해독기 | Vin AI
무료 VIN 해독기
기본 VIN 해독은 무료입니다. VIN 1개 전체 AI 보고서 $3.99, 두 차량 비교 $5.99. Vin AI 앱에서 일회성 구매, 구독 없음.
무료 기본 제원 · 출처: NHTSA (미국 데이터). 제공 범위는 다릅니다.
무료: 기본 VIN 해독.
연비
전체 AI 보고서
두 차량 모두의 전체 AI 보고서
Vin AI 앱에서 전체 보고서 확인
이용 방법
시장 가치
모델 연도
구독 없음.
VIN 1개
일회성 결제.
일회성 결제. 구독 없음.
생산 국가
가격
보고서 미리보기가 잠겨 있습니다. 데이터 제공 여부는 차량과 출처에 따라 다릅니다.
다시 시도
안전 리콜 및 소유자 불만
출처: NHTSA vPIC. 제원만 제공하며 제공 여부는 차량에 따라 다릅니다.
VIN부터 시작하세요.
차량 2대
두 차량 나란히 비교
USD
VIN 해독기
차량 제원 및 AI 분석
Vin AI 가격 | AI 보고서 및 차량 비교
기통''',
'zh': '''17个字符
更清晰的决定。
AI判断 + 0–100评分
车辆基本参数
车身类别
在应用内购买，下次解码VIN时即可打开完整报告。
对比两辆车
无法连接NHTSA。请检查网络后重试。
碰撞测试评级
数据可用性因车辆和来源而异。
解码VIN
免费查看车辆基本参数。
免费解码VIN：查看NHTSA提供的品牌、车型、发动机及基本参数。完整AI报告请前往Vin AI应用。
正在解码VIN…
此VIN的详细数据可在Vin AI应用中查看
驱动方式
请输入17位英文字母和数字，不可包含I、O或Q。
输入VIN
免费VIN解码器 | Vin AI
免费VIN解码器
基础VIN解码免费。单个VIN完整AI报告$3.99，两车对比$5.99。在Vin AI应用内一次性购买，无需订阅。
免费基本参数 · 来源：NHTSA（美国数据）。覆盖范围有所不同。
免费：基础VIN解码。
燃油经济性
完整AI报告
两辆车的完整AI报告
在Vin AI应用中获取完整报告
使用方法
市场价值
车型年份
无需订阅。
一个VIN
一次性付款。
一次性付款，无需订阅。
生产国家
价格
报告预览已锁定。数据可用性因车辆和来源而异。
重试
安全召回与车主投诉
来源：NHTSA vPIC。仅提供车辆参数，数据可用性因车辆而异。
从VIN开始。
两辆车
两车并排对比
USD
VIN解码器
车辆参数与AI分析
Vin AI价格 | AI报告与车辆对比
缸'''
}

def install(root):
    for lang, text in COPY.items():
        values = text.splitlines()
        assert len(values) == len(KEYS), (lang, len(values), len(KEYS))
        path = root/'i18n'/f'{lang}.json'
        strings = json.loads(path.read_text(encoding='utf-8'))
        strings.update(zip(KEYS, values))
        strings['Engine specifications'] = {'ru':'Двигатель','de':'Motor','es':'Motor','fr':'Moteur','it':'Motore','pt':'Motor','tr':'Motor','ko':'엔진','zh':'发动机'}[lang]
        path.write_text(json.dumps(strings,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__ == '__main__':
    install(Path(__file__).resolve().parent.parent)
