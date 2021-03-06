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
        dev_vowels = Arrays.asList("???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???".split(","));
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
        gu_vowels = Arrays.asList("???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???".split(","));
        vowel_map.put(LanguageType.GU, gu_vowels);

        List<String> pa_vowels = new ArrayList<String>();
        pa_vowels = Arrays.asList("???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???".split(","));
        vowel_map.put(LanguageType.PA, pa_vowels);

        List<String> bn_vowels = new ArrayList<String>();
        bn_vowels = Arrays.asList("???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???".split(","));
        vowel_map.put(LanguageType.BN, bn_vowels);
        vowel_map.put(LanguageType.AS, bn_vowels);

        List<String> or_vowels = new ArrayList<String>();
        or_vowels = Arrays.asList("???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???,???".split(","));
        vowel_map.put(LanguageType.OR, or_vowels);

        //initialize stop lists
        List<String> dev_stop_list = new ArrayList<String>();
        dev_stop_list = Arrays.asList("???,???".split(","));
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
        gu_stop_list = Arrays.asList("???,???".split(","));
        stop_list.put(LanguageType.GU, gu_stop_list);

        List<String> pa_stop_list = new ArrayList<String>();
        pa_stop_list = Arrays.asList("???,???".split(","));
        stop_list.put(LanguageType.PA, pa_stop_list);

        List<String> bn_stop_list = new ArrayList<String>();
        bn_stop_list = Arrays.asList("???,???,???".split(","));
        stop_list.put(LanguageType.BN, bn_stop_list);
        stop_list.put(LanguageType.AS, bn_stop_list);

        List<String> or_stop_list = new ArrayList<String>();
        or_stop_list = Arrays.asList("???,???,???".split(","));
        stop_list.put(LanguageType.OR, or_stop_list);

        List<String> ta_stop_list = new ArrayList<String>();
        ta_stop_list = Arrays.asList("???,???".split(","));
        stop_list.put(LanguageType.TA, ta_stop_list);

        List<String> ml_stop_list = new ArrayList<String>();
        ml_stop_list = Arrays.asList("???,???".split(","));
        stop_list.put(LanguageType.ML, ml_stop_list);

        List<String> kn_stop_list = new ArrayList<String>();
        kn_stop_list = Arrays.asList("???,???".split(","));
        stop_list.put(LanguageType.KN, kn_stop_list);

        List<String> te_stop_list = new ArrayList<String>();
        te_stop_list = Arrays.asList("???,???".split(","));
        stop_list.put(LanguageType.TE, te_stop_list);


        //hindi consonants mapping.
        Map<String, List<String>> en_hi_map = new HashMap<>();
        en_hi_map.put("b", Arrays.asList("???,???".split(",")));
        en_hi_map.put("c", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_hi_map.put("d", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_hi_map.put("f", Arrays.asList("???,???".split(",")));
        en_hi_map.put("g", Arrays.asList("???,???,???,???,???".split(",")));
        en_hi_map.put("j", Arrays.asList("???,???".split(",")));
        en_hi_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_hi_map.put("l", Arrays.asList("???,???,???".split(",")));
        en_hi_map.put("m", Arrays.asList("???"));
        en_hi_map.put("n", Arrays.asList("???,???".split(",")));
        en_hi_map.put("p", Arrays.asList("???,???,???".split(",")));
        en_hi_map.put("q", Arrays.asList("???".split(",")));
        en_hi_map.put("r", Arrays.asList("???,???,???".split(",")));
        en_hi_map.put("s", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_hi_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_hi_map.put("v", Arrays.asList("???"));
        en_hi_map.put("w", Arrays.asList("???"));
        en_hi_map.put("x", Arrays.asList("???,??????".split(",")));
        en_hi_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.HI, en_hi_map);

        //marathi consonants mapping.
        Map<String, List<String>> en_mr_map = new HashMap<>();
        en_mr_map.put("b", Arrays.asList("???,???".split(",")));
        en_mr_map.put("c", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_mr_map.put("d", Arrays.asList("???,???,???,???,???,???,???,???".split(",")));
        en_mr_map.put("f", Arrays.asList("???,???".split(",")));
        en_mr_map.put("g", Arrays.asList("???,???,???,???,???".split(",")));
        en_mr_map.put("j", Arrays.asList("???,???".split(",")));
        en_mr_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_mr_map.put("l", Arrays.asList("???,???,???,???".split(",")));
        en_mr_map.put("m", Arrays.asList("???"));
        en_mr_map.put("n", Arrays.asList("???,???,???,???".split(",")));
        en_mr_map.put("p", Arrays.asList("???,???,???".split(",")));
        en_mr_map.put("q", Arrays.asList("???,???".split(",")));
        en_mr_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_mr_map.put("s", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_mr_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_mr_map.put("v", Arrays.asList("???"));
        en_mr_map.put("w", Arrays.asList("???"));
        en_mr_map.put("x", Arrays.asList("???,??????".split(",")));
        en_mr_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.MR, en_mr_map);

        //maithili consonants mapping.
        Map<String, List<String>> en_mai_map = new HashMap<>();
        en_mai_map.put("b", Arrays.asList("???,???".split(",")));
        en_mai_map.put("c", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_mai_map.put("d", Arrays.asList("???,???,???,???,???,???,???,???".split(",")));
        en_mai_map.put("f", Arrays.asList("???,???".split(",")));
        en_mai_map.put("g", Arrays.asList("???,???,???,???,???".split(",")));
        en_mai_map.put("j", Arrays.asList("???,???".split(",")));
        en_mai_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_mai_map.put("l", Arrays.asList("???,???,???,???".split(",")));
        en_mai_map.put("m", Arrays.asList("???"));
        en_mai_map.put("n", Arrays.asList("???,???,???,???".split(",")));
        en_mai_map.put("p", Arrays.asList("???,???,???".split(",")));
        en_mai_map.put("q", Arrays.asList("???,???".split(",")));
        en_mai_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_mai_map.put("s", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_mai_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_mai_map.put("v", Arrays.asList("???"));
        en_mai_map.put("w", Arrays.asList("???"));
        en_mai_map.put("x", Arrays.asList("???,??????".split(",")));
        en_mai_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.MAI, en_mai_map);

        //kokani consonants mapping
        Map<String, List<String>> en_kok_map = new HashMap<>();
        en_kok_map.put("b", Arrays.asList("???,???".split(",")));
        en_kok_map.put("c", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_kok_map.put("d", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_kok_map.put("f", Arrays.asList("???,???".split(",")));
        en_kok_map.put("g", Arrays.asList("???,???,???,???,???".split(",")));
        en_kok_map.put("j", Arrays.asList("???,???".split(",")));
        en_kok_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_kok_map.put("l", Arrays.asList("???,???".split(",")));
        en_kok_map.put("m", Arrays.asList("???"));
        en_kok_map.put("n", Arrays.asList("???,???,???,???".split(",")));
        en_kok_map.put("p", Arrays.asList("???,???,???".split(",")));
        en_kok_map.put("q", Arrays.asList("???,???".split(",")));
        en_kok_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_kok_map.put("s", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_kok_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_kok_map.put("v", Arrays.asList("???"));
        en_kok_map.put("w", Arrays.asList("???"));
        en_kok_map.put("x", Arrays.asList("???,??????".split(",")));
        en_kok_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.KOK, en_kok_map);

        //sanskrit consonants mapping
        Map<String, List<String>> en_sa_map = new HashMap<>();
        en_sa_map.put("b", Arrays.asList("???,???".split(",")));
        en_sa_map.put("c", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_sa_map.put("d", Arrays.asList("???,???,???,???,???,???,???,???".split(",")));
        en_sa_map.put("f", Arrays.asList("???,???".split(",")));
        en_sa_map.put("g", Arrays.asList("???,???,???,???,???".split(",")));
        en_sa_map.put("j", Arrays.asList("???,???".split(",")));
        en_sa_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_sa_map.put("l", Arrays.asList("???,???,???,???".split(",")));
        en_sa_map.put("m", Arrays.asList("???"));
        en_sa_map.put("n", Arrays.asList("???,???,???,???".split(",")));
        en_sa_map.put("p", Arrays.asList("???,???,???".split(",")));
        en_sa_map.put("q", Arrays.asList("???,???".split(",")));
        en_sa_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_sa_map.put("s", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_sa_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_sa_map.put("v", Arrays.asList("???"));
        en_sa_map.put("w", Arrays.asList("???"));
        en_sa_map.put("x", Arrays.asList("???,??????".split(",")));
        en_sa_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.SA, en_sa_map);

         //nepali consonants mapping
        Map<String, List<String>> en_ne_map = new HashMap<>();
        en_ne_map.put("b", Arrays.asList("???,???".split(",")));
        en_ne_map.put("c", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_ne_map.put("d", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_ne_map.put("f", Arrays.asList("???,???".split(",")));
        en_ne_map.put("g", Arrays.asList("???,???,???,???".split(",")));
        en_ne_map.put("j", Arrays.asList("???,???".split(",")));
        en_ne_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_ne_map.put("l", Arrays.asList("???,???,???".split(",")));
        en_ne_map.put("m", Arrays.asList("???"));
        en_ne_map.put("n", Arrays.asList("???,???,???".split(",")));
        en_ne_map.put("p", Arrays.asList("???,???,???".split(",")));
        en_ne_map.put("q", Arrays.asList("???"));
        en_ne_map.put("r", Arrays.asList("???,???,???".split(",")));
        en_ne_map.put("s", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_ne_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_ne_map.put("v", Arrays.asList("???"));
        en_ne_map.put("w", Arrays.asList("???"));
        en_ne_map.put("x", Arrays.asList("???,??????".split(",")));
        en_ne_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.NE, en_ne_map);

        //bodo consonants mapping
        Map<String, List<String>> en_brx_map = new HashMap<>();
        en_brx_map.put("b", Arrays.asList("???,???".split(",")));
        en_brx_map.put("c", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_brx_map.put("d", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_brx_map.put("f", Arrays.asList("???,???".split(",")));
        en_brx_map.put("g", Arrays.asList("???,???,???,???,???".split(",")));
        en_brx_map.put("j", Arrays.asList("???,???".split(",")));
        en_brx_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_brx_map.put("l", Arrays.asList("???,???,???".split(",")));
        en_brx_map.put("m", Arrays.asList("???"));
        en_brx_map.put("n", Arrays.asList("???,???".split(",")));
        en_brx_map.put("p", Arrays.asList("???,???,???".split(",")));
        en_brx_map.put("q", Arrays.asList("???"));
        en_brx_map.put("r", Arrays.asList("???,???,???".split(",")));
        en_brx_map.put("s", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_brx_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_brx_map.put("v", Arrays.asList("???"));
        en_brx_map.put("w", Arrays.asList("???"));
        en_brx_map.put("x", Arrays.asList("???,??????".split(",")));
        en_brx_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.BRX, en_brx_map);

        //dogri consonants mapping
        Map<String, List<String>> en_doi_map = new HashMap<>();
        en_doi_map.put("b", Arrays.asList("???,???".split(",")));
        en_doi_map.put("c", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_doi_map.put("d", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_doi_map.put("f", Arrays.asList("???,???,??????".split(",")));
        en_doi_map.put("g", Arrays.asList("???,???,???,???,???".split(",")));
        en_doi_map.put("j", Arrays.asList("???,???".split(",")));
        en_doi_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_doi_map.put("l", Arrays.asList("???,???,???".split(",")));
        en_doi_map.put("m", Arrays.asList("???"));
        en_doi_map.put("n", Arrays.asList("???,???".split(",")));
        en_doi_map.put("p", Arrays.asList("???,???,???".split(",")));
        en_doi_map.put("q", Arrays.asList("???"));
        en_doi_map.put("r", Arrays.asList("???,???,???,???,??????".split(",")));
        en_doi_map.put("s", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_doi_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_doi_map.put("v", Arrays.asList("???"));
        en_doi_map.put("w", Arrays.asList("???"));
        en_doi_map.put("x", Arrays.asList("???,??????".split(",")));
        en_doi_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.DOI, en_doi_map);

        //kashmiri consonants mapping
        Map<String, List<String>> en_ks_map = new HashMap<>();
        en_ks_map.put("b", Arrays.asList("???,???".split(",")));
        en_ks_map.put("c", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_ks_map.put("d", Arrays.asList("???,???,???,???,???,???,???,???".split(",")));
        en_ks_map.put("f", Arrays.asList("???,???".split(",")));
        en_ks_map.put("g", Arrays.asList("???,???,???,???,???".split(",")));
        en_ks_map.put("j", Arrays.asList("???,???".split(",")));
        en_ks_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_ks_map.put("l", Arrays.asList("???,???,???,???".split(",")));
        en_ks_map.put("m", Arrays.asList("???"));
        en_ks_map.put("n", Arrays.asList("???,???,???,???".split(",")));
        en_ks_map.put("p", Arrays.asList("???,???,???".split(",")));
        en_ks_map.put("q", Arrays.asList("???,???".split(",")));
        en_ks_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_ks_map.put("s", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_ks_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_ks_map.put("v", Arrays.asList("???"));
        en_ks_map.put("w", Arrays.asList("???"));
        en_ks_map.put("x", Arrays.asList("???,??????".split(",")));
        en_ks_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.KS, en_ks_map);

        //gujarati consonants mapping
        Map<String, List<String>> en_gu_map = new HashMap<>();
        en_gu_map.put("b", Arrays.asList("???,???".split(",")));
        en_gu_map.put("c", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_gu_map.put("d", Arrays.asList("???,???,???,???,???".split(",")));
        en_gu_map.put("f", Arrays.asList("???".split(",")));
        en_gu_map.put("g", Arrays.asList("???,???,???".split(",")));
        en_gu_map.put("j", Arrays.asList("???,???".split(",")));
        en_gu_map.put("k", Arrays.asList("???,???".split(",")));
        en_gu_map.put("l", Arrays.asList("???,???".split(",")));
        en_gu_map.put("m", Arrays.asList("???"));
        en_gu_map.put("n", Arrays.asList("???,???".split(",")));
        en_gu_map.put("p", Arrays.asList("???,???".split(",")));
        en_gu_map.put("q", Arrays.asList("???,???".split(",")));
        en_gu_map.put("r", Arrays.asList("???,???".split(",")));
        en_gu_map.put("s", Arrays.asList("???,???,???,???".split(",")));
        en_gu_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_gu_map.put("v", Arrays.asList("???"));
        en_gu_map.put("w", Arrays.asList("???"));
        en_gu_map.put("x", Arrays.asList("??????,??????,??????,???".split(",")));
        en_gu_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.GU, en_gu_map);

        //punjabi consonants mapping
        Map<String, List<String>> en_pa_map = new HashMap<>();
        en_pa_map.put("b", Arrays.asList("???,???,???".split(",")));
        en_pa_map.put("c", Arrays.asList("???,???,???,???,???".split(",")));
        en_pa_map.put("d", Arrays.asList("???,???,???,???,???".split(",")));
        en_pa_map.put("f", Arrays.asList("???,???".split(",")));
        en_pa_map.put("g", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_pa_map.put("j", Arrays.asList("???,???,???,???".split(",")));
        en_pa_map.put("k", Arrays.asList("???,???,???".split(",")));
        en_pa_map.put("l", Arrays.asList("???,???".split(",")));
        en_pa_map.put("m", Arrays.asList("???"));
        en_pa_map.put("n", Arrays.asList("???,???,???".split(",")));
        en_pa_map.put("p", Arrays.asList("???,???".split(",")));
        en_pa_map.put("q", Arrays.asList("???,???".split(",")));
        en_pa_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_pa_map.put("s", Arrays.asList("???,???,???,???".split(",")));
        en_pa_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_pa_map.put("v", Arrays.asList("???"));
        en_pa_map.put("w", Arrays.asList("???"));
        en_pa_map.put("x", Arrays.asList("??????,??????,???".split(",")));
        en_pa_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.PA, en_pa_map);

        //bengali consonants mapping
        Map<String, List<String>> en_bn_map = new HashMap<>();
        en_bn_map.put("b", Arrays.asList("???,???".split(",")));
        en_bn_map.put("c", Arrays.asList("???,???,???,???".split(",")));
        en_bn_map.put("d", Arrays.asList("???,???,???,???".split(",")));
        en_bn_map.put("f", Arrays.asList("???,???".split(",")));
        en_bn_map.put("g", Arrays.asList("???,???,???".split(",")));
        en_bn_map.put("j", Arrays.asList("???,???,???".split(",")));
        en_bn_map.put("k", Arrays.asList("???,???".split(",")));
        en_bn_map.put("l", Arrays.asList("???".split(",")));
        en_bn_map.put("m", Arrays.asList("???"));
        en_bn_map.put("n", Arrays.asList("???,???,???,???".split(",")));
        en_bn_map.put("p", Arrays.asList("???,???".split(",")));
        en_bn_map.put("q", Arrays.asList("???".split(",")));
        en_bn_map.put("r", Arrays.asList("???,???,???,???,???".split(",")));
        en_bn_map.put("s", Arrays.asList("???,???,???".split(",")));
        en_bn_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_bn_map.put("v", Arrays.asList("???,???,???"));
        en_bn_map.put("w", Arrays.asList("???,???,???"));
        en_bn_map.put("x", Arrays.asList("??????,??????,??????".split(",")));
        en_bn_map.put("z", Arrays.asList("???,???".split(",")));
        consonants_map.put(LanguageType.BN, en_bn_map);
        consonants_map.put(LanguageType.AS, en_bn_map);

        //oriya consonants mapping
        Map<String, List<String>> en_or_map = new HashMap<>();
        en_or_map.put("b", Arrays.asList("???,???,???".split(",")));
        en_or_map.put("c", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_or_map.put("d", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_or_map.put("f", Arrays.asList("???"));
        en_or_map.put("g", Arrays.asList("???,???,???".split(",")));
        en_or_map.put("j", Arrays.asList("???,???,???".split(",")));
        en_or_map.put("k", Arrays.asList("???,???,???".split(",")));
        en_or_map.put("l", Arrays.asList("???,???".split(",")));
        en_or_map.put("m", Arrays.asList("???"));
        en_or_map.put("n", Arrays.asList("???,???,???".split(",")));
        en_or_map.put("p", Arrays.asList("???,???".split(",")));
        en_or_map.put("q", Arrays.asList("???"));
        en_or_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_or_map.put("s", Arrays.asList("???,???,???,???,???".split(",")));
        en_or_map.put("t", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_or_map.put("v", Arrays.asList("???"));
        en_or_map.put("w", Arrays.asList("???"));
        en_or_map.put("x", Arrays.asList("??????,??????,???".split(",")));
        en_or_map.put("z", Arrays.asList("???,???".split(",")));
        consonants_map.put(LanguageType.BN, en_or_map);

        // Tamil consonant mapping
        Map<String, List<String>> en_ta_map = new HashMap<>();
        en_ta_map.put("b", Arrays.asList("???".split(",")));
        en_ta_map.put("c", Arrays.asList("???,???,???".split(",")));
        en_ta_map.put("d", Arrays.asList("???,???".split(",")));
        en_ta_map.put("f", Arrays.asList("???".split(",")));
        en_ta_map.put("g", Arrays.asList("???,???".split(",")));
        en_ta_map.put("j", Arrays.asList("???".split(",")));
        en_ta_map.put("k", Arrays.asList("???".split(",")));
        en_ta_map.put("l", Arrays.asList("???,???,???".split(",")));
        en_ta_map.put("m", Arrays.asList("???"));
        en_ta_map.put("n", Arrays.asList("???,???,???".split(",")));
        en_ta_map.put("p", Arrays.asList("???".split(",")));
        en_ta_map.put("q", Arrays.asList("???".split(",")));
        en_ta_map.put("r", Arrays.asList("???".split(",")));
        en_ta_map.put("s", Arrays.asList("???,???,???,???".split(",")));
        en_ta_map.put("t", Arrays.asList("???,???".split(",")));
        en_ta_map.put("v", Arrays.asList("???"));
        en_ta_map.put("w", Arrays.asList("???"));
        en_ta_map.put("x", Arrays.asList("??????,??????,??????".split(",")));
        en_ta_map.put("z", Arrays.asList("???,???,???".split(",")));
        consonants_map.put(LanguageType.TA, en_ta_map);

        // Malayalam consonant mapping
        Map<String, List<String>> en_ml_map = new HashMap<>();
        en_ml_map.put("b", Arrays.asList("???,???".split(",")));
        en_ml_map.put("c", Arrays.asList("???,???,???,???".split(",")));
        en_ml_map.put("d", Arrays.asList("???,???,???,???,???,???,???".split(",")));
        en_ml_map.put("f", Arrays.asList("???".split(",")));
        en_ml_map.put("g", Arrays.asList("???,???,???,???".split(",")));
        en_ml_map.put("j", Arrays.asList("???,???,???".split(",")));
        en_ml_map.put("k", Arrays.asList("???,???,???,???".split(",")));
        en_ml_map.put("l", Arrays.asList("???,???,???,???,???".split(",")));
        en_ml_map.put("m", Arrays.asList("???"));
        en_ml_map.put("n", Arrays.asList("???,???,???,???".split(",")));
        en_ml_map.put("p", Arrays.asList("???,???".split(",")));
        en_ml_map.put("q", Arrays.asList("???".split(",")));
        en_ml_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_ml_map.put("s", Arrays.asList("???,???,???".split(",")));
        en_ml_map.put("t", Arrays.asList("???,???,???,???,???".split(",")));
        en_ml_map.put("v", Arrays.asList("???"));
        en_ml_map.put("w", Arrays.asList("???"));
        en_ml_map.put("x", Arrays.asList("??????".split(",")));
        en_ml_map.put("z", Arrays.asList("???,???,???,???".split(",")));
        consonants_map.put(LanguageType.ML, en_ml_map);

        // Kannada consonant mapping
        Map<String, List<String>> en_kn_map = new HashMap<>();
        en_kn_map.put("b", Arrays.asList("???,???".split(",")));
        en_kn_map.put("c", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_kn_map.put("d", Arrays.asList("???,???,???,???".split(",")));
        en_kn_map.put("f", Arrays.asList("???".split(",")));
        en_kn_map.put("g", Arrays.asList("???,???,???,???".split(",")));
        en_kn_map.put("j", Arrays.asList("???,???".split(",")));
        en_kn_map.put("k", Arrays.asList("???,???".split(",")));
        en_kn_map.put("l", Arrays.asList("???,???,???".split(",")));
        en_kn_map.put("m", Arrays.asList("???"));
        en_kn_map.put("n", Arrays.asList("???,???".split(",")));
        en_kn_map.put("p", Arrays.asList("???,???".split(",")));
        en_kn_map.put("q", Arrays.asList("???".split(",")));
        en_kn_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_kn_map.put("s", Arrays.asList("???,???,???,???,???".split(",")));
        en_kn_map.put("t", Arrays.asList("???,???,???,???,???,???,???,???".split(",")));
        en_kn_map.put("v", Arrays.asList("???"));
        en_kn_map.put("w", Arrays.asList("???"));
        en_kn_map.put("x", Arrays.asList("??????".split(",")));
        en_kn_map.put("z", Arrays.asList("???,???".split(",")));
        consonants_map.put(LanguageType.KN, en_kn_map);

        // Telugu consonant mapping
        Map<String, List<String>> en_te_map = new HashMap<>();
        en_te_map.put("b", Arrays.asList("???,???".split(",")));
        en_te_map.put("c", Arrays.asList("???,???,???,???,???,???".split(",")));
        en_te_map.put("d", Arrays.asList("???,???,???,???".split(",")));
        en_te_map.put("f", Arrays.asList("???".split(",")));
        en_te_map.put("g", Arrays.asList("???,???,???,???".split(",")));
        en_te_map.put("j", Arrays.asList("???,???".split(",")));
        en_te_map.put("k", Arrays.asList("???,???".split(",")));
        en_te_map.put("l", Arrays.asList("???,???,???,???".split(",")));
        en_te_map.put("m", Arrays.asList("???"));
        en_te_map.put("n", Arrays.asList("???,???".split(",")));
        en_te_map.put("p", Arrays.asList("???,???".split(",")));
        en_te_map.put("q", Arrays.asList("???".split(",")));
        en_te_map.put("r", Arrays.asList("???,???,???,???".split(",")));
        en_te_map.put("s", Arrays.asList("???,???,???,???,???".split(",")));
        en_te_map.put("t", Arrays.asList("???,???,???,???,???,???,???,???".split(",")));
        en_te_map.put("v", Arrays.asList("???"));
        en_te_map.put("w", Arrays.asList("???"));
        en_te_map.put("x", Arrays.asList("??????".split(",")));
        en_te_map.put("z", Arrays.asList("???,???".split(",")));
        consonants_map.put(LanguageType.TE, en_te_map);
    }

    public static void main(String[] args) throws IOException
    {
        String Lang = "MAI";
        String indic_word = "????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????";
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
            //!a(97), !e(101), !'???'(47), !nuqta(60) as end char.
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

        eng_word = eng_word.replaceAll("[aeiouhy\'???]", "");

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
