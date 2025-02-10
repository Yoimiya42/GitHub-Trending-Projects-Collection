
# Brief

You will then want to plan your implementation in more detail. Some questions you might want to ask 
include: 
- How do users typically interact with your program/system? What are the inputs your system 
works with, and what outputs does it produce? 
- What main features would you like to include in the system, and how will you prioritize them? 
- What languages, frameworks, tools, etc. will be useful for implementing this project? 
- How will you divide work or work on the project together?

Consider including the following content in your report: 
- A brief introduction that motivates and describes the tool you’re proposing, including the 
intended user base for the tool. 
- An overview of the core features/functionality of your system. 
- A brief summary of the findings of your ethics analysis: mention potential ethical issues and 
how you have designed your system to try to mitigate these issues. 
- A list of components, data storage, data structures, algorithms, etc. needed to implement your 
tool. 
- Appropriate diagrams as needed to illustrate important concepts for your proposal. 
- A framework/language that you propose to implement this tool in.


-- Description:
## Introduction
    motivation, intended user base
## Features
## Ethics Analysis
## Diagrams

-- Technical details:
## Components: Data storage, data structures, algorithms
## Framework/language


___

### Idea1: Learning log web site

- Features:
  - `attach and store files, images, url of video website or article`  
    - find a resource but not use it immediately, and forget it later
    - visit a video platform, like YouTube, to watch educational content, they might get distracted by recommendations on the homepage.
  - `timeline of tasks`
    -  import a calender?
  - `priority management`
    -  main: up to 1, moderate: up to 3, low: ...
   -  divide areas by usage domain(entertainment, study, fitness, habits...) with different style(color, background, font..)
  - `user authentication and sync both on laptop and phone`
  - `Deploy on server`
  
- Framework:
  - front-end: `CSS` for appearance, `javascript` for interactivity
  - back-end: python - `django`,  `database`?(some have embedded in django)


difficulty: * * * * (javascript, django)
creativity: * * 
usefulness: * *     (too many similar apps)

### Idea2: Github RepoGuide
Call the `GitHub search API` 
- Functions:
  - Homepage, filter by:
    - `language`
    - `stars`
    - `forks`
    - `Created date`
    - `Topics`
    - `number of contributors`
    - `organization`
    - `Country`(based on published location, natural language...)
  - some interesting statistics
    - most popular repositories in past 7 days, 30 days (show in line graph)
    - trending languages  (show in pie chart)
    - trending topics -> `word cloud` 
    - `organization` with most repositories
    - `contributors` with most followers
  - Dedicated zones for various user purposes:
    - For "Beginner": 
      - repositories with detailed README.md
      - more pdf, image, video, website url in README.md
      - with wiki
      - more forks
      - more stars
      - low contributors
      - more issues 
      - with "guide" in README.md
      - with "tutorial" in README.md
      - sponsored by famous organization
    - Just exploring some interesting repositories:
      - most stars in past 7 days
      -  high star growth in past 7 days
      -  include hot topics
      -  many contributors
      -  published by famous organization
    - some students / practitioners want to take part in open source project:
      - more forks
      - more contributors
      - more issues
      - more pull requests
    - install, deploy or customize some useful open source tools/software/games:
      - with keywords like "download", "install", "deploy", "setup"
      - with "license" information
      - with CLT tool in README.md
      - with API description in README.md
      - Dockerfile included
    - translator:
      -  set origin language and target language
      -  certain number of stars
      -  certain technical field
      -  translate requirements in issues...
    - read official documentation of some software / language/ framework / library:
      -  with "official" in README.md
      - with "documentation" in README.md
      -  published by official organization/ company
      -  many many files in repository
  
- Implementation:
- Front-end: `HTML`, `CSS`, a little`JavaScript`
- back-end: `python`, `plotly`, `matplotlib`for data visualization
- `GitHub API` for data collection

difficulty: * *  (github API, data visualization)
creativity: * * * (a little unnecessary, github already has most of the functions)
usefulness: * * * * (help users find suitable repositories quickly, let users keep track of the trend of open source projects, technical industry)
  
intended user base: 
- programming beginners
- people from non-computer-related industries who are interested in tech projects
- students who want to gain experience in open source projects


### Idea3: Steam game recommendation system

- Features:
  - sales
  - history lowest price
  - user reviews  
  - media reviews
  - all-time peak players
  - current players
  - average playtime
  - theme/genre

- Implementation:
- Front-end: `HTML`, `CSS`, a little`JavaScript`
- back-end: `python`(scraping), `pandas`,  for data analysis
- `Steam API` for data collection(only access partially data)
- `plotly`, `matplotlib`for data visualization
!! No public API for steam game data, need to scrape data from steam related website.

difficulty: * * * * (scraping, data analysis)
creativity: * * * 
usefulness: * * * * * (help users find interesting games)

### Ideas4: online quiz

about 10 pages  
a question with 4 options   
give feedback after each question, and show the correct answer  
next, prev page  

attach cyber security related videos, url, articles
