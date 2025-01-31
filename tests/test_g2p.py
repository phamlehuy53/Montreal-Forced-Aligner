import os
import pytest
from montreal_forced_aligner.utils import get_pretrained_g2p_path
from montreal_forced_aligner.g2p.trainer import PyniniTrainer, G2P_DISABLED

from montreal_forced_aligner.config.train_g2p_config import load_basic_train_g2p_config
from montreal_forced_aligner.config.g2p_config import load_basic_g2p_config

from montreal_forced_aligner.g2p.generator import PyniniDictionaryGenerator, clean_up_word
from montreal_forced_aligner.dictionary import check_bracketed

from montreal_forced_aligner.models import G2PModel

from montreal_forced_aligner import __version__


def test_clean_up_word():
    original_word = '+abc'
    w, m = clean_up_word(original_word, ['a', 'b', 'c'])
    assert(w == 'abc')
    assert m == ['+']


def test_check_bracketed():
    """Checks if the brackets are removed correctly and handling an empty string works"""
    word_set = ['uh',  '(the)', 'sick', '<corpus>', '[a]', '{cold}', '']
    expected_result = ['uh', 'sick', '']
    assert [x for x in word_set if not check_bracketed(x)] == expected_result


def test_training(sick_dict, sick_g2p_model_path, temp_dir):
    if G2P_DISABLED:
        pytest.skip('No Pynini found')
    train_config = load_basic_train_g2p_config()
    train_config.random_starts = 1
    train_config.max_iterations = 5
    trainer = PyniniTrainer(sick_dict, sick_g2p_model_path, temp_directory=temp_dir, train_config=train_config)
    trainer.validate()

    trainer.train()
    model = G2PModel(sick_g2p_model_path, root_directory=temp_dir)
    assert model.meta['version'] == __version__
    assert model.meta['architecture'] == 'pynini'
    assert model.meta['phones'] == sick_dict.nonsil_phones


def test_generator(sick_g2p_model_path, sick_corpus, g2p_sick_output):
    if G2P_DISABLED:
        pytest.skip('No Pynini found')
    model = G2PModel(sick_g2p_model_path)

    assert not model.validate(sick_corpus.word_set)
    assert model.validate([x for x in sick_corpus.word_set if not check_bracketed(x)])
    gen = PyniniDictionaryGenerator(model, sick_corpus.word_set)
    gen.output(g2p_sick_output)
    assert os.path.exists(g2p_sick_output)

def test_generator_pretrained(english_g2p_model):
    if G2P_DISABLED:
        pytest.skip('No Pynini found')
    model_path = get_pretrained_g2p_path('english_g2p')
    model = G2PModel(model_path)
    words = ['petted', 'petted-patted', 'pedal']
    gen = PyniniDictionaryGenerator(model, words, num_pronunciations=3)
    results = gen.generate()
    print(results)
    assert len(results['petted']) == 3