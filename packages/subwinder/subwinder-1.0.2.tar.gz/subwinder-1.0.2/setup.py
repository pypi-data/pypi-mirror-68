# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subwinder']

package_data = \
{'': ['*']}

install_requires = \
['atomicwrites>=1.4,<2.0']

setup_kwargs = {
    'name': 'subwinder',
    'version': '1.0.2',
    'description': 'An ergonomic python library for the opensubtitles.org API',
    'long_description': '## Subwinder\n\nAn ergonomic python library for the [opensubtitles.org](https://opensubtitles.org) API.\n\n### Quickstart\n\nOur task is composed of 3 simple steps\n\n1. Search for English subtitles for a movie at `/path/to/movie.mkv` and French subtitles for a tv show episode at `/path/to/episode.avi`.\n2. Print out any comments that people left on the subtitles.\n3. Download the subtitles next to the original media file with the naming format `{media name}.{3 letter lang code}.{extension}` (something like `/path/to/movie.eng.ssa` and `/path/to/episode.fre.srt`)\n\n**Note:** This does require a free opensubtitles account.\n\n**Note:** The user agent is specific to the program using the API. You can look [here](https://trac.opensubtitles.org/projects/opensubtitles/wiki/DevReadFirst) under "How to request a new user agent" to see about what user agent you can set for development, or how to get an official user agent for your program.\n\n```python\nfrom subwinder import AuthSubwinder, Media\n\nfrom datetime import datetime as dt\nfrom pathlib import Path\n\n# Step 1. Getting our `Media` objects created and searching\n# You can create the `Media` by passing in the filepath\nmovie = Media("/path/to/movie.mkv")\n# Or if you are already using `Path`s then you can pass in a path too (or you\n# can build it from the individual pieces if you don\'t have local files)\nepisode = Media(Path("/path/to/episode.avi"))\nwith AuthSubwinder("<username>", "<password>", "<useragent>") as asw:\n    results = asw.search_subtitles([(movie, "en"), (episode, "fr")])\n    # We\'re assuming both `Media` returned a `SearchResult` for this example\n    assert None not in results\n\n    # Step 2. Print any comments for both of our `SearchResult`s\n    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"\n    results_comments = asw.get_comments(results)\n    for result, result_comments in zip(results, results_comments):\n        print(f"{result.media.filename} Comments:")\n        for comment in result_comments:\n            date = dt.strftime(comment.date, TIME_FORMAT)\n            print(f"{date} {comment.author.name}: {comment.text}")\n        print()\n\n    # Step 3. Download both of the subtitles next to the original files\n    # We\'re assuming we have enough remaining downloads for these, if not then\n    # a `SubDownloadError` will be raised by `.download_subtitles(...)`\n    assert asw.daily_download_info().remaining >= len(results)\n    download_paths = asw.download_subtitles(\n        results, name_format="{media_name}.{lang_3}.{ext}"\n    )\n```\n\nAnd that\'s it, with ~20 sloc you can search, get comments, and download a couple subtitles!\n\n### Installation\n\n**Note:** The minimum required Python version is `3.7`, you can check your current version with `python -V` or `python3 -V` if you\'re unsure of your current version.\n\nInstall the [subwinder](https://pypi.org/project/subwinder/) library with your standard Python package manager e.g.\n\n```text\n$ pip install subwinder\n```\n\nAs always you are recommended to install into a virtual environment.\n\n### Documentation\n\nThere is pretty thorough documentation in the [docs directory](https://github.com/LovecraftianHorror/subwinder/blob/master/docs/README.md) that covers all the functionality currently exposed by the library. If anything in the docs are incorrect or confusing then please [raise an issue](https://github.com/LovecraftianHorror/subwinder/issues) to address this.\n\n### Benefits from using `subwinder`\n\n* Easy to develop in\n    * Use objects defined by the library, and take and return objects in a logical order to provide a clean interface\n    * Efforts are made to prevent re-exposing the same information under slightly different key names, or under different types to provide a consistent experience\n    * Values are parsed to built-in Python types when it makes sense\n    * Endpoints that batch do so automatically to the maximum batch size\n* Robust, but if it fails then fail fast\n    * Custom `Exception`s are defined and used to provide context on failures\n    * If something will fail, try to detect it and raise an `Exception` as early as possible\n    * Automatically retry requests using an exponential back-off to deal with rate-limiting\n* Small footprint\n    * Only one direct dependency is required.\n\n### Caveats from using `subwinder`\n\n* Python 3.7+ is required (at this point 3.7 is already several years old)\n* Not all values from the API are exposed: however, I\'m flexible on this so if you have a use for one of the missing values then please bring it up in [an issue](https://github.com/LovecraftianHorror/subwinder/issues)!\n* Currently only English is supported for the internal API. You can still search for subtitles in other languages, but the media names and long language names will all be in English. This will be worked on after the API is in a more stable state\n\n### License\n\n`subwinder` is licensed under AGPL v3 which should be included with the library. If not then you can find an online copy [here](https://www.gnu.org/licenses/agpl-3.0.en.html).\n',
    'author': 'Lovecraftian Horror',
    'author_email': 'LovecraftianHorror@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LovecraftianHorror/subwinder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
