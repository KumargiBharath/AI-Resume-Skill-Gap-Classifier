import os
import sys
from loguru import logger

# -------------------------------------------------------
# SETUP LOGURU
# -------------------------------------------------------
# Remove the default handler to prevent duplicate logs
logger.remove()
# Add a new handler with a custom format and colors
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

# BASE_DIR is the root of the project (one level up from 'src')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory Paths
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Ensure directories exist
logger.info("Verifying project directories...")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Classification Labels
CLASS_LABELS = [
    "Strong Match", 
    "Moderate Match", 
    "Skill Gap", 
    "High Skill Gap"
]

# Maps variations to the standard skill name in SKILL_TAXONOMY
# Keys are variations found in resumes, Values are the standard name.
SKILL_SYNONYMS = {
    # --- Programming Languages ---
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "golang": "go",
    "cplusplus": "c++",
    "cpp": "c++",
    "csharp": "c#",
    "objective c": "objective-c",
    "perl scripting": "perl",

    # --- Web Development (Frontend) ---
    "hypertext markup language": "html",
    "cascading style sheets": "css",
    "reactjs": "react",
    "react.js": "react",
    "vuejs": "vue",
    "vue.js": "vue",
    "angularjs": "angular", # Mapping older Angular versions to main keyword
    "next js": "nextjs",
    "sass": "scss", # Often used interchangeably
    
    # --- Web Development (Backend) ---
    "nodejs": "node.js",
    "node": "node.js",
    "expressjs": "express",
    "django rest framework": "django",
    "springboot": "spring boot",
    "aspnet": "asp.net",
    "dotnet": ".net",
    "ruby on rails": "rails",
    
    # --- Databases ---
    "postgres": "postgresql",
    "psql": "postgresql",
    "mongo": "mongodb",
    "structured query language": "sql",
    "sequel": "sql", # Common pronunciation/spelling
    "ms sql": "sql server",
    "microsoft sql server": "sql server",
    "elk stack": "elasticsearch",
    "elastic": "elasticsearch",
    "redis cache": "redis",
    
    # --- Data Science & AI ---
    "ml": "machine learning",
    "dl": "deep learning",
    "ds": "data science",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "nn": "neural networks",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "tf": "tensorflow",
    "torch": "pytorch",
    "cv2": "opencv",
    "apache spark": "spark",
    "apache hadoop": "hadoop",
    "data viz": "data visualization",
    "predictive analytics": "predictive modeling",
    
    # --- Cloud & DevOps ---
    "amazon web services": "aws",
    "gcp": "google cloud",
    "google cloud platform": "google cloud",
    "ms azure": "azure",
    "k8s": "kubernetes",
    "cicd": "ci/cd",
    "continuous integration": "ci/cd",
    "continuous deployment": "ci/cd",
    "infra as code": "terraform",
    "docker containers": "docker",
    "containerization": "docker",
    "shell": "shell scripting",
    "bash scripting": "shell scripting",
    "unix shell": "unix",
    
    # --- Mobile Development ---
    "android development": "android",
    "ios development": "ios",
    "swiftui": "swift",
    "xamarin forms": "xamarin",
    
    # --- Software Testing ---
    "quality assurance": "qa",
    "sdet": "qa", # Software Dev Engineer in Test
    "test automation": "automation testing",
    "webdriver": "selenium",
    
    # --- Architecture & Methodologies ---
    "oop": "object-oriented programming",
    "object oriented design": "object-oriented programming",
    "vcs": "version control",
    "source control": "version control",
    "microservices architecture": "microservices",
    "tdd": "agile", # Often associated, though distinct
    "scrum master": "scrum",
    
    # --- Soft Skills ---
    "team player": "team work",
    "team leadership": "leadership",
    "problem solving skills": "problem solving",
    "critical thinking skills": "critical thinking"
}
# Skill Taxonomy (Simplified list for our MVP)
# Skill Taxonomy (Comprehensive Industry Standard)
SKILL_TAXONOMY = [
    # --- Programming Languages ---
    "python", "java", "javascript", "c++", "c#", "c", "ruby", "php", "swift", 
    "go", "golang", "rust", "kotlin", "scala", "perl", "r", "matlab", "typescript",
    
    # --- Web Development (Frontend) ---
    "html", "css", "react", "angular", "vue", "vuejs", "jquery", "bootstrap", 
    "sass", "less", "redux", "nextjs", "responsive design",
    
    # --- Web Development (Backend) ---
    "nodejs", "node.js", "django", "flask", "fastapi", "spring", "spring boot", 
    "express", "expressjs", "asp.net", ".net", "laravel", "rails", "ruby on rails",
    "rest api", "graphql", "api development",
    
    # --- Databases ---
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", "sql server", 
    "redis", "cassandra", "elasticsearch", "dynamodb", "firebase", "database management",
    
    # --- Data Science & AI ---
    "machine learning", "deep learning", "data science", "data analysis", 
    "artificial intelligence", "nlp", "natural language processing", 
    "computer vision", "neural networks", "pandas", "numpy", "scikit-learn", 
    "tensorflow", "pytorch", "keras", "opencv", "hadoop", "spark", "etl",
    "data mining", "predictive modeling", "power bi", "tableau",
    
    # --- Cloud & DevOps ---
    "aws", "amazon web services", "azure", "google cloud", "gcp", "docker", 
    "kubernetes", "jenkins", "ci/cd", "devops", "terraform", "ansible", 
    "linux", "unix", "bash", "shell scripting", "cloud computing", "serverless",
    
    # --- Mobile Development ---
    "android", "ios", "react native", "flutter", "mobile development", 
    "xamarin", "objective-c",
    
    # --- Software Testing ---
    "selenium", "testing", "qa", "quality assurance", "automation testing", 
    "junit", "manual testing", "performance testing", "jira",
    
    # --- Architecture & Methodologies ---
    "microservices", "system design", "agile", "scrum", "git", "github", 
    "gitlab", "bitbucket", "version control", "mvc", "object-oriented programming",
    
    # --- Soft Skills ---
    "leadership", "communication", "team work", "problem solving", 
    "critical thinking", "project management"
]
# Database of free learning resources mapped to SKILL_TAXONOMY
LEARNING_RESOURCES = {
    # --- Programming Languages ---
    "python": [
        {"title": "Official Python Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "Documentation"},
        {"title": "Real Python", "url": "https://realpython.com/", "type": "Articles & Tutorials"}
    ],
    "java": [
        {"title": "Oracle Java Tutorials", "url": "https://docs.oracle.com/javase/tutorial/", "type": "Documentation"},
        {"title": "freeCodeCamp Java Course", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "type": "Course"}
    ],
    "javascript": [
        {"title": "MDN JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "type": "Documentation"},
        {"title": "JavaScript.info", "url": "https://javascript.info/", "type": "Tutorial"}
    ],
    "c++": [
        {"title": "LearnCpp.com", "url": "https://www.learncpp.com/", "type": "Tutorial"},
        {"title": "CppReference", "url": "https://en.cppreference.com/", "type": "Documentation"}
    ],
    "c#": [
        {"title": "Microsoft C# Docs", "url": "https://learn.microsoft.com/en-us/dotnet/csharp/", "type": "Documentation"},
        {"title": "C# Station", "url": "http://csharp-station.com/Tutorial.aspx", "type": "Tutorial"}
    ],
    "c": [
        {"title": "Learn-C.org", "url": "https://www.learn-c.org/", "type": "Interactive"},
        {"title": "GNU C Manual", "url": "https://www.gnu.org/software/gnu-c-manual/", "type": "Documentation"}
    ],
    "ruby": [
        {"title": "Ruby in Twenty Minutes", "url": "https://www.ruby-lang.org/en/documentation/quickstart/", "type": "Tutorial"},
        {"title": "RubyMonk", "url": "https://rubymonk.com/", "type": "Interactive"}
    ],
    "php": [
        {"title": "PHP Manual", "url": "https://www.php.net/manual/en/", "type": "Documentation"},
        {"title": "W3Schools PHP", "url": "https://www.w3schools.com/php/", "type": "Tutorial"}
    ],
    "swift": [
        {"title": "Swift.org Docs", "url": "https://swift.org/documentation/", "type": "Documentation"},
        {"title": "Hacking with Swift", "url": "https://www.hackingwithswift.com/100", "type": "Course"}
    ],
    "go": [
        {"title": "A Tour of Go", "url": "https://tour.golang.org/welcome/1", "type": "Interactive"},
        {"title": "Go by Example", "url": "https://gobyexample.com/", "type": "Tutorial"}
    ],
    "golang": [
        {"title": "A Tour of Go", "url": "https://tour.golang.org/welcome/1", "type": "Interactive"}
    ],
    "rust": [
        {"title": "The Rust Book", "url": "https://doc.rust-lang.org/book/", "type": "Book"},
        {"title": "Rust by Example", "url": "https://doc.rust-lang.org/rust-by-example/", "type": "Tutorial"}
    ],
    "kotlin": [
        {"title": "Kotlin Docs", "url": "https://kotlinlang.org/docs/getting-started.html", "type": "Documentation"}
    ],
    "scala": [
        {"title": "Scala Book", "url": "https://docs.scala-lang.org/overviews/scala-book/introduction.html", "type": "Book"}
    ],
    "perl": [
        {"title": "Perl Tutorial Hub", "url": "https://perltutorial.org/", "type": "Tutorial"}
    ],
    "r": [
        {"title": "R for Data Science", "url": "https://r4ds.had.co.nz/", "type": "Book"},
        {"title": "DataCamp R Basics (Free)", "url": "https://www.datacamp.com/courses/free-introduction-to-r", "type": "Course"}
    ],
    "matlab": [
        {"title": "MATLAB Onramp", "url": "https://www.mathworks.com/learn/tutorials/matlab-onramp.html", "type": "Course"}
    ],
    "typescript": [
        {"title": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/handbook/", "type": "Documentation"}
    ],
    
    # --- Web Development (Frontend) ---
    "html": [
        {"title": "MDN HTML Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "type": "Tutorial"}
    ],
    "css": [
        {"title": "MDN CSS Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS", "type": "Tutorial"},
        {"title": "Flexbox Froggy", "url": "https://flexboxfroggy.com/", "type": "Game"}
    ],
    "react": [
        {"title": "React Official Docs", "url": "https://react.dev/learn", "type": "Tutorial"}
    ],
    "angular": [
        {"title": "Angular Tour of Heroes", "url": "https://angular.io/tutorial", "type": "Tutorial"}
    ],
    "vue": [
        {"title": "Vue.js Guide", "url": "https://vuejs.org/guide/introduction.html", "type": "Documentation"}
    ],
    "vuejs": [
        {"title": "Vue.js Guide", "url": "https://vuejs.org/guide/introduction.html", "type": "Documentation"}
    ],
    "jquery": [
        {"title": "jQuery Learning Center", "url": "https://learn.jquery.com/", "type": "Documentation"}
    ],
    "bootstrap": [
        {"title": "Bootstrap Docs", "url": "https://getbootstrap.com/docs/5.3/getting-started/introduction/", "type": "Documentation"}
    ],
    "sass": [
        {"title": "Sass Guide", "url": "https://sass-lang.com/guide/", "type": "Documentation"}
    ],
    "less": [
        {"title": "Less Docs", "url": "https://lesscss.org/", "type": "Documentation"}
    ],
    "redux": [
        {"title": "Redux Essentials", "url": "https://redux.js.org/tutorials/essentials/part-1-overview-concepts", "type": "Tutorial"}
    ],
    "nextjs": [
        {"title": "Learn Next.js", "url": "https://nextjs.org/learn", "type": "Course"}
    ],
    "responsive design": [
        {"title": "Responsive Web Design (freeCodeCamp)", "url": "https://www.freecodecamp.org/learn/responsive-web-design/", "type": "Course"}
    ],
    
    # --- Web Development (Backend) ---
    "nodejs": [
        {"title": "Node.js Docs", "url": "https://nodejs.org/en/docs/", "type": "Documentation"}
    ],
    "node.js": [
        {"title": "Node.js Docs", "url": "https://nodejs.org/en/docs/", "type": "Documentation"}
    ],
    "django": [
        {"title": "Django Official Tutorial", "url": "https://docs.djangoproject.com/en/4.2/intro/tutorial01/", "type": "Tutorial"}
    ],
    "flask": [
        {"title": "Flask Mega-Tutorial", "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world", "type": "Tutorial"}
    ],
    "fastapi": [
        {"title": "FastAPI User Guide", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "Tutorial"}
    ],
    "spring": [
        {"title": "Spring Guides", "url": "https://spring.io/guides", "type": "Tutorial"}
    ],
    "spring boot": [
        {"title": "Spring Boot Docs", "url": "https://spring.io/projects/spring-boot", "type": "Documentation"}
    ],
    "express": [
        {"title": "Express Docs", "url": "https://expressjs.com/en/starter/installing.html", "type": "Documentation"}
    ],
    "expressjs": [
        {"title": "Express Docs", "url": "https://expressjs.com/", "type": "Documentation"}
    ],
    "asp.net": [
        {"title": "ASP.NET Docs", "url": "https://learn.microsoft.com/en-us/aspnet/core/", "type": "Documentation"}
    ],
    ".net": [
        {"title": ".NET Docs", "url": "https://learn.microsoft.com/en-us/dotnet/", "type": "Documentation"}
    ],
    "laravel": [
        {"title": "Laravel Docs", "url": "https://laravel.com/docs/10.x", "type": "Documentation"}
    ],
    "rails": [
        {"title": "Ruby on Rails Guides", "url": "https://guides.rubyonrails.org/", "type": "Documentation"}
    ],
    "ruby on rails": [
        {"title": "Ruby on Rails Guides", "url": "https://guides.rubyonrails.org/", "type": "Documentation"}
    ],
    "rest api": [
        {"title": "RESTful API Design (Stanford)", "url": "https://restfulapi.net/", "type": "Tutorial"}
    ],
    "graphql": [
        {"title": "Introduction to GraphQL", "url": "https://graphql.org/learn/", "type": "Documentation"}
    ],
    "api development": [
        {"title": "API University", "url": "https://www.api-university.com/", "type": "Articles"}
    ],
    
    # --- Databases ---
    "sql": [
        {"title": "SQLZoo", "url": "https://sqlzoo.net/", "type": "Interactive"},
        {"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "Tutorial"}
    ],
    "mysql": [
        {"title": "MySQL Tutorial", "url": "https://www.mysqltutorial.org/", "type": "Documentation"}
    ],
    "postgresql": [
        {"title": "PostgreSQL Tutorial", "url": "https://www.postgresqltutorial.com/", "type": "Tutorial"}
    ],
    "mongodb": [
        {"title": "MongoDB University (Free)", "url": "https://university.mongodb.com/", "type": "Course"}
    ],
    "sqlite": [
        {"title": "SQLite Tutorial", "url": "https://www.sqlitetutorial.net/", "type": "Tutorial"}
    ],
    "oracle": [
        {"title": "Oracle Learning Library", "url": "https://apexapps.oracle.com/pls/apex/f?p=44785:141:107758987046619::::P141_PAGE_ID,P141_SECTION_ID:141,2937", "type": "Course"}
    ],
    "sql server": [
        {"title": "Microsoft SQL Docs", "url": "https://learn.microsoft.com/en-us/sql/sql-server/", "type": "Documentation"}
    ],
    "redis": [
        {"title": "Redis University (Free)", "url": "https://university.redis.com/", "type": "Course"}
    ],
    "cassandra": [
        {"title": "DataStax Academy", "url": "https://www.datastax.com/learn", "type": "Course"}
    ],
    "elasticsearch": [
        {"title": "Elasticsearch Guide", "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html", "type": "Documentation"}
    ],
    "dynamodb": [
        {"title": "DynamoDB Guide", "url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html", "type": "Documentation"}
    ],
    "firebase": [
        {"title": "Firebase Documentation", "url": "https://firebase.google.com/docs", "type": "Documentation"}
    ],
    "database management": [
        {"title": "Stanford DB Course", "url": "https://online.stanford.edu/courses/soe-ydatabases-databases", "type": "Course"}
    ],
    
    # --- Data Science & AI ---
    "machine learning": [
        {"title": "Andrew Ng's ML Course (Audit Free)", "url": "https://www.coursera.org/learn/machine-learning", "type": "Course"},
        {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn/machine-learning", "type": "Interactive"}
    ],
    "deep learning": [
        {"title": "fast.ai Course", "url": "https://course.fast.ai/", "type": "Course"},
        {"title": "Deep Learning Book", "url": "https://www.deeplearningbook.org/", "type": "Book"}
    ],
    "data science": [
        {"title": "Data Science Handbook", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/", "type": "Book"}
    ],
    "data analysis": [
        {"title": "Data Analysis with Python (freeCodeCamp)", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/", "type": "Course"}
    ],
    "artificial intelligence": [
        {"title": "Elements of AI", "url": "https://www.elementsofai.com/", "type": "Course"}
    ],
    "nlp": [
        {"title": "Stanford CS224N", "url": "https://web.stanford.edu/class/cs224n/", "type": "Video Lectures"}
    ],
    "natural language processing": [
        {"title": "Stanford CS224N", "url": "https://web.stanford.edu/class/cs224n/", "type": "Video Lectures"}
    ],
    "computer vision": [
        {"title": "OpenCV Python Tutorials", "url": "https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html", "type": "Tutorial"}
    ],
    "neural networks": [
        {"title": "Neural Networks and Deep Learning", "url": "http://neuralnetworksanddeeplearning.com/", "type": "Book"}
    ],
    "pandas": [
        {"title": "Pandas Getting Started", "url": "https://pandas.pydata.org/docs/getting_started/index.html", "type": "Documentation"}
    ],
    "numpy": [
        {"title": "Numpy User Guide", "url": "https://numpy.org/doc/stable/user/index.html", "type": "Documentation"}
    ],
    "scikit-learn": [
        {"title": "Scikit-learn User Guide", "url": "https://scikit-learn.org/stable/user_guide.html", "type": "Documentation"}
    ],
    "tensorflow": [
        {"title": "TensorFlow Tutorials", "url": "https://www.tensorflow.org/tutorials", "type": "Interactive"}
    ],
    "pytorch": [
        {"title": "PyTorch Tutorials", "url": "https://pytorch.org/tutorials/", "type": "Documentation"}
    ],
    "keras": [
        {"title": "Keras.io Guides", "url": "https://keras.io/guides/", "type": "Documentation"}
    ],
    "opencv": [
        {"title": "OpenCV Docs", "url": "https://docs.opencv.org/4.x/", "type": "Documentation"}
    ],
    "hadoop": [
        {"title": "Hadoop Tutorial", "url": "https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html", "type": "Documentation"}
    ],
    "spark": [
        {"title": "Apache Spark Docs", "url": "https://spark.apache.org/docs/latest/", "type": "Documentation"}
    ],
    "etl": [
        {"title": "ETL Fundamentals", "url": "https://www.talend.com/resources/etl-tools/", "type": "Article"}
    ],
    "data mining": [
        {"title": "Data Mining Book", "url": "https://www-users.cs.umn.edu/~kumar001/dmbook/index.php", "type": "Book"}
    ],
    "predictive modeling": [
        {"title": "Kaggle Predictive Modeling", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "type": "Interactive"}
    ],
    "power bi": [
        {"title": "Microsoft Learn Power BI", "url": "https://learn.microsoft.com/en-us/power-bi/", "type": "Documentation"}
    ],
    "tableau": [
        {"title": "Tableau Training", "url": "https://www.tableau.com/learn/training", "type": "Video"}
    ],
    
    # --- Cloud & DevOps ---
    "aws": [
        {"title": "AWS Skill Builder", "url": "https://explore.skillbuilder.aws/learn", "type": "Course"}
    ],
    "amazon web services": [
        {"title": "AWS Skill Builder", "url": "https://aws.amazon.com/training/", "type": "Course"}
    ],
    "azure": [
        {"title": "Microsoft Learn Azure", "url": "https://learn.microsoft.com/en-us/training/azure/", "type": "Interactive"}
    ],
    "google cloud": [
        {"title": "Google Cloud Skills Boost", "url": "https://www.cloudskillsboost.google/", "type": "Interactive"}
    ],
    "gcp": [
        {"title": "Google Cloud Skills Boost", "url": "https://www.cloudskillsboost.google/", "type": "Interactive"}
    ],
    "docker": [
        {"title": "Docker Curriculum", "url": "https://docker-curriculum.com/", "type": "Tutorial"}
    ],
    "kubernetes": [
        {"title": "Kubernetes Basics", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "type": "Interactive"}
    ],
    "jenkins": [
        {"title": "Jenkins User Documentation", "url": "https://www.jenkins.io/doc/", "type": "Documentation"}
    ],
    "ci/cd": [
        {"title": "CI/CD with GitLab", "url": "https://docs.gitlab.com/ee/ci/", "type": "Documentation"}
    ],
    "devops": [
        {"title": "Roadmap.sh DevOps", "url": "https://roadmap.sh/devops", "type": "Guide"}
    ],
    "terraform": [
        {"title": "HashiCorp Learn", "url": "https://developer.hashicorp.com/terraform/tutorials", "type": "Interactive"}
    ],
    "ansible": [
        {"title": "Ansible Documentation", "url": "https://docs.ansible.com/", "type": "Documentation"}
    ],
    "linux": [
        {"title": "Linux Journey", "url": "https://linuxjourney.com/", "type": "Interactive"}
    ],
    "unix": [
        {"title": "Unix Tutorial", "url": "https://www.tutorialspoint.com/unix/index.htm", "type": "Tutorial"}
    ],
    "bash": [
        {"title": "Bash Guide for Beginners", "url": "https://tldp.org/LDP/Bash-Beginners-Guide/html/", "type": "Book"}
    ],
    "shell scripting": [
        {"title": "Shell Scripting Tutorial", "url": "https://www.shellscript.sh/", "type": "Tutorial"}
    ],
    "cloud computing": [
        {"title": "Cloud Computing Basics (Coursera)", "url": "https://www.coursera.org/learn/cloud-computing-basics", "type": "Course"}
    ],
    "serverless": [
        {"title": "Serverless Framework Docs", "url": "https://www.serverless.com/framework/docs/", "type": "Documentation"}
    ],
    
    # --- Mobile Development ---
    "android": [
        {"title": "Android Developer Training", "url": "https://developer.android.com/courses", "type": "Course"}
    ],
    "ios": [
        {"title": "Apple Developer Documentation", "url": "https://developer.apple.com/learn/", "type": "Documentation"}
    ],
    "react native": [
        {"title": "React Native Docs", "url": "https://reactnative.dev/docs/getting-started", "type": "Documentation"}
    ],
    "flutter": [
        {"title": "Flutter Codelabs", "url": "https://docs.flutter.dev/codelabs", "type": "Interactive"}
    ],
    "mobile development": [
        {"title": "Google Developers Training", "url": "https://developers.google.com/learn", "type": "Platform"}
    ],
    "xamarin": [
        {"title": "Xamarin Docs", "url": "https://learn.microsoft.com/en-us/xamarin/", "type": "Documentation"}
    ],
    "objective-c": [
        {"title": "Programming with Objective-C", "url": "https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html", "type": "Book"}
    ],
    
    # --- Software Testing ---
    "selenium": [
        {"title": "Selenium Easy", "url": "https://www.seleniumeasy.com/", "type": "Tutorial"}
    ],
    "testing": [
        {"title": "Software Testing Help", "url": "https://www.softwaretestinghelp.com/", "type": "Tutorials"}
    ],
    "qa": [
        {"title": "Guru99 QA Tutorials", "url": "https://www.guru99.com/software-testing.html", "type": "Tutorial"}
    ],
    "quality assurance": [
        {"title": "ISTQB Foundation (Free Resources)", "url": "https://www.istqb.org/", "type": "Documentation"}
    ],
    "automation testing": [
        {"title": "Test Automation University", "url": "https://testautomationu.applitools.com/", "type": "Course"}
    ],
    "junit": [
        {"title": "JUnit 5 User Guide", "url": "https://junit.org/junit5/docs/current/user-guide/", "type": "Documentation"}
    ],
    "manual testing": [
        {"title": "Software Testing Tutorial", "url": "https://www.tutorialspoint.com/software_testing/index.htm", "type": "Tutorial"}
    ],
    "performance testing": [
        {"title": "Apache JMeter Docs", "url": "https://jmeter.apache.org/usermanual/index.html", "type": "Documentation"}
    ],
    "jira": [
        {"title": "Jira University", "url": "https://university.atlassian.com/", "type": "Course"}
    ],
    
    # --- Architecture & Methodologies ---
    "microservices": [
        {"title": "Microservices.io", "url": "https://microservices.io/", "type": "Pattern Guide"}
    ],
    "system design": [
        {"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "type": "GitHub Repo"}
    ],
    "agile": [
        {"title": "Atlassian Agile Coach", "url": "https://www.atlassian.com/agile", "type": "Articles"}
    ],
    "scrum": [
        {"title": "Scrum.org Resources", "url": "https://www.scrum.org/resources", "type": "Articles"}
    ],
    "git": [
        {"title": "Pro Git Book", "url": "https://git-scm.com/book/en/v2", "type": "Book"},
        {"title": "Learn Git Branching", "url": "https://learngitbranching.js.org/", "type": "Interactive"}
    ],
    "github": [
        {"title": "GitHub Learning Lab", "url": "https://lab.github.com/", "type": "Interactive"}
    ],
    "gitlab": [
        {"title": "GitLab Docs", "url": "https://docs.gitlab.com/", "type": "Documentation"}
    ],
    "bitbucket": [
        {"title": "Bitbucket Tutorials", "url": "https://www.atlassian.com/git/tutorials", "type": "Tutorial"}
    ],
    "version control": [
        {"title": "Pro Git Book", "url": "https://git-scm.com/book/en/v2", "type": "Book"}
    ],
    "mvc": [
        {"title": "MVC Explanation", "url": "https://developer.mozilla.org/en-US/docs/Glossary/MVC", "type": "Article"}
    ],
    "object-oriented programming": [
        {"title": "OOP Concepts (Oracle)", "url": "https://docs.oracle.com/javase/tutorial/java/concepts/", "type": "Tutorial"}
    ],
    
    # --- Soft Skills ---
    "leadership": [
        {"title": "Leadership & Management (edX)", "url": "https://www.edx.org/learn/leadership-management", "type": "Course List"}
    ],
    "communication": [
        {"title": "Communication Skills (Coursera)", "url": "https://www.coursera.org/learn/wharton-communication-skills", "type": "Course (Audit)"}
    ],
    "team work": [
        {"title": "Teamwork Skills (LinkedIn Learning)", "url": "https://www.linkedin.com/learning/topics/teamwork", "type": "Course"}
    ],
    "problem solving": [
        {"title": "Problem Solving (Coursera)", "url": "https://www.coursera.org/learn/problem-solving-skills", "type": "Course (Audit)"}
    ],
    "critical thinking": [
        {"title": "Critical Thinking (edX)", "url": "https://www.edx.org/learn/critical-thinking-skills", "type": "Course List"}
    ],
    "project management": [
        {"title": "Google Project Management Cert", "url": "https://www.coursera.org/professional-certificates/google-project-management", "type": "Course (Audit)"}
    ]
}

logger.info(f"[Config] Project initialized. Root: {BASE_DIR}")