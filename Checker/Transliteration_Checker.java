import java.io.*;
import java.util.*;
import java.util.HashMap;
import java.util.Map;

enum LanguageType {
    AS,
    BN,
    BRX,
    DOI,
    EN,
    GU,
    HI,
    KOK,
    KN,
    KS,
    MAI,
    ML,
    MNI,
    MR,
    NE,
    PA,
    OR,
    SA,
    SAT,
    SD,
    TE,
    TA,
    UR,
    ISL
  }

public class Validation_Checker
{
    static List<String> eng_vowels = new ArrayList<String>();
    static List<String> eng_stop_list = new ArrayList<String>();
    static Map <LanguageType, Integer> lang_base = new HashMap<>();
    static Map <LanguageType,List<String>> vowel_map = new HashMap<>();
    static Map <LanguageType,List<String>> stop_list = new HashMap<>();
    static Map <LanguageType,Map<String, List<String>>> consonants_map = new HashMap<>();

    public static void init()
    {
        // initialize eng vowels
        eng_vowels.add("a");
        eng_vowels.add("e");
        eng_vowels.add("i");
        eng_vowels.add("o");
        eng_vowels.add("u");

        // initialize eng stop list
        eng_stop_list.add("h");
        eng_stop_list.add("y");

        //initialize Language base
        lang_base.put(LanguageType.HI,2304);
        lang_base.put(LanguageType.MR,2304);
        lang_base.put(LanguageType.MAI,2304);
        lang_base.put(LanguageType.KOK,2304);
        lang_base.put(LanguageType.SA,2304);
        lang_base.put(LanguageType.NE,2304);
        lang_base.put(LanguageType.BRX,2304);
        lang_base.put(LanguageType.DOI,2304);
        lang_base.put(LanguageType.KS,2304);
        lang_base.put(LanguageType.GU,2688);
        lang_base.put(LanguageType.PA,2560);
        lang_base.put(LanguageType.BN,2432);
        lang_base.put(LanguageType.AS,2432);
        lang_base.put(LanguageType.OR,2816);
        lang_base.put(LanguageType.TE,3072);
        lang_base.put(LanguageType.TA,2944);
        lang_base.put(LanguageType.KN,3200);
        lang_base.put(LanguageType.ML,3328);
        lang_base.put(LanguageType.UR,1536);
        lang_base.put(LanguageType.SD,1536);
        lang_base.put(LanguageType.MNI,43968);
        lang_base.put(LanguageType.SAT,6648);

        //initialize vowel map
        List<String> dev_vowels = new ArrayList<String>();
        dev_vowels = Arrays.asList("ा,ॅ,ॉ,ि,ी,ु,ू,ृ,े,ै,ो,ौ,ः,अ,आ,ऑ,इ,ई,उ,ऊ,ए,ऐ,ओ,औ,ऎ,ॆ,ॊ,ऒ,ऽ,ॷ,ॶ".split(","));
        vowel_map.put(LanguageType.HI, dev_vowels);
        vowel_map.put(LanguageType.MR, dev_vowels);
        vowel_map.put(LanguageType.MAI, dev_vowels);
        vowel_map.put(LanguageType.KOK, dev_vowels);
        vowel_map.put(LanguageType.SA, dev_vowels);
        vowel_map.put(LanguageType.NE, dev_vowels);
        vowel_map.put(LanguageType.BRX, dev_vowels);
        vowel_map.put(LanguageType.DOI, dev_vowels);
        vowel_map.put(LanguageType.KS, dev_vowels);

        List<String> gu_vowels = new ArrayList<String>();
        gu_vowels = Arrays.asList("ા,િ,ી,ુ,ૂ,ૃ,ૄ,ૅ,ે,ૈ,ૉ,ો,ૌ,ઃ,અ,આ,ઇ,ઈ,ઉ,ઊ,ઌ,ઍ,એ,ઐ,ઑ,ઓ,ઔ".split(","));
        vowel_map.put(LanguageType.GU, gu_vowels);

        List<String> pa_vowels = new ArrayList<String>();
        pa_vowels = Arrays.asList("ਃ,ਿ,ੀ,ਾ,ੁ,ੂ,ੇ,ੈ,ੋ,ੌ,ਅ,ਆ,ਇ,ਈ,ਉ,ਊ,ਏ,ਐ,ਓ,ਔ".split(","));
        vowel_map.put(LanguageType.PA, pa_vowels);

        List<String> bn_vowels = new ArrayList<String>();
        bn_vowels = Arrays.asList("া,ি,ী,ু,ূ,ঃ,ৃ,ৄ,ে,ৈ,ো,ৌ,ৗ,অ,আ,ই,ঈ,উ,ঊ,ঋ,ঌ,এ,ঐ,ও,ঔ".split(","));
        vowel_map.put(LanguageType.BN, bn_vowels);
        vowel_map.put(LanguageType.AS, bn_vowels);

        List<String> or_vowels = new ArrayList<String>();
        or_vowels = Arrays.asList("ଅ,ଆ,ଇ,ଈ,ଉ,ଊ,ଋ,ଌ,ଏ,ଐ,ଓ,ଔ,ା,ି,ୀ,ୁ,ୂ,ୃ,ୄ,େ,ୈ,ୋ,ୌ".split(","));
        vowel_map.put(LanguageType.OR, or_vowels);

        //initialize stop lists
        List<String> dev_stop_list = new ArrayList<String>();
        dev_stop_list = Arrays.asList("य,ह".split(","));
        stop_list.put(LanguageType.HI, dev_stop_list);
        stop_list.put(LanguageType.MR, dev_stop_list);
        stop_list.put(LanguageType.MAI, dev_stop_list);
        stop_list.put(LanguageType.KOK, dev_stop_list);
        stop_list.put(LanguageType.SA, dev_stop_list);
        stop_list.put(LanguageType.NE, dev_stop_list);
        stop_list.put(LanguageType.BRX, dev_stop_list);
        stop_list.put(LanguageType.DOI, dev_stop_list);
        stop_list.put(LanguageType.KS, dev_stop_list);

        List<String> gu_stop_list = new ArrayList<String>();
        gu_stop_list = Arrays.asList("હ,ય".split(","));
        stop_list.put(LanguageType.GU, gu_stop_list);

        List<String> pa_stop_list = new ArrayList<String>();
        pa_stop_list = Arrays.asList("ਯ,ਹ".split(","));
        stop_list.put(LanguageType.PA, pa_stop_list);

        List<String> bn_stop_list = new ArrayList<String>();
        bn_stop_list = Arrays.asList("হ,য,য়".split(","));
        stop_list.put(LanguageType.BN, bn_stop_list);
        stop_list.put(LanguageType.AS, bn_stop_list);

        List<String> or_stop_list = new ArrayList<String>();
        or_stop_list = Arrays.asList("ହ,ଯ,ୟ".split(","));
        stop_list.put(LanguageType.OR, or_stop_list);

        List<String> ta_stop_list = new ArrayList<String>();
        ta_stop_list = Arrays.asList("ய,ஹ".split(","));
        stop_list.put(LanguageType.TA, ta_stop_list);

        List<String> ml_stop_list = new ArrayList<String>();
        ml_stop_list = Arrays.asList("യ,ഹ".split(","));
        stop_list.put(LanguageType.ML, ml_stop_list);

        List<String> kn_stop_list = new ArrayList<String>();
        kn_stop_list = Arrays.asList("ಯ,ಹ".split(","));
        stop_list.put(LanguageType.KN, kn_stop_list);

        List<String> te_stop_list = new ArrayList<String>();
        te_stop_list = Arrays.asList("య,హ".split(","));
        stop_list.put(LanguageType.TE, te_stop_list);


        //hindi consonants mapping.
        Map<String, List<String>> en_hi_map = new HashMap<>();
        en_hi_map.put("b", Arrays.asList("ब,भ".split(",")));
        en_hi_map.put("c", Arrays.asList("क,च,छ,स,श,ष,क़".split(",")));
        en_hi_map.put("d", Arrays.asList("ड,ड़,ढ,ढ़,द,ध".split(",")));
        en_hi_map.put("f", Arrays.asList("फ,फ़".split(",")));
        en_hi_map.put("g", Arrays.asList("ग,घ,ङ,ज,ग़".split(",")));
        en_hi_map.put("j", Arrays.asList("ज,झ".split(",")));
        en_hi_map.put("k", Arrays.asList("क,ख,क़,ख़".split(",")));
        en_hi_map.put("l", Arrays.asList("ल,ळ,ऌ".split(",")));
        en_hi_map.put("m", Arrays.asList("म"));
        en_hi_map.put("n", Arrays.asList("ण,न".split(",")));
        en_hi_map.put("p", Arrays.asList("प,फ,फ़".split(",")));
        en_hi_map.put("q", Arrays.asList("क".split(",")));
        en_hi_map.put("r", Arrays.asList("र,ऋ,ऱ".split(",")));
        en_hi_map.put("s", Arrays.asList("स,ज,झ,ज़,श,ष".split(",")));
        en_hi_map.put("t", Arrays.asList("ट,ठ,त,थ,श,च".split(",")));
        en_hi_map.put("v", Arrays.asList("व"));
        en_hi_map.put("w", Arrays.asList("व"));
        en_hi_map.put("x", Arrays.asList("ज़,कस".split(",")));
        en_hi_map.put("z", Arrays.asList("ज़,ज,झ".split(",")));
        consonants_map.put(LanguageType.HI, en_hi_map);

        //marathi consonants mapping.
        Map<String, List<String>> en_mr_map = new HashMap<>();
        en_mr_map.put("b", Arrays.asList("ब,भ".split(",")));
        en_mr_map.put("c", Arrays.asList("क,च,छ,स,श,ष,क़".split(",")));
        en_mr_map.put("d", Arrays.asList("ड,ड़,ढ,ढ़,द,ध,ज,ळ".split(",")));
        en_mr_map.put("f", Arrays.asList("फ,फ़".split(",")));
        en_mr_map.put("g", Arrays.asList("ग,घ,ङ,ज,ग़".split(",")));
        en_mr_map.put("j", Arrays.asList("ज,झ".split(",")));
        en_mr_map.put("k", Arrays.asList("क,ख,क़,ख़".split(",")));
        en_mr_map.put("l", Arrays.asList("ल,ळ,ऌ,ऴ".split(",")));
        en_mr_map.put("m", Arrays.asList("म"));
        en_mr_map.put("n", Arrays.asList("ण,न,ऩ,ञ".split(",")));
        en_mr_map.put("p", Arrays.asList("प,फ,फ़".split(",")));
        en_mr_map.put("q", Arrays.asList("क,क़".split(",")));
        en_mr_map.put("r", Arrays.asList("र,ऋ,ऱ,ढ़".split(",")));
        en_mr_map.put("s", Arrays.asList("स,ज,झ,ज़,श,ष".split(",")));
        en_mr_map.put("t", Arrays.asList("ट,ठ,त,थ,श,च".split(",")));
        en_mr_map.put("v", Arrays.asList("व"));
        en_mr_map.put("w", Arrays.asList("व"));
        en_mr_map.put("x", Arrays.asList("ज़,कस".split(",")));
        en_mr_map.put("z", Arrays.asList("ज़,ज,झ".split(",")));
        consonants_map.put(LanguageType.MR, en_mr_map);

        //maithili consonants mapping.
        Map<String, List<String>> en_mai_map = new HashMap<>();
        en_mai_map.put("b", Arrays.asList("ब,भ".split(",")));
        en_mai_map.put("c", Arrays.asList("क,च,छ,स,श,ष,क़".split(",")));
        en_mai_map.put("d", Arrays.asList("ड,ड़,ढ,ढ़,द,ध,ज,ळ".split(",")));
        en_mai_map.put("f", Arrays.asList("फ,फ़".split(",")));
        en_mai_map.put("g", Arrays.asList("ग,घ,ङ,ज,ग़".split(",")));
        en_mai_map.put("j", Arrays.asList("ज,झ".split(",")));
        en_mai_map.put("k", Arrays.asList("क,ख,क़,ख़".split(",")));
        en_mai_map.put("l", Arrays.asList("ल,ळ,ऌ,ऴ".split(",")));
        en_mai_map.put("m", Arrays.asList("म"));
        en_mai_map.put("n", Arrays.asList("ण,न,ऩ,ञ".split(",")));
        en_mai_map.put("p", Arrays.asList("प,फ,फ़".split(",")));
        en_mai_map.put("q", Arrays.asList("क,क़".split(",")));
        en_mai_map.put("r", Arrays.asList("र,ऋ,ऱ,ढ़".split(",")));
        en_mai_map.put("s", Arrays.asList("स,ज,झ,ज़,श,ष".split(",")));
        en_mai_map.put("t", Arrays.asList("ट,ठ,त,थ,श,च".split(",")));
        en_mai_map.put("v", Arrays.asList("व"));
        en_mai_map.put("w", Arrays.asList("व"));
        en_mai_map.put("x", Arrays.asList("ज़,कस".split(",")));
        en_mai_map.put("z", Arrays.asList("ज़,ज,झ".split(",")));
        consonants_map.put(LanguageType.MAI, en_mai_map);

        //kokani consonants mapping
        Map<String, List<String>> en_kok_map = new HashMap<>();
        en_kok_map.put("b", Arrays.asList("ब,भ".split(",")));
        en_kok_map.put("c", Arrays.asList("क,च,छ,स,श,ष,क़".split(",")));
        en_kok_map.put("d", Arrays.asList("ड,ड़,ढ,ढ़,द,ध,ज".split(",")));
        en_kok_map.put("f", Arrays.asList("फ,फ़".split(",")));
        en_kok_map.put("g", Arrays.asList("ग,घ,ङ,ज,ग़".split(",")));
        en_kok_map.put("j", Arrays.asList("ज,झ".split(",")));
        en_kok_map.put("k", Arrays.asList("क,ख,क़,ख़".split(",")));
        en_kok_map.put("l", Arrays.asList("ल,ऌ".split(",")));
        en_kok_map.put("m", Arrays.asList("म"));
        en_kok_map.put("n", Arrays.asList("ण,न,ऩ,ञ".split(",")));
        en_kok_map.put("p", Arrays.asList("प,फ,फ़".split(",")));
        en_kok_map.put("q", Arrays.asList("क,क़".split(",")));
        en_kok_map.put("r", Arrays.asList("र,ऋ,ऱ,ढ़".split(",")));
        en_kok_map.put("s", Arrays.asList("स,ज,झ,ज़,श,ष".split(",")));
        en_kok_map.put("t", Arrays.asList("ट,ठ,त,थ,श,च".split(",")));
        en_kok_map.put("v", Arrays.asList("व"));
        en_kok_map.put("w", Arrays.asList("व"));
        en_kok_map.put("x", Arrays.asList("ज़,कस".split(",")));
        en_kok_map.put("z", Arrays.asList("ज़,ज,झ".split(",")));
        consonants_map.put(LanguageType.KOK, en_kok_map);

        //sanskrit consonants mapping
        Map<String, List<String>> en_sa_map = new HashMap<>();
        en_sa_map.put("b", Arrays.asList("ब,भ".split(",")));
        en_sa_map.put("c", Arrays.asList("क,च,छ,स,श,ष,क़".split(",")));
        en_sa_map.put("d", Arrays.asList("ड,ड़,ढ,ढ़,द,ध,ज,ळ".split(",")));
        en_sa_map.put("f", Arrays.asList("फ,फ़".split(",")));
        en_sa_map.put("g", Arrays.asList("ग,घ,ङ,ज,ग़".split(",")));
        en_sa_map.put("j", Arrays.asList("ज,झ".split(",")));
        en_sa_map.put("k", Arrays.asList("क,ख,क़,ख़".split(",")));
        en_sa_map.put("l", Arrays.asList("ल,ळ,ऌ,ऴ".split(",")));
        en_sa_map.put("m", Arrays.asList("म"));
        en_sa_map.put("n", Arrays.asList("ण,न,ऩ,ञ".split(",")));
        en_sa_map.put("p", Arrays.asList("प,फ,फ़".split(",")));
        en_sa_map.put("q", Arrays.asList("क,क़".split(",")));
        en_sa_map.put("r", Arrays.asList("र,ऋ,ऱ,ढ़".split(",")));
        en_sa_map.put("s", Arrays.asList("स,ज,झ,ज़,श,ष".split(",")));
        en_sa_map.put("t", Arrays.asList("ट,ठ,त,थ,श,च".split(",")));
        en_sa_map.put("v", Arrays.asList("व"));
        en_sa_map.put("w", Arrays.asList("व"));
        en_sa_map.put("x", Arrays.asList("ज़,कस".split(",")));
        en_sa_map.put("z", Arrays.asList("ज़,ज,झ".split(",")));
        consonants_map.put(LanguageType.SA, en_sa_map);

         //nepali consonants mapping
        Map<String, List<String>> en_ne_map = new HashMap<>();
        en_ne_map.put("b", Arrays.asList("ब,भ".split(",")));
        en_ne_map.put("c", Arrays.asList("क,च,छ,स,श,ष,क़".split(",")));
        en_ne_map.put("d", Arrays.asList("ड,ड़,ढ,ढ़,द,ध".split(",")));
        en_ne_map.put("f", Arrays.asList("फ,फ़".split(",")));
        en_ne_map.put("g", Arrays.asList("ग,घ,ज,ग़".split(",")));
        en_ne_map.put("j", Arrays.asList("ज,झ".split(",")));
        en_ne_map.put("k", Arrays.asList("क,ख,क़,ख़".split(",")));
        en_ne_map.put("l", Arrays.asList("ल,ळ,ऌ".split(",")));
        en_ne_map.put("m", Arrays.asList("म"));
        en_ne_map.put("n", Arrays.asList("ण,न,ङ".split(",")));
        en_ne_map.put("p", Arrays.asList("प,फ,फ़".split(",")));
        en_ne_map.put("q", Arrays.asList("क"));
        en_ne_map.put("r", Arrays.asList("र,ऋ,ऱ".split(",")));
        en_ne_map.put("s", Arrays.asList("स,ज,झ,ज़,श,ष".split(",")));
        en_ne_map.put("t", Arrays.asList("ट,ठ,त,थ,श,च".split(",")));
        en_ne_map.put("v", Arrays.asList("व"));
        en_ne_map.put("w", Arrays.asList("व"));
        en_ne_map.put("x", Arrays.asList("ज़,कस".split(",")));
        en_ne_map.put("z", Arrays.asList("ज़,ज,झ".split(",")));
        consonants_map.put(LanguageType.NE, en_ne_map);

        //bodo consonants mapping
        Map<String, List<String>> en_brx_map = new HashMap<>();
        en_brx_map.put("b", Arrays.asList("ब,भ".split(",")));
        en_brx_map.put("c", Arrays.asList("क,च,छ,स,श,ष,क़".split(",")));
        en_brx_map.put("d", Arrays.asList("ड,ड़,ढ,ढ़,द,ध".split(",")));
        en_brx_map.put("f", Arrays.asList("फ,फ़".split(",")));
        en_brx_map.put("g", Arrays.asList("ग,घ,ङ,ज,ग़".split(",")));
        en_brx_map.put("j", Arrays.asList("ज,झ".split(",")));
        en_brx_map.put("k", Arrays.asList("क,ख,क़,ख़".split(",")));
        en_brx_map.put("l", Arrays.asList("ल,ळ,ऌ".split(",")));
        en_brx_map.put("m", Arrays.asList("म"));
        en_brx_map.put("n", Arrays.asList("ण,न".split(",")));
        en_brx_map.put("p", Arrays.asList("प,फ,फ़".split(",")));
        en_brx_map.put("q", Arrays.asList("क"));
        en_brx_map.put("r", Arrays.asList("र,ऋ,ऱ".split(",")));
        en_brx_map.put("s", Arrays.asList("स,ज,झ,श,ष,च,छ".split(",")));
        en_brx_map.put("t", Arrays.asList("ट,ठ,त,थ,श,च".split(",")));
        en_brx_map.put("v", Arrays.asList("व"));
        en_brx_map.put("w", Arrays.asList("व"));
        en_brx_map.put("x", Arrays.asList("ज़,कस".split(",")));
        en_brx_map.put("z", Arrays.asList("ज़,ज,झ".split(",")));
        consonants_map.put(LanguageType.BRX, en_brx_map);

        //dogri consonants mapping
        Map<String, List<String>> en_doi_map = new HashMap<>();
        en_doi_map.put("b", Arrays.asList("ब,भ".split(",")));
        en_doi_map.put("c", Arrays.asList("क,च,छ,स,श,ष,क़".split(",")));
        en_doi_map.put("d", Arrays.asList("ड,ड़,ढ,ढ़,द,ध".split(",")));
        en_doi_map.put("f", Arrays.asList("फ,फ़,थ़".split(",")));
        en_doi_map.put("g", Arrays.asList("ग,घ,ङ,ज,ग़".split(",")));
        en_doi_map.put("j", Arrays.asList("ज,झ".split(",")));
        en_doi_map.put("k", Arrays.asList("क,ख,क़,ख़".split(",")));
        en_doi_map.put("l", Arrays.asList("ल,ळ,ऌ".split(",")));
        en_doi_map.put("m", Arrays.asList("म"));
        en_doi_map.put("n", Arrays.asList("ण,न".split(",")));
        en_doi_map.put("p", Arrays.asList("प,फ,फ़".split(",")));
        en_doi_map.put("q", Arrays.asList("क"));
        en_doi_map.put("r", Arrays.asList("र,ऋ,ऱ,ढ़,ड़".split(",")));
        en_doi_map.put("s", Arrays.asList("स,झ,ज़,श,ष,फ़".split(",")));
        en_doi_map.put("t", Arrays.asList("ट,ठ,त,थ,श,च".split(",")));
        en_doi_map.put("v", Arrays.asList("व"));
        en_doi_map.put("w", Arrays.asList("व"));
        en_doi_map.put("x", Arrays.asList("ज़,कस".split(",")));
        en_doi_map.put("z", Arrays.asList("ज़,ज,झ".split(",")));
        consonants_map.put(LanguageType.DOI, en_doi_map);

        //kashmiri consonants mapping
        Map<String, List<String>> en_ks_map = new HashMap<>();
        en_ks_map.put("b", Arrays.asList("ब,भ".split(",")));
        en_ks_map.put("c", Arrays.asList("क,च,छ,स,श,ष,क़".split(",")));
        en_ks_map.put("d", Arrays.asList("ड,ड़,ढ,ढ़,द,ध,ज,ळ".split(",")));
        en_ks_map.put("f", Arrays.asList("फ,फ़".split(",")));
        en_ks_map.put("g", Arrays.asList("ग,घ,ङ,ज,ग़".split(",")));
        en_ks_map.put("j", Arrays.asList("ज,झ".split(",")));
        en_ks_map.put("k", Arrays.asList("क,ख,क़,ख़".split(",")));
        en_ks_map.put("l", Arrays.asList("ल,ळ,ऌ,ऴ".split(",")));
        en_ks_map.put("m", Arrays.asList("म"));
        en_ks_map.put("n", Arrays.asList("ण,न,ऩ,ञ".split(",")));
        en_ks_map.put("p", Arrays.asList("प,फ,फ़".split(",")));
        en_ks_map.put("q", Arrays.asList("क,क़".split(",")));
        en_ks_map.put("r", Arrays.asList("र,ऋ,ऱ,ढ़".split(",")));
        en_ks_map.put("s", Arrays.asList("स,ज,झ,ज़,श,ष".split(",")));
        en_ks_map.put("t", Arrays.asList("ट,ठ,त,थ,श,च".split(",")));
        en_ks_map.put("v", Arrays.asList("व"));
        en_ks_map.put("w", Arrays.asList("व"));
        en_ks_map.put("x", Arrays.asList("ज़,कस".split(",")));
        en_ks_map.put("z", Arrays.asList("ज़,ज,झ".split(",")));
        consonants_map.put(LanguageType.KS, en_ks_map);

        //gujarati consonants mapping
        Map<String, List<String>> en_gu_map = new HashMap<>();
        en_gu_map.put("b", Arrays.asList("બ,ભ".split(",")));
        en_gu_map.put("c", Arrays.asList("ક,ચ,છ,સ,શ,ષ".split(",")));
        en_gu_map.put("d", Arrays.asList("ડ,ઢ,દ,ધ,ળ".split(",")));
        en_gu_map.put("f", Arrays.asList("ફ".split(",")));
        en_gu_map.put("g", Arrays.asList("ગ,ઘ,જ".split(",")));
        en_gu_map.put("j", Arrays.asList("જ,ઝ".split(",")));
        en_gu_map.put("k", Arrays.asList("ક,ખ".split(",")));
        en_gu_map.put("l", Arrays.asList("લ,ળ".split(",")));
        en_gu_map.put("m", Arrays.asList("મ"));
        en_gu_map.put("n", Arrays.asList("ન,ણ".split(",")));
        en_gu_map.put("p", Arrays.asList("પ,ફ".split(",")));
        en_gu_map.put("q", Arrays.asList("ક,ખ".split(",")));
        en_gu_map.put("r", Arrays.asList("ર,ઋ".split(",")));
        en_gu_map.put("s", Arrays.asList("શ,ષ,સ,ઝ".split(",")));
        en_gu_map.put("t", Arrays.asList("ચ,થ,ત,ઠ,ટ,શ".split(",")));
        en_gu_map.put("v", Arrays.asList("વ"));
        en_gu_map.put("w", Arrays.asList("વ"));
        en_gu_map.put("x", Arrays.asList("કસ,કશ,કષ,ઝ".split(",")));
        en_gu_map.put("z", Arrays.asList("ઝ,ૹ,જ".split(",")));
        consonants_map.put(LanguageType.GU, en_gu_map);

        //punjabi consonants mapping
        Map<String, List<String>> en_pa_map = new HashMap<>();
        en_pa_map.put("b", Arrays.asList("ਬ,ਭ,ਤ".split(",")));
        en_pa_map.put("c", Arrays.asList("ਚ,ਛ,ਕ,ਸ,ਸ਼".split(",")));
        en_pa_map.put("d", Arrays.asList("ਡ,ਢ,ਦ,ਧ,ੜ".split(",")));
        en_pa_map.put("f", Arrays.asList("ਫ਼,ਫ".split(",")));
        en_pa_map.put("g", Arrays.asList("ਗ,ਘ,ਙ,ਝ,ਗ਼,ਜ".split(",")));
        en_pa_map.put("j", Arrays.asList("ਜ,ਝ,ਞ,ਙ".split(",")));
        en_pa_map.put("k", Arrays.asList("ਕ,ਖ,ਖ਼".split(",")));
        en_pa_map.put("l", Arrays.asList("ਲ,ਲ਼".split(",")));
        en_pa_map.put("m", Arrays.asList("ਮ"));
        en_pa_map.put("n", Arrays.asList("ਣ,ਨ,ਙ".split(",")));
        en_pa_map.put("p", Arrays.asList("ਫ,ਪ".split(",")));
        en_pa_map.put("q", Arrays.asList("ਕ,ਖ".split(",")));
        en_pa_map.put("r", Arrays.asList("ਰ,ੜ,ੲ,ੳ".split(",")));
        en_pa_map.put("s", Arrays.asList("ਸ,ਸ਼,ਜ,ਛ".split(",")));
        en_pa_map.put("t", Arrays.asList("ਟ,ਠ,ਤ,ਥ,ਚ,ਸ਼".split(",")));
        en_pa_map.put("v", Arrays.asList("ਵ"));
        en_pa_map.put("w", Arrays.asList("ਵ"));
        en_pa_map.put("x", Arrays.asList("ਕਸ,ਕਸ਼,ਜ਼".split(",")));
        en_pa_map.put("z", Arrays.asList("ਜ਼,ਜ,ਝ".split(",")));
        consonants_map.put(LanguageType.PA, en_pa_map);

        //bengali consonants mapping
        Map<String, List<String>> en_bn_map = new HashMap<>();
        en_bn_map.put("b", Arrays.asList("ব,ভ".split(",")));
        en_bn_map.put("c", Arrays.asList("চ,ছ,স,ক".split(",")));
        en_bn_map.put("d", Arrays.asList("ড,ঢ,দ,ধ".split(",")));
        en_bn_map.put("f", Arrays.asList("প,ফ".split(",")));
        en_bn_map.put("g", Arrays.asList("গ,ঘ,জ".split(",")));
        en_bn_map.put("j", Arrays.asList("জ,ঝ,য".split(",")));
        en_bn_map.put("k", Arrays.asList("ক,খ".split(",")));
        en_bn_map.put("l", Arrays.asList("ল".split(",")));
        en_bn_map.put("m", Arrays.asList("ম"));
        en_bn_map.put("n", Arrays.asList("ঙ,ঞ,ণ,ন".split(",")));
        en_bn_map.put("p", Arrays.asList("প,ফ".split(",")));
        en_bn_map.put("q", Arrays.asList("ক".split(",")));
        en_bn_map.put("r", Arrays.asList("র,ড়,ঢ়,ৰ,ঋ".split(",")));
        en_bn_map.put("s", Arrays.asList("শ,ষ,স".split(",")));
        en_bn_map.put("t", Arrays.asList("ট,ঠ,ত,থ,ৎ,ব".split(",")));
        en_bn_map.put("v", Arrays.asList("ব,ভ,ৱ"));
        en_bn_map.put("w", Arrays.asList("ব,ভ,ৱ"));
        en_bn_map.put("x", Arrays.asList("কশ,কস,কষ".split(",")));
        en_bn_map.put("z", Arrays.asList("জ,ঝ".split(",")));
        consonants_map.put(LanguageType.BN, en_bn_map);
        consonants_map.put(LanguageType.AS, en_bn_map);

        //oriya consonants mapping
        Map<String, List<String>> en_or_map = new HashMap<>();
        en_or_map.put("b", Arrays.asList("ବ,ଭ,ଵ".split(",")));
        en_or_map.put("c", Arrays.asList("କ,ଚ,ଛ,ଶ,ଷ,ସ".split(",")));
        en_or_map.put("d", Arrays.asList("ଡ,ଢ,ଦ,ଧ,ଡ଼,ଢ଼".split(",")));
        en_or_map.put("f", Arrays.asList("ଫ"));
        en_or_map.put("g", Arrays.asList("ଗ,ଘ,ଜ".split(",")));
        en_or_map.put("j", Arrays.asList("ଜ,ଝ,ଯ".split(",")));
        en_or_map.put("k", Arrays.asList("କ,ଖ,ଚ".split(",")));
        en_or_map.put("l", Arrays.asList("ଲ,ଳ".split(",")));
        en_or_map.put("m", Arrays.asList("ମ"));
        en_or_map.put("n", Arrays.asList("ନ,ଣ,ଞ".split(",")));
        en_or_map.put("p", Arrays.asList("ପ,ଫ".split(",")));
        en_or_map.put("q", Arrays.asList("କ"));
        en_or_map.put("r", Arrays.asList("ଋ,ର,ଡ଼,ଢ଼".split(",")));
        en_or_map.put("s", Arrays.asList("ଶ,ଷ,ସ,ଜ,ଝ".split(",")));
        en_or_map.put("t", Arrays.asList("ଟ,ଥ,ଠ,ତ,ଛ,ଶ".split(",")));
        en_or_map.put("v", Arrays.asList("ଵ"));
        en_or_map.put("w", Arrays.asList("ଵ"));
        en_or_map.put("x", Arrays.asList("କସ,କଷ,ଝ".split(",")));
        en_or_map.put("z", Arrays.asList("ଝ,ଜ".split(",")));
        consonants_map.put(LanguageType.BN, en_or_map);

        // Tamil consonant mapping
        Map<String, List<String>> en_ta_map = new HashMap<>();
        en_ta_map.put("b", Arrays.asList("ப".split(",")));
        en_ta_map.put("c", Arrays.asList("க,ச,ஸ".split(",")));
        en_ta_map.put("d", Arrays.asList("ட,த".split(",")));
        en_ta_map.put("f", Arrays.asList("ப".split(",")));
        en_ta_map.put("g", Arrays.asList("க,ஹ".split(",")));
        en_ta_map.put("j", Arrays.asList("ஜ".split(",")));
        en_ta_map.put("k", Arrays.asList("க".split(",")));
        en_ta_map.put("l", Arrays.asList("ல,ள,ழ".split(",")));
        en_ta_map.put("m", Arrays.asList("ம"));
        en_ta_map.put("n", Arrays.asList("ண,ந,ன".split(",")));
        en_ta_map.put("p", Arrays.asList("ப".split(",")));
        en_ta_map.put("q", Arrays.asList("க".split(",")));
        en_ta_map.put("r", Arrays.asList("ர".split(",")));
        en_ta_map.put("s", Arrays.asList("ச,ஶ,ஷ,ஸ".split(",")));
        en_ta_map.put("t", Arrays.asList("ட,த".split(",")));
        en_ta_map.put("v", Arrays.asList("வ"));
        en_ta_map.put("w", Arrays.asList("வ"));
        en_ta_map.put("x", Arrays.asList("கஸ,கஶ,கஷ".split(",")));
        en_ta_map.put("z", Arrays.asList("ழ,ஸ,ச".split(",")));
        consonants_map.put(LanguageType.TA, en_ta_map);

        // Malayalam consonant mapping
        Map<String, List<String>> en_ml_map = new HashMap<>();
        en_ml_map.put("b", Arrays.asList("ബ,ഭ".split(",")));
        en_ml_map.put("c", Arrays.asList("ൿ,ക,ച,ഛ".split(",")));
        en_ml_map.put("d", Arrays.asList("ട,ഡ,ഢ,ഥ,ദ,ധ,ഠ".split(",")));
        en_ml_map.put("f", Arrays.asList("ഫ".split(",")));
        en_ml_map.put("g", Arrays.asList("ഖ,ഗ,ഘ,ക".split(",")));
        en_ml_map.put("j", Arrays.asList("ജ,ഝ,സ".split(",")));
        en_ml_map.put("k", Arrays.asList("ക,ഖ,ഗ,ഘ".split(",")));
        en_ml_map.put("l", Arrays.asList("ഌ,ൽ,ൾ,ല,ള".split(",")));
        en_ml_map.put("m", Arrays.asList("മ"));
        en_ml_map.put("n", Arrays.asList("ൺ,ൻ,ണ,ന".split(",")));
        en_ml_map.put("p", Arrays.asList("പ,ഫ".split(",")));
        en_ml_map.put("q", Arrays.asList("ക".split(",")));
        en_ml_map.put("r", Arrays.asList("ഋ,ർ,ര,റ".split(",")));
        en_ml_map.put("s", Arrays.asList("ശ,ഷ,സ".split(",")));
        en_ml_map.put("t", Arrays.asList("ട,ഠ,ത,ഥ,ഢ".split(",")));
        en_ml_map.put("v", Arrays.asList("വ"));
        en_ml_map.put("w", Arrays.asList("വ"));
        en_ml_map.put("x", Arrays.asList("കസ".split(",")));
        en_ml_map.put("z", Arrays.asList("ഴ,സ,ജ,ഝ".split(",")));
        consonants_map.put(LanguageType.ML, en_ml_map);

        // Kannada consonant mapping
        Map<String, List<String>> en_kn_map = new HashMap<>();
        en_kn_map.put("b", Arrays.asList("ಬ,ಭ".split(",")));
        en_kn_map.put("c", Arrays.asList("ಕ,ಚ,ಛ,ಶ,ಷ,ಸ".split(",")));
        en_kn_map.put("d", Arrays.asList("ಡ,ಢ,ದ,ಧ".split(",")));
        en_kn_map.put("f", Arrays.asList("ಫ".split(",")));
        en_kn_map.put("g", Arrays.asList("ಗ,ಘ,ಙ,ಜ".split(",")));
        en_kn_map.put("j", Arrays.asList("ಜ,ಝ".split(",")));
        en_kn_map.put("k", Arrays.asList("ಕ,ಖ".split(",")));
        en_kn_map.put("l", Arrays.asList("ಲ,ಳ,ಌ".split(",")));
        en_kn_map.put("m", Arrays.asList("ಮ"));
        en_kn_map.put("n", Arrays.asList("ಣ,ನ".split(",")));
        en_kn_map.put("p", Arrays.asList("ಪ,ಫ".split(",")));
        en_kn_map.put("q", Arrays.asList("ಕ".split(",")));
        en_kn_map.put("r", Arrays.asList("ೠ,ರ,ಱ,ಋ".split(",")));
        en_kn_map.put("s", Arrays.asList("ಶ,ಷ,ಸ,ಜ,ಝ".split(",")));
        en_kn_map.put("t", Arrays.asList("ಟ,ಠ,ತ,ಥ,ಶ,ಷ,ಚ,ದ".split(",")));
        en_kn_map.put("v", Arrays.asList("ವ"));
        en_kn_map.put("w", Arrays.asList("ವ"));
        en_kn_map.put("x", Arrays.asList("ಕಸ".split(",")));
        en_kn_map.put("z", Arrays.asList("ಜ,ಝ".split(",")));
        consonants_map.put(LanguageType.KN, en_kn_map);

        // Telugu consonant mapping
        Map<String, List<String>> en_te_map = new HashMap<>();
        en_te_map.put("b", Arrays.asList("బ,భ".split(",")));
        en_te_map.put("c", Arrays.asList("క,చ,ఛ,ಶ,ಷ,ಸ".split(",")));
        en_te_map.put("d", Arrays.asList("డ,ఢ,ద,ధ".split(",")));
        en_te_map.put("f", Arrays.asList("ఫ".split(",")));
        en_te_map.put("g", Arrays.asList("గ,ఘ,ఙ,జ".split(",")));
        en_te_map.put("j", Arrays.asList("జ,ఝ".split(",")));
        en_te_map.put("k", Arrays.asList("క,ఖ".split(",")));
        en_te_map.put("l", Arrays.asList("ల,ళ,,ఌ".split(",")));
        en_te_map.put("m", Arrays.asList("మ"));
        en_te_map.put("n", Arrays.asList("ణ,న".split(",")));
        en_te_map.put("p", Arrays.asList("ప,ఫ".split(",")));
        en_te_map.put("q", Arrays.asList("క".split(",")));
        en_te_map.put("r", Arrays.asList("ఋ,ర,ఱ,ౠ".split(",")));
        en_te_map.put("s", Arrays.asList("శ,ష,స,జ,ఝ".split(",")));
        en_te_map.put("t", Arrays.asList("ట,ఠ,త,థ,శ,ష,చ,ద".split(",")));
        en_te_map.put("v", Arrays.asList("వ"));
        en_te_map.put("w", Arrays.asList("వ"));
        en_te_map.put("x", Arrays.asList("కస".split(",")));
        en_te_map.put("z", Arrays.asList("జ,ఝ".split(",")));
        consonants_map.put(LanguageType.TE, en_te_map);
    }

    public static void main(String[] args) throws IOException
    {
        String Lang = "MAI";
        String indic_word = "समस्तवेदार्थसाससंग्रहात्मिकेतिसमस्तवेदार्थसाससंग्रहात्मिकेतिसमस्तवेदार्थसाससंग्रहात्मिकेतिसमस्तवेदार्थसाससंग्रहात्मिकेति";
        String eng_word = "samastvedarthsahsasangrahtmiketisamastvedarthsahsasangrahtmiketisamastvedarthsahsasangrahtmiketisamastvedarthsahsasangrahtmiketi";
        System.out.println(Validate_Xlit(Lang,indic_word.toLowerCase(),eng_word.toLowerCase()));
    }
    public static boolean Validate_Xlit(String Lang, String indic_word, String eng_word) throws IOException
    {
        init();
        int base = lang_base.get(LanguageType.valueOf(Lang));
        List<String> indic_vowels = vowel_map.get(LanguageType.valueOf(Lang));
        List<String> indic_stop_list = stop_list.get(LanguageType.valueOf(Lang));
        Map <String, List<String>> eng_indic_map = consonants_map.get(LanguageType.valueOf(Lang));

        //ml nad ta - !u as end char and !y as first char.
        if (base == 3328 || base == 2944 || base == 3200 || base == 3072)
        {
            if(eng_word.charAt(eng_word.length() - 1) != 'u' && eng_vowels.contains(Character.toString(eng_word.charAt(eng_word.length() - 1))) && eng_word.charAt(eng_word.length() - 1) != 'a' && eng_word.charAt(eng_word.length() - 1) != 'e' && !(indic_vowels.contains(Character.toString(indic_word.charAt(indic_word.length() - 1)))) && indic_word.charAt(indic_word.length() - 1) != (char)(base + 47) && indic_word.charAt(indic_word.length() - 1) != (char)(base + 3))
            {
                return false;
            }
            if(eng_word.charAt(0) != 'y' && !(eng_vowels.contains(Character.toString(eng_word.charAt(0)))) && indic_vowels.contains(Character.toString(indic_word.charAt(0))))
            {
                return false;
            }
        }
        //bn - !o(111), !'ga' in bn.
        else if(base == 2432)
        {
            if(eng_vowels.contains(Character.toString(eng_word.charAt(eng_word.length() - 1))) && eng_word.charAt(eng_word.length() - 1) != 'a' && eng_word.charAt(eng_word.length() - 1) != 'e' && eng_word.charAt(eng_word.length() - 1) != 'o' && !(indic_vowels.contains(Character.toString(indic_word.charAt(indic_word.length() - 1)))) && indic_word.charAt(indic_word.length() - 1) != (char)(base+47) && indic_word.charAt(indic_word.length() - 1) != (char)(base + 23) && (indic_word.charAt(indic_word.length() - 1) != (char)(base + 60)))
            {
                return false;
            }
        }
        else if(base == 2688)
        {
            if(eng_vowels.contains(Character.toString(eng_word.charAt(eng_word.length() - 1))) && eng_word.charAt(eng_word.length() - 1) != 'a' && eng_word.charAt(eng_word.length() - 1) != 'e' && !(indic_vowels.contains(Character.toString(indic_word.charAt(indic_word.length() - 1)))) && indic_word.charAt(indic_word.length() - 1) != (char)(base + 47) && indic_word.charAt(indic_word.length() - 1) != (char)(base + 60) && indic_word.charAt(indic_word.length() - 1) != (char)(2690))
            {
                return false;
            }
        }
        else
        {
            //!a(97), !e(101), !'य'(47), !nuqta(60) as end char.
            if(eng_vowels.contains(Character.toString(eng_word.charAt(eng_word.length() - 1))) && eng_word.charAt(eng_word.length() - 1) != 'a' && eng_word.charAt(eng_word.length() - 1) != 'e' && !(indic_vowels.contains(Character.toString(indic_word.charAt(indic_word.length() - 1)))) && indic_word.charAt(indic_word.length() - 1) != (char)(base + 47) && indic_word.charAt(indic_word.length() - 1) != (char)(base + 60))
            {
                return false;
            }
        }
        //!w(119) as end char, or char not in stop list.
        if(eng_word.charAt(eng_word.length() - 1) != 'w' && !(eng_vowels.contains(Character.toString(eng_word.charAt(eng_word.length() - 1)))) && indic_vowels.contains(Character.toString(indic_word.charAt(indic_word.length() - 1))) && !(eng_stop_list.contains(Character.toString(eng_word.charAt(eng_word.length() - 1)))))
        {
            return false;
        }
        if(eng_vowels.contains(Character.toString(eng_word.charAt(0))) && !(indic_vowels.contains(Character.toString(indic_word.charAt(0)))) && indic_word.charAt(0) != (char)(base + 47))
        {
            return false;
        }
        if(base != 3328 && base != 2944 && !(eng_vowels.contains(Character.toString(eng_word.charAt(0)))) && indic_vowels.contains(Character.toString(indic_word.charAt(0))))
        {
            return false;
        }

        eng_word = eng_word.replaceAll("[aeiouhy\'’]", "");

        ArrayList<String> indic_word_new = new ArrayList<String>();
        indic_word_new.add(0, "");

        for(int i = 0; i < indic_word.length(); i++)
        {
            char spelling = indic_word.charAt(i);
            if(spelling == (char)(base + 0) || spelling == (char)(base + 1) || spelling == (char)(base + 2) || spelling == (char)(3328) || spelling == (char)(3076) || spelling == (char)(2672)) // Nasalisation, te - 3072 + 4, ml - 3328 + 0, pa - 2560 + 112.
            {
                int temp = indic_word_new.size();
                int temp2 = indic_word_new.size();
                for(int j = 0; j < temp2; j++)
                {
                    if (base == 2432)
                    {
                        indic_word_new.add(temp, indic_word_new.get(j) + (char)(base + 40) + (char)(base + 23)); // "Ng" for Bengali.
                        indic_word_new.add(temp + 1, indic_word_new.get(j) + (char)(base + 46));
                        indic_word_new.add(temp + 2, indic_word_new.get(j) + (char)(base + 40));
                        temp += 3;
                    }
                    else
                    {
                        indic_word_new.add(temp, indic_word_new.get(j) + (char)(base + 46));
                        indic_word_new.add(temp + 1, indic_word_new.get(j) + (char)(base + 40));
                        temp += 2;
                    }
                }

            }
            else if(spelling == (char)(base + 67) || spelling == (char)(base + 68)) // "Ra" addition.
             {
                for(int j = 0; j < indic_word_new.size(); j++)
                {
                    indic_word_new.set(j, indic_word_new.get(j) + (char)(base + 48));
                }
            }
            else if((base == 3328 || base == 3200 || base == 3072) && (spelling == (char)(base + 97) || spelling == (char)(base + 98) || spelling == (char)(base + 99))) // "Ll" addition for Malayalam, Telugu, Kannada.
            {
                for(int j = 0; j < indic_word_new.size(); j++)
                {
                    indic_word_new.set(j, indic_word_new.get(j) + (char)(base + 50));
                }
            }
            else if(base == 3328 && spelling == (char)(base + 25)) // "Ng" addition for Malayalam.
            {
                int temp = indic_word_new.size();
                int temp2 = indic_word_new.size();
                for(int j = 0; j < temp2; j++)
                {
                    indic_word_new.add(temp, indic_word_new.get(j) + (char)(base + 40) + (char)(base + 23));
                    indic_word_new.add(temp + 1, indic_word_new.get(j) + (char)(base + 40));
                    temp += 2;
                }
            }
            else if(base == 2944 && spelling == (char)(base + 25)) // "Ng" addition for Tamil.
            {
                int temp = indic_word_new.size();
                int temp2 = indic_word_new.size();
                for(int j = 0; j < temp2; j++)
                {
                    indic_word_new.add(temp, indic_word_new.get(j) + (char)(base + 40)  + (char)(base + 21));
                    indic_word_new.add(temp + 1, indic_word_new.get(j) + (char)(base + 40));
                    temp += 2;
                }
            }
            else if(spelling == (char)(base + 30)) // "Nj" addition for Tamil and Malayalam, "Nya" for all other languages.
            {
                int temp = indic_word_new.size();
                int temp2 = indic_word_new.size();
                for(int j = 0; j < temp2; j++)
                {
                    if((base == 3328 || base == 2944))
                    {
                        indic_word_new.add(temp, indic_word_new.get(j) + (char)(base + 40) + (char)(base + 28));
                        indic_word_new.add(temp + 1, indic_word_new.get(j) + (char)(base + 40));
                        temp += 2;
                    }
                    else
                    {
                        indic_word_new.add(temp, indic_word_new.get(j) + (char)(base + 40));
                        indic_word_new.add(temp + 1, indic_word_new.get(j));
                        temp += 2;
                    }
                }
            }
            else if(base == 2944 && spelling == (char)(base + 49)) // "Tra" addition for Tamil.
            {
                int temp = indic_word_new.size();
                int temp2 = indic_word_new.size();
                for(int j = 0; j < temp2; j++)
                {
                    indic_word_new.add(temp, indic_word_new.get(j) + (char)(base + 31) + (char)(base + 48));
                    indic_word_new.add(temp + 1, indic_word_new.get(j) + (char)(base + 48));
                    temp += 2;
                }
            }
            else if((spelling == (char)(base + 95) && (base == 2304 || base == 2432)) || spelling == (char)(base + 60) || spelling == (char)(base + 61) || spelling == (char)(base + 77) || (spelling == (char)(base + 113) && base != 2432) || indic_stop_list.contains(Character.toString(spelling)) || indic_vowels.contains(Character.toString(spelling))) // List of ignored characters.
            {
                continue;
            }
            else
            {
                for(int j = 0; j < indic_word_new.size(); j++)
                {
                    indic_word_new.set(j, indic_word_new.get(j) + spelling);
                }
            }
        }
        int count = 0;
        List<String> checks = new ArrayList<String>();
        List<String> prev = new ArrayList<String>();
        String[] arr = eng_word.split("");
        try
        {
          for(int i = 0; i < arr.length; i++)
          {
              if (count%10 == 0)
              {
                  for(int k = 0; k < indic_word_new.size(); k++)
                  {
                     String s = indic_word_new.get(k).substring(0, Math.min(indic_word_new.get(k).length(), count));
                     checks.add(s);
                  }
                  prev.retainAll(checks);
              }
              if(arr[i].equals(""))
              {
                  continue;
              }
              else if(i == 0){
                  List<String> temp_list = eng_indic_map.get(arr[0]);
                  prev = temp_list;
              }
              else
              {
                  List<String> temp_list = new ArrayList<String>();
                  for(String str: prev)
                  {
                      for(String mapping: eng_indic_map.get(arr[i]))
                      {
                          temp_list.add(str + mapping);
                      }
                  }
                  prev = temp_list;
              }
              count += 1;
          }
        }
        catch(Exception e)
        {
            return false;
        }
        catch(Error e)
        {
            return false;
        }
        for(int i = 0; i < indic_word_new.size(); i++)
        {
            indic_word_new.set(i, indic_word_new.get(i).replaceAll("(?i)(.)\\1+", "$1"));
        }
        if(indic_word_new.get(0) == "" && prev == null)
        {
            return true;
        }
        else if((indic_word_new.get(0) == "" && indic_word_new.size() == 1 && prev != null) || (indic_word_new.get(0) != "" && prev == null))
        {
            return false;
        }
        else
        {
            for(int i = 0; i < prev.size(); i++)
            {
                prev.set(i , prev.get(i).replaceAll("(?i)(.)\\1+", "$1"));
            }
        }
        for(int i = 0; i < indic_word_new.size(); i++)
        {
            if(prev.contains(indic_word_new.get(i)))
            {
                return true;
            }
        }
        return false;
    }
}
