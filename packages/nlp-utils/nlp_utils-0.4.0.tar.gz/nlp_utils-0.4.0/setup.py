from setuptools import setup

setup(
    name="nlp_utils",
    version="0.4.0",
    packages=["nlp_utils", "nlp_utils.dataset", "nlp_utils.preprocess"],
    url="",
    license="MIT",
    author="Xiaoquan Kong",
    author_email="u1mail2me@gmail.com",
    description="Utils for NLP",
    install_requires=["nltk", "numpy", "tensorflow", "micro_toolkit"],
)
