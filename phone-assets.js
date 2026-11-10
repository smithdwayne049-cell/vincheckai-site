// Resolve from this module, so nested locale routes use the same asset root.
const languages = new Set(['en','ru','de','es','fr','it','pt','tr','ko','zh']);
const locale = document.documentElement.lang.split('-')[0];
const language = languages.has(locale) ? locale : 'en';
export function phoneAsset(index = 0) {
  const name = ['phone','phone-specs','phone-flags','phone-compare'][index] || 'phone';
  return new URL(`./assets/web/screens/${language}/${name}.webp`, import.meta.url).href;
}
