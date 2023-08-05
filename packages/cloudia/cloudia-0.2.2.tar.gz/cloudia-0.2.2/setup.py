# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudia']

package_data = \
{'': ['*']}

install_requires = \
['japanize_matplotlib>=1.1.1,<2.0.0',
 'joblib',
 'matplotlib',
 'nagisa',
 'pandas',
 'wordcloud',
 'wurlitzer']

entry_points = \
{'console_scripts': ['my-script = cloudia:main']}

setup_kwargs = {
    'name': 'cloudia',
    'version': '0.2.2',
    'description': 'Tools to easily create a word cloud',
    'long_description': '# Cloudia\nTools to easily create a word cloud.\n\n  \n### from string\n\nfrom str or List[str]\n```\nfrom cloudia import Cloudia\n\ntext1 = "text data..."\ntext2 = "text data..."\n\n# from str\nCloudia(text1).plot()\n\n# from list\nCloudia([text1, text2]).plot()\n```\n \nexample from : [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/)\n\n![sample_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/sample_img.png?raw=true, "sample_img")\n  \n\nWe can also make it from Tuple.\n```\nfrom cloudia import Cloudia\n\ntext1 = "text data..."\ntext2 = "text data..."\nCloudia([ ("cloudia 1", text1), ("cloudia 2", text2) ]).plot()\n```\nTuple is ("IMAGE TITLE", "TEXT").  \n  \n  \n### from pandas\n\nWe can use pandas.\n\n```\ndf = pd.DataFrame({\'wc1\': [\'sample1\',\'sample2\'], \'wc2\': [\'hoge hoge piyo piyo fuga\', \'hoge\']})\n\n# plot from df\nCloudia(df).plot()\n\n# add df method\ndf.wc.plot(dark_theme=True)\n```\n\nfrom pandas.DataFrame or pandas.Series.\n\n![pandas_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/pandas_img.png?raw=true, "pandas_img")\n![dark_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/dark_img.png?raw=true, "dark_img")\n  \nWe can use Tuple too.\n```\nCloudia( ("IMAGE TITLE", pd.Series([\'hoge\'])) ).plot()\n```\n  \n  \n### from japanese\n\nWe can process Japanese too.\n```\ntext = "これはCloudiaのテストです。WordCloudをつくるには本来、形態素解析の導入が必要になります。Cloudiaはmecabのような形態素解析器の導入は必要はなくnagisaを利用した動的な生成を行う事ができます。nagisaとjapanize-matplotlibは、形態素解析を必要としてきたWordCloud生成に対して、Cloudiaに対して大きく貢献しました。ここに感謝の意を述べたいと思います。"\n\nCloudia(text).plot()\n```\n\nfrom japanese without morphological analysis module.  \n  \n![japanese_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/japanese_img.png?raw=true, "jap_img")  \n  \nNo need to introduce morphological analysis.\n  \n  \n# Install\n\n```\npip install cloudia\n```\n  \n  \n# Args\n\nCloudia args.\n```\nCloudia(\n  data,    # text data\n  single_words=[],    # It\'s not split word list, example: ["neural network"]\n  stop_words=STOPWORDS,    # not count words, default is wordcloud.STOPWORDS\n  extract_postags=[\'名詞\', \'英単語\', \'ローマ字文\'],    # part of speech for japanese\n  parse_func=None,    # split text function, example: lambda x: x.split(\',\')\n  multiprocess=True,    # Flag for using multiprocessing\n  individual=False    # flag for \' \'.join(word) with parse \n)\n```\n  \n  \nplot method args.\n```\nCloudia().plot(\n    dark_theme=False,    # color theme\n    title_size=12,     # title text size\n    row_num=3,    # for example, 12 wordcloud, row_num=3 -> 4*3image\n    figsize_rate=2    # figure size rate\n)\n```\n\nsave method args.\n```\nCloudia().save(\n    file_path,    # save figure image path\n    dark_theme=False,\n    title_size=12, \n    row_num=3,\n    figsize_rate=2\n)\n```\n\npandas.DataFrame, pandas.Series wc.plot method args.\n```\nDataFrame.wc.plot(\n  single_words=[],    # It\'s not split word list, example: ["neural network"]\n  stop_words=STOPWORDS,    # not count words, default is wordcloud.STOPWORDS\n  extract_postags=[\'名詞\', \'英単語\', \'ローマ字文\'],    # part of speech for japanese\n  parse_func=None,    # split text function, example: lambda x: x.split(\',\')\n  multiprocess=True,    # Flag for using multiprocessing\n  individual=False,    # flag for \' \'.join(word) with parse \n  dark_theme=False,    # color theme\n  title_size=12,     # title text size\n  row_num=3,    # for example, 12 wordcloud, row_num=3 -> 4*3image\n  figsize_rate=2    # figure size rate\n)\n```\nIf we use wc.save, setting file_path args.\n  \n  \n# Thanks\n\n- [japanize-matplotlib](https://github.com/uehara1414/japanize-matplotlib)\n- [nagisa](https://github.com/taishi-i/nagisa)\n',
    'author': 'vaaaaanquish',
    'author_email': '6syun9@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vaaaaanquish/cloudia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
