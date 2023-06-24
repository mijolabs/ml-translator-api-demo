# Translator API Demo
This is a demo project for a REST API for translating text using pretrained language models. The stack consists of FastAPI and Uvicorn to provide the API service, FastTrack and accompanying language identification model is used for automatic language detection, and Opus-MT language models are used for the text translation. Currently only supports the following language pairs, but additional Opus-MT models can be added.
- `ru-en`
- `zh-en`

### Local Development
1. `git clone ...`
2. `cd src`
3. `pip install -r requirements-dev.txt`

### Docker Build
1. `cd src`
2. `docker build -t translator .`
3. `docker run -p "80:80" translator`

To start a local dev server:
1. `cd src/dev-tools`
2. `python start-server.py`


### Language Models
https://huggingface.co/Helsinki-NLP/opus-mt-ru-en
https://huggingface.co/Helsinki-NLP/opus-mt-zh-en
```bibtex
@InProceedings{TiedemannThottingal:EAMT2020,
  author = {J{\"o}rg Tiedemann and Santhosh Thottingal},
  title = {{OPUS-MT} — {B}uilding open translation services for the {W}orld},
  booktitle = {Proceedings of the 22nd Annual Conferenec of the European Association for Machine Translation (EAMT)},
  year = {2020},
  address = {Lisbon, Portugal}
  }
```
https://github.com/facebookresearch/fastText
```bibtex
@article{joulin2016bag,
  title={Bag of Tricks for Efficient Text Classification},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1607.01759},
  year={2016}
}
```
```bibtex
@article{joulin2016fasttext,
  title={FastText.zip: Compressing text classification models},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Douze, Matthijs and J{\'e}gou, H{\'e}rve and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1612.03651},
  year={2016}
}
```
