# Empiric!

The Python package `Empiric!` provides an easy-to-use framework to conduct empirical experiments, with a particular focus on geospatial data perception and contribution.

When running an experiment in `Empiric!`, a web server is started.  Interviewees visit the website offered by the server to participate in interactive experiments and answer questions.  The way these experiments, questionnaires, and other pages are shown is defined in a manuscript, which makes, among others, possible to divide the group of interviewees into several comparison groups and to dynamically react to the results provided by the interviewees.  A log is created for each of the interviewees and the results of the experiments and questionnaires are stored in JSON files, which can be used by any application you want.  In addition, `Empiric!` offers a statistical analysis of the results, which includes visualiatzions offered on a website.

## Installation

To install `Empiric!`, you will need `python3` and `pip` ([How to install pip](https://pip.pypa.io/en/stable/installing/)). Then execute:
```bash
pip install Empiric
```
On some operating systems, `pip` for `python3` is named `pip3`:
```bash
pip3 install Empiric
```

Further, you need the JavaScript package manager [`Yarn`](https://yarnpkg.com) to run `Empiric!`.  It will be used to automatically download the JavaScript libraries needed for the web interface.  If you have [Node.js](https://nodejs.org) with [npm](https://www.npmjs.com) installed, you can install `Yarn` as follows:
```bash
npm install -g yarn
```
Please find further information about how to install Yarn on [https://yarnpkg.com](https://yarnpkg.com).

## Minimal Example

To get `Empiric!` running and serve your first simple questionnaire, create a python file in which you define a manuscript for the interviews first:
```python
from Empiric import Experiment, pageQuestionnaire

def manuscript(m):
  pageQuestionnaire(m, questions='''
    <choice
      key="doYouLikeEmpiric"
      text="Do you like Empiric?"
    >
      <option>yes, of course!</option>
      <option>maybe</option>
      <option>no</option>
    </choice>
    <text
      key="comments"
      text="Do you have any comments?"
    ></text>
  ''')
```
When running this manuscript, a questionnaire is shown that consists of a question with corresponding answers to reply with, and a text box to provide some comments.

In order to run the experiment, you execute the following after defining the manuscript:
```python
experiment = Experiment()
experiment.run(manuscript)
```

Congratulations!  You have prepared your first experiment.  When running the code, the website will be served for local use only.  It will automatically be opened in your default browser.  The first interviewee can start with the interview.  Further modes are available to run the website even in a non local mode, allowing interviewees to participate over internet.  For further information, see Section [**Experiment**](docs/experiment.md).

## Usage

The following modules are available (please click on their names to access further documentation):

* [**Manuscripts**](docs/manuscripts.md) - Manuscripts describe which pages are shown to the interviewee and in which order
* [**Experiments**](docs/experiments.md) - Experiments are the heart of `Empiric!`
* [**Page ‘Info’**](docs/pageInfo.md) - A page showing only general information; often used as a welcome page
* [**Page ‘Questionnaire’**](docs/pageQuestionnaire.md) - A page that shows a questionnaire
* [**Page ‘Map’**](docs/pageMap.md) - A page that allows for interaction with elements on a map
* [**Page ‘Final’**](docs/pageFinal.md) - A page saying ‘Thank You’
* [**Creating new pages**](docs/creatingNewPages.md) - How to create and use a new page
* [**Collected data**](docs/collectedData.md) – The data format of the data stored
* [**Statistics**](docs/statistics.md) – How to access the results of the experiment and analyse them

## Author

This software is written and maintained by Franz-Benjamin Mocnik, <mail@mocnik-science.net>.

(c) by Franz-Benjamin Mocnik, 2020.

## License

The code is licensed under the [GPL-3](https://github.com/mocnik-science/empiric/blob/master/LICENSE).
