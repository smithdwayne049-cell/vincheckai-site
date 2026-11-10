// The VIN is kept on this device and sent only to the public NHTSA endpoint.
for (const decoder of document.querySelectorAll('.vin-decoder')) {
  const form = decoder.querySelector('form');
  const input = form.querySelector('input');
  const button = form.querySelector('button');
  const status = decoder.querySelector('.vin-status');
  const output = decoder.querySelector('.vin-output');
  const copy = Object.fromEntries([...decoder.querySelectorAll('[data-copy]')].map(el => [el.dataset.copy, el.textContent]));
  let pending = false;
  try { input.value = localStorage.getItem('vinai:last-vin') || ''; } catch { /* Storage can be disabled. */ }
  input.addEventListener('input', () => {
    const start = input.selectionStart;
    input.value = input.value.toUpperCase();
    if (start !== null) input.setSelectionRange(start, start);
    input.removeAttribute('aria-invalid');
    status.textContent = '';
  });
  const el = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  function appLink() {
    const link = document.querySelector('a.play[href^="https://play.google.com/"]');
    return link.cloneNode(true);
  }
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (pending) return;
    const vin = input.value.trim().toUpperCase();
    input.value = vin;
    if (!/^[A-HJ-NPR-Z0-9]{17}$/.test(vin)) {
      output.replaceChildren();
      status.textContent = copy.invalid;
      input.setAttribute('aria-invalid', 'true');
      input.focus();
      return;
    }
    try { localStorage.setItem('vinai:last-vin', vin); } catch { /* Optional persistence. */ }
    pending = true;
    button.disabled = true;
    status.textContent = copy.loading;
    output.setAttribute('aria-busy', 'true');
    output.replaceChildren();
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(`https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/${vin}?format=json`, {signal:controller.signal, credentials:'omit', referrerPolicy:'no-referrer'});
      if (!response.ok) throw new Error('NHTSA request failed');
      const payload = await response.json();
      const row = payload?.Results?.[0];
      if (!row || typeof row !== 'object') throw new Error('Invalid NHTSA response');
      const clean = value => typeof value === 'string' ? value.trim() : '';
      const codes = clean(row.ErrorCode).split(',').map(s => s.trim()).filter(Boolean);
      if (!clean(row.Make) || !clean(row.Model) || codes.some(code => code !== '0')) {
        output.append(el('p', copy.unavailable), appLink());
      } else {
        output.append(el('h2', copy.result));
        const specs = el('dl', '', 'specs');
        const engine = [clean(row.DisplacementL) && `${Number(row.DisplacementL) || row.DisplacementL} L`, clean(row.EngineCylinders) && `${row.EngineCylinders} ${copy.cylinders}`, clean(row.FuelTypePrimary)].filter(Boolean).join(' · ');
        const fields = {make:row.Make, model:row.Model, year:row.ModelYear, trim:row.Trim, engine, transmission:row.TransmissionStyle, drive:row.DriveType, body:row.BodyClass, country:row.PlantCountry};
        for (const [key, value] of Object.entries(fields)) {
          if (!clean(value)) continue;
          const item = el('div');
          item.append(el('dt', copy[key]), el('dd', value));
          specs.append(item);
        }
        output.append(specs, el('p', copy.source, 'micro'));
      }
      const upsell = decoder.querySelector('.vin-upsell');
      if (upsell) output.append(upsell.content.cloneNode(true));
      status.textContent = '';
      button.textContent = copy.decode;
    } catch {
      status.textContent = copy.network;
      button.textContent = copy.retry;
    } finally {
      clearTimeout(timeout);
      pending = false;
      button.disabled = false;
      output.removeAttribute('aria-busy');
    }
  });
}
