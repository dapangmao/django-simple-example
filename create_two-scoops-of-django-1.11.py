import os
import sys
sys.stdout = open('combine.py','wt')
all_files = os.listdir("./code")

def get_chapter_titles():
    _chapters = """
    Chapter 1: Coding Style
    Chapter 2: The Optimal Django Environment Setup
    Chapter 3: How to Lay Out Django Projects
    Chapter 4: Fundamentals of Django App Design
    Chapter 5: Settings and Requirements Files
    Chapter 6: Model Best Practices
    Chapter 7: Queries and the Database Layer
    Chapter 8: Function- and Class-Based Views
    Chapter 9: Best Practices for Function-Based Views
    Chapter 10: Best Practices for Class-Based Views
    Chapter 11: Form Fundamentals
    Chapter 12: Common Patterns for Forms
    Chapter 13: Templates: Best Practices
    Chapter 14: Template Tags and Filters
    Chapter 15: Django Templates and Jinja2
    Chapter 16: Building REST APIs with Django REST Framework (NEW)
    Chapter 17: Consuming REST APIs
    Chapter 18: Tradeoffs of Replacing Core Components
    Chapter 19: Working With the Django Admin
    Chapter 20: Dealing with the User Model
    Chapter 21: Django's Secret Sauce: Third-Party Packages
    Chapter 22: Testing Chapter of Doom!
    Chapter 23: Documentation: Be Obsessed
    Chapter 24: Finding and Reducing Bottlenecks
    Chapter 25: Security Best Practices
    Chapter 26: Logging: What's It For, Anyway?
    Chapter 27: Signals: Use Cases and Avoidance Techniques
    Chapter 28: What About Those Random Utilities?
    Chapter 29: Deployment: Platforms as a Service
    Chapter 30: Deploying Django Projects
    Chapter 31: Continuous Integration
    Chapter 32: The Art of Debugging
    Chapter 33: Where and How to Ask Django Questions
    """

    chapters = [x.strip() for x in _chapters.split("\n") if x]
    cdict = {}
    for chapter in chapters:
        if not chapter:
            continue
        key = int(chapter.split(" ")[1][:-1])
        cdict[key] = chapter
    return cdict

def write2file(cdict):
    pass_id = 0
    for file in all_files:
        with open(os.path.join("code", file), 'r') as infile:
            id = int(file.split("_")[1])
            if id in cdict and id != pass_id:
                print("# " + cdict.get(id) + "\n")
            print('"""{} """\n'.format(file))
            for i, l in enumerate(infile):
                if i > 36:
                    print(l.rstrip())
            print("\n")
            pass_id = id

            
cdict = get_chapter_titles()
write2file(cdict=cdict)
