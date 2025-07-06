# ML Translator API Demo
This is a demo project showcasing a REST API for text translation using pretrained language models.

The stack consists of [FastAPI](https://github.com/fastapi/fastapi) with [Uvicorn](https://github.com/encode/uvicorn) for serving the API, [FastText by Facebook Research](https://github.com/facebookresearch/fastText) for automatic language detection, and [OPUS-MT models by Helsinki-NLP](https://huggingface.co/Helsinki-NLP) for the machine translation.

The project dependencies are managed by [uv](https://github.com/astral-sh/uv).

Currently, only a limited set of language pairs are supported, but additional OPUS-MT models can be integrated easily. The following language pairs come bundled in the app:
- `ru-en`
- `zh-en`

This repo stores the model files with Git LFS. Run `git lfs pull` after cloning the repository to make the model files available locally.

## Instructions
To start the service, either run it locally with `uv run src/main.py` or buildrun it with Docker:
1. `docker build -t translator .`
2. `docker run -p "8080:8080" translator`

Browse to http://localhost:8080/docs to view the API docs.

### Tests
Run tests with `uv run pytest src`.

## References
### Language Identification (LID) Model

- https://github.com/facebookresearch/fastText

```bibtex
@InProceedings{joulin2017bag,
  title={Bag of Tricks for Efficient Text Classification},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Mikolov, Tomas},
  booktitle={Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: Volume 2, Short Papers},
  month={April},
  year={2017},
  publisher={Association for Computational Linguistics},
  pages={427--431},
}

@article{joulin2016fasttext,
  title={FastText.zip: Compressing text classification models},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Douze, Matthijs and J{\'e}gou, H{\'e}rve and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1612.03651},
  year={2016}
}
```

### Neural Machine Translation (NMT) Models
- https://huggingface.co/Helsinki-NLP/opus-mt-ru-en
- https://huggingface.co/Helsinki-NLP/opus-mt-zh-en

```bibtex
@article{tiedemann2023democratizing,
  title={Democratizing neural machine translation with {OPUS-MT}},
  author={Tiedemann, J{\"o}rg and Aulamo, Mikko and Bakshandaeva, Daria and Boggia, Michele and Gr{\"o}nroos, Stig-Arne and Nieminen, Tommi and Raganato\
, Alessandro and Scherrer, Yves and Vazquez, Raul and Virpioja, Sami},
  journal={Language Resources and Evaluation},
  number={58},
  pages={713--755},
  year={2023},
  publisher={Springer Nature},
  issn={1574-0218},
  doi={10.1007/s10579-023-09704-w}
}

@InProceedings{TiedemannThottingal:EAMT2020,
  author = {J{\"o}rg Tiedemann and Santhosh Thottingal},
  title = {{OPUS-MT} — {B}uilding open translation services for the {W}orld},
  booktitle = {Proceedings of the 22nd Annual Conferenec of the European Association for Machine Translation (EAMT)},
  year = {2020},
  address = {Lisbon, Portugal}
 }
 ```
