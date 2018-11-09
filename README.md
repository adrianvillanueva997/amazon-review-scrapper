# amazon-review-scrapper
Simple script that gets reviews from amazon given a reviews url

# How to use
Just put the urls in ``urls.txt`` with this format: 
```
https://www.amazon.es/Apple-iPhone-Plata-Smartphone-Reacondicionado/product-reviews/B01L9KX26S/ref=cm_cr_getr_d_paging_btm_3?ie=UTF8&reviewerType=all_reviews&pageNumber=
```
Later just edit the end of the python script with the filenames and paths that you want

## Installation

OS X & Linux:

```sh
sudo apt install python3.6
sudo apt install python3-pip
pip3 install bs4
```

Windows:
Just get python 3.6 from [here](https://www.python.org/downloads/release/python-366/)
```sh
pip3 install bs4
```

## Meta

Distributed under the GPLV3 license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/adrianvillanueva997/amazon-review-scrapper/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
