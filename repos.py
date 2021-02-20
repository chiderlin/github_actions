import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS


url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
res = requests.get(url)
print("Status code:", res.status_code)

response_dict = res.json()
print("Total repositories:", response_dict['total_count'])
repo_dicts = response_dict["items"]


names, plot_dicts = [], []
for repo in repo_dicts:
    names.append(repo['name'])

    # Get the project description, if one available.
    description = repo['description']
    if not description:
        description = "No description provided."

    plot_dict = {
        'value': repo['stargazers_count'],
        'label': description,
    }

    plot_dicts.append(plot_dict)

# Make visualization
my_style = LS('#333366', base_style=LCS)
my_style.title_font_size = 24
my_style.label_font_size = 14
my_style.major_label_font_size = 18

my_config = pygal.Config()
my_config.x_label_rotation = 45 # x軸字的角度45度
my_config.show_legend = False # 顏色標籤
my_config.truncate_label = 15 # x軸把較長的字元，只顯示15個字元
my_config.show_y_guides = False # 背後的水平線條
my_config.width = 1000 # 瀏覽器中可用空間寬度

chart = pygal.Bar(my_config, style=my_style)
# chart = pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)
chart.title = "Most-Starred Python Projects on Github"
chart.x_labels = names

chart.add('', plot_dicts)
chart.render_to_file('python_repos.svg')