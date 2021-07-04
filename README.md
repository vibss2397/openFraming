# OpenFraming

## Introduction

We have introduced [OpenFraming](http://www.openframing.org), a Web-based system for analyzing and classifying frames in the text documents. OpenFraming is designed to lower the barriers to applying machine learning for frame analysis, including giving researchers the capability to build models using their own labeled data. Its architecture is designed to be user-friendly and easily navigable, empowering researchers to com- fortably make sense of their text corpora without specific machine learning knowledge.

You can find the preprint of our work [here](https://arxiv.org/pdf/2008.06974.pdf)

## Requirements

### Docker
You need [Docker](https://docs.docker.com/get-docker/). Feel free to read up on Docker if you wish.
Our best short explanation for Docker is that, Docker is for deploying applications with complicated
dependencies, what the printing press was to publishing books (it allows you to do it in a much quicker,
and much more reproducible way).

The link above has guides on how to install Docker on the most popular platforms.

## How to install

 1. `git clone https://github.com/vibss2397/openFraming.git`
 2. `cd openFraming`
 3. `docker-compose build`
 4. `docker-compose up`
 
 You might have to add `sudo` at the beginning of commands at step 3 and 4 if using linux/macOS.


## E-mails
If you want to send actual e-mails through Sendgrid with this system (as opposed to just
printing the e-mails that would be sent to the console),  please set the environment
variables:

```bash
export SENDGRID_API_KEY=     # An API key from Sendgrid
export SENGRID_FROM_EMAIL=   # An email address to put in the "from" field. Note that
			     # you'll have to verify this email in Sendgrid as a 
			     # "Sender". 
```

If you happen to need `sudo` in the section above, please pass the `-E` flag to make
sure these environment variables are picked up. i.e.,

```bash
sudo -E docker-compose up
```

## Video demonstration

You can check the following YouTube video for a quick demonstration of our Website's features.

[![IMAGE ALT TEXT](http://img.youtube.com/vi/u8SJAZ-EbgU/0.jpg)]("https://www.youtube.com/watch?v=GGxcEFsaV7o")

## Getting help

If you have any question, concern, or bug report, please file an issue in this repository's Issue Tracker and we will respond accordingly.

## Funding

This research is funded by the following NSF Award:

   [NSF Award #1838193](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1838193&HistoricalAwards=false) BIGDATA: IA: Multiplatform, Multilingual, and Multimodal Tools for Analyzing Public Communication in over 100 Languages
    
    
## Acknowledgement

We are truly grateful to Gerard Shockley, Boston University Cloud Broker, for helping us seamlessly host our Website and run in an Amazon Web Services EC2 instance.


## Credits

[Vibhu Bhatia](https://vibss2397.github.io), [Vidya Prasad Akavoor](https://www.linkedin.com/in/vidya-akavoor), [Sejin Paik](http://www.google.com), [Lei Guo](https://www.leiguo.net), [Mona Jalal](http://monajalal.com)<sup>&ast;</sup>, [Alyssa Smith](https://www.linkedin.com/in/alyssa-smith-2463b7a0)<sup>&ast;</sup>, [David Assefa Tofu](https://davidatbu.github.io)<sup>&ast;</sup>, [Edward Edberg Halim](https://id.linkedin.com/in/edward-edberg-halim-241014111), [Yimeng Sun](https://www.linkedin.com/in/yimengsun0104),  [Margrit Betke](http://www.cs.bu.edu/~betke), [Prakash Ishwar](http://sites.bu.edu/pi), [Derry Wijaya](https://derrywijaya.github.io)
