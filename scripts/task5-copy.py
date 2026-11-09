"""Offline translations for the three new Revision 5 strings."""
import json
from pathlib import Path

keys = ['Vin AI provides informational insights to help you decide. Always inspect a car before you buy.',
        'Sample report for illustration.', 'Check the VIN. Then decide.']
copy = {
'en': keys,
'ru': ['Vin AI помогает разобраться в информации и принять решение. Всегда осматривай автомобиль перед покупкой.', 'Пример отчёта для ознакомления.', 'Проверь VIN. Затем решай.'],
'de': ['Vin AI bietet Informationen als Entscheidungshilfe. Prüfe ein Auto immer vor dem Kauf.', 'Beispielbericht zur Veranschaulichung.', 'Prüfe die VIN. Dann entscheide.'],
'es': ['Vin AI ofrece información para ayudarte a decidir. Inspecciona siempre el coche antes de comprarlo.', 'Informe de ejemplo con fines ilustrativos.', 'Comprueba el VIN. Luego decide.'],
'fr': ['Vin AI fournit des informations pour vous aider à décider. Inspectez toujours une voiture avant de l’acheter.', 'Rapport donné à titre d’exemple.', 'Vérifiez le VIN. Puis décidez.'],
'it': ['Vin AI offre informazioni per aiutarti a decidere. Ispeziona sempre un’auto prima di acquistarla.', 'Rapporto di esempio a scopo illustrativo.', 'Controlla il VIN. Poi decidi.'],
'pt': ['O Vin AI oferece informações para ajudar você a decidir. Sempre inspecione o carro antes de comprar.', 'Relatório de exemplo para ilustração.', 'Verifique o VIN. Depois decida.'],
'tr': ['Vin AI, karar vermene yardımcı olacak bilgiler sunar. Satın almadan önce aracı mutlaka incele.', 'Örnek amaçlı rapor.', 'VIN’i kontrol et. Sonra karar ver.'],
'ko': ['Vin AI는 결정을 돕는 참고 정보를 제공합니다. 구매 전에 항상 차량을 점검하세요.', '이해를 돕기 위한 샘플 보고서입니다.', '차대번호를 확인하고 결정하세요.'],
'zh': ['Vin AI 提供参考信息，帮助你做出决定。购车前请务必检查车辆。', '示例报告，仅供参考。', '先查车架号，再做决定。'],
}
for lang, values in copy.items():
    path = Path('i18n') / f'{lang}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    data = {k:v for k,v in data.items() if not any(term in k for term in ('NMVTIS', 'Carfax', 'What does Vin AI NOT include?', 'A real Vin AI sample report.'))}
    data.update(zip(keys, values))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
