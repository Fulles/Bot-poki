import requests
from lxml import html
import random

response = requests.get('http://olikart.blogspot.com/2011/09/blog-post_23.html')
tree = html.fromstring(response.content)
text = tree.xpath('//*[@id="post-body-2655186918807662008"]/div[1]/text()')
count = 0
anekdots = []
anekdot = ''


while count < len(text):
    print(count)
    try:
        if len(text[count]) > 1:
            while len(text[count]) > 1:
                anekdot = anekdot + text[count]
                count += 1
            anekdots.append(anekdot)
            anekdot = ''


        if len(text[count]) >= 1:
            count+= 1

    except:
         print('Completed')


num = random.randint(0, len(anekdots))
print(anekdots[num])





