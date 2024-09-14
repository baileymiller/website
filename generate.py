from enum import Enum
import os
from bs4 import BeautifulSoup

STYLE_ASSETS = [
  'font-awesome/css/font-awesome.css' ,
  'bootstrap.min.css',
  'style.css'
]

class FontAwesomeIcons(str, Enum):
  NONE        = ""
  PDF         = "fa fa-fw fa-file-pdf-o"
  ENVELOPE    = "fa fa-fw fa-envelope"
  ARCHIVE     = "fa fa-fw fa-archive"
  BOOK        = "fa fa-fw fa-book"
  GITHUB      = "fa fa-fw fa-github"
  ZIP         = "fa fa-fw fa-file-archive-o"
  CODE        = "fa fa-fw fa-file-code-o"
  COPY        = "fa fa-fw fa-clipboard"
  GLOBE       = "fa fa-fw fa-globe"
  BACK_ARROW  = "fa fa-fw fa-long-arrow-left"
  GRAD_CAP    = "fa fa-fw fa-graduation-cap"
  MAP_MARKER  = "fa fa-fw fa-map-marker"
  FILE        = "fa fa-fw fa-file"
  LINKEDIN    = "fa fa-fw fa-linkedin-square"
  NEWS        = "fa fa-fw fa-newspaper-o"
  DOWNLOAD    = "fa-solid fa-chevron-down"

  def __str__(self):
    return self.value

class Person:
  def __init__(self, name, website, me = False):
    self.name = name
    self.website = website
    self.me = me 

class Publication:
  def __init__(self, 
               image, 
               title, 
               url,
               authors = [], 
               joint_authors = {},
               venue = '', 
               award = ''):
    self.image = image
    self.title = title
    self.url = url 
    self.authors = authors 
    self.joint_authors = joint_authors
    self.venue = venue
    self.award = award

  def get_author_suffix(self, author):
    suffix = ''
    for contribution_suffix, authors in self.joint_authors.items():
      if author in authors:
        suffix = contribution_suffix
    return suffix

  def get_author_names(self):
    names = ''
    for i, author in enumerate(self.authors):
      name = author.name
      name += self.get_author_suffix(author)

      if (author.me):
        names += f'<b>{name}</b>'

      elif (len(author.website) > 0):
        names += f'<a href={author.website}>{name}</a>'

      else:
        names += name
      
      if i == len(self.authors) - 2:
        names += " and "
      elif i < len(self.authors) - 1:
        names += ", "

    return names

class ProjectResources:
  def __init__(self, publication = [], code = []):
    self.publication = publication
    self.code = code

class Resource:
  def __init__(self, icon = FontAwesomeIcons.NONE, path = '', name = ''):
    self.icon = icon
    self.path = path
    self.name = name

class Course:
  def __init__(self, image, name, url, role, details):
    self.image = image
    self.name = name
    self.url = url
    self.role = role
    self.details = details

class Video:
  def __init__(self, name, id):
    self.name = name
    self.id = id

class AboutMe:
  def __init__(self, name, image, resources):
    self.name = name
    self.image = image
    self.resources = resources

  def get_html(self):
    links = ''
    for resource in self.resources:
      links += f'''
        <div class="d-block profile-row">
          <i class="{resource.icon}"></i>
          <a
            class="pl-2"
            href="{resource.path}"
          >
            {resource.name}
          </a>
        </div>
      '''
    return f'''
      <div class="d-flex pl-5 pt-5 justify-content-start">
        <div>
          <img
            id="profile-pic"
            class="float-left"
            src="{self.image}"
            alt="Bailey"
          />
        </div>
        <div class="col">
          <div class="d-block profile-row">
            <h1>{self.name}</h1>
          </div>
          {links}
        </div>
      </div>
    '''

class Home:
  def __init__(self, about_me, bio, publications = [], courses = []):
    self.about_me = about_me
    self.bio = bio
    self.publications = publications 
    self.courses = courses

  def get_publications_list_html(self):
    pub_list = ''
    for _, pub in self.publications.items():
      pub_award_text = f'''<div class="paper-award">{pub.award}</div>'''
      pub_list += f'''
        <div>
          <div class="d-flex flex-row pb-4 align-items-center">
            <img
              src={pub.image}
              class="thumbnail img-responsive"
            />
            <div class="d-flex flex-column pl-4">
              <span>
                <a href={pub.url} class="item-title">{pub.title}</a>
              </span>
              <div>
                {pub.get_author_names()}
              </div>
              <div>
                {pub.venue}
              </div>
              <div>
                {pub_award_text if pub.award else ''}
              </div>
            </div>
          </div>
        </div>
      '''
    return pub_list

  def get_teaching_list_html(self):
    teaching_list = ''
    for course in self.courses:
      teaching_list += f'''
        <div>
          <div class="d-flex flex-row pb-4 align-items-center">
            <img
              src={course.image}
              class="thumbnail img-responsive"
            />
            <div class="d-flex flex-column pl-4">
              <span>
                <a href={course.url} class="item-title">{course.name}</a>
              </span>
              <div>
                <b>{course.role}</b>
              </div>
              <div>
                {course.details}
              </div>
            </div>
          </div>
        </div>
      '''
    return teaching_list

  def generate(self, path):
    soup = BeautifulSoup('<!DOCTYPE html> <html></html>', 'html.parser')

    # add styling 
    head = soup.new_tag('head')
    soup.html.append(head)

    head.append(soup.new_tag('meta', charset="UTF-8"))
    links = [
      soup.new_tag('link', rel='stylesheet', type='text/css', 
                   href=os.path.join('assets', style_asset))
      for style_asset in STYLE_ASSETS
    ]
    [head.append(link) for link in links]

    # construct page
    body = soup.new_tag('body')
    soup.html.append(body)
    about_me_section = self.about_me.get_html()
    publications_list = self.get_publications_list_html()
    teaching_list = self.get_teaching_list_html()
    body.append(BeautifulSoup(f''' 
      <div class="container">
        {about_me_section} 
      </div>
      <div class="container">
        <div class="d-flex flex-column pl-5 pt-3">
          <div>
            <p>{self.bio}</p>
          </div>
          <div>
            <h4>Publications</h4>
            <hr/>
            {publications_list}
            <div class="pb-5">(*, † indicate equal contribution)</div>
          </div>
          <div>
            <h4>Teaching</h4>
            <hr/>
            {teaching_list}
          </div>
        </div>
        <br>
        <div class="text-center">
          <h6 class="font-weight-light"> 
            Source code for this website is <a href=https://github.com/baileymiller/website>available on Github</a>
          </h6>
        </div>
      </div>
    ''', 'html.parser'))
    with open(os.path.join(path, 'index.html'), "w") as file:
      file.write(str(soup))

class Project:
  def __init__(self, 
               image,
               image_caption, 
               abstract, 
               videos = [], 
               resources = ProjectResources(), 
               acknowledgements= '', 
               citation = ''):
    self.image = image
    self.image_caption = image_caption
    self.abstract = abstract
    self.videos = videos
    self.resources = resources
    self.acknowledgements = acknowledgements
    self.citation = citation

  def create_section(self, name, content):
    return f'''
      <div>
        <h2 class="mt-4 font-weight-normal">{name}</h2>
        <hr>
        {content}
      </div>
    '''

  def create_resources_list(self, name, resources):
    resources_list = ''
    for resource in resources:
      resources_list += f'''
        <div class="container mt-1 mb-1">
          <i class="{resource.icon}"></i>
          <a href="{resource.path}">
            {resource.name}
          </a>
        </div>
        '''
    return f'''
      <div>
        <h4 class="mt-4 font-weight-light">
          {name}
        </h4>
        {resources_list}
      </div>
    '''

  def get_abstract_html(self):
    if len(self.abstract) == 0:
      return ''
    return self.create_section('Abstract', f'<p>{self.abstract}</p>')

  def get_video_html(self):
    if len(self.videos) == 0:
      return ''
    video_list = '<div class="container">'
    for video in self.videos:
      video_list += f'''
        <div class="img-container">
        <h4 class="font-weight-light">{video.name}</h4>
          <iframe class="embed-responsive-item project-video" 
                  src="https://www.youtube.com/embed/{video.id}" allowfullscreen>
          </iframe>
        </div>
      '''
    video_list += '</div>'

    return self.create_section('Videos', video_list)

  def get_resources_html(self):
    resources_html = ''

    if len(self.resources.publication) > 0:
      resources_html += self.create_resources_list('Publication', self.resources.publication)
    
    if len(self.resources.code) > 0:
      resources_html += self.create_resources_list('Code', self.resources.code)

    return self.create_section('Resources', resources_html)

  def get_acknowledgements_html(self):
    if len(self.acknowledgements) == 0:
      return ''
    return self.create_section('Acknowledgements', f'<p>{self.acknowledgements}</p>')

  def get_citation_html(self):
    if len(self.citation) == 0:
      return ''

    return self.create_section('Cite', f'''
      <script>
      function copyText() {{
        var text = document.getElementById("citation-to-copy")
        navigator.clipboard.writeText(text.innerText)
      }}
      </script>
      <div class="code-background">
        <button class="code-copy-btn" onClick=copyText()>
          <i class="{FontAwesomeIcons.COPY}"></i>
        </button>
        <pre id="citation-to-copy">
        {self.citation}</pre>
      </div>
      '''
    )

  def generate(self, path, publication):
    soup = BeautifulSoup('<!DOCTYPE html> <html></html>', 'html.parser')

    # add styling 
    head = soup.new_tag('head')
    head.append(soup.new_tag('meta', charset="UTF-8"))
    soup.html.append(head)
    links = [
      soup.new_tag('link', rel='stylesheet', type='text/css', 
                   href=os.path.join('../../assets', style_asset))
      for style_asset in STYLE_ASSETS
    ]
    [head.append(link) for link in links] 
  
    # construct page
    body = soup.new_tag('body')
    soup.html.append(body)
    body.append(BeautifulSoup(f'''
      <div class="container">
        <nav class="navbar navbar-expand-lg">
          <div class="container-fluid">
            <ul class="navbar-nav ml-auto">
              <li class="nav-item"> 
                <a href="../../">
                <i class="{FontAwesomeIcons.BACK_ARROW}"></i>
                home
                </a>
                </li>
            </ul>
          </div>
        </nav>
        <h1 class="card-title font-weight-normal">{publication.title}</h1>
        <h4 class="font-weight-light">{publication.get_author_names()}</h4>
        <img src={project.image} class="card-img-top mt-3" alt="{publication.title}-teaser">
        <p class="font-italic mt-2">{project.image_caption} </p>
        {self.get_abstract_html()}
        {self.get_resources_html()}
        {self.get_video_html()}
        {self.get_citation_html()}
        {self.get_acknowledgements_html()}
      </div>
    ''', 'html.parser'))

    if not os.path.exists(path):
      os.makedirs(path)

    with open(os.path.join(path, 'index.html'), "w") as file:
      file.write(str(soup))

PEOPLE = {
  'your-name': Person(
    name = 'Your Name',
    website = '',
    me = True
  ),
  'coauthor-name': Person(
    name = 'Coauthor Name',
    website = ''
  ),
  'coauthor-name-other': Person(
    name = 'Coauthor Other',
    website = ''
  )
}

ABOUT_ME = AboutMe(
  name = 'Your Name',
  image = 'data/images/profile.png', 
  resources=[
    Resource(
      icon=FontAwesomeIcons.MAP_MARKER,
      name='Carnegie Mellon University',
      path='https://www.cs.cmu.edu'
    ),
    Resource(
      icon=FontAwesomeIcons.ENVELOPE,
      name='your-email@gmail.com',
      path='mailto:your-email@gmail.com'
    ),
    Resource(
      icon=FontAwesomeIcons.GITHUB,
      name='Github',
      path='https://github.com'
    ),
    Resource(
      icon=FontAwesomeIcons.GRAD_CAP,
      name='Google Scholar',
      path='https://scholar.google.com'
    ),
    Resource(
      icon=FontAwesomeIcons.FILE,
      name='CV',
      path='data/documents/cv.pdf'
    )
  ]
)

BIO = '''Add your bio here'''

PUBLICATIONS = {
  'pub1': Publication(
    image =  'data/images/thumbnails/box.png',
    title =  'Your Project Name 1',
    url = 'project/pub1',
    authors =  [
      PEOPLE['your-name'],
      PEOPLE['coauthor-name'],
      PEOPLE['coauthor-name-other']
    ],
    venue = 'ACM Transactions on Graphics (SIGGRAPH), 2024',
  ),
  'pub2': Publication(
    image =  'data/images/thumbnails/glass.png',
    title =  'Your Project Name 2',
    url = 'project/pub1',
    authors =  [
      PEOPLE['your-name'],
      PEOPLE['coauthor-name']
    ],
    venue = 'ACM Transactions on Graphics (SIGGRAPH), 2023',
  ),
  'pub3': Publication(
    image =  'data/images/thumbnails/cloud.png',
    title =  'Your Project Name 3',
    url = 'project/pub1',
    authors =  [
      PEOPLE['your-name'],
      PEOPLE['coauthor-name']
    ],
    venue = 'ACM Transactions on Graphics (SIGGRAPH), 2022',
  )
}

COURSES = [
  Course(
    image = 'data/images/thumbnails/class.png',
    name = 'Course 1',
    url = 'https://www.cmu.edu',
    role = 'Teaching Assistant',
    details = 'CMU, Spring 2023, Fall 2024'
  ),
  Course(
    image = 'data/images/thumbnails/class.png',
    name = 'Course 2',
    url = 'https://www.cmu.edu',
    role = 'Teaching Assistant',
    details = 'CMU, Spring 2021'
  )
]

PROJECT_PAGES = {
  'pub1': Project(
    image = '../../data/images/project.png',
    image_caption = 'placeholder caption',
    abstract = 'placeholder abstract',
    resources = ProjectResources(
      publication = [
        Resource(
          icon = FontAwesomeIcons.PDF,
          path = '../../data/papers/pub1.pdf',
          name = 'Paper'
        ),
        Resource(
          icon = FontAwesomeIcons.BOOK,
          path = 'https://www.acm.org/',
          name =  'Publisher\'s Version'
        ),
        Resource(
          icon =  FontAwesomeIcons.ARCHIVE,
          path =  'https://arxiv.org',
          name =  'ArXiv Version'
        )
      ],
      code = [
        Resource(
          icon =  FontAwesomeIcons.GITHUB,
          path =  'https://github.com',
          name = 'Github project with full source code'
        )
      ],
    ),
    videos = [
      Video(
        name =  'presentation slides',
        id = 'tjYVcOJONdI'
      )
    ],
    acknowledgements = 'This work was generously supported by XYZ',
    citation = '''
    @article{
      Author:PAPER:2024,
      title={Placeholder Title},
      volume={42},
      ISSN={1557-7368},
      url={https://www.arxiv.org},
      number={4},
      journal={ACM Transactions on Graphics},
      publisher={Association for Computing Machinery (ACM)},
      authors={YourName}
      year={2024},
      month=jul, 
      pages={1-100}
    }'''
  )
}


if __name__ == '__main__':
  directory = 'docs/'
  if not os.path.exists(directory):
    os.makedirs(directory)

  home = Home(about_me=ABOUT_ME, 
              bio=BIO, 
              publications=PUBLICATIONS, 
              courses=COURSES)
  home.generate(directory)
  
  for id, project in PROJECT_PAGES.items():
    project_path = os.path.join(directory, f'project/{id}')
    paper = PUBLICATIONS[id]
    project.generate(project_path, paper)


