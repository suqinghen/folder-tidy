import pathlib
from media_organizer.classifier import Classifier, MediaType

def test_classifier_init():
    classifier = Classifier()
    assert isinstance(classifier, Classifier)

def test_classifier_classify_music():
    classifier = Classifier()
    assert classifier.classify(pathlib.Path("song.mp3")) == MediaType.MUSIC

def test_classifier_classify_movie():
    classifier = Classifier()
    assert classifier.classify(pathlib.Path("movie.mkv")) == MediaType.MOVIE

def test_classifier_classify_ebook():
    classifier = Classifier()
    assert classifier.classify(pathlib.Path("book.epub")) == MediaType.EBOOK

def test_classifier_classify_unknown():
    classifier = Classifier()
    assert classifier.classify(pathlib.Path("unknown.xyz")) == MediaType.UNKNOWN
