<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Random People Data Project</h3>

  <p align="center">
    Randomly generized people data to use as a mock data
    <br />
    <br />
    <a href="https://github.com/spiridonovfed/EPAM_Training_Final_Task/issues">Report Bug</a>
    ·
    <a href="https://github.com/spiridonovfed/EPAM_Training_Final_Task/issues">Request Feature</a>
    <br />
  </p>
</p>
<br />


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This project is built as a final part of Python Basics Training conducted by EPAM.
It renders a random people data table using [Randomuser.me](https://randomuser.me/) API. By default quantity of entries is set to 1000, but it can be changed.
User can create new entry manually, edit or delete existing exntries.

### Built With

* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [PostgreSQL](https://www.postgresql.org/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [FLASK-WTF](https://flask-wtf.readthedocs.io/en/0.15.x/)
* [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)


<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/spiridonovfed/EPAM_Training_Final_Task
   ```
2. Install required packages
   ```sh
   pip install -r requirements.txt
   ```
3. Change config.py (/persons_table/config.py) if neccessary.
4. Run flask server
   ```sh
   flask run
   ```



<!-- USAGE EXAMPLES -->
## Usage

Use empty field and "Change Number" button at the top of a homepage to change quantity of entries in the table. The exceptable range is 1-5000. Upper limit is dictated by Randomuser.me API restrictions. If number inputted is greater than current number of entries, it will add lacking number of entries (i.e. current entries will not be rewritten).
All the data is essentally a mock and have nothing to do with real people.

Use "Create an entry" button to create an entry manulally. It will become the last entry in the table after creation.

The last column contains links to perosnal pages. From there, you can delete the entry or go to an editing page.
Go to http://homepage/random to get random person personal page.

Dockerfile and docker-compose.yml files are also added. Make sure to review and redact environmental variables there before dockerizing. 



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact

Your Name - [@spiridonovfed](https://t.me/spiridonovfedor) - spiridonovfed@yandex.ru

Project Link: [https://github.com/spiridonovfed/EPAM_Training_Final_Task](https://github.com/spiridonovfed/EPAM_Training_Final_Task)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
