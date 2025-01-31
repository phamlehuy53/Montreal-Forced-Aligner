import os
import pytest

from montreal_forced_aligner.command_line.adapt import run_adapt_model
from montreal_forced_aligner.command_line.mfa import parser


#@pytest.mark.skip(reason='Optimization')
def test_adapt_basic(basic_corpus_dir, sick_dict_path, generated_dir, large_dataset_dictionary, temp_dir,
                     basic_align_config, english_acoustic_model):
    adapted_model_path = os.path.join(generated_dir, 'basic_adapted.zip')
    command = ['adapt', basic_corpus_dir, large_dataset_dictionary, english_acoustic_model, adapted_model_path,
               '-t', temp_dir, '-q', '--clean', '-d']
    args, unknown = parser.parse_known_args(command)
    run_adapt_model(args, unknown)
    assert os.path.exists(adapted_model_path)

#@pytest.mark.skip(reason='Optimization')
def test_adapt_multilingual(multilingual_ipa_corpus_dir, ipa_speaker_dict_path, generated_dir, temp_dir,
                     basic_align_config, english_acoustic_model,  english_ipa_acoustic_model):
    adapted_model_path = os.path.join(generated_dir, 'multilingual_adapted.zip')
    command = ['adapt', multilingual_ipa_corpus_dir, ipa_speaker_dict_path, english_ipa_acoustic_model, adapted_model_path,
               '-t', temp_dir, '-c', basic_align_config, '-q', '--clean', '-d']
    args, unknown = parser.parse_known_args(command)
    print(args)
    run_adapt_model(args, unknown)
    assert os.path.exists(adapted_model_path)

