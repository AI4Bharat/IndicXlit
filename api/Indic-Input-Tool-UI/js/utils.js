const PERSO_ARABIC_LANGS = ['ur', 'sd'];

function setQuillTextDirection(value, quill) {
    // Src: https://github.com/quilljs/quill/blob/1.3.7/modules/toolbar.js#L219
    let align = quill.getFormat()['align'];
    if (value === 'rtl' && align == null) {
        quill.format('align', 'right', Quill.sources.USER);
    } else if (!value && align === 'right') {
        quill.format('align', false, Quill.sources.USER);
    }
    quill.format('direction', value, Quill.sources.USER);
}

function setQuillTextDirectionAutomatically(lang_code, quill) {
    // For PersoArabic scripts, text direction is RTL
    // Otherwise, it's predominantly LTR

    const direction =  PERSO_ARABIC_LANGS.includes(lang_code) ? 'rtl' : null;
    setQuillTextDirection(direction, quill);
}
