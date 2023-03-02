# polyglot-api
A REST API for translating Chinese and Russian into English using pretrained language models.


### Features
- Language detection using FastText.
- 


### Local Development
1. `git clone ...`
2. `cd src`
3. `pip install -r requirements-dev.txt`

### Docker Build
1. `cd src`
2. `docker build -t polyglot .`
3. `docker run -p "80:80" polyglot`

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
