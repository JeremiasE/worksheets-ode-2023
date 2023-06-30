import os
#files = [f for  f in os.listdir("examples") if f.endswith(".ipynb")]
#files.sort()
#files
with open("examples/worksheets.txt","r") as f:
    lines = f.readlines()
s = ""
s+= """# worksheets-ode-2023
Worksheets Gewöhnliche Differentialgleichungen SS 2023

## Worksheets
<table>
"""
for l in lines:
    (filename,title) = l.strip().split(",")
    s+= '<tr>\n'
    s+= '  <td>\n'
    s+=f'    <a href="/JeremiasE/worksheets-ode-2023/blob/main/examples/{filename}">{title}</a>\n'
    s+= '  </td>\n'
    s+= '  <td>\n'
    s+=f'    <a href="https://mybinder.org/v2/gh/JeremiasE/worksheets-ode-2023/HEAD?labpath=examples%2F{filename}" rel="nofollow">\n'
    s+= '      <img src="https://mybinder.org/badge_logo.svg" alt="Open In MyBinder "   height="22ex">\n'
    s+= '    </a>\n'
    s+= '  </td>\n'
    s+= '  <td>\n'
    s+=f'    <a href="https://kaggle.com/kernels/welcome?src=https://github.com/JeremiasE/worksheets-ode-2023/blob/main/examples/{filename}" rel="nofollow">\n'
    s+='      <img src="https://kaggle.com/static/images/open-in-kaggle.svg" alt="Open in Kaggle" height="22ex">\n'
    s+= '    </a>\n'
    s+= '  </td>\n'
    s+= '  <td>\n'
    s+=f'    <a href="https://colab.research.google.com/github/JeremiasE/worksheets-ode-2023/blob/main/examples/{filename}" rel="nofollow">\n'
    s+='      <img src="https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667" alt="Open In Colab" height="22ex">\n'
    s+= '    </a>\n'
    s+= '  </td>\n'
    s+= '</tr>\n'
s+="""</table>
"""
print(s)
