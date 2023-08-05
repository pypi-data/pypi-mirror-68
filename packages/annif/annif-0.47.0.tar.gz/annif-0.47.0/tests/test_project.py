"""Unit tests for projects in Annif"""

import pytest
import annif.project
import annif.backend.dummy
from annif.exception import ConfigurationException, NotSupportedException
from annif.project import Access


def test_create_project_wrong_access(app):
    with pytest.raises(ConfigurationException):
        annif.project.AnnifProject(
            'example',
            {'name': 'Example', 'language': 'en', 'access': 'invalid'},
            '.')


def test_get_project_en(app):
    with app.app_context():
        project = annif.project.get_project('dummy-en')
    assert project.project_id == 'dummy-en'
    assert project.language == 'en'
    assert project.analyzer.name == 'snowball'
    assert project.analyzer.param == 'english'
    assert project.access == Access.hidden
    assert isinstance(project.backend, annif.backend.dummy.DummyBackend)


def test_get_project_fi(app):
    with app.app_context():
        project = annif.project.get_project('dummy-fi')
    assert project.project_id == 'dummy-fi'
    assert project.language == 'fi'
    assert project.analyzer.name == 'snowball'
    assert project.analyzer.param == 'finnish'
    assert project.access == Access.public
    assert isinstance(project.backend, annif.backend.dummy.DummyBackend)


def test_get_project_dummydummy(app):
    with app.app_context():
        project = annif.project.get_project('dummydummy')
    assert project.project_id == 'dummydummy'
    assert project.language == 'en'
    assert project.analyzer.name == 'snowball'
    assert project.analyzer.param == 'english'
    assert project.access == Access.private
    assert isinstance(project.backend, annif.backend.dummy.DummyBackend)


def test_get_project_fi_dump(app):
    with app.app_context():
        project = annif.project.get_project('dummy-fi')
    pdump = project.dump()
    assert pdump == {
        'project_id': 'dummy-fi',
        'name': 'Dummy Finnish',
        'language': 'fi',
        'backend': {
            'backend_id': 'dummy',
        }
    }


def test_get_project_nonexistent(app):
    with app.app_context():
        with pytest.raises(ValueError):
            annif.project.get_project('nonexistent')


def test_get_project_noanalyzer(app):
    with app.app_context():
        project = annif.project.get_project('noanalyzer')
        with pytest.raises(ConfigurationException):
            project.analyzer


def test_get_project_novocab(app):
    with app.app_context():
        project = annif.project.get_project('novocab')
        with pytest.raises(ConfigurationException):
            project.vocab


def test_get_project_nobackend(app):
    with app.app_context():
        project = annif.project.get_project('nobackend')
        with pytest.raises(ConfigurationException):
            project.backend


def test_get_project_noname(app):
    with app.app_context():
        project = annif.project.get_project('noname')
        assert project.name == project.project_id


def test_get_project_default_params_tfidf(app):
    with app.app_context():
        project = annif.project.get_project('noparams-tfidf-fi')
    expected_default_params = {
        'limit': 100  # From AnnifBackend class
    }
    actual_params = project.backend.params
    for param, val in expected_default_params.items():
        assert param in actual_params and actual_params[param] == val


def test_get_project_default_params_fasttext(app):
    pytest.importorskip("annif.backend.fasttext")
    with app.app_context():
        project = annif.project.get_project('noparams-fasttext-fi')
    expected_default_params = {
        'limit': 100,  # From AnnifBackend class
        'dim': 100,    # Rest from FastTextBackend class
        'lr': 0.25,
        'epoch': 5,
        'loss': 'hs'}
    actual_params = project.backend.params
    for param, val in expected_default_params.items():
        assert param in actual_params and actual_params[param] == val


def test_get_project_invalid_config_file():
    app = annif.create_app(
        config_name='annif.default_config.TestingInvalidProjectsConfig')
    with app.app_context():
        with pytest.raises(ConfigurationException):
            annif.project.get_project('duplicatedvocab')


def test_project_load_vocabulary_tfidf(app, vocabulary, testdatadir):
    with app.app_context():
        project = annif.project.get_project('tfidf-fi')
    project.vocab.load_vocabulary(vocabulary, 'fi')
    assert testdatadir.join('vocabs/yso-fi/subjects').exists()
    assert testdatadir.join('vocabs/yso-fi/subjects').size() > 0


def test_project_train_tfidf(app, document_corpus, testdatadir):
    with app.app_context():
        project = annif.project.get_project('tfidf-fi')
    project.train(document_corpus)
    assert testdatadir.join('projects/tfidf-fi/tfidf-index').exists()
    assert testdatadir.join('projects/tfidf-fi/tfidf-index').size() > 0


def test_project_train_tfidf_nodocuments(app, empty_corpus):
    with app.app_context():
        project = annif.project.get_project('tfidf-fi')
    with pytest.raises(NotSupportedException) as excinfo:
        project.train(empty_corpus)
    assert 'Cannot train tfidf project with no documents' in str(excinfo.value)


def test_project_learn(app, tmpdir):
    tmpdir.join('doc1.txt').write('doc1')
    tmpdir.join('doc1.tsv').write('<http://example.org/key1>\tkey1')
    tmpdir.join('doc2.txt').write('doc2')
    tmpdir.join('doc2.tsv').write('<http://example.org/key2>\tkey2')
    docdir = annif.corpus.DocumentDirectory(str(tmpdir))

    with app.app_context():
        project = annif.project.get_project('dummy-fi')
        project.learn(docdir)
        result = project.suggest('this is some text')
        assert len(result) == 1
        assert result[0].uri == 'http://example.org/key1'
        assert result[0].label == 'key1'
        assert result[0].score == 1.0


def test_project_learn_not_supported(app, tmpdir):
    tmpdir.join('doc1.txt').write('doc1')
    tmpdir.join('doc1.tsv').write('<http://example.org/key1>\tkey1')
    tmpdir.join('doc2.txt').write('doc2')
    tmpdir.join('doc2.tsv').write('<http://example.org/key2>\tkey2')
    docdir = annif.corpus.DocumentDirectory(str(tmpdir))

    with app.app_context():
        project = annif.project.get_project('tfidf-fi')
        with pytest.raises(NotSupportedException):
            project.learn(docdir)


def test_project_load_vocabulary_fasttext(app, vocabulary, testdatadir):
    pytest.importorskip("annif.backend.fasttext")
    with app.app_context():
        project = annif.project.get_project('fasttext-fi')
    project.vocab.load_vocabulary(vocabulary, 'fi')
    assert testdatadir.join('vocabs/yso-fi/subjects').exists()
    assert testdatadir.join('vocabs/yso-fi/subjects').size() > 0


def test_project_train_fasttext(app, document_corpus, testdatadir):
    pytest.importorskip("annif.backend.fasttext")
    with app.app_context():
        project = annif.project.get_project('fasttext-fi')
    project.train(document_corpus)
    assert testdatadir.join('projects/fasttext-fi/fasttext-model').exists()
    assert testdatadir.join('projects/fasttext-fi/fasttext-model').size() > 0


def test_project_suggest(app):
    with app.app_context():
        project = annif.project.get_project('dummy-en')
    result = project.suggest('this is some text')
    assert len(result) == 1
    assert result[0].uri == 'http://example.org/dummy'
    assert result[0].label == 'dummy'
    assert result[0].score == 1.0


def test_project_suggest_combine(app):
    with app.app_context():
        project = annif.project.get_project('dummydummy')
    result = project.suggest('this is some text')
    assert len(result) == 1
    assert result[0].uri == 'http://example.org/dummy'
    assert result[0].label == 'dummy'
    assert result[0].score == 1.0


def test_project_not_initialized(app):
    with app.app_context():
        project = annif.project.get_project('dummy-en')
    assert not project.initialized


def test_project_initialized(app_with_initialize):
    with app_with_initialize.app_context():
        project = annif.project.get_project('dummy-en')
    assert project.initialized
    assert project.backend.initialized


def test_project_file_not_found():
    app = annif.create_app(
        config_name='annif.default_config.TestingNoProjectsConfig')
    with app.app_context():
        with pytest.raises(ValueError):
            annif.project.get_project('dummy-en')
