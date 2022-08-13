while getopts l:i:b:n:r: module
do
    case "${module}" in
        l)lang_abr=${OPTARG};;
        i)input_file=${OPTARG};;
        b)beam=${OPTARG};;
        n)nbest=${OPTARG};;
        r)rerank=${OPTARG};;
    esac
done
bash interactive.sh $lang_abr $input_file $beam $nbest 
python3 generate_result_files.py $lang_abr $rerank
